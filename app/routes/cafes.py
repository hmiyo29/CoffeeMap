from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/cafes",
    tags=["cafes"],
)

# -------------------------------------
# Get all cafes
# -------------------------------------
@router.get("/", response_model=List[schemas.Cafe])
def read_cafes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cafes = crud.get_cafes(db, skip=skip, limit=limit)
    return cafes

# -------------------------------------
# Get single cafe by ID
# -------------------------------------
@router.get("/{cafe_id}", response_model=schemas.Cafe)
def read_cafe(cafe_id: int, db: Session = Depends(get_db)):
    cafe = crud.get_cafe(db, cafe_id=cafe_id)
    if cafe is None:
        raise HTTPException(status_code=404, detail="Cafe not found")
    return cafe

# -------------------------------------
# Create a new cafe
# -------------------------------------
@router.post("/", response_model=schemas.Cafe)
def create_cafe(cafe: schemas.CafeCreate, db: Session = Depends(get_db)):
    return crud.create_cafe(db, cafe)

# -------------------------------------
# Soft delete a cafe
# -------------------------------------
@router.delete("/{cafe_id}", response_model=schemas.Cafe)
def delete_cafe(cafe_id: int, db: Session = Depends(get_db)):
    deleted_cafe = crud.delete_cafe(db, cafe_id=cafe_id)
    if deleted_cafe is None:
        raise HTTPException(status_code=404, detail="Cafe not found")
    return deleted_cafe


# -------------------------------------
# # Restore a soft-deleted cafe
# -------------------------------------
@router.put("/{cafe_id}/restore", response_model=schemas.Cafe)
def restore_cafe(cafe_id: int, db: Session = Depends(get_db)):
    restored_cafe = crud.restore_cafe(db, cafe_id=cafe_id)
    if restored_cafe is None:
        raise HTTPException(status_code=404, detail="Cafe not found")
    return restored_cafe
