# Spotter ELD Simulator (HOS & Routing)

## Project Objective
Develop a Full-Stack application (Django + React) that plans freight truck routes and automatically generates Electronic Logging Device (ELD) logs based on the FMCSA Hours of Service (HOS) regulations for property-carrying drivers.

## Tech Stack
- **Backend:** Django + Django REST Framework (DRF)
- **Frontend:** React + Tailwind CSS
- **Maps:** Free routing API (OpenRouteService or Mapbox) + Leaflet for rendering
- **Deployment:** Vercel (Frontend), Render/Railway (Backend)

## Business Rules (FMCSA - Property-Carrying Regulations)
- **11-Hour Driving Limit:** Max 11 hours driving after 10 consecutive hours off duty.
- **14-Hour Driving Window:** No driving beyond the 14th consecutive hour after coming on duty (non-driving "On Duty" tasks allowed after 14 hours).
- **30-Minute Rest Break:** 30-minute consecutive break after 8 cumulative hours of driving (can be "On Duty (Not Driving)").
- **70-Hour/8-Day Limit:** No driving after 70 hours on duty in any 8 consecutive days.
- **34-Hour Restart:** 34 consecutive hours "Off Duty" or in "Sleeper Berth" resets the 70-hour cycle.

### Assessment Assumptions
- 1 hour fixed "On Duty (Not Driving)" at Pickup and Drop-off locations.
- At least one 30-minute "On Duty (Not Driving)" fueling stop every 1,000 miles.
- No adverse driving conditions.

## Required Inputs
- `current_location`: Driver's starting point
- `pickup_location`: Where the load is picked up
- `dropoff_location`: Where the load is delivered
- `current_cycle_used`: Hours already consumed in the current 70-hour cycle

## Required Outputs
- **Interactive Map:** Calculated route and pinpointed stops (rests, sleep, fueling)
- **Digital Daily Logs:** 24-hour Graph Grid for each day, mapped to 4 duty statuses:
  - Off Duty
  - Sleeper Berth
  - Driving
  - On Duty (not driving)

## Architecture (Hexagonal / Ports and Adapters)
- **Domain Layer:** Pure Python entities and FMCSA (HOS) rules (no Django/ORM/external APIs)
- **Application Layer (Ports):** Use Cases and interfaces (e.g., GenerateRouteAndLogsUseCase)
- **Infrastructure Layer (Adapters):**
  - Driving Adapters: DRF views/urls
  - Driven Adapters: Routing API implementations

### Suggested Folder Structure
```
backend/
├── domain/               # Pure Python entities and FMCSA (HOS) rules
├── application/          # Use cases and interfaces (Ports)
├── infrastructure/       # Adapters (Routing APIs, DRF Views)
└── spotter_api/          # Core Django configuration (settings.py)
```

## Development Sprints
### Sprint 1: El Corazón del Sistema (4 horas)
- Lógica matemática FMCSA funcionando perfectamente
- Dominio puro Python, algoritmo HOSCalculator, pruebas unitarias

### Sprint 2: Infraestructura y Datos (4 horas)
- Adaptador API de mapas, casos de uso, endpoint DRF, validación de flujo

### Sprint 3: Visualización e Interfaz (4 horas)
- React UI, Leaflet mapa, LogGrid componente

### Sprint 4: Pulido, Despliegue y Demo (4 horas)
- UI/UX, despliegue, documentación, demo

## Commits
- Agregar commits claros para cada sprint y funcionalidad clave.

---

For more details, see PROJECT_CONTEXT.md.
