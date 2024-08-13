# AuroraIOT - Backend - API

## Overview

AuroraIOT is a Python and Django-based application designed for real-time energy consumption monitoring in buildings. By leveraging pzem-004t sensors and ESP32 microcontrollers, AuroraIOT captures precise energy consumption data and transmits it securely and efficiently via Wi-Fi using the MQTT protocol. This data is processed by the central AuroraIOT backend, providing building managers with accurate and timely insights for optimizing building management.

![image](https://github.com/user-attachments/assets/7edb3edf-1566-4256-ac5b-6c0dbe2b16c5)

## Features

- **Real-Time Monitoring**: Continuously monitor energy consumption with high precision.
- **Sensor Integration**: Utilizes pzem-004t sensors for capturing energy data.
- **Microcontroller Support**: Integrated with ESP32 for data collection and transmission.
- **MQTT Protocol**: Ensures secure and efficient data communication to the backend.
- **Django Backend**: Robust and scalable backend system built with Django.

## Technology Stack

- **Backend**: Python, Django
- **Microcontroller**: ESP32
- **Sensors**: pzem-004t
- **Communication Protocol**: MQTT
- **Network**: Wi-Fi

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/jrodriguez19/AuroraIOT.git
   ```

2. **Navigate to the Project Directory**

   ```bash
   cd auroraiot-backend
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**

   ```bash
   python manage.py migrate
   ```

5. **Run the Server**

   ```bash
   python manage.py runserver
   ```

## Configuration

Ensure that your ESP32 microcontroller is configured to connect to the same network as the AuroraIOT backend. The MQTT broker details should also be configured in the microcontroller's firmware.

## Usage

Once the backend is running and the microcontrollers are connected, energy consumption data will be automatically transmitted and can be monitored through the Django admin interface or custom frontend applications.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

## Contact

For any inquiries or support, please contact [jrodrigueznocua@gmail.com](mailto:your-email@example.com).
