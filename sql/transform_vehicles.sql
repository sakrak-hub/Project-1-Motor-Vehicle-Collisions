ALTER TABLE motor_vehicle_collisions.temp_transform_vehicles_silver
ALTER COLUMN crash_date TYPE DATE USING crash_date::DATE;

ALTER TABLE motor_vehicle_collisions.temp_transform_vehicles_silver
ALTER COLUMN crash_time TYPE TIME USING crash_time::TIME;

ALTER TABLE motor_vehicle_collisions.temp_transform_vehicles_silver
ALTER COLUMN unique_id TYPE INTEGER USING unique_id::INTEGER;

ALTER TABLE motor_vehicle_collisions.temp_transform_vehicles_silver
ALTER COLUMN vehicle_id TYPE VARCHAR(25) USING vehicle_id::VARCHAR(25);

ALTER TABLE motor_vehicle_collisions.temp_transform_vehicles_silver
ALTER COLUMN collision_id TYPE INTEGER USING collision_id::INTEGER;

UPDATE motor_vehicle_collisions.temp_transform_vehicles_silver
SET state_registration = 'N/A'
WHERE state_registration IS NULL;

ALTER TABLE motor_vehicle_collisions.temp_transform_vehicles_silver
ALTER COLUMN state_registration TYPE VARCHAR(3) USING state_registration::VARCHAR(3);

UPDATE motor_vehicle_collisions.temp_transform_vehicles_silver
SET vehicle_type = 'Unknown'
WHERE vehicle_type IS NULL OR  vehicle_type='UNKNOWN';

ALTER TABLE motor_vehicle_collisions.temp_transform_vehicles_silver
ALTER COLUMN vehicle_type TYPE VARCHAR(25) USING vehicle_type::VARCHAR(25);

UPDATE motor_vehicle_collisions.temp_transform_vehicles_silver
SET vehicle_make = 'Unknown'
WHERE vehicle_make IS NULL ;

ALTER TABLE motor_vehicle_collisions.temp_transform_vehicles_silver
ALTER COLUMN vehicle_make TYPE VARCHAR(25) USING vehicle_make::VARCHAR(25);

ALTER TABLE motor_vehicle_collisions.temp_transform_vehicles_silver
ALTER COLUMN vehicle_year TYPE INTEGER USING vehicle_year::INTEGER;

UPDATE motor_vehicle_collisions.temp_transform_vehicles_silver
SET travel_direction = 'Unknown'
WHERE travel_direction IS NULL ;

ALTER TABLE motor_vehicle_collisions.temp_transform_vehicles_silver
ALTER COLUMN travel_direction TYPE VARCHAR(10) USING travel_direction::VARCHAR(10);

ALTER TABLE motor_vehicle_collisions.temp_transform_vehicles_silver
ALTER COLUMN vehicle_occupants TYPE INTEGER USING vehicle_occupants::INTEGER;

UPDATE motor_vehicle_collisions.temp_transform_vehicles_silver
SET pre_crash = 'Unknown'
WHERE pre_crash IS NULL ;

ALTER TABLE motor_vehicle_collisions.temp_transform_vehicles_silver
ALTER COLUMN pre_crash TYPE VARCHAR(50) USING pre_crash::VARCHAR(50);

UPDATE motor_vehicle_collisions.temp_transform_vehicles_silver
SET point_of_impact = 'Unspecified'
WHERE point_of_impact IS NULL ;

ALTER TABLE motor_vehicle_collisions.temp_transform_vehicles_silver
ALTER COLUMN point_of_impact TYPE VARCHAR(50) USING point_of_impact::VARCHAR(50);

UPDATE motor_vehicle_collisions.temp_transform_vehicles_silver
SET vehicle_damage = 'Unspecified'
WHERE vehicle_damage IS NULL ;

ALTER TABLE motor_vehicle_collisions.temp_transform_vehicles_silver
ALTER COLUMN vehicle_damage TYPE VARCHAR(50) USING vehicle_damage::VARCHAR(50);

UPDATE motor_vehicle_collisions.temp_transform_vehicles_silver
SET public_property_damage = 'Unspecified'
WHERE public_property_damage IS NULL ;

ALTER TABLE motor_vehicle_collisions.temp_transform_vehicles_silver
ALTER COLUMN public_property_damage TYPE VARCHAR(50) USING public_property_damage::VARCHAR(50);

UPDATE motor_vehicle_collisions.temp_transform_vehicles_silver
SET contributing_factor_1 = (
 CASE WHEN contributing_factor_1 ~ '^[0-9\.]+$' = true THEN 'Unspecified'
 	WHEN contributing_factor_1 IS NULL THEN 'Unspecified'
	ELSE contributing_factor_1
	END
);

ALTER TABLE motor_vehicle_collisions.temp_transform_vehicles_silver
ALTER COLUMN contributing_factor_1 TYPE VARCHAR(50) USING contributing_factor_1::VARCHAR(50);

UPDATE motor_vehicle_collisions.temp_transform_vehicles_silver
SET contributing_factor_2 = (
 CASE WHEN contributing_factor_2 ~ '^[0-9\.]+$' = true THEN 'Unspecified'
 	WHEN contributing_factor_2 IS NULL THEN 'Unspecified'
	ELSE contributing_factor_2
	END
);

ALTER TABLE motor_vehicle_collisions.temp_transform_vehicles_silver
ALTER COLUMN contributing_factor_2 TYPE VARCHAR(50) USING contributing_factor_2::VARCHAR(50);

CREATE TABLE IF NOT EXISTS motor_vehicle_collisions.mvc_vehicles_silver
AS (SELECT _dlt_id,
 _dlt_load_id,
 unique_id,
 vehicle_id,
 collision_id,
 crash_date,
 crash_time,
 state_registration,
 vehicle_type,
 vehicle_make,
 vehicle_year,
 travel_direction,
 vehicle_occupants,
 pre_crash,
 point_of_impact,
 vehicle_damage,
 public_property_damage,
 contributing_factor_1,
 contributing_factor_2
  FROM motor_vehicle_collisions.temp_transform_vehicles_silver);

DROP TABLE IF EXISTS motor_vehicle_collisions.temp_transform_vehicles_silver;
