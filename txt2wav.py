import re
import wave
import sys
import numpy as np
import tensorflow as tf
import soundfile as sf

from tensorflow_tts.inference import AutoProcessor
from tensorflow_tts.inference import TFAutoModel

def parse_text_fragments(filename):
    with open(filename, 'r') as file:
        text = file.read()
        text = re.sub('(\\\\begin{title})', '\\\\pause{}\\1', text)
        text = re.sub('(\\\\end{title})', '\\1\\\\pause{}', text)
        fragments = [fragment.strip() for fragment in text.split('\\pause{}') if fragment.strip()]
        fragments = [(re.sub('\\\\begin{title}', '', re.sub('\\\\end{title}', '', fragment)).strip(),
            True if (fragment.startswith('\\begin{title}') and
            fragment.endswith('\\end{title}')) else False) for fragment in fragments]
        return fragments

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} <ebook_txt_filename> <ebook_wav_filename>')
        sys.exit(1)
        
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    fragments = parse_text_fragments(input_filename)

    processor = AutoProcessor.from_pretrained("tensorspeech/tts-tacotron2-synpaflex-fr")
    tacotron2 = TFAutoModel.from_pretrained("tensorspeech/tts-tacotron2-synpaflex-fr")
    mb_melgan = TFAutoModel.from_pretrained("tensorspeech/tts-mb_melgan-synpaflex-fr")

    title_speaker = 0
    maintext_speaker = 0

    sample_width = 2
    frame_rate = 22050
    pause = b'\x00' * frame_rate * sample_width # 1 second of silence

    i = 1
    with wave.open(output_filename, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(sample_width)
        f.setframerate(frame_rate)

        for text, is_title in fragments:
            speaker_id = title_speaker if is_title else maintext_speaker

            input_ids = processor.text_to_sequence(text)

            # tacotron2 inference (text-to-mel)
            decoder_output, mel_outputs, stop_token_prediction, alignment_history = tacotron2.inference(
                input_ids=tf.expand_dims(tf.convert_to_tensor(input_ids, dtype=tf.int32), 0),
                input_lengths=tf.convert_to_tensor([len(input_ids)], tf.int32),
                speaker_ids=tf.convert_to_tensor([speaker_id], dtype=tf.int32),
            )

            # melgan inference (mel-to-wav)
            audio = mb_melgan.inference(mel_outputs)[0, :, 0]

            sf.write(f'./audio_{i}.wav', audio, 22050, "PCM_16")
            
            audio = np.int16(audio/np.max(np.abs(audio)) * 32767)
            f.writeframes(audio)
            f.writeframes(pause)
                        
            print(f'{i}/{len(fragments)}')
            i = i + 1

