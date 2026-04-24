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

## 3. Data Merging & Preparation
The foundation of Végam is a robust data integration pipeline that consolidates four critical components:
- **Factories.csv**: Supply-side information (capacity, variability).
- **Projects.csv**: Demand-side data (locations, priority levels).
- **Deliveries.csv**: Core transactional records.
- **External_Factors.csv**: Daily environmental conditions (weather, traffic).

### Step 1: Defining the Objective
We reformulated the problem from a simple "On-Time vs. Delayed" classification into a **Continuous Regression Problem** by creating the target variable **delay_hours** (*actual delivery time − expected delivery time*). This allows the model to capture the exact severity of delays.

### Step 2: Preventing Data Leakage
To ensure technical rigor, we eliminated all post-delivery signals (Actual Time, Delay Flag) and high-cardinality noise (Delivery IDs, Zero-variance features) before training. This ensures the model learns true underlying logistics patterns rather than memorizing shortcuts.

### Step 3: Feature Engineering Strategy
Rather than using raw columns, we engineered high-signal features:
- **Routing Complexity**: Actual road distance vs. straight-line distance.
- **Supply Risk**: Composite of factory capacity and production variability.
- **Compound Effects**: Interactions between weather and traffic.
- **Temporal Signals**: Cyclical encoding of days and weeks.

---

## 4. Technical & Modeling Differentiators (Our Edge)
### Operational Loss Optimization (MAE over MSE)
Most teams use MSE, which over-penalizes outliers. We optimized for **Mean Absolute Error (MAE)**, ensuring our model speaks the language of operational reality: "On average, the prediction is accurate within X hours."

### Mathematically Consistent Forensics (TreeSHAP)
We move beyond biased "Feature Importance" metrics by integrating **TreeSHAP**. This ensures that the "credit" for a delay is distributed fairly and mathematically, guaranteeing that the sum of the forensic parts exactly equals the total prediction.

### Digital Twin Optimization Heuristic
We use the model as a **Simulator**. Our engine takes high-risk deliveries and re-simulates them across thousands of permutations (different days, different factories) to mathematically search for the highest "Reward" configuration.

---

## 5. Product & Strategic Differentiators
### "Glass-Box" Forensics
We don't just say "there is a 6-hour delay"—we prove why (e.g., "Traffic added 1.5h, but high-priority status saved 0.4h"). This provides the mathematical audit trail essential for industrial trust.

### Actionable Optimization
Végam is prescriptive. Our Optimization Module doesn't just flag risks; it proposes validated solutions like Factory Swaps or Rescheduling to maximize "Reward-at-Risk."

### The AI-to-Executive Bridge
Using **Groq/Llama-3**, technical SHAP vectors are translated into plain-English **Forensic Narratives**, making data-driven intelligence accessible to board-level stakeholders.

---

## 6. Model Architecture: XGBoost + TreeSHAP
We utilize a **Tuned XGBoost Regressor** for its superior performance on non-linear tabular data. The model is wrapped in a TreeSHAP explainer to provide local feature attribution for every single inference call.

---

## 7. Forensic Impact Analysis
Our **"Force Field Analysis"** chart (Diverging Bar) translates game-theory mathematics into a visual "Tug-of-War":
- **Negative Forces (Green)**: Factors pulling the delay down.
- **Positive Forces (Orange)**: Factors pushing the delay up.
This allows a "root-cause audit" in under 5 seconds.

---

## 8. Technical Stack
- **Engine**: Python 3.10+, XGBoost, TreeSHAP
- **Interface**: Streamlit (Industrial Design System)
- **Intelligence**: Groq / Llama-3 (Executive Narrative Generation)
- **Analytics**: Plotly (Force Field Visuals)

---

## 9. Appendix: Feature & Module Inventory

### Model Input Features
1. **Distance (km)** | 2. **Weather Index** | 3. **Traffic Index** | 4. **External Severity** | 5. **Base Production** | 6. **Production Variability** | 7. **Routing Complexity** | 8. **Supply Risk** | 9. **Priority Level** | 10. **Day of Week** | 11. **Weekend Flag** | 12. **Week of Month**

### Dashboard Functional Modules
1. **Operations Overview** | 2. **Delivery Optimizer** | 3. **Deep Dive Analysis** | 4. **Forensic Report**

---
**TEAM CHIRUTHA // LOGISTICS_INTEL**
*Predict. Prioritize. Optimize.*
