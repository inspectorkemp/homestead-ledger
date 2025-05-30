from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel

# Common base
class NotesBase(BaseModel):
    notes: Optional[str] = None

# GARDEN

class GardenBedBase(BaseModel):
    name: str
    soil_type: Optional[str] = None
    area_sqft: Optional[float] = None
    notes: Optional[str] = None

class GardenBedCreate(GardenBedBase): pass
class GardenBed(GardenBedBase):
    id: int
    class Config:
        orm_mode = True

class CropBase(BaseModel):
    crop_type: str
    variety: Optional[str] = None
    plant_date: Optional[date] = None
    bed_id: Optional[int] = None
    estimated_first_harvest: Optional[date] = None
    estimated_last_harvest: Optional[date] = None
    estimated_yield: Optional[float] = None
    yield_unit: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class CropCreate(CropBase): pass
class Crop(CropBase):
    id: int
    last_updated: Optional[datetime]
    class Config:
        orm_mode = True

class CropHarvestBase(BaseModel):
    crop_id: int
    harvest_date: date
    quantity: float
    unit: str
    notes: Optional[str] = None

class CropHarvestCreate(CropHarvestBase): pass
class CropHarvest(CropHarvestBase):
    id: int
    class Config:
        orm_mode = True

class CropTreatmentBase(BaseModel):
    crop_id: int
    treatment_date: date
    treatment_type: str
    product_name: Optional[str] = None
    amount_used: Optional[float] = None
    unit: Optional[str] = None
    method: Optional[str] = None
    notes: Optional[str] = None

class CropTreatmentCreate(CropTreatmentBase): pass
class CropTreatment(CropTreatmentBase):
    id: int
    class Config:
        orm_mode = True

class CropNoteBase(BaseModel):
    crop_id: int
    note_date: date
    note: str

class CropNoteCreate(CropNoteBase): pass
class CropNote(CropNoteBase):
    id: int
    class Config:
        orm_mode = True

# CHICKENS

class ChickenBase(BaseModel):
    name: str
    breed: Optional[str] = None
    purpose: str
    sex: str
    hatch_date: Optional[date] = None
    acquired_date: Optional[date] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class ChickenCreate(ChickenBase): pass
class Chicken(ChickenBase):
    id: int
    class Config:
        orm_mode = True

class EggProductionBase(BaseModel):
    chicken_id: int
    lay_date: date
    egg_count: int
    egg_color: Optional[str] = None
    notes: Optional[str] = None

class EggProductionCreate(EggProductionBase): pass
class EggProduction(EggProductionBase):
    id: int
    class Config:
        orm_mode = True

class ChickenWeightBase(BaseModel):
    chicken_id: int
    weigh_date: date
    weight_lbs: float
    notes: Optional[str] = None

class ChickenWeightCreate(ChickenWeightBase): pass
class ChickenWeight(ChickenWeightBase):
    id: int
    class Config:
        orm_mode = True

# PETS

class PetBase(BaseModel):
    name: str
    species: str
    breed: Optional[str] = None
    sex: str
    birth_date: Optional[date] = None
    acquired_date: Optional[date] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class PetCreate(PetBase): pass
class Pet(PetBase):
    id: int
    class Config:
        orm_mode = True

class PetHealthRecordBase(BaseModel):
    pet_id: int
    record_date: date
    type: str
    description: Optional[str] = None
    cost: Optional[float] = None
    notes: Optional[str] = None

class PetHealthRecordCreate(PetHealthRecordBase): pass
class PetHealthRecord(PetHealthRecordBase):
    id: int
    class Config:
        orm_mode = True

# EQUIPMENT

class EquipmentBase(BaseModel):
    name: str
    brand: Optional[str] = None
    model: Optional[str] = None
    purchase_date: Optional[date] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class EquipmentCreate(EquipmentBase): pass
class Equipment(EquipmentBase):
    id: int
    class Config:
        orm_mode = True

class EquipmentMaintenanceBase(BaseModel):
    equipment_id: int
    maintenance_date: date
    type: str
    description: Optional[str] = None
    cost: Optional[float] = None
    performed_by: Optional[str] = None
    notes: Optional[str] = None

class EquipmentMaintenanceCreate(EquipmentMaintenanceBase): pass
class EquipmentMaintenance(EquipmentMaintenanceBase):
    id: int
    class Config:
        orm_mode = True

# GENERAL NOTES

class GeneralNoteBase(BaseModel):
    category: str
    reference_id: Optional[int] = None
    note_date: date
    note: str

class GeneralNoteCreate(GeneralNoteBase): pass
class GeneralNote(GeneralNoteBase):
    id: int
    class Config:
        orm_mode = True