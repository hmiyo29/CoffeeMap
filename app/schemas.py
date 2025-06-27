from pydantic import BaseModel
from typing import Optional, List

# --------------------------------------
# Cafe Schemas
# --------------------------------------

class CafeBase(BaseModel):
    name: str
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    brew_methods: Optional[str] = None  # e.g. "V60, Aeropress, Espresso"

class CafeCreate(CafeBase):
    name: str  # Ensure name is required on create

class Cafe(CafeBase):
    id: int

    class Config:
        orm_mode = True

# --------------------------------------
# Review Schemas
# --------------------------------------

class ReviewBase(BaseModel):
    reviewer_name: str
    rating: int
    brew_method: Optional[str] = None
    roast_notes: Optional[str] = None
    review_text: Optional[str] = None

class ReviewCreate(ReviewBase):
    cafe_id: int  # Required to link review to a cafe

class Review(ReviewBase):
    id: int
    cafe_id: int

    class Config:
        orm_mode = True

# --------------------------------------
# Nested Example (Optional)
# For showing reviews within cafe responses
# --------------------------------------

class CafeWithReviews(Cafe):
    reviews: List[Review] = []
