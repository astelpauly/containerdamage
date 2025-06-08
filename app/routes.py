import os
from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from PIL import Image, ImageDraw

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

os.makedirs("app/static/uploads/original",exist_ok=True)
os.makedirs("app/static/uploads/predicted",exist_ok=True)


@router.get("/",response_class=HTMLResponse)
def home(request : Request):
    return templates.TemplateResponse("index.html",{"request":request})


@router.post("/detect_damage",response_class=HTMLResponse)
async def detect_damage(request:Request,file: UploadFile = File(...)):
    original_path = f"app/static/uploads/original/{file.filename}"
    with open(original_path,"wb") as buffer:
        buffer.write(await file.read())

    predicted_path = f"app/static/uploads/predicted/{file.filename}"

    image = Image.open(original_path)
    draw = ImageDraw.Draw(image)
    draw.rectangle([50, 50, 200, 200], outline="red", width=5)
    image.save(predicted_path)

    original_url = f"/static/uploads/original/{file.filename}"
    predicted_url = f"/static/uploads/predicted/{file.filename}"

    return templates.TemplateResponse("result.html",{
    "request":request,
    "original_url": original_url,
    "predicted_url":predicted_url})









