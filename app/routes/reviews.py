from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
)

# -------------------------------------
# Get all reviews
# -------------------------------------
@router.get("/", response_model=List[schemas.Review])
def read_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reviews = crud.get_reviews(db, skip=skip, limit=limit)
    return reviews

# -------------------------------------
# Get single review by ID
# -------------------------------------
@router.get("/{review_id}", response_model=schemas.Review)
def read_review(review_id: int, db: Session = Depends(get_db)):
    review = crud.get_review(db, review_id=review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

# -------------------------------------
# Create a new review
# -------------------------------------
@router.post("/", response_model=schemas.Review)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.create_review(db, review)

# -------------------------------------
# Soft delete a review
# -------------------------------------
@router.delete("/{review_id}", response_model=schemas.Review)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    deleted_review = crud.delete_review(db, review_id=review_id)
    if deleted_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return deleted_review

# -------------------------------------
# Restore a soft-deleted review
# -------------------------------------
@router.put("/{review_id}/restore", response_model=schemas.Review)
def restore_review(review_id: int, db: Session = Depends(get_db)):
    restored_review = crud.restore_review(db, review_id=review_id)
    if restored_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return restored_review
