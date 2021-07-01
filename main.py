import os
from fastapi import FastAPI
from source.segmenter import Segmentation
from source.service_definitions import SegmentResponse, SegmentRequest,invoke_segmentation


app = FastAPI(title="Endeavour Image Segmentation Service",
              description="API for video editing, transcription and rendering",
              version = "0.0.1"
              )

tags_metadata=[
    {"name", "Image Segmentation Service",
     "description", "Provide image segments"
    },
]



print("--> " + os.getcwd())

@app.post("/segmentation/", tags=["ImageSegmenter"], response_model=SegmentResponse, status_code=200)
def reqestImageSegmentation(segRequest:SegmentRequest):
    print("About to call")
    sgm = Segmentation()
    result = invoke_segmentation(segRequest, sgm)
    del sgm
    return result

print("Image Segmenter Started Successfully")
