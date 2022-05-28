FROM pytorch/pytorch

WORKDIR /app
RUN mkdir -p /app/inputs/
RUN mkdir -p /app/outputs/
RUN mkdir -p /app/logs/

RUN apt update && apt install git wget -y

RUN git clone https://github.com/PeterL1n/RobustVideoMatting.git && \
    cd RobustVideoMatting && \
    git checkout 81a10937c73f68eeddb863221c61fe6a60a1cca2 && \
    pip install -r requirements_inference.txt

RUN wget https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_resnet50.pth

COPY common common
COPY rvm rvm

RUN pip install -r common/requirements.txt

ENV PYTHONPATH="/app:/app/RobustVideoMatting"
ENV RESNET_PATH="rvm_resnet50.pth"
ENV LOG_DIR="/app/logs/"

ENTRYPOINT ["python", "-m", "rvm"]
# CMD ["--input-video", "", "--output-directory", ""]
