FROM python:3.7

RUN mkdir segmentation_api
WORKDIR /segmentation_api
COPY ./requirements_api.txt .
COPY ./requirements_MaskRCNN.txt .
RUN apt update && \
    apt-get install -y git && \
    git clone https://github.com/md-experiments/Mask_RCNN.git
WORKDIR /segmentation_api/Mask_RCNN
RUN python3 setup.py install
WORKDIR /segmentation_api
RUN pip3 install --no-cache-dir -r requirements_api.txt && \
    pip3 install --no-cache-dir -r requirements_MaskRCNN.txt
COPY ./main.py .
COPY ./download_model.py .
RUN python3 download_model.py
COPY ./source/ ./source/
COPY ./saturday-night-live-elon-musk.jpg .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]




