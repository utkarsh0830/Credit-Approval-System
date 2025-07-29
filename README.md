# 🏦 Credit Approval System

A Django-based backend system to automate customer credit approvals and loan management. It loads customer and loan data from Excel files and provides REST APIs for registration, loan eligibility check, loan creation, and loan viewing. Built with PostgreSQL, Celery, Redis, and Docker.

---

## 🔧 Tech Stack

- **Backend**: Django 5, Django REST Framework
- **Database**: PostgreSQL
- **Task Queue**: Celery with Redis
- **Containerization**: Docker & Docker Compose
- **Excel Parsing**: openpyxl

---

## 🚀 Getting Started

### 🔁 Prerequisites

Make sure you have the following installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

### 🧩 Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/credit-approval-system.git
   cd credit-approval-system

### Run
docker-compose up --build
