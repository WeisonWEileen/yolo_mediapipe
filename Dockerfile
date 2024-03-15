FROM ultralytics/ultralytics@sha256:1680334f0dc9e779fcd193782a1fa6e41accfc1cc555e65ac168c7f0cbb9d016

WORKDIR /usr/src

RUN /opt/conda/bin/python -m pip install mediapipe                        && \   
    cd /usr/src/                                                          && \   
    RUN git clone https://github.com/WeisonWEileen/yolo_mediapipe.git
