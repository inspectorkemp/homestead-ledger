from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter()

@router.get("/", response_model=list[schemas.GardenBed])
def list_garden_beds(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.GardenBed).offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.GardenBed)
def create_garden_bed(bed: schemas.GardenBedCreate, db: Session = Depends(get_db)):
    db_bed = models.GardenBed(**bed.dict())
    db.add(db_bed)
    db.commit()
    db.refresh(db_bed)
    return db_bed

@router.get("/{bed_id}", response_model=schemas.GardenBed)
def get_garden_bed(bed_id: int, db: Session = Depends(get_db)):
    bed = db.query(models.GardenBed).filter(models.GardenBed.id == bed_id).first()
    if bed is None:
        raise HTTPException(status_code=404, detail="Garden bed not found")
    return bed

@router.put("/{bed_id}", response_model=schemas.GardenBed)
def update_garden_bed(bed_id: int, bed: schemas.GardenBedCreate, db: Session = Depends(get_db)):
    db_bed = db.query(models.GardenBed).filter(models.GardenBed.id == bed_id).first()
    if db_bed is None:
        raise HTTPException(status_code=404, detail="Garden bed not found")
    for k, v in bed.dict().items():
        setattr(db_bed, k, v)
    db.commit()
    db.refresh(db_bed)
    return db_bed

@router.delete("/{bed_id}")
def delete_garden_bed(bed_id: int, db: Session = Depends(get_db)):
    bed = db.query(models.GardenBed).filter(models.GardenBed.id == bed_id).first()
    if bed is None:
        raise HTTPException(status_code=404, detail="Garden bed not found")
    db.delete(bed)
    db.commit()
    return {"ok": True}