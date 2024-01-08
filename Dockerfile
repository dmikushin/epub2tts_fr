FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    golang \
    python3-numba

RUN go install moul.io/number-to-words/cmd/number-to-words@latest

COPY . .

RUN pip install --upgrade pip

RUN cd tensorflow-gpu-dummy && pip install .

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV OS=ubuntu2204
ENV cudnn_version=8.6.0.163
ENV cuda_version=cuda11.8
ENV cuda_version2=11-8

RUN wget https://developer.download.nvidia.com/compute/cuda/repos/${OS}/x86_64/cuda-${OS}.pin

RUN mv cuda-${OS}.pin /etc/apt/preferences.d/cuda-repository-pin-600
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/${OS}/x86_64/3bf863cc.pub
RUN echo "deb https://developer.download.nvidia.com/compute/cuda/repos/${OS}/x86_64/ /" >/etc/apt/sources.list.d/cuda.list
RUN apt-get update && apt-get install -y libcudnn8=${cudnn_version}-1+${cuda_version} libcufft-${cuda_version2} cuda-cudart-${cuda_version2} libcublas-${cuda_version2} libcusparse-${cuda_version2} libcusolver-${cuda_version2} cuda-nvcc-${cuda_version2}

ENV LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/local/cuda/lib64"

ENTRYPOINT ["python3.10", "txt2wav.py"]
