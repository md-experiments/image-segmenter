import uuid,json
from typing import Optional
from pydantic import BaseModel,Field
from segmentation_api.utils import get_a_uuid, print_attributes

class SegmentRequest(BaseModel):
    user_id: str  = Field(...,example="user1234")
    image_path: str = Field(...,example="../../../auto_vlogger/auto_vlog/static/spacex_musk/raw_images/")
    image_file_name: str = Field(...,example="ksZaXDrJVhW95Nie79NeMK.jpg")
    output_path: str  = Field(...,example="../")

class SegmentResponse(BaseModel):
    requestId: str = Field(..., example="1234")
    user_id: str  = Field(...,example="user1234")
    image_path: str = Field(...,example="../../../auto_vlogger/auto_vlog/static/spacex_musk/raw_images/")
    image_file_name: str = Field(...,example="ksZaXDrJVhW95Nie79NeMK.jpg")
    output_path: str  = Field(...,example="../")
    output_files: list = Field(...,example=[
                'segment_0.jpg',
                'segment_1.jpg',
            ])
    success_code: str
    exception_message: str

def segment_images(sgmRequest:SegmentRequest, sgm):
    print("YouTube Download Request Received")
    requestId = get_a_uuid()
    print_attributes(sgmRequest)
    try:
        messages = ''
        output_files = sgm.run_segmentation(sgmRequest.image_path, sgmRequest.image_file_name, sgmRequest.output_path, )
        success_code = 200
    except Exception as inst:
        messages = str(inst)
        success_code = 500

    response = SegmentResponse(
        requestId = requestId,
        user_id = sgmRequest.user_id,
        image_path = sgmRequest.image_path, 
        image_file_name = sgmRequest.image_file_name, 
        output_path = sgmRequest.output_path, 
        output_files = output_files,
        success_code = success_code,
        exception_message = messages
    )
    return response
