# 🚗 Motor Vehicle Collision ELT Pipeline and Data Analysis

This project automates the extraction, transformation, and visualization of motor vehicle collision data from NYC Open Data. It covers crash events, involved vehicles, and persons affected, and produces a weekly updated dashboard with analytical insights.

---

## 📌 Problem Statement

NYC's collision datasets contain **millions of rows**, making manual downloading and processing impractical. Additionally, data is **updated retroactively** and lacks stable unique identifiers for deduplication.

This project solves the problem by:

1. Automating **weekly ingestion** of three datasets (crashes, vehicles, persons).
2. Using **DLT** to load raw data into **PostgreSQL** (bronze layer).
3. Performing **data cleaning and transformation** (silver layer) using **Python (Pandas)** and **SQLAlchemy**.
4. Generating **aggregated insights and visualizations** using **Streamlit**.

---

## 🛠️ Technologies Used

- `DLT` – Extraction and loading
- `PostgreSQL` – Raw and transformed data storage
- `SQLAlchemy + Pandas` – Transformations and cleaning
- `Streamlit` – Interactive dashboard
- `Docker + Docker Compose` – Environment and orchestration
- `cron` – Monthly automation

---

## 🔄 ELT Workflow

![Pipeline Overview](MVC_ELT_Pipeline.png)

---

## 🧪 Workflow Process

1. A **cron job** triggers a Python script **every Monday at 10 AM**.
2. This script executes a **Docker Compose** setup: Python app + PostgreSQL + PGAdmin.
3. The Python pipeline extracts and loads NYC Open Data into **PostgreSQL** (bronze layer).
4. **Transform SQL queries** clean and prepare data into new tables (silver layer).
5. **Streamlit app** displays aggregated data on `localhost:8501`.

---

## 📊 Analysis and Insights

### 🕒 Time-Based Analysis
- Crashes by **hour of day**
- Crashes by **day of week** and **month**
- **Year-over-year** trends

### 🌍 Geographic Analysis
- Crashes by **borough**
- **Hotspot heatmaps** (lat/lon clustering)
- **Zip code** crash analysis

### 💥 Severity Analysis
- Fatality rates by **vehicle type** and **cause**
- Injury severity distribution (injured vs killed)
- Casualties by role: **pedestrian**, **cyclist**, **motorist**

### ⚠️ Contributing Factors
- Most common crash causes
- Factors linked to high fatality rates
- Vehicle-specific contributing patterns

### 👤 Demographic Patterns
- **Age** group distribution
- Gender patterns across crash types
- Injury rates by person type (driver/passenger/pedestrian)

### 🚘 Vehicle Patterns
- Top **vehicle types and makes** in crashes
- Impact of **vehicle age**
- **Occupancy patterns** and outcomes

---

## 📁 Directory Structure

```
.
├── src/
│   ├── extraction/
│   ├── transformation/
│   ├── loading/
│   ├── visualisation/
│   └── utils/
├── sql/
├── data/
├── Dockerfile
├── docker-compose.yaml
├── main.py
├── requirements.txt
└── README.md
```

---

## ✅ Future Improvements

- Add **unit tests** and data quality checks
- Connect to **cloud warehouse (BigQuery/Snowflake)**
- Add **real-time alerts** and anomaly detection

---

### 🔗 Access Dashboard

- **PostgreSQL**: [localhost:5432](http://localhost:5432)
- **PGAdmin**: [localhost:5050](http://localhost:5050)
- **Dashboard**: [localhost:8501](http://localhost:8501)
