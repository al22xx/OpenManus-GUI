FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl git unzip poppler-utils libmagic1 \
    python3-venv python3-dev build-essential

RUN pip install --no-cache-dir uv

RUN git clone https://github.com/mannaandpoem/OpenManus.git /workspace
WORKDIR /workspace

RUN uv venv --python 3.12

COPY requirements.txt .
RUN . .venv/bin/activate && uv pip install -r requirements.txt

COPY .env /workspace/.env
COPY gui.py /workspace/gui.py
COPY file_processor.py /workspace/file_processor.py

EXPOSE 7860

CMD ["/workspace/.venv/bin/python", "gui.py"]