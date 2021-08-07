import os
from typing import Optional
from pydantic import BaseModel,Field
from source.utils import get_a_uuid, print_attributes, make_dirs
from source.content_management import upload_to_minio
import colorsys

class SegmentRequest(BaseModel):
    user_id: str  = Field(...,example="user1234")
    image_set: list = Field(...,example=[{
        "image_path": "../data/video_images",
        "image_file_name": "saturday-night-live-elon-musk.jpg"
        }])
    output_path: str  = Field(...,example="../data/video_segments")
    color_rgb: tuple = Field(...,example=(0, 0, 102))

class SegmentResponse(BaseModel):
    requestId: str = Field(..., example="1234")
    user_id: str  = Field(...,example="user1234")
    output_path: str  = Field(...,example="./")
    color_rgb: tuple = Field(...,example=(0, 0, 102))
    results: list = Field(...,example=[{
        "image_path": "../data/video_images",
        "image_file_name": "saturday-night-live-elon-musk.jpg",
        'output_files': ['segment_0.jpg','segment_1.jpg',]
        }])
    success_code: str
    exception_message: str

def invoke_segmentation(sgmRequest:SegmentRequest, sgm):
    print("########## Segmentation Request Received ##########")
    requestId = get_a_uuid()
    print_attributes(sgmRequest)
    #try:
    messages = ''
    make_dirs([sgmRequest.output_path])

    color = colorsys.hsv_to_rgb(*sgmRequest.color_rgb)
    results = sgm.run_list_segmentation(image_set = sgmRequest.image_set, output_path = sgmRequest.output_path, color = color)
    for result in results:
        upload_to_minio(result['output_files'], os.path.join(sgmRequest.user_id, sgmRequest.output_path))
    success_code = 200
    #except Exception as inst:
    #    messages = str(inst)
    #    success_code = 500
    #    output_files = {}

    response = SegmentResponse(
        requestId = requestId,
        user_id = sgmRequest.user_id,
        output_path = sgmRequest.output_path, 
        color_rgb = sgmRequest.color_rgb,
        results = results,
        success_code = success_code,
        exception_message = messages
    )
    print("########## Segmentation Request Completed ##########")
    print_attributes(response)
    return response
