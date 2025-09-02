from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

# --------------------------------------
# Cafe Model
# --------------------------------------

class Cafe(Base):
    __tablename__ = "cafes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    brew_methods = Column(String, nullable=True)  # e.g. "V60, Aeropress, Espresso"
    adstat = Column(String, default="A")  # Default status is "A" (active)
    # Relationships
    # reviews = relationship("Review", back_populates="cafe")

    reviews = relationship("Review", back_populates="cafe", cascade="all, delete-orphan")
# --------------------------------------
# Review Model
# --------------------------------------

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    cafe_id = Column(Integer, ForeignKey("cafes.id"))
    created_at = Column(DateTime, nullable=False)
    rating = Column(Integer, nullable=False)
    brew_method = Column(String, nullable=True)
    roast_notes = Column(String, nullable=True)
    review_text = Column(String, nullable=True)
    adstat = Column(String, default="A")  # Default status is "A" (active)


    # Relationships
    cafe = relationship("Cafe", back_populates="reviews")


