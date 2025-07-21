from fastapi import APIRouter, Depends, HTTPException, Form, Request
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from geopy.geocoders import Nominatim
from app import crud, schemas
from app.database import get_db
from app.models import Cafe # Assuming app.models is where Cafe is defined

router = APIRouter(
    prefix="/cafes",
    tags=["cafes"],
)
templates = Jinja2Templates(directory="app/frontend/templates")
geolocator = Nominatim(user_agent="CafeFinder")  # choose a unique app name


# -------------------------------------
# Create a new cafe (HTML form and submission endpoint)
# Place more specific paths first
# -------------------------------------

@router.get("/new", response_class=HTMLResponse)
def create_cafe_form(request: Request):
    return templates.TemplateResponse(
        "create_cafe.html",
        {
            "request": request,
            "message": "Please fill out the form to create a new cafe."
        }
    )

@router.post("/newcafe")
def create_cafe_by_address(
    name: str = Form(...),
    street: str = Form(...),
    street_number: str = Form(...),
    city: str = Form(...),
    brew_methods: str = Form(None),
    db: Session = Depends(get_db)
):
    # Combine into full address
    address = f"{street} {street_number}, {city}, Netherlands"

    location = geolocator.geocode(address)
    if location is None:
        raise HTTPException(status_code=400, detail="Address could not be geocoded")
    latitude, longitude = location.latitude, location.longitude
    cafe = schemas.CafeCreate(
        name=name,
        address=address,
        latitude=latitude,
        longitude=longitude,
        brew_methods=brew_methods
    )
    
    crud.create_cafe(db, cafe)
    if not db.query(Cafe).filter(Cafe.name == name).first():
        raise HTTPException(status_code=500, detail="Cafe creation failed")
    
    return RedirectResponse(url="/cafes/newcafesuccess", status_code=303)

@router.get("/newcafesuccess", response_class=HTMLResponse)
def create_cafe_success(request: Request):
    return templates.TemplateResponse(
        "create_cafe_success.html",
        {
            "request": request,
            "message": "Cafe created successfully!"
        }
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
# This should come after specific static paths like /new or /newcafe
# -------------------------------------
@router.get("/{cafe_id}", response_model=schemas.Cafe)
def read_cafe(cafe_id: int, db: Session = Depends(get_db)):
    cafe = crud.get_cafe(db, cafe_id=cafe_id)
    if cafe is None:
        raise HTTPException(status_code=404, detail="Cafe not found")
    return cafe
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
# Restore a soft-deleted cafe
# -------------------------------------
@router.put("/{cafe_id}/restore", response_model=schemas.Cafe)
def restore_cafe(cafe_id: int, db: Session = Depends(get_db)):
    restored_cafe = crud.restore_cafe(db, cafe_id=cafe_id)
    if restored_cafe is None:
        raise HTTPException(status_code=404, detail="Cafe not found")
    return restored_cafe