# Vegam Delivery Delay Tracker

## Project Overview

Vegam is an advanced operational intelligence platform designed to predict, analyze, and mitigate delivery delays in complex supply chain networks. Developed for the TVASTR '26 hackathon, the system transitions from reactive logistics management to proactive optimization using high-fidelity gradient boosting and game-theoretic explainability.

The platform provides logistics managers with a "war room" dashboard to identify systemic bottlenecks, understand the root causes of predicted delays, and execute optimized interventions such as delivery rescheduling and factory-source swapping.

## Core Features

### 1. Predictive Forensics
Utilizing an XGBoost-based regression model, the system predicts delivery delays (in hours) based on a multi-dimensional feature set including weather severity, traffic indices, factory production variability, and routing complexity.

### 2. SHAP Explainability
The system integrates the TreeSHAP algorithm to decompose every prediction into its constituent drivers. This provides "glass-box" transparency, allowing users to see exactly how specific factors like high traffic or factory supply risk are contributing to a predicted delay.

### 3. Optimization & Intervention Layer
Beyond mere prediction, Vegam simulates corrective actions. The optimization engine evaluates thousands of alternatives for high-risk deliveries, proposing either temporal shifts (rescheduling) or spatial shifts (factory swaps) to maximize the "Reward at Risk" and ensure on-time delivery.

### 4. Interactive Strategic Dashboard
A multi-page Streamlit application provides:
- **Operations Overview**: High-level KPIs and global risk distributions.
- **Delivery Optimizer**: Daily dispatch rankings and automated recommendation summaries.
- **Deep Dive Analysis**: Granular per-delivery forensic reports with SHAP waterfall visualizations.
- **Executive Reporting**: Automated forensic narratives for board-level decision-making.

## Methodology & Technical Implementation

### 1. Data Engineering & Feature Architecture
The system processes multi-dimensional logistics data, transforming raw operational metrics into predictive signals:
- **Environmental Factors**: Weather and Traffic indices are synthesized into an `external_severity` score.
- **Operational Load**: Factory-side pressure is measured via `base_production_per_week` and `production_variability`.
- **Complexity Metrics**: Structural risk is quantified through `routing_complexity` and `distance_km`.

### 2. Predictive Modeling (The Engine)
We utilize **XGBoost (Extreme Gradient Boosting)** as the core predictive engine:
- **Model Selection**: Chosen for its superior performance on tabular logistics data and robustness against outliers.
- **Loss Function**: Optimized for Mean Absolute Error (MAE) to provide tangible, hour-based delay estimates.
- **Training Pipeline**: Includes automated hyperparameter tuning and cross-validation for high generalization.

### 3. Explainability Forensics (The 'Why')
Transparency is a core pillar. We implement **TreeSHAP (SHAP Values)** to decompose every prediction:
- **Global Importance**: Identifies primary delay drivers across the entire fleet.
- **Local Attribution**: Every delivery features a SHAP Waterfall Decomposition showing specific feature contributions.
- **Game Theory Foundation**: Ensures a mathematically defensible forensic audit trail for every prediction.

### 4. Optimization Engine (Actionable Intelligence)
The **Optimization Module** uses a reward-based heuristic to suggest interventions:
- **Reward Function**: Balances delivery priority against the magnitude of predicted delay.
- **What-If Simulations**: Tests alternative temporal (reschedule) and spatial (factory swap) scenarios.
- **Simulation Sandbox**: Allows real-time human-in-the-loop adjustments to observe non-linear impacts.

### 5. AI Narrative Synthesis
Integrated **Large Language Models (via Groq/Llama-3)** bridge the gap between data and decision-making:
- **Automated Reporting**: Generates high-fidelity narrative forensic reports.
- **Executive Summaries**: Translates technical SHAP values into plain-English "Top Critical Interventions."

## Technical Stack
- **ML Framework**: XGBoost
- **Explainability**: SHAP (Lundberg et al.)
- **Dashboard**: Streamlit (Custom Industrial Design System)
- **Visualizations**: Plotly (High-contrast grid systems)
- **AI Backend**: Groq / Llama-3-70B

## Installation

### Prerequisites
- Python 3.13 or higher
- Git

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/pranavrajgali/Vegam_DeliveryDelayTracker.git
   cd Vegam_DeliveryDelayTracker
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Data Precomputation
Before launching the dashboard, the precomputation script must be executed to process the raw datasets and generate the optimization reports:
```bash
python app/precompute.py
```
This script will generate all necessary CSV and JSON artifacts in the `app/data/` directory.

### 2. Launching the Dashboard
Start the Streamlit application from the project root:
```bash
streamlit run app/main.py
```
The dashboard will be accessible via your web browser (typically at `http://localhost:8501`).

## Team and Event Details
- **Project Name**: Vegam
- **Team Name**: Team Vegam
- **Event**: TVASTR '26
- **Objective**: Enhancing Supply Chain Resilience through Predictive Analytics
