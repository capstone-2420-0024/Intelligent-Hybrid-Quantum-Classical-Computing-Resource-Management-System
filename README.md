# Quantum Computing Task Scheduler & Data Processing

## Project Overview
This project focuses on **data acquisition, processing, task scheduling, and anomaly detection** in a hybrid **quantum-classical computing system**. It integrates **real-time IoT sensor data** from the quantum environment, enabling smart resource scheduling and system health monitoring for optimized performance.

---

## System Architecture

### Major Components
1. **Sensor Simulator** – Cleans, synchronizes, and generates synthetic data.
2. **Task Scheduling System** – Assigns computing tasks to classical CPUs or QPUs.

---

## Data Processing Pipeline

### 1. Data Acquisition & Storage
- Collects from IoT sensors
- Storage formats:
  - `.csv`: `temperature.csv`, `maxigauge.csv`, `cooling.csv`
  
### 2. Data Preprocessing
- Outlier Detection 
- Noise Filtering (Moving Average, Low-Pass)
- Time Synchronization
- Normalization & Standardization

### 3. Data Management
- Output formats:
  - CSV for analysis

### 4. Data Forecasting
- **Forecasting Models**:
  - ARIMA
  - TimeGan
  - Transformer

---

## Task Scheduling for Quantum Computing

### Flow Overview
1. User submits task via frontend.
2. Scheduler routes to CPU or QPU.
3. Cluster Manager allocates resources.
4. Anomaly system monitors and mitigates risks.

**Features**:
- Dynamic Resource Management
- Quantum-Classical Load Balancing
- Fault Recovery & Rerouting

---

## Installation & Setup

### Install Dependencies
```bash
pip install -r requirements.txt

