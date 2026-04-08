from sqlalchemy import Column, Integer, String, Text
from database import Base

class ImageAnalysis(Base):
    __tablename__ = "image_analysis"

    id = Column(Integer, primary_key=True, index=True)
    objects = Column(Text)
    activity = Column(String)
    context = Column(String)
    confidence = Column(String)