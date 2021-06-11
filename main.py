import os
from fastapi import FastAPI
from source.segmenter import Segmentation
from source.service_definitions import SegmentResponse, SegmentRequest,invoke_segmentation


app = FastAPI(title="Endeavour Video Editor Service",
              description="API for video editing, transcription and rendering",
              version = "0.0.1"
              )

tags_metadata=[
    {"name", "TranscriptServiceGCP",
     "description", "Use GCP Transcription services for video-to-text transcript to be consumed by SummarizationService"
    },
]



print("--> " + os.getcwd())

@app.post("/segmentation/", tags=["ImageSegmenter"], response_model=SegmentResponse, status_code=200)
def reqestContentSummarisation(segRequest:SegmentRequest):
    print("About to call")
    sgm = Segmentation()
    return invoke_segmentation(segRequest, sgm)

print("Image Segmenter Started Successfully")
