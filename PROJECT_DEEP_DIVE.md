# Végam: Logistics Intelligence & Forensic Deep Dive
### Technical Whitepaper | Team Chirutha | TVASTR '26

---

## 1. Executive Summary
**Végam** is an industrial-grade intelligence layer built to solve the "Black Box" problem in logistics delay prediction. Unlike standard predictive models that merely provide a number, Végam provides a **Forensic Audit Trail** for every delivery. By combining high-performance gradient boosting with TreeSHAP explainability and a reward-driven optimization engine, we transform passive data into active operational strategy.

---

## 2. The Problem Statement
Logistics networks are plagued by "unearned" delays—bottlenecks caused by weather, traffic, and production variability. Standard ERP systems fail because:
1. **Lack of Explainability**: Dispatchers see a delay but don't know *why*.
2. **Static Scheduling**: Decisions are made based on intuition, not mathematical reward maximization.
3. **Information Silos**: External factors (Weather/Traffic) are rarely integrated into the internal production forecast.

---

## 3. Data Engineering & Pipeline
Our pipeline is designed for high-frequency operational environments:
- **Feature Synthesis**: We ingest raw logistics data and synthesize complex features like *External Severity Index* (a weighted combination of weather and traffic) and *Routing Complexity*.
- **Temporal Encoding**: We use cyclical encoding for time-based features (Day of Week, Week of Month) to ensure the model understands the periodic nature of logistics bottlenecks.
- **Pre-computed Inference**: To ensure zero-latency in the "War Room" dashboard, we maintain a pre-computed forensic cache that stores SHAP attributions for the entire active fleet.

---

## 4. Model Architecture: XGBoost + TreeSHAP
At the core of Végam sits a **Tuned XGBoost Regressor**. 
- **Why XGBoost?** It excels at handling the non-linear, tabular data typical of logistics (where the relationship between distance and delay is often skewed by factory-specific production caps).
- **The Explainability Layer**: We utilize **TreeSHAP** (a fast, exact SHAP value estimation for tree models). Every prediction is broken down into its constituent forces, allowing us to quantify exactly how many minutes were added by traffic vs. how many were saved by high-priority dispatch.

---

## 5. Forensic Impact Analysis
Our "Force Field Analysis" chart is the project's signature. It translates complex game-theory mathematics (SHAP values) into a visual "Tug-of-War":
- **Negative Forces (Green)**: Factors pulling the delay down (e.g., Low Supply Risk, Efficient Factory).
- **Positive Forces (Orange)**: Factors pushing the delay up (e.g., Extreme Weather, High Distance).
This allows non-technical judges and operational managers to perform a "root-cause audit" in under 5 seconds.

---

## 6. Optimization & Reward Logic
Végam doesn't just predict; it **Optimizes**. We've implemented a custom **Reward Function**:
- **Reward = (Base_Value - Actual_Delay) * Priority_Multiplier**
The system runs thousands of simulations per delivery (swapping factories, rescheduling dates) to find the "Global Optimum"—the specific action that yields the highest reward gain for the fleet.

---

## 7. The "War-Room" Design System
Our UI is built on the **Industrial Intelligence** philosophy:
- **Editorial Typography**: Using *Playfair Display* for metrics to signal confidence and authority.
- **High-Density Data**: Monospaced *DM Mono* for all forensic data to ensure technical precision.
- **Decision Support**: The "What-If Simulator" allows human operators to interact with the AI, testing their own hypotheses against the model's logic in real-time.

---

## 8. Technical Stack
- **Engine**: Python 3.10+, XGBoost, TreeSHAP
- **Interface**: Streamlit (Industrial Design System)
- **Intelligence**: Groq / Llama-3 (Executive Narrative Generation)
- **Analytics**: Plotly (Force Field Visuals)
- **Deployment**: Integrated Git-managed operational pipeline

---

**TEAM CHIRUTHA // LOGISTICS_INTEL**
*Predict. Prioritize. Optimize.*
