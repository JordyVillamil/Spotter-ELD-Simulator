Project Context: Spotter ELD Simulator (HOS & Routing)
1. Project Objective
Develop a Full-Stack application (Django + React) that plans freight truck routes and automatically generates Electronic Logging Device (ELD) logs based on the FMCSA Hours of Service (HOS) regulations for property-carrying drivers.

2. Tech Stack
Backend: Django + Django REST Framework (DRF).

Frontend: React + Tailwind CSS.

Maps: Free routing API (OpenRouteService or Mapbox) + Leaflet for rendering.

Deployment: Vercel (Frontend), Render/Railway (Backend).

3. Business Rules (FMCSA - Property-Carrying Regulations)
The simulation algorithm in the backend must strictly enforce the following HOS rules:

11-Hour Driving Limit: May drive a maximum of 11 hours after 10 consecutive hours off duty.

14-Hour Driving Window: May not drive beyond the 14th consecutive hour after coming on duty (though the driver can perform non-driving "On Duty" tasks after 14 hours).

30-Minute Rest Break: Requires a 30-minute consecutive break after 8 cumulative hours of driving. This break can be taken in an "On Duty (Not Driving)" status (e.g., fueling).

70-Hour/8-Day Limit: May not drive after having been on duty for 70 hours in any 8 consecutive days.

34-Hour Restart: Any period of 34 consecutive hours "Off Duty" or in the "Sleeper Berth" resets the 70-hour cycle back to zero.

Assessment Assumptions:

1 hour fixed "On Duty (Not Driving)" at the Pickup location.

1 hour fixed "On Duty (Not Driving)" at the Drop-off location.

Fueling: At least one 30-minute "On Duty (Not Driving)" stop every 1,000 miles.

No adverse driving conditions.

4. Required Inputs
The API must accept the following data:

current_location: Driver's starting point.

pickup_location: Where the load is picked up.

dropoff_location: Where the load is delivered.

current_cycle_used: Hours already consumed in the current 70-hour cycle (float/integer).

5. Required Outputs
Interactive Map: Display the calculated route and pinpoint stops (rests, 10h sleep periods, fueling).

Digital Daily Logs: Generate a 24-hour Graph Grid for each day of the trip. The timeline must be mapped to 4 specific duty statuses:

Off Duty

Sleeper Berth

Driving

On Duty (not driving)

6. Suggested Architecture (Hexagonal / Ports and Adapters)
To ensure maximum precision in the HOS calculations and facilitate testing, the Django backend must be implemented using a Hexagonal Architecture pattern.

1. Domain Layer: The pure core of the system. This is where entities (Trip, DailyLog, Event) and the HOS business rule engine (HOSCalculator) live.

Strict rule for CLI: There must be absolutely no Django imports, database ORMs, or external API calls in this layer. It must be pure Python.

2. Application Layer (Ports): - Contains the Use Cases (e.g., GenerateRouteAndLogsUseCase).

Defines the interfaces/abstractions (Ports) that the domain needs to communicate with the outside world, such as MapRoutingPort.

3. Infrastructure Layer (Adapters): - Driving Adapters: Django REST Framework views (views.py / urls.py) that receive the HTTP request, call the Use Case, and return the JSON response.

Driven Adapters: The actual implementations of the interfaces, such as the HTTP calls to OpenRouteService/Mapbox (MapboxAdapter).

Suggested Folder Structure for the CLI:

Plaintext
backend/
├── domain/               # Pure Python entities and FMCSA (HOS) rules
├── application/          # Use cases and interfaces (Ports)
├── infrastructure/       # Adapters (Routing APIs, DRF Views)
└── spotter_api/          # Core Django configuration (settings.py)
Instructions for GitHub Copilot CLI
Step 1 (Domain Models): Generate the pure Python classes for TripEvent and DailyLog in the domain/ folder.

Step 2 (HOS Engine): Write a function/class in the Domain layer that receives total driving distance/time and current_cycle_used, and returns a list of chronological TripEvent objects applying the FMCSA rules defined in Section 3.

Step 3 (Infrastructure): Create an adapter that fetches the real distance and polyline from a mapping API, and a DRF View to expose the Use Case.

Step 4 (Frontend): Create a React component named LogGrid that takes an array of events (with start_time, end_time, and status) and draws horizontal lines on a 24-hour timeline using CSS Grid or SVG, mimicking the physical FMCSA driver's daily log.

Sprint 1: El Corazón del Sistema (4 horas)
Objetivo: Tener la lógica matemática de la FMCSA funcionando perfectamente.

Hora 1: Configuración del entorno (Repo de Git, Proyecto Django, Proyecto React con Vite/Tailwind).

Hora 2-3: Desarrollo de la Capa de Dominio. Implementación del algoritmo HOSCalculator en Python puro. Es vital que este motor ya sepa cuándo el conductor debe dormir o parar por gasolina.

Hora 4: Pruebas unitarias básicas para la lógica HOS. Si la lógica falla, el mapa y la UI no sirven de nada.

Hito final: Código de dominio subido a GitHub (primer commit importante).

Sprint 2: Infraestructura y Datos (4 horas)
Objetivo: Conectar el backend con el mundo exterior.

Hora 1-2: Implementación del adaptador para la API de mapas (OpenRouteService o Mapbox). Obtención de distancias y polilíneas de ruta reales.

Hora 3: Creación de los Casos de Uso y el endpoint de Django REST Framework que reciba el origen/destino y devuelva el JSON con la ruta y los logs.

Hora 4: Validación del flujo completo de datos (Backend -> API Mapas -> Lógica HOS).

Hito final: API funcional que entrega los datos necesarios para el frontend.

Sprint 3: Visualización e Interfaz (4 horas)
Objetivo: Hacer que los datos se vean profesionales y fáciles de usar.

Hora 1: Estructura básica en React (Formulario de entrada con Tailwind).

Hora 2: Integración de Leaflet para mostrar el mapa con la ruta pintada y los iconos de paradas calculadas.

Hora 3-4: El Componente LogGrid. Esta es la parte estética clave. Dibujar las líneas de la bitácora electrónica siguiendo el formato del PDF que analizamos.

Hito final: Aplicación visualmente funcional (MVP).

Sprint 4: Pulido, Despliegue y Demo (4 horas)
Objetivo: Asegurar la estética y preparar una entrega impecable.

Hora 1: "Polishing" de UI/UX. Mejora de colores, tipografía y manejo de estados de carga (skeletons/spinners). Esto compensa cualquier pequeña imprecisión técnica.

Hora 2: Despliegue (Vercel para React, Render/Railway para Django). Asegúrate de que los enlaces "Live" funcionen perfectamente.

Hora 3: Grabación del video de Loom. Explica tu decisión de usar Arquitectura Hexagonal y cómo tu algoritmo respeta las reglas de la FMCSA.

Hora 4: Documentación final en el README.md y envío del correo.

agregar commits a cada uno de los sprints