-- SQLite

--TYPE
DELETE FROM sensors_sensor_type;

INSERT INTO sensors_sensor_type
(id, type)
VALUES
(1, 'Temperature'), (2, 'Humidity'), (3, 'Energy');

SELECT * FROM sensors_sensor_type;

--Sensor Configuration
DELETE FROM sensors_sensor_configuration;

INSERT INTO sensors_sensor_configuration
(id, update_ms)
VALUES
(1, 1000);

SELECT * FROM sensors_sensor_configuration;

-- Sensor
DELETE FROM sensors_sensor;

INSERT INTO sensors_sensor 
(id, name, brand, location, type_id, sensor_configuration_id)
VALUES 
(1, 'pzem-004t', 'Peacefair', 'First Floor', 3, 1);

SELECT * FROM sensors_sensor;

-- DATA
DELETE FROM sensors_data;

INSERT INTO sensors_data 
(id, time, sensor_id_id, data)
VALUES 
(1, CURRENT_TIMESTAMP, 1, '{"V":100, "A":3.32, "F":55, "PF":0.87, "E":2.74}');

SELECT * FROM sensors_data;
