import uuid,json
from typing import Optional
from pydantic import BaseModel,Field
from source.utils import get_a_uuid, print_attributes

class SegmentRequest(BaseModel):
    user_id: str  = Field(...,example="user1234")
    image_set: list = Field(...,example=[{
        "image_path": "../auto_vlogger/auto_vlog/static/spacex_musk/raw_images/",
        "image_file_name": "saturday-night-live-elon-musk.jpg"
        }
        ])
    output_path: str  = Field(...,example="./")

class SegmentResponse(BaseModel):
    requestId: str = Field(..., example="1234")
    user_id: str  = Field(...,example="user1234")
    image_set: list = Field(...,example=[{
        "image_path": "../auto_vlogger/auto_vlog/static/spacex_musk/raw_images/",
        "image_file_name": "saturday-night-live-elon-musk.jpg"
        }
        ])
    output_path: str  = Field(...,example="./")
    output_files: dict = Field(...,example={
        "saturday-night-live-elon-musk.jpg":
                ['segment_0.jpg','segment_1.jpg',]
    })
    success_code: str
    exception_message: str

def invoke_segmentation(sgmRequest:SegmentRequest, sgm):
    print("YouTube Download Request Received")
    requestId = get_a_uuid()
    print_attributes(sgmRequest)
    #try:
    messages = ''
    output_files = sgm.run_list_segmentation(sgmRequest.image_set, sgmRequest.output_path, )
    success_code = 200
    #except Exception as inst:
    #    messages = str(inst)
    #    success_code = 500
    #    output_files = {}

    response = SegmentResponse(
        requestId = requestId,
        user_id = sgmRequest.user_id,
        image_set = sgmRequest.image_set, 
        output_path = sgmRequest.output_path, 
        output_files = output_files,
        success_code = success_code,
        exception_message = messages
    )
    return response
