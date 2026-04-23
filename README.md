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

## Technical Architecture

The project follows a decoupled architecture to ensure high performance:
- **Model Core**: XGBoost 3.2.0 trained on historical logistics datasets.
- **Data Pipeline**: A precomputation layer (`precompute.py`) that handles model inference, SHAP value calculation, and optimization simulations offline.
- **Frontend**: Streamlit-based interface utilizing Plotly for high-density data visualization.
- **Design System**: A custom industrial design language (Carbon/Paprika/Floral White) optimized for high-information density environments.

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
