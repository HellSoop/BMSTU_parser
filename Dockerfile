FROM nvidia/cuda:12.9.1-base-ubuntu24.04
LABEL authors="HellSoop"

RUN groupadd -r botgroup && useradd -r -g botgroup botuser

RUN apt update
RUN apt install -y python3 wget
RUN wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py --break-system-packages

WORKDIR /app

COPY . .
RUN mkdir -p expose/logs hf_home

RUN pip install --break-system-packages --no-cache-dir -r requirements.txt
ENV HF_HOME=/app/hf_home

VOLUME /app/expose

RUN chgrp -R botgroup /app/
RUN chmod -R g+rwx /app/
USER botuser

ENTRYPOINT ["python3", "docker_entrypoint.py"]
