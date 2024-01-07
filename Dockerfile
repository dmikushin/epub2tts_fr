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

CMD ["python", "your_script.py"]
