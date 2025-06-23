ALTER TABLE motor_vehicle_collisions.temp_transform_persons_silver 
ALTER COLUMN crash_date TYPE DATE USING crash_date::DATE;

ALTER TABLE motor_vehicle_collisions.temp_transform_persons_silver 
ALTER COLUMN crash_time TYPE TIME USING crash_time::TIME;

ALTER TABLE motor_vehicle_collisions.temp_transform_persons_silver
ALTER COLUMN person_id TYPE VARCHAR(25) USING person_id::VARCHAR(25);

ALTER TABLE motor_vehicle_collisions.temp_transform_persons_silver
ALTER COLUMN vehicle_id TYPE INTEGER USING vehicle_id::INTEGER;

ALTER TABLE motor_vehicle_collisions.temp_transform_persons_silver
ALTER COLUMN collision_id TYPE INTEGER USING collision_id::INTEGER;

ALTER TABLE motor_vehicle_collisions.temp_transform_persons_silver
ALTER COLUMN unique_id TYPE INTEGER USING unique_id::INTEGER;

ALTER TABLE motor_vehicle_collisions.temp_transform_persons_silver
ALTER COLUMN person_type TYPE VARCHAR(25) USING person_type::VARCHAR(25);

ALTER TABLE motor_vehicle_collisions.temp_transform_persons_silver
ALTER COLUMN person_injury TYPE VARCHAR(25) USING person_injury::VARCHAR(25);

UPDATE motor_vehicle_collisions.temp_transform_persons_silver
SET ped_role = 'Unspecified'
WHERE ped_role IS NULL;

ALTER TABLE motor_vehicle_collisions.temp_transform_persons_silver
ALTER COLUMN ped_role TYPE VARCHAR(25) USING ped_role::VARCHAR(25);

ALTER TABLE motor_vehicle_collisions.temp_transform_persons_silver
ALTER COLUMN person_sex TYPE VARCHAR(3) USING person_sex::VARCHAR(3);

UPDATE motor_vehicle_collisions.temp_transform_persons_silver
SET person_sex = 'N/A'
WHERE person_sex IS NULL;

ALTER TABLE motor_vehicle_collisions.temp_transform_persons_silver
ALTER COLUMN person_age TYPE INTEGER USING person_age::INTEGER;

UPDATE motor_vehicle_collisions.temp_transform_persons_silver
SET person_age = NULL
WHERE person_age < 0 OR person_age > 110;

UPDATE motor_vehicle_collisions.temp_transform_persons_silver
SET ejection = 'Unknown'
WHERE ejection IS NULL;

ALTER TABLE motor_vehicle_collisions.temp_transform_persons_silver
ALTER COLUMN ejection TYPE VARCHAR(25) USING ejection::VARCHAR(25);

UPDATE motor_vehicle_collisions.temp_transform_persons_silver
SET emotional_status = 'Unknown'
WHERE emotional_status IS NULL;

ALTER TABLE motor_vehicle_collisions.temp_transform_persons_silver
ALTER COLUMN emotional_status TYPE VARCHAR(25) USING emotional_status::VARCHAR(25);

UPDATE motor_vehicle_collisions.temp_transform_persons_silver
SET bodily_injury = 'Unknown'
WHERE bodily_injury IS NULL;

ALTER TABLE motor_vehicle_collisions.temp_transform_persons_silver
ALTER COLUMN bodily_injury TYPE VARCHAR(25) USING bodily_injury::VARCHAR(25);

UPDATE motor_vehicle_collisions.temp_transform_persons_silver
SET position_in_vehicle = 'Unknown'
WHERE position_in_vehicle IS NULL;

ALTER TABLE motor_vehicle_collisions.temp_transform_persons_silver
ALTER COLUMN position_in_vehicle TYPE VARCHAR(25) USING position_in_vehicle::VARCHAR(25);

UPDATE motor_vehicle_collisions.temp_transform_persons_silver
SET safety_equipment = 'Unknown'
WHERE safety_equipment IS NULL;

ALTER TABLE motor_vehicle_collisions.temp_transform_persons_silver
ALTER COLUMN safety_equipment TYPE VARCHAR(25) USING safety_equipment::VARCHAR(25);

UPDATE motor_vehicle_collisions.temp_transform_persons_silver
SET complaint = 'Unknown'
WHERE complaint IS NULL;

ALTER TABLE motor_vehicle_collisions.temp_transform_persons_silver
ALTER COLUMN complaint TYPE VARCHAR(25) USING complaint::VARCHAR(25);

DROP TABLE IF EXISTS motor_vehicle_collisions.mvc_persons_silver;

CREATE TABLE IF NOT EXISTS motor_vehicle_collisions.mvc_persons_silver
AS (SELECT _dlt_id,
 _dlt_load_id,
 person_id,
 vehicle_id,
 collision_id,
 unique_id,
 crash_date,
 crash_time,
 person_type,
 person_injury,
 ped_role,
 person_sex,
 person_age,
 ejection,
 emotional_status,
 bodily_injury,
 position_in_vehicle,
 safety_equipment,
 complaint 
 FROM motor_vehicle_collisions.temp_transform_persons_silver);

DROP TABLE IF EXISTS motor_vehicle_collisions.temp_transform_persons_silver;
