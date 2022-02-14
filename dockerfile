FROM ubuntu:18.04

RUN apt update && apt-get update && \
    apt install -y python3 && \
    apt-get install -y python3-pip && \
    apt install -y wget git unzip && \

    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y /google-chrome-stable_current_amd64.deb && \

    wget https://chromedriver.storage.googleapis.com/98.0.4758.80/chromedriver_linux64.zip && \
    unzip /chromedriver_linux64.zip && \

    git clone https://github.com/tml104/xmu_auto_punch.git && \
    pip3 install -r /xmu_auto_punch/requirements.txt

WORKDIR /xmu_auto_punch

# CMD ["python3","auto_punch.py"]