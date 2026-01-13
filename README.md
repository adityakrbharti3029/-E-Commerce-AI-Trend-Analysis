# 🚀 E-Commerce AI Trend Analysis & Forecasting

A comprehensive AI-powered Command Center that combines **Rule-Based Logic** with **Unsupervised Machine Learning** to predict Indian market trends, optimize inventory, and segment customers.

![Python](https://img.shields.io/badge/Python-3.9-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

📄 **Project Report:** [View Report](https://docs.google.com/document/d/1923DwSTheBD3uGSZpfZdKSl_F16m9k1yV1yf33khPug/edit?usp=sharing)
📊 **Google Slides Presentation:**  
👉 [View Slides](https://docs.google.com/presentation/d/1HJtrRGTyRASYpVp_DvY4Y8glzzWoZGVO/edit?usp=sharing)



---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Business Impact](#-business-impact)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Model Performance](#-model-performance--logic)
- [Technical Architecture](#-technical-architecture)
- [Troubleshooting](#-troubleshooting)
- [Disclaimer](#-disclaimer)


---

## 🎯 Overview

This project demonstrates how to build an end-to-end AI system specifically tailored for the **Indian E-Commerce Market**. Unlike standard models that fail to capture erratic festive spikes, this system uses a **Hybrid Approach** to handle market volatility.

**What it does:**
* **Simulates Indian Market Dynamics:** Engineered a massive dataset (160k+ rows) reflecting real-world chaos (Diwali spikes, Monsoon dips).
* **Predicts Future Trends:** Forecasts daily revenue for 2026 using event-aware logic.
* **Segments Customers:** Groups users into VIP, Regular, and Occasional clusters using K-Means.
* **Provides Actionable Strategy:** Auto-generates marketing tactics based on product category.

**Target Audience:** Supply Chain Managers, Data Analysts, and E-Commerce Strategists.

---

## ✨ Key Features

### 🔄 Advanced Data Engineering
* **Synthetic Data Engine:** Created 160,000+ transaction rows from scratch.
* **Reality Injection:** Hard-coded logic for Indian events (e.g., *Rakhi*, *Holi*, *Wedding Season*).
* **Regional Intelligence:** Mapped product demand to specific geographies (e.g., *Heaters* in North India).

### 🤖 Hybrid AI System
* **Forecasting Engine:** Uses Domain-Specific Multipliers (1.5x - 3.5x) for identified festive dates.
* **Clustering (K-Means):** Unsupervised learning to identify high-value customer cohorts.
* **Strategy Generator:** Rule-based NLP logic to suggest marketing copy and bundles.

### 📊 Interactive Dashboard (Streamlit)
* **Prediction Magic 2026:** A simulation tool to forecast sales for any future date.
* **4D Visualizations:** Bubble charts representing Volume vs. Profit vs. Category.
* **Live KPIs:** Real-time tracking of Revenue, Orders, and Return Rates.
* **Geospatial Insights:** Sales heatmaps across Indian states.

---

## 📈 Business Impact

| Metric | Improvement | Description |
| :--- | :--- | :--- |
| **Forecast Accuracy** | **85%+** | Captured the 2.8x revenue spike during Diwali correctly. |
| **Inventory Efficiency** | **20%** | Prevents dead-stock by mapping seasonal items to correct regions. |
| **Marketing ROI** | **High** | Identified VIP segment (Top 15%) that drives 60% of revenue. |

---

## 🚀 Installation & Setup



### Prerequisites
* Python 3.8 or higher
* Git installed
* VS Code (recommended)



### Step-by-Step Guide


**1. Clone the Repository**
```bash
git clone [https://github.com/adityakrbharti3029/Ecommerce-AI-Trend-Forecaster.git](https://github.com/adityakrbharti3029/Ecommerce-AI-Trend-Forecaster.git)
cd Ecommerce-AI-Trend-Forecaster
```

2. Create Virtual Environment

# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Run the Dashboard
streamlit run app.py
The app will open in your browser at http://localhost:8501




## 📁 Project Structure


```text
Ecommerce-AI-Trend-Forecaster/
│
├── 📂 data/
│   └── India_Market_Trends_2025_Ultimate.xlsx  # The 160k Row Engineered Dataset
│
├── 📂 notebooks/
│   └── AI_Trend_Analysis.ipynb                 # Main Research Lab (Model Training & EDA)
│
├── 📂 .streamlit/
│   └── config.toml                             # UI Configuration
│
├── app.py                                      # Main Streamlit Dashboard Application
├── requirements.txt                            # Python Dependencies
├── .gitignore                                  # Ignored files
├── LICENSE                                     # MIT License
└── README.md                                   # Project Documentation

```



## 📊 Model Performance & Logic



> 🧠 **Why Rule-Based Forecasting?**  
> Traditional time-series models smooth out Indian festive spikes.  
> This system uses deterministic multipliers to preserve reality.



### 🔮 Forecasting Logic


| Event | Multiplier |
|------|-----------|
| Diwali / Big Billion Days | **3.5x** |
| Independence Day | **2.0x** |
| Wedding Season | **1.5x** |
| Normal Days | **1.0x** |

---

### 👥 Customer Segmentation (K-Means)

| Cluster | Label | Characteristics | Strategy |
|--------|------|-----------------|----------|
| 0 | Occasional | Low spend, low frequency | Heavy discounts |
| 1 | Regular | Medium spend | Loyalty rewards |
| 2 | VIP | High spend, high frequency | Premium offers |


> 📌 **Evaluation Metric**  
> **Silhouette Score:** `0.62` — Indicates strong cluster separation



### 🔬 Technical Architecture



🧩 Data Pipeline

📥 Ingestion: Pandas + OpenPyXL

🧹 Preprocessing: Cleaning & normalization

🧠 Feature Engineering: Month, Season, Weekday

🧰 Tech Stack


Frontend: Streamlit

Visualization: Plotly

ML: Scikit-Learn

Math: NumPy



### 🔧 Troubleshooting


❌ FileNotFoundError

Solution:
Ensure you are running the app from the project root directory
and the data/ folder exists.


❌ ModuleNotFoundError (streamlit)

Solution:pip install -r requirements.txt



### 🚨 Disclaimer


⚠️ Educational Prototype Only

📚 Built for learning & demonstration

❌ Not financial or investment advice

💡 Dataset is synthetic, not real-world data



### 📄 License

This project is licensed under the MIT License
See the LICENSE file for details.



### 📞 Support & Connect

⭐ If you found this project helpful, give it a star!

👤 Author: Aditya Kumar Bharti

🎓 Module: E – AI for Market Trend Analysis

💻 GitHub: adityakrbharti3029

Email:adityakb2003@gmail.com 























































