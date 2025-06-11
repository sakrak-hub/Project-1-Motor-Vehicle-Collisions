ALTER TABLE motor_vehicle_collisions.temp_transform_crashes_silver ALTER COLUMN crash_date TYPE DATE USING crash_date::DATE;

ALTER TABLE motor_vehicle_collisions.temp_transform_crashes_silver ALTER COLUMN crash_time TYPE TIME USING crash_time::TIME;

UPDATE motor_vehicle_collisions.temp_transform_crashes_silver
SET on_street_name = 'UNKNOWN'
WHERE on_street_name = (
SELECT DISTINCT(on_street_name) FROM motor_vehicle_collisions.temp_transform_crashes_silver
ORDER BY 1
LIMIT 1 
)
OR on_street_name IS NULL;

ALTER TABLE motor_vehicle_collisions.temp_transform_crashes_silver
ALTER COLUMN on_street_name TYPE VARCHAR(255) USING on_street_name::VARCHAR(255);

UPDATE motor_vehicle_collisions.temp_transform_crashes_silver
SET off_street_name = 'UNKNOWN'
WHERE off_street_name = (
SELECT DISTINCT(off_street_name) FROM motor_vehicle_collisions.temp_transform_crashes_silver
ORDER BY 1
LIMIT 1 
)
OR off_street_name IS NULL;

ALTER TABLE motor_vehicle_collisions.temp_transform_crashes_silver
ALTER COLUMN off_street_name TYPE VARCHAR(255) USING off_street_name::VARCHAR(255);

ALTER TABLE motor_vehicle_collisions.temp_transform_crashes_silver
ALTER COLUMN number_of_persons_injured TYPE INTEGER USING number_of_persons_injured::INTEGER;

ALTER TABLE motor_vehicle_collisions.temp_transform_crashes_silver
ALTER COLUMN number_of_persons_killed TYPE INTEGER USING number_of_persons_killed::INTEGER;

ALTER TABLE motor_vehicle_collisions.temp_transform_crashes_silver
ALTER COLUMN number_of_pedestrians_injured TYPE INTEGER USING number_of_pedestrians_injured::INTEGER;

ALTER TABLE motor_vehicle_collisions.temp_transform_crashes_silver
ALTER COLUMN number_of_pedestrians_killed TYPE INTEGER USING number_of_pedestrians_killed::INTEGER;

ALTER TABLE motor_vehicle_collisions.temp_transform_crashes_silver
ALTER COLUMN number_of_cyclist_injured TYPE INTEGER USING number_of_cyclist_injured::INTEGER;

ALTER TABLE motor_vehicle_collisions.temp_transform_crashes_silver
ALTER COLUMN number_of_cyclist_killed TYPE INTEGER USING number_of_cyclist_killed::INTEGER;

ALTER TABLE motor_vehicle_collisions.temp_transform_crashes_silver
ALTER COLUMN number_of_motorist_injured TYPE INTEGER USING number_of_motorist_injured::INTEGER;

ALTER TABLE motor_vehicle_collisions.temp_transform_crashes_silver
ALTER COLUMN number_of_motorist_killed TYPE INTEGER USING number_of_motorist_killed::INTEGER;

UPDATE motor_vehicle_collisions.temp_transform_crashes_silver
SET contributing_factor_vehicle_1 = 'Unspecified'
WHERE contributing_factor_vehicle_1 IN (
SELECT DISTINCT(contributing_factor_vehicle_1) FROM motor_vehicle_collisions.temp_transform_crashes_silver
ORDER BY 1
LIMIT 2 
)
OR contributing_factor_vehicle_1 IS NULL;

ALTER TABLE motor_vehicle_collisions.temp_transform_crashes_silver
ALTER COLUMN contributing_factor_vehicle_1 TYPE VARCHAR(255) USING contributing_factor_vehicle_1::VARCHAR(255);

UPDATE motor_vehicle_collisions.temp_transform_crashes_silver
SET contributing_factor_vehicle_2 = 'Unspecified'
WHERE contributing_factor_vehicle_2 IN (
SELECT DISTINCT(contributing_factor_vehicle_2) FROM motor_vehicle_collisions.temp_transform_crashes_silver
ORDER BY 1
LIMIT 2 
)
OR contributing_factor_vehicle_2 IS NULL;

ALTER TABLE motor_vehicle_collisions.temp_transform_crashes_silver
ALTER COLUMN contributing_factor_vehicle_2 TYPE VARCHAR(255) USING contributing_factor_vehicle_2::VARCHAR(255);

ALTER TABLE motor_vehicle_collisions.temp_transform_crashes_silver
ALTER COLUMN collision_id TYPE INTEGER USING collision_id::INTEGER;

UPDATE motor_vehicle_collisions.temp_transform_crashes_silver
SET vehicle_type_code1 = 'Unspecified'
WHERE vehicle_type_code1 IS NULL;

ALTER TABLE motor_vehicle_collisions.temp_transform_crashes_silver
ALTER COLUMN vehicle_type_code1 TYPE VARCHAR(255) USING vehicle_type_code1::VARCHAR(255);

UPDATE motor_vehicle_collisions.temp_transform_crashes_silver
SET vehicle_type_code2 = 'Unspecified'
WHERE vehicle_type_code2 IS NULL;

ALTER TABLE motor_vehicle_collisions.temp_transform_crashes_silver
ALTER COLUMN vehicle_type_code2 TYPE VARCHAR(255) USING vehicle_type_code2::VARCHAR(255);

UPDATE motor_vehicle_collisions.temp_transform_crashes_silver
SET borough = 'Unspecified'
WHERE borough IS NULL;

ALTER TABLE motor_vehicle_collisions.temp_transform_crashes_silver
ALTER COLUMN borough TYPE VARCHAR(255) USING borough::VARCHAR(255);

UPDATE motor_vehicle_collisions.temp_transform_crashes_silver
SET zip_code = NULL
WHERE zip_code IN (
SELECT DISTINCT(zip_code) FROM motor_vehicle_collisions.temp_transform_crashes_silver
ORDER BY 1
LIMIT 1 
);

ALTER TABLE motor_vehicle_collisions.temp_transform_crashes_silver
ALTER COLUMN zip_code TYPE INTEGER USING zip_code::INTEGER;

ALTER TABLE motor_vehicle_collisions.temp_transform_crashes_silver
ALTER COLUMN latitude TYPE INTEGER USING latitude::NUMERIC;

ALTER TABLE motor_vehicle_collisions.temp_transform_crashes_silver
ALTER COLUMN longitude TYPE INTEGER USING longitude::NUMERIC;

ALTER TABLE motor_vehicle_collisions.temp_transform_crashes_silver
DROP COLUMN IF EXISTS location__latitude, DROP COLUMN IF EXISTS location__longitude;

CREATE TABLE IF NOT EXISTS motor_vehicle_collisions.mvc_crashes_silver
AS (SELECT _dlt_id, _dlt_load_id, collision_id, crash_date, crash_time,
       on_street_name, off_street_name, number_of_persons_injured,
       number_of_persons_killed, number_of_pedestrians_injured,
       number_of_pedestrians_killed, number_of_cyclist_injured,
       number_of_cyclist_killed, number_of_motorist_injured,
       number_of_motorist_killed, contributing_factor_vehicle_1,
       contributing_factor_vehicle_2, vehicle_type_code1,
       vehicle_type_code2, borough, zip_code, latitude, longitude
       FROM motor_vehicle_collisions.temp_transform_crashes_silver);

DROP TABLE IF EXISTS motor_vehicle_collisions.temp_transform_crashes_silver;