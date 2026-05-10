# FastAPI Todo Backend with Async Email Processing

A production-oriented backend project built using FastAPI, PostgreSQL, RabbitMQ, and Celery.

This project started as a simple Todo CRUD application and gradually evolved into a backend system focused on asynchronous task processing, clean architecture principles, and scalable backend patterns.

---

# Features

* User Authentication with JWT
* Access + Refresh Token Flow
* Todo CRUD APIs
* Async PostgreSQL Integration
* Layered / Service-Based Architecture
* RabbitMQ Message Broker
* Celery Worker Integration
* Asynchronous Email Processing
* Dockerized Development Environment
* Retry Handling for Background Jobs
* Structured Dependency Injection
* Environment-Based Configuration

---

# Tech Stack

## Backend

* Python
* FastAPI
* SQLAlchemy (Async)
* PostgreSQL

## Async Processing

* RabbitMQ
* Celery

## Authentication

* JWT Access Tokens
* JWT Refresh Tokens
* Password Hashing

## DevOps / Tooling

* Docker
* Docker Compose
* Alembic
* GitHub Actions (planned)

---

# Architecture Overview

```text
Client Request
      ↓
FastAPI Router
      ↓
Service Layer
      ↓
Repository Layer
      ↓
PostgreSQL

Async Flow:
Service Layer
      ↓
RabbitMQ Queue
      ↓
Celery Worker
      ↓
Email Service
```

---

# Why Asynchronous Email Processing?

Sending emails synchronously blocks the request lifecycle and increases API latency.

Instead of sending emails directly inside the API request:

1. API publishes a background job to RabbitMQ
2. Celery worker consumes the job
3. Worker sends the email independently
4. API response remains fast and non-blocking

This pattern improves:

* scalability
* responsiveness
* fault tolerance

---

# Project Structure

```text
app/
├── api/
├── core/
├── db/
├── models/
├── repository/
├── schemas/
├── services/
├── queue/
├── workers/
├── tasks/
└── utils/
```

---

# Authentication Flow

* User Login
* Generate Access Token
* Generate Refresh Token
* Protected Routes using JWT
* Current User Dependency Injection

---

# Background Job Flow

```text
Todo completed
     ↓
Service Layer publishes message
     ↓
RabbitMQ Queue
     ↓
Celery Worker consumes message
     ↓
Task completted email notification sent
```

---

# Reliability Concepts Explored

This project also explores several production backend concepts:

* Retries for failed jobs
* ACK/NACK message handling
* Prefetch tuning
* Dead Letter Queue discussions
* Backpressure concepts
* Worker crash handling
* Separation of synchronous vs asynchronous workloads

---


## Start Docker Services

```bash
docker compose up -d
```

---

## Run FastAPI Server

```bash
uvicorn app.main:app --reload
```

---

## Start Celery Worker

```bash
celery -A app.tasks.celery_app worker --loglevel=info
```

---

# API Endpoints

## Auth

* POST /auth/register
* POST /auth/login
* POST /auth/refresh

## Todos

* GET /todos
* POST /todos
* PATCH /todos/{id}
* DELETE /todos/{id}

---

# Future Improvements

* Redis Caching
* Rate Limiting
* Observability / Metrics
* Structured Logging
* Distributed Tracing
* CI/CD Pipeline
* Kubernetes Deployment
* WebSocket/SSE Notifications

---

# What I did

* Designing layered backend systems
* Async task processing
* Message broker workflows
* Worker-based architectures
* Retry and failure handling
* Dependency Injection in FastAPI
* Dockerized backend development
* Authentication and authorization patterns

---

# Motivation

The goal of this project was not just to build CRUD APIs, but to understand how production backend systems handle asynchronous workloads and scale beyond synchronous request-response architecture in python using fastAPI.
