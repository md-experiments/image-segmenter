FROM python:3.7

RUN mkdir segmentation_api
WORKDIR /segmentation_api
COPY ./requirements_api.txt .
COPY ./requirements_MaskRCNN.txt .
RUN apt update && \
    apt-get install -y git && \
    pip3 install --no-cache-dir -r requirements_api.txt && \
    pip3 install --no-cache-dir -r requirements_MaskRCNN.txt && \
    git clone https://github.com/md-experiments/Mask_RCNN.git && \
    python3 setup.py install
COPY ./src/ ./src/

WORKDIR /app_root

ENV PYTHONPATH "${PYTHONPATH}:/app_root/text_structure"
CMD [ "python", "./agent/AppAgent.py", "./app/config/configDocker.yml" ]




