from sqlalchemy.orm import Session
from database import SessionLocal
import crud
import schemas

# Create a DB session
db: Session = SessionLocal()

# -------------------------------------
# Test: Create a cafe
# -------------------------------------
new_cafe = schemas.CafeCreate(
    name="Test Cafe",
    address="Test Street 123",
    latitude=51.9225,
    longitude=4.47917,
    brew_methods="Espresso, V60"
)

created_cafe = crud.create_cafe(db, new_cafe)
print("Created cafe:", created_cafe)

# -------------------------------------
# Test: Get all cafes
# -------------------------------------
cafes = crud.get_cafes(db)
print("All active cafes:")
for cafe in cafes:
    print(cafe.id, cafe.name, cafe.adstat)

# -------------------------------------
# Test: Soft delete a cafe
# -------------------------------------
deleted_cafe = crud.delete_cafe(db, created_cafe.id)
print("Deleted cafe (adstat should be 'D'):", deleted_cafe.adstat)

# -------------------------------------
# Test: Get all cafes after deletion
# -------------------------------------
cafes = crud.get_cafes(db)
print("All active cafes after deletion (should not include deleted cafe):")
for cafe in cafes:
    print(cafe.id, cafe.name, cafe.adstat)
