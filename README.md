# 🌿 CarbonLens

**CarbonLens** is a full-stack carbon behavior analysis and recommendation platform. It collects data on individuals' daily habits — energy use, travel, food, and waste — and uses a machine learning recommendation engine to surface personalized, actionable suggestions for reducing their carbon footprint.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Dataset](#dataset)
- [Getting Started](#getting-started)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [API Reference](#api-reference)
- [Recommendation Engine](#recommendation-engine)

---

## Overview

CarbonLens bridges the gap between climate awareness and individual action. Users answer a short survey about their lifestyle — how much electricity they consume, how they commute, what they eat, and how they manage waste — and the platform responds with a tailored set of recommendations ranked by impact and feasibility.

The project is designed around a real behavioral dataset collected via survey, and augmented with synthetic data to improve model training coverage across demographics, occupations, and living situations.

---

## Features

- 📋 **Behavioral Survey** — Captures 56 features spanning demographics, energy, transport, diet, and waste habits
- 🤖 **ML Recommendation Engine** — Trained on carbon behavior data to match users with the most relevant sustainability actions
- 🔍 **Barrier-Aware Suggestions** — Recommendations factor in user-declared barriers (cost, time, awareness, convenience, social influence)
- 📊 **Data Pipeline** — Includes cleaning, deduplication, and synthetic data augmentation scripts
- 🌐 **REST API** — Python backend exposes endpoints consumed by the React frontend
- ⚡ **Responsive Frontend** — Built with React and JavaScript for a smooth survey and results experience

---

## Project Structure

```
CarbonLens/
├── backend/                  # Python Flask/FastAPI backend
│   ├── app.py                # Main application entry point
│   ├── model/                # ML recommendation model and training scripts
│   └── requirements.txt      # Python dependencies
│
├── carbonlens-frontend/      # React frontend
│   ├── src/
│   │   ├── components/       # Survey, results, and UI components
│   │   └── App.js            # Root component
│   ├── public/
│   └── package.json
│
└── data/                     # Dataset files
    └── carbon_behavior_dataset.csv   # Cleaned survey + synthetic data (130 entries, 23 features)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, JavaScript, CSS |
| Backend | Python (Flask / FastAPI) |
| ML / Data | scikit-learn, pandas, numpy |
| Data Format | CSV |

---

## Dataset

The model is trained on `carbon_behavior_dataset.csv`, which contains **130 unique entries** and **23 features** covering:

| Category | Features |
|---|---|
| Demographics | `age_group`, `gender`, `education`, `occupation`, `living_situation` |
| Energy & Travel | `electricity_kwh`, `weekly_travel_km`, `transport_mode` |
| Diet & Waste | `nonveg_meals_per_week`, `food_order_freq`, `waste_kg_per_week` |
| Current Behaviors | `reduce_electricity`, `public_transport_usage`, `vegetarian_choice`, `reduce_plastic`, `waste_segregation` |
| Attitudes | `climate_concern`, `tried_reduce_carbon` |
| Willingness | `willing_reduce_electricity`, `willing_public_transport`, `willing_reduce_nonveg`, `willing_reduce_plastic` |
| Barrier | `barrier` *(Cost / Lack of time / Lack of awareness / Convenience / Social influence / Not interested)* |

The dataset combines original survey responses with demographically balanced synthetic records generated to improve training coverage.

---

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- npm or yarn

---

### Backend Setup

```bash
# 1. Navigate to the backend directory
cd backend

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
python app.py
```

The API will be available at `http://localhost:5000` by default.

---

### Frontend Setup

```bash
# 1. Navigate to the frontend directory
cd carbonlens-frontend

# 2. Install dependencies
npm install

# 3. Start the development server
npm start
```

The app will be available at `http://localhost:3000` by default.

> **Note:** Make sure the backend server is running before launching the frontend.

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/recommend` | Submit survey responses and receive personalized recommendations |
| `GET` | `/health` | Check if the API is running |

**Example request body for `/recommend`:**

```json
{
  "age_group": "21-25",
  "gender": "Female",
  "education": "Undergraduate",
  "occupation": "Student",
  "living_situation": "Hostel / shared accommodation",
  "electricity_kwh": 150,
  "weekly_travel_km": 40,
  "transport_mode": "Public transport",
  "nonveg_meals_per_week": 2,
  "food_order_freq": "1-2",
  "waste_kg_per_week": 3.5,
  "climate_concern": 4,
  "barrier": "Cost"
}
```

---

## Recommendation Engine

The recommendation engine is a supervised ML model trained on behavioral survey data. It maps user input profiles to the most impactful and feasible carbon reduction actions based on:

- **Behavioral similarity** — Users with similar profiles and which changes they found most actionable
- **Willingness scores** — Predicted openness to changing electricity, transport, diet, and plastic habits
- **Barrier alignment** — Filters or ranks recommendations based on the user's stated barriers

Recommendations are ranked by predicted impact score and grouped into categories: *Energy*, *Transport*, *Diet*, and *Waste*.

---




---

*Built with 🌱 to make sustainable living a little more accessible.*
