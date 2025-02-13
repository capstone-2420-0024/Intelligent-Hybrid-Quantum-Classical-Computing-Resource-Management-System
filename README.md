# Quantum Computing Task Scheduler & Data Processing

## Project Overview
This project focuses on **data acquisition, processing, task scheduling, and anomaly detection** in a **quantum computing system**. The system integrates **real-time IoT sensor data** from the quantum environment, processes it efficiently, and detects anomalies for optimized computing performance.

---

## System Architecture
### **Overall Structure**
The system consists of the following major components:
1. **Task Scheduling System** – Manages computational tasks between CPUs and Quantum Processing Units (QPU).  
2. **Anomaly Detection System** – Monitors system health and triggers maintenance mechanisms.  
3. **Data Acquisition & Storage** – Collects and stores temperature, pressure, and cooling system data in a time-series database.  
4. **Data Processing & Machine Learning** – Performs cleaning, anomaly detection, and predictive modeling.

### **System Flowchart**
![System Architecture](docs/system_architecture.png)

- **Frontend** → Allows users to submit quantum computing tasks.
- **Task Scheduler** → Distributes tasks to **CPU clusters** or **Quantum Processing Units (QPU)**.
- **Sensor Monitoring** → Collects data from **temperature & pressure sensors**.
- **Anomaly Detection** → Uses machine learning models to identify abnormal system behavior.

---

## Data Processing Pipeline
### **1.Data Acquisition & Storage**
- Data is collected from **IoT sensors** and stored in an **SQLite database** or **InfluxDB (for time-series data).**
- Key data types:
  - `temperature.csv` – Temperature readings from the QPU & cooling system.
  - `maxigauge.csv` – Pressure sensor readings.
  - `cooling.csv` – Cooling system activity & liquid temperature.

### **2.Data Preprocessing**
  **Outlier Detection (IQR method)** – Filters extreme values.  
  **Moving Average & Low-Pass Filtering** – Smooths fluctuations and removes noise.  
  **Time Synchronization** – Ensures sensor data is aligned for accurate analysis.  
  **Standardization & Normalization** – Converts values to standardized formats.  

### **3.Data Storage & Management**
- Processed data is stored in:
  - **CSV format** – Easy access for analysis.
  - **SQLite database** – For structured storage & SQL queries.
  - **Parquet files** – Optimized for large-scale processing.

### **4.Machine Learning & Forecasting**
- **Anomaly Detection Models**
  - **Isolation Forest**
  - **Local Outlier Factor (LOF)**
  - **Autoencoder (LSTM-based)**
- **Time Series Forecasting**
  - **ARIMA** – Classical statistical forecasting.
  - **LSTM** – Deep learning-based forecasting.
  - **XGBoost** – Gradient boosting method for prediction.

---

## Task Scheduling & Quantum Computing
### **Task Flow**
1️⃣ User submits computational tasks through the **frontend interface**.  
2️⃣ Task is sent to the **Task Scheduling Module**, which determines whether to execute on **CPU clusters** or **Quantum Processing Units (QPU)**.  
3️⃣ The **Computing Cluster Management System** dynamically adjusts the resource allocation.  
4️⃣ The **Anomaly Detection System** continuously monitors system health.  

### **Task Scheduling Diagram**
![Task Scheduling](docs/task_scheduling.png)

**Key Features**
  **Dynamic Resource Management** – Expands or reduces computational resources based on demand.  
  **Quantum-Classical Hybrid Computing** – Balances load between classical CPUs and QPU clusters.  
  **Fault Recovery Mechanism** – Automatically reroutes tasks in case of system failure.  

---

## Anomaly Detection System
### **How it Works**
1️⃣ **Data Collection** – Retrieves temperature, pressure, and cooling data from sensors.  
2️⃣ **Feature Engineering** – Extracts statistical and time-series features.  
3️⃣ **Anomaly Detection Models** – Uses Isolation Forest, LOF, and Autoencoders to identify system failures.  
4️⃣ **Trigger Maintenance Mechanism** – Sends alerts or re-allocates tasks to maintain system stability.  

### **Anomaly Detection Flowchart**
![Anomaly Detection](docs/anomaly_detection.png)

---

## Installation & Setup for requirments packages
```bash
pip freeze > requirements.txt
