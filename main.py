from fastapi import FastAPI, File, UploadFile
from services.vision import analyze_image

from database import SessionLocal, engine, Base
from models import ImageAnalysis

import json


Base.metadata.create_all(bind=engine)

app = FastAPI()


# 🔹 POST - ANALIZAR IMAGEN
@app.post("/analyze-image")
async def analyze(file: UploadFile = File(...)):
    result = await analyze_image(file)

    db = SessionLocal()

    try:
        if "error" not in result:
            new_record = ImageAnalysis(
                objects=json.dumps(result.get("objects", [])),
                activity=result.get("activity"),
                context=result.get("context"),
                confidence=result.get("confidence")
            )

            db.add(new_record)
            db.commit()
            db.refresh(new_record)

    finally:
        db.close()

    return result



@app.get("/analyses")
def get_analyses():
    db = SessionLocal()

    try:
        analyses = db.query(ImageAnalysis).all()

        results = []
        for item in analyses:
            results.append({
                "id": item.id,
                "objects": json.loads(item.objects),
                "activity": item.activity,
                "context": item.context,
                "confidence": item.confidence
            })

        return results

    finally:
        db.close()



@app.get("/analyses/{analysis_id}")
def get_analysis_by_id(analysis_id: int):
    db = SessionLocal()

    try:
        item = db.query(ImageAnalysis).filter(ImageAnalysis.id == analysis_id).first()

        if not item:
            return {"error": "No encontrado"}

        return {
            "id": item.id,
            "objects": json.loads(item.objects),
            "activity": item.activity,
            "context": item.context,
            "confidence": item.confidence
        }

    finally:
        db.close()