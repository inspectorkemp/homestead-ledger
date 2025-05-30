from sqlalchemy import (
    Column, Integer, String, DECIMAL, Date, Enum, ForeignKey, Text, TIMESTAMP
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# GARDEN

class GardenBed(Base):
    __tablename__ = "garden_beds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    soil_type = Column(String(100))
    area_sqft = Column(DECIMAL(10, 2))
    notes = Column(Text)

    crops = relationship("Crop", back_populates="bed")


class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)
    crop_type = Column(String(100))
    variety = Column(String(100))
    plant_date = Column(Date)
    bed_id = Column(Integer, ForeignKey("garden_beds.id", ondelete="SET NULL"))
    estimated_first_harvest = Column(Date)
    estimated_last_harvest = Column(Date)
    estimated_yield = Column(DECIMAL(10, 2))
    yield_unit = Column(String(20))
    status = Column(Enum('planned', 'planted', 'growing', 'harvested', 'abandoned', name="crop_status"), default='planned')
    last_updated = Column(TIMESTAMP)
    notes = Column(Text)

    bed = relationship("GardenBed", back_populates="crops")
    harvests = relationship("CropHarvest", back_populates="crop", cascade="all, delete")
    treatments = relationship("CropTreatment", back_populates="crop", cascade="all, delete")
    notes_rel = relationship("CropNote", back_populates="crop", cascade="all, delete")


class CropHarvest(Base):
    __tablename__ = "crop_harvests"
    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id", ondelete="CASCADE"))
    harvest_date = Column(Date)
    quantity = Column(DECIMAL(10,2))
    unit = Column(String(20))
    notes = Column(Text)

    crop = relationship("Crop", back_populates="harvests")


class CropTreatment(Base):
    __tablename__ = "crop_treatments"
    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id", ondelete="CASCADE"))
    treatment_date = Column(Date)
    treatment_type = Column(Enum('insecticide', 'herbicide', 'fungicide', 'fertilizer', 'other', name="treatment_type"))
    product_name = Column(String(100))
    amount_used = Column(DECIMAL(10,2))
    unit = Column(String(20))
    method = Column(String(50))
    notes = Column(Text)

    crop = relationship("Crop", back_populates="treatments")


class CropNote(Base):
    __tablename__ = "crop_notes"
    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id", ondelete="CASCADE"))
    note_date = Column(Date)
    note = Column(Text)

    crop = relationship("Crop", back_populates="notes_rel")

# CHICKENS

class Chicken(Base):
    __tablename__ = "chickens"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    breed = Column(String(100))
    purpose = Column(Enum('egg', 'meat', 'dual', name="chicken_purpose"))
    sex = Column(Enum('hen', 'rooster', 'unknown', name="chicken_sex"))
    hatch_date = Column(Date)
    acquired_date = Column(Date)
    status = Column(Enum('alive', 'butchered', 'sold', 'dead', name="chicken_status"), default='alive')
    notes = Column(Text)

    eggs = relationship("EggProduction", back_populates="chicken", cascade="all, delete")
    weights = relationship("ChickenWeight", back_populates="chicken", cascade="all, delete")


class EggProduction(Base):
    __tablename__ = "egg_production"
    id = Column(Integer, primary_key=True, index=True)
    chicken_id = Column(Integer, ForeignKey("chickens.id", ondelete="CASCADE"))
    lay_date = Column(Date)
    egg_count = Column(Integer)
    egg_color = Column(String(50))
    notes = Column(Text)

    chicken = relationship("Chicken", back_populates="eggs")


class ChickenWeight(Base):
    __tablename__ = "chicken_weights"
    id = Column(Integer, primary_key=True, index=True)
    chicken_id = Column(Integer, ForeignKey("chickens.id", ondelete="CASCADE"))
    weigh_date = Column(Date)
    weight_lbs = Column(DECIMAL(5,2))
    notes = Column(Text)

    chicken = relationship("Chicken", back_populates="weights")

# PETS

class Pet(Base):
    __tablename__ = "pets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    species = Column(Enum('dog', 'cat', 'other', name="pet_species"))
    breed = Column(String(100))
    sex = Column(Enum('male', 'female', 'unknown', name="pet_sex"))
    birth_date = Column(Date)
    acquired_date = Column(Date)
    status = Column(Enum('alive', 'deceased', 'rehomed', name="pet_status"), default='alive')
    notes = Column(Text)

    health_records = relationship("PetHealthRecord", back_populates="pet", cascade="all, delete")


class PetHealthRecord(Base):
    __tablename__ = "pet_health_records"
    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id", ondelete="CASCADE"))
    record_date = Column(Date)
    type = Column(Enum('vaccination', 'vet visit', 'treatment', 'weight', 'other', name="health_type"))
    description = Column(Text)
    cost = Column(DECIMAL(10,2))
    notes = Column(Text)

    pet = relationship("Pet", back_populates="health_records")

# EQUIPMENT

class Equipment(Base):
    __tablename__ = "equipment"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    brand = Column(String(100))
    model = Column(String(100))
    purchase_date = Column(Date)
    status = Column(Enum('in use', 'stored', 'sold', 'broken', name="equipment_status"), default='in use')
    notes = Column(Text)

    maintenance = relationship("EquipmentMaintenance", back_populates="equipment", cascade="all, delete")


class EquipmentMaintenance(Base):
    __tablename__ = "equipment_maintenance"
    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id", ondelete="CASCADE"))
    maintenance_date = Column(Date)
    type = Column(String(100))
    description = Column(Text)
    cost = Column(DECIMAL(10,2))
    performed_by = Column(String(100))
    notes = Column(Text)

    equipment = relationship("Equipment", back_populates="maintenance")

# GENERAL NOTES

class GeneralNote(Base):
    __tablename__ = "general_notes"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(Enum('garden', 'chicken', 'pet', 'equipment', 'general', name="note_category"))
    reference_id = Column(Integer)
    note_date = Column(Date)
    note = Column(Text)