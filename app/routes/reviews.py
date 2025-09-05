from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.requests import Request
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db

from datetime import datetime

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
# Create a new review
# -------------------------------------
@router.post("/createfromform/", response_model=schemas.Review)
def create_review(
    cafe_name: str = Form(...),
    reviewer_name: str = Form(...),
    rating: int = Form(...),
    brew_method: str = Form(None),
    roast_notes: str = Form(None),
    review_text: str = Form(None),
    db: Session = Depends(get_db)
):
    # Find the cafe by name
    cafe = crud.get_cafe_by_name(db, cafe_name=cafe_name)
    if cafe is None:
        raise HTTPException(status_code=404, detail="Cafe not found")


    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Build review schema
    review = schemas.ReviewCreate(
        cafe_id=cafe.id,
        created_at=created_at,
        reviewer_name=reviewer_name,
        rating=rating,
        brew_method=brew_method,
        roast_notes=roast_notes,
        review_text=review_text
    )

    # Store review in DB
    crud.create_review(db, review)

    # Redirect back to cafe detail page
    return RedirectResponse(
        url=f"/cafes/{cafe.name}", status_code=303
    )


# -------------------------------------
# Create a new review
# -------------------------------------
@router.post("/create", response_model=schemas.Review)
def create_review(
    cafe_name: str = Form(...),
    reviewer_name: str = Form(...),
    rating: int = Form(...),
    brew_method: str = Form(None),
    roast_notes: str = Form(None),
    review_text: str = Form(None),
    db: Session = Depends(get_db)
):
    # Find the cafe by name
    cafe = crud.get_cafe_by_name(db, cafe_name=cafe_name)
    if cafe is None:
        raise HTTPException(status_code=404, detail="Cafe not found")


    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Build review schema
    review = schemas.ReviewCreate(
        cafe_id=cafe.id,
        created_at=created_at,
        reviewer_name=reviewer_name,
        rating=rating,
        brew_method=brew_method,
        roast_notes=roast_notes,
        review_text=review_text
    )

    # Store review in DB
    crud.create_review(db, review)

    # Redirect back to cafe detail page
    return RedirectResponse(
        url=f"/cafes/{cafe.name}", status_code=303
    )

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
