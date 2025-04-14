from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import base64
from io import BytesIO
from PIL import Image
from app.services.binarization import binarize_image

router = APIRouter()


class ImageRequest(BaseModel):
    image: str
    algorithm: str


class ImageResponse(BaseModel):
    binarized_image: str


@router.post("/binary_image", response_model=ImageResponse)
async def binary_image(request: ImageRequest):
    try:
        image_data = base64.b64decode(request.image)
        image = Image.open(BytesIO(image_data))
        binarized = binarize_image(image, request.algorithm)
        buffered = BytesIO()
        binarized.save(buffered, format="PNG")
        binarized_base64 = base64.b64encode(buffered.getvalue()).decode()

        return {"binarized_image": binarized_base64}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))