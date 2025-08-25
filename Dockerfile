FROM nvidia/cuda:12.9.1-base-ubuntu24.04
LABEL authors="HellSoop"

RUN groupadd -r botgroup && useradd -r -g botgroup botuser

RUN apt update
RUN apt install -y python3 python3-pip python3-venv

WORKDIR /app

COPY . .
RUN mkdir -p expose/logs
RUN pip install --break-system-packages -r requirements.txt
VOLUME /app/expose

USER botuser
ENTRYPOINT ["python3", "docker_entrypoint.py"]
