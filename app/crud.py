from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas

# --------------------------------------
# Cafe CRUD
# --------------------------------------

# Get all cafes
# This function retrieves all cafes with an active status (adstat = "A").
def get_cafes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cafe).filter(models.Cafe.adstat == "A").offset(skip).limit(limit).all()

def get_cafes_all(db: Session, skip: int = 0, limit: int = 100):
    """
    This function retrieves all cafes regardless of their status.
    Useful for administrative purposes.
    """
    return db.query(models.Cafe).offset(skip).limit(limit).all()

# Get a single cafe by ID
def get_cafe(db: Session, cafe_id: int):
    return db.query(models.Cafe).filter(models.Cafe.id == cafe_id, models.Cafe.adstat == "A").first()

# Create a new cafe
# This function creates a new cafe entry in the database.
def create_cafe(db: Session, cafe: schemas.CafeCreate):
    db_cafe = models.Cafe(**cafe.dict())
    db.add(db_cafe)
    db.commit()
    db.refresh(db_cafe)
    return db_cafe

# Soft delete cafe
def delete_cafe(db: Session, cafe_id: int):
    db_cafe = db.query(models.Cafe).filter(models.Cafe.id == cafe_id).first()
    if db_cafe:
        db_cafe.adstat = "D"
        db.commit()
        db.refresh(db_cafe)
    return db_cafe

# bring back ADSTAT to "A"
def restore_cafe(db: Session, cafe_id: int):
    db_cafe = db.query(models.Cafe).filter(models.Cafe.id == cafe_id).first()
    if db_cafe:
        db_cafe.adstat = "A"
        db.commit()
        db.refresh(db_cafe)
    return db_cafe

# --------------------------------------
# Review CRUD
# --------------------------------------

def get_reviews(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Review).filter(models.Review.adstat == "A").offset(skip).limit(limit).all()

def get_review(db: Session, review_id: int):
    return db.query(models.Review).filter(models.Review.id == review_id, models.Review.adstat == "A").first()

def create_review(db: Session, review: schemas.ReviewCreate):
    db_review = models.Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

# Soft delete review
def delete_review(db: Session, review_id: int):
    db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if db_review:
        db_review.adstat = "D"
        db.commit()
        db.refresh(db_review)
    return db_review

# bring back ADSTAT to "A"
def restore_review(db: Session, review_id: int):
    db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if db_review:
        db_review.adstat = "A"
        db.commit()
        db.refresh(db_review)
    return db_review
