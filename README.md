# Plant Monitor — Arduino + Flask IoT Project

[![Build status](https://github.com/DevilinAus/plantproject/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/DevilinAus/plantproject/actions/workflows/test.yml)

A full-stack IoT plant monitoring system combining Arduino hardware with a Python Flask web app. Measures plant data over WiFi and displays results live with charts and user authentication.

---

## Features

- Arduino R4 Uno running WiFi web server, serving sensor data as JSON
- Manual HTTP response construction on Arduino for lightweight operation
- Arduino exposes multiple API routes:
  - `/sensor` — returns sensor data (soil moisture) as JSON
  - `/stats` — returns WiFi status and free memory info as JSON
- Flask backend using SQLAlchemy ORM for database management
- User login system with Flask-Login for authentication and security
- Interactive charts powered by Chart.js visualizing sensor trends
- Weather API integration (key stored in `.env`) for environmental context

---

## Getting Started

### Arduino Setup

1. Configure your WiFi network credentials in `SECRETS.H`.
2. Upload the Arduino sketch to your Arduino R4 Uno board.
3. The Arduino hosts a WiFi web server and sends sensor data over HTTP.

### Flask Backend Setup

1. Create a `.env` file in the backend directory with your weather API key, for example:

```
WEATHER_API_KEY=your_api_key_here
```

2. Install required Python packages:

```
pip install -r requirements.txt
```

3. Run the Flask app (testing mode):

```
flask run
```

4. Deploy the app to a WSGI webserver

---

## API Endpoints

- `/sensor` — Returns sensor data JSON (e.g., `{ "sensor": 212}`)
- `/info` — Returns WiFi strength and free memory info JSON (e.g., `{ "wifiStrength": "-53", "freeRam": 15600 }`)

---

## Technologies Used

- **Arduino R4 Uno** with manual HTTP response handling over WiFi
- **Flask** web framework for backend
- **SQLAlchemy** ORM for database modeling and interactions
- **Flask-Login** for secure user authentication
- **Chart.js** for dynamic frontend data visualization
- Integration with a **weather API** ([weatherapi.com](https://www.weatherapi.com/)) for enhanced environmental data

---

## Usage

- Access the Flask app via browser to view live plant data visualized in charts
- Login functionality restricts sensitive data and allows user-specific settings
- Arduino device continuously monitors plants and sends data over WiFi

---
