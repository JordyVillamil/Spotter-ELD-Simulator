# Spotter ELD Simulator (HOS & Routing)

## 📌 Project Objective
A Full-Stack application designed to plan freight truck routes and automatically generate Electronic Logging Device (ELD) logs. This simulator strictly adheres to the FMCSA Hours of Service (HOS) regulations for property-carrying drivers, demonstrating complex domain logic isolated within a modern web framework.

## 🛠️ Tech Stack
- **Backend:** Python, Django, Django REST Framework (DRF)
- **Frontend:** React, Vite, Tailwind CSS v4
- **Mapping & Visualization:** Leaflet (react-leaflet), Custom React Gantt Chart
- **Architecture:** Hexagonal Architecture (Ports and Adapters)

---

## 🚀 Getting Started (Local Development)

The project is divided into a Django backend and a React frontend. You will need two terminal instances to run the application.

### 1. Backend Setup (Terminal 1)
Make sure you are in the root directory of the project.

```bash
# Create and activate the virtual environment
python -m venv venv
.\venv\Scripts\activate  # On Windows
# source venv/bin/activate # On Mac/Linux

# Install dependencies
pip install django djangorestframework django-cors-headers requests python-dotenv

# Run database migrations (Required for Django's core)
python manage.py migrate

# Start the development server
python manage.py runserver

# The backend API will run on http://127.0.0.1:8000/
```

## 2. Frontend Setup (Terminal 2)

Open a new terminal and navigate to the frontend folder.

```bash
# Enter the frontend directory
cd frontend

# Install Node dependencies
npm install

# Start the Vite development server
npm run dev
```

The React application will be available at http://localhost:5173/

## 🏗️ Architecture Design (Hexagonal)

This project implements a Hexagonal Architecture (Ports and Adapters) to decouple the core 
FMCSA business rules from the Django framework.

```
backend/
├── domain/           # Pure Python: HOS rules, Entities, and logic (Zero Django dependencies)
├── application/      # Ports: Use cases orchestrating the flow of data
├── infrastructure/   # Adapters: DRF Views, URLs, and external map API integrations
spotter_api/          # Core Django configuration
```

Benefits: The HOS calculation engine can be unit-tested instantly without a database, and the framework (Django) or the UI (React) can be replaced without touching the business logic.

## ⚖️ Business Rules Implemented (FMCSA)
- **11-Hour Driving Limit:** Max 11 hours driving after 10 consecutive hours off duty.
- **14-Hour Driving Window:** No driving beyond the 14th consecutive hour after coming on duty.
- **30-Minute Rest Break:** 30-minute consecutive break required after 8 cumulative hours of driving.
- **10-Hour Reset:** 10 consecutive hours of Sleeper Berth / Off Duty to reset driving hours.
- **Simulation Assumptions:** 1-hour fixed On-Duty time at Pickup/Drop-off, and a mandatory 30-min fueling stop every 1,000 miles.

## 📊 Features
- **Route Planner:** Input current, pickup, and drop-off locations.
- **Interactive Map:** Visualizes the calculated route using Leaflet.
- **ELD 24-Hour Logbook:** A dynamic, color-coded Gantt chart displaying the driver's duty status (Off Duty, Sleeper Berth, Driving, On Duty) over time.
- **Detailed Log Table:** Step-by-step breakdown of timestamps, locations, and status remarks.