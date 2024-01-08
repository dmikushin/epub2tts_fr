# Fast and fair quality audiobook generator for EPUB books in French with synpaflex-fr

This repository combines several tools to generate audiobooks from .epub e-books in French. Sound synthesis with [synpaflex-fr](https://huggingface.co/tensorspeech/tts-mb_melgan-synpaflex-fr) is very fast, and the quaility is fairly good.

## Steps

Given a .epub e-book, the following steps have to be done:

1. Use [epub2txt2](https://github.com/kevinboone/epub2txt2) tool to convert .epub to .txt
2. TTS is not able to pronounce numbers, so use [number-to-words](https://github.com/moul/number-to-words) tool to convert all digital numbers to text
3. Use [synpaflex-fr](https://huggingface.co/tensorspeech/tts-mb_melgan-synpaflex-fr) to produce audio from text. Based on TensorFlowTTS, it supports both CPU and GPU-based inference. On CPU the processing speed is moderate.

## Prerequisites

```
go install moul.io/number-to-words/cmd/number-to-words@latest
```

## Building

The current solution only supports Python 3.10 (not Python 3.11):

```
python3.10 -m venv ./venv
source venv/bin/activate.fish
```

`TensorFlowTTS` depends on `tensorflow-gpu` package, which has been removed. To fitful the missing dependency, we have to mock up the package:

```
cd tensorflow-gpu-dummy
pip install .
```

The steps above can be now followed by packages installation:

```
pip install -r requirements.txt
```

## Docker

```
docker build -t epub2tts_fr .
```

In order to have GPU support in Docker, CUDA>=11.7 must be present on the host machine

## Usage

```
python3.10 ./txt2wav example/oceania.txt example/oceania.wav
```

Usage through Docker container:

```
bash -c 'docker run --gpus all -v "$PWD:$PWD" -v ~/.cache/tensorflow_tts/:/root/.cache/tensorflow_tts/ -v ~/.cache/tensorflow_tts/:/root/.cache/tensorflow_tts/ -v ~/nltk_data:/root/nltk_data -w "$PWD" epub2tts_fr example/oceania.txt example/oceania.wav'
```

