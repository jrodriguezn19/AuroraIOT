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
(id, description, update_ms)
VALUES
(1,'Basic configuration for pzem-004t', 1000);

SELECT * FROM sensors_sensor_configuration;

-- Sensor
DELETE FROM sensors_sensor;

INSERT INTO sensors_sensor 
(id, name, brand, location, type_id, sensor_configuration_id)
VALUES 
(1, 'pzem-004t', 'Peacefair', 'Electric board - ground floor', 3, 1),
(2, 'pzem-004t', 'Peacefair', 'Electric board - ground floor', 3, 1);


SELECT * FROM sensors_sensor;

-- DATA
DELETE FROM mqttclient_data;

-- INSERT INTO mqttclient_data 
-- (id, time, sensor_id_id, data)
-- VALUES 
-- (1, CURRENT_TIMESTAMP, 1, '{"Voltage":100, "Current":3.32, "Frequency":55, "pf":0.87, "energy":2.74}');

SELECT * FROM mqttclient_data;
