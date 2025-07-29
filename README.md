# 🏦 Credit Approval System

A scalable Django-based backend system for managing customers and loan applications, with support for asynchronous data loading using Celery and Redis. The system includes endpoints for customer registration, eligibility checks, loan creation, and more.

---

## 🚀 Features

- Customer registration and loan management
- Loan eligibility checker based on creditworthiness
- Celery-powered async task to preload customer and loan data from `.xlsx` files
- PostgreSQL for database
- Redis as Celery broker
- Dockerized for simple setup and deployment

---

## 🧾 Project Structure

credit_approval_system/
│
├── backend/ # Django project
│ ├── core/ # Core app: models, views, tasks
│ ├── backend/ # Django settings
│ └── manage.py
│
├── docker/ # Docker and compose files
│ ├── docker-compose.yml
│ └── Dockerfile
│
├── customer_data.xlsx # Input file for initial customer data
├── loan_data.xlsx # Input file for initial loan data
└── README.md


---

## ⚙️ Setup Instructions

### 🔧 Prerequisites

- Docker & Docker Compose installed
- Git

---

### 📦 Clone the repository

```bash
git clone https://github.com/utkarsh0830/Credit-Approval-System.git
cd Credit-Approval-System
