from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import (
    garden_beds, crops, crop_harvests, crop_treatments, crop_notes,
    chickens, egg_production, chicken_weights,
    pets, pet_health_records,
    equipment, equipment_maintenance,
    general_notes
)
from backend.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Homestead Tracking Portal")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(garden_beds.router, prefix="/api/garden_beds", tags=["Garden Beds"])
app.include_router(crops.router, prefix="/api/crops", tags=["Crops"])
app.include_router(crop_harvests.router, prefix="/api/crop_harvests", tags=["Crop Harvests"])
app.include_router(crop_treatments.router, prefix="/api/crop_treatments", tags=["Crop Treatments"])
app.include_router(crop_notes.router, prefix="/api/crop_notes", tags=["Crop Notes"])

app.include_router(chickens.router, prefix="/api/chickens", tags=["Chickens"])
app.include_router(egg_production.router, prefix="/api/egg_production", tags=["Egg Production"])
app.include_router(chicken_weights.router, prefix="/api/chicken_weights", tags=["Chicken Weights"])

app.include_router(pets.router, prefix="/api/pets", tags=["Pets"])
app.include_router(pet_health_records.router, prefix="/api/pet_health_records", tags=["Pet Health Records"])

app.include_router(equipment.router, prefix="/api/equipment", tags=["Equipment"])
app.include_router(equipment_maintenance.router, prefix="/api/equipment_maintenance", tags=["Equipment Maintenance"])

app.include_router(general_notes.router, prefix="/api/general_notes", tags=["General Notes"])