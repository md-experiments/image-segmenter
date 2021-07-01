import uuid,json
from typing import Optional
from pydantic import BaseModel,Field
from source.utils import get_a_uuid, print_attributes, make_dirs

class SegmentRequest(BaseModel):
    user_id: str  = Field(...,example="user1234")
    image_set: list = Field(...,example=[{
        "image_path": "./",
        "image_file_name": "saturday-night-live-elon-musk.jpg"
        }])
    output_path: str  = Field(...,example="./")

class SegmentResponse(BaseModel):
    requestId: str = Field(..., example="1234")
    user_id: str  = Field(...,example="user1234")
    output_path: str  = Field(...,example="./")
    results: list = Field(...,example=[{
        "image_path": "./",
        "image_file_name": "saturday-night-live-elon-musk.jpg",
        'output_files': ['segment_0.jpg','segment_1.jpg',]
        }])
    success_code: str
    exception_message: str

def invoke_segmentation(sgmRequest:SegmentRequest, sgm):
    print("YouTube Download Request Received")
    requestId = get_a_uuid()
    print_attributes(sgmRequest)
    #try:
    messages = ''
    make_dirs([sgmRequest.output_path])
    results = sgm.run_list_segmentation(sgmRequest.image_set, sgmRequest.output_path, )
    success_code = 200
    #except Exception as inst:
    #    messages = str(inst)
    #    success_code = 500
    #    output_files = {}

    response = SegmentResponse(
        requestId = requestId,
        user_id = sgmRequest.user_id,
        output_path = sgmRequest.output_path, 
        results = results,
        success_code = success_code,
        exception_message = messages
    )
    return response
