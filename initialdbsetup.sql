-- ===============================
-- Homestead Tracking Database
-- ===============================

-- Create the database and switch to it
CREATE DATABASE IF NOT EXISTS homestead;
USE homestead;

-- ===============================
-- Garden Beds and Crops
-- ===============================

-- Table: garden_beds
CREATE TABLE IF NOT EXISTS garden_beds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE,
    soil_type VARCHAR(100),
    area_sqft DECIMAL(10,2),
    notes TEXT
);

-- Table: crops
CREATE TABLE IF NOT EXISTS crops (
    id INT AUTO_INCREMENT PRIMARY KEY,
    crop_type VARCHAR(100),
    variety VARCHAR(100),
    plant_date DATE,
    bed_id INT,
    estimated_first_harvest DATE,
    estimated_last_harvest DATE,
    estimated_yield DECIMAL(10,2),
    yield_unit VARCHAR(20),
    status ENUM('planned', 'planted', 'growing', 'harvested', 'abandoned') DEFAULT 'planned',
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (bed_id) REFERENCES garden_beds(id) ON DELETE SET NULL
);


-- Table: crop_harvests
CREATE TABLE IF NOT EXISTS crop_harvests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    crop_id INT,
    harvest_date DATE,
    quantity DECIMAL(10,2),
    unit VARCHAR(20),
    notes TEXT,
    FOREIGN KEY (crop_id) REFERENCES crops(id) ON DELETE CASCADE
);

-- Table: crop_treatments
CREATE TABLE IF NOT EXISTS crop_treatments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    crop_id INT,
    treatment_date DATE,
    treatment_type ENUM('insecticide', 'herbicide', 'fungicide', 'fertilizer', 'other'),
    product_name VARCHAR(100),
    amount_used DECIMAL(10,2),
    unit VARCHAR(20),
    method VARCHAR(50),
    notes TEXT,
    FOREIGN KEY (crop_id) REFERENCES crops(id) ON DELETE CASCADE
);

-- Table: crop_notes
CREATE TABLE IF NOT EXISTS crop_notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    crop_id INT,
    note_date DATE,
    note TEXT,
    FOREIGN KEY (crop_id) REFERENCES crops(id) ON DELETE CASCADE
);

-- ===============================
-- Chickens (Egg and Meat Tracking)
-- ===============================

-- Table: chickens
CREATE TABLE IF NOT EXISTS chickens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    breed VARCHAR(100),
    purpose ENUM('egg', 'meat', 'dual'),
    sex ENUM('hen', 'rooster', 'unknown'),
    hatch_date DATE,
    acquired_date DATE,
    status ENUM('alive', 'butchered', 'sold', 'dead') DEFAULT 'alive',
    notes TEXT
);

-- Table: egg_production
CREATE TABLE IF NOT EXISTS egg_production (
    id INT AUTO_INCREMENT PRIMARY KEY,
    chicken_id INT,
    lay_date DATE,
    egg_count INT,
    egg_color VARCHAR(50),
    notes TEXT,
    FOREIGN KEY (chicken_id) REFERENCES chickens(id) ON DELETE CASCADE
);

-- Table: chicken_weights
CREATE TABLE IF NOT EXISTS chicken_weights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    chicken_id INT,
    weigh_date DATE,
    weight_lbs DECIMAL(5,2),
    notes TEXT,
    FOREIGN KEY (chicken_id) REFERENCES chickens(id) ON DELETE CASCADE
);

-- ===============================
-- Pets (Dogs, Cats, Other)
-- ===============================

-- Table: pets
CREATE TABLE IF NOT EXISTS pets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    species ENUM('dog', 'cat', 'other'),
    breed VARCHAR(100),
    sex ENUM('male', 'female', 'unknown'),
    birth_date DATE,
    acquired_date DATE,
    status ENUM('alive', 'deceased', 'rehomed') DEFAULT 'alive',
    notes TEXT
);

-- Table: pet_health_records
CREATE TABLE IF NOT EXISTS pet_health_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id INT,
    record_date DATE,
    type ENUM('vaccination', 'vet visit', 'treatment', 'weight', 'other'),
    description TEXT,
    cost DECIMAL(10,2),
    notes TEXT,
    FOREIGN KEY (pet_id) REFERENCES pets(id) ON DELETE CASCADE
);

-- ===============================
-- Equipment Maintenance
-- ===============================

-- Table: equipment
CREATE TABLE IF NOT EXISTS equipment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    brand VARCHAR(100),
    model VARCHAR(100),
    purchase_date DATE,
    status ENUM('in use', 'stored', 'sold', 'broken') DEFAULT 'in use',
    notes TEXT
);

-- Table: equipment_maintenance
CREATE TABLE IF NOT EXISTS equipment_maintenance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_id INT,
    maintenance_date DATE,
    type VARCHAR(100),
    description TEXT,
    cost DECIMAL(10,2),
    performed_by VARCHAR(100),
    notes TEXT,
    FOREIGN KEY (equipment_id) REFERENCES equipment(id) ON DELETE CASCADE
);

-- ===============================
-- Optional: General Notes
-- ===============================

CREATE TABLE IF NOT EXISTS general_notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category ENUM('garden', 'chicken', 'pet', 'equipment', 'general'),
    reference_id INT,
    note_date DATE,
    note TEXT
);
