FROM python:3.7

RUN mkdir app
RUN mkdir app/segmentation_api
RUN mkdir app/data
RUN mkdir app/data/video_images

WORKDIR /app/segmentation_api
COPY ./requirements_api.txt .
COPY ./requirements_MaskRCNN.txt .
RUN apt update && \
    apt-get install -y git && \
    git clone https://github.com/md-experiments/Mask_RCNN.git
WORKDIR /app/segmentation_api/Mask_RCNN
RUN python3 setup.py install
WORKDIR /app/segmentation_api
RUN pip3 install --no-cache-dir -r requirements_api.txt && \
    pip3 install --no-cache-dir -r requirements_MaskRCNN.txt

WORKDIR /app
COPY ./download_model.py /app/
RUN python3 download_model.py

COPY ./main.py /app/
COPY ./minio_config.yml /app/
COPY ./source/ /app/source/
COPY ./saturday-night-live-elon-musk.jpg /app/data/video_images

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]




