# Fast and fair quality audiobook generator for EPUB books in French

This repository combines several tools to generate audiobooks from .epub e-books in French. Sound synthesis with Vosk is very fast, and the quaility is fairly good.

## Steps

Given a .epub e-book, the following steps have to be done:

1. Use [epub2txt2](https://github.com/kevinboone/epub2txt2) tool to convert .epub to .txt
2. Vosk TTS is not able to pronounce numbers, so use [num2t4ru](https://github.com/razzor58/num2t4ru) tool (`to-pypi` branch) to convert all digital numbers to text
3. Use [vosk-tts](https://github.com/alphacep/vosk-tts.git) to produce audio from text. Based on ONNX runtime, currently it works only with the CPU backend, GPU backend has strange reshape errors. Processing speed is moderate.

## Prerequisites

```
go install moul.io/number-to-words/cmd/number-to-words@latest
```

## Building

```
python3.10 -m venv ./venv

```
