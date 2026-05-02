# Technical Assessment: Microservices & System Design

This repository contains the implementation of a logging middleware, a vehicle maintenance scheduling microservice, and a notification system design.

## 📂 Project Structure
```text
ra2311003020244/
├── logging middleware/
│   └── logger.py                # Centralized logging utility
├── vehicle_maintence_scheduler/
│   ├── scheduler.py             # Knapsack-based optimization logic
│   └── (screenshots)            # Execution proof for Depots 1-5
├── notification_app_be/
│   ├── priority_inbox.py        # Stage 6: Notification sorting logic
│   └── (screenshots)            # Execution proof for Priority Inbox
└── notification_system_design.md # Stages 1-5: System Architecture & Design
```

---

## 🛠️ Components

### 1. Logging Middleware
A reusable logging module designed to send system logs to a centralized server. It categorizes logs by:
- **Application:** (e.g., backend)
- **Level:** (info, error, fatal)
- **Log Type:** (api, service, handler)

### 2. Vehicle Maintenance Scheduler
A microservice that solves the **0/1 Knapsack Problem** using Dynamic Programming. 
- **Goal:** Maximize the "Impact" score of vehicles serviced within a fixed "Mechanic Hours" budget per depot.
- **Complexity:** $O(N \cdot W)$ where $N$ is the number of vehicles and $W$ is the hour budget.

### 3. Notification System Design
A comprehensive design document covering:
- **Scalability:** Database indexing for millions of records.
- **Performance:** Implementation of Redis caching for high-frequency read operations.
- **Reliability:** Transitioning from synchronous loops to asynchronous message queues (RabbitMQ/Celery) for mass notifications.
- **Functional Logic:** A Priority Inbox algorithm that weights notifications by type (Placement > Result > Event).

---

## 🚀 Setup & Execution

### Prerequisites
- Python 3.x
- `requests` library

### Running the Scheduler
```bash
cd vehicle_maintence_scheduler
python scheduler.py
```

### Running the Priority Inbox
```bash
cd notification_app_be
python priority_inbox.py
```

---
*Generated for technical evaluation purposes.*
