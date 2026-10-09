# RepreZ-AI 🤖

**AI representatives for real businesses.**

RepreZ-AI is a platform for creating AI-powered business representatives that can interact with users, answer questions using business-specific knowledge, and help automate everyday business interactions.

The idea is simple: businesses shouldn't have to answer the same questions repeatedly or manually handle every initial customer interaction. They should be able to create an AI representative that understands their business and helps users get the information they need.

## 💡 The Problem

Small businesses often rely on manual communication to answer questions, explain services, and share information with potential customers.

This can lead to repetitive work, delayed responses, and missed opportunities.

RepreZ-AI explores how AI agents can make these interactions more accessible, consistent, and scalable.

## 🚀 What I'm Building

* **Business-specific AI representatives** — Create an AI representative associated with a business.
* **Knowledge onboarding** — Build a workflow for collecting and managing information about a business.
* **Knowledge-driven interactions** — Enable representatives to use business-specific information when responding to users.
* **Agent management** — Provide a way to create and manage business representatives through a web interface.
* **A foundation for workflow automation** — Explore how AI representatives can eventually handle more complex business tasks.

The goal is to move beyond a generic chatbot toward an AI representative grounded in the context of a real business.

## 🛠️ Tech Stack

**Frontend**

* Next.js
* React
* TypeScript
* CSS

**Backend**

* Python
* FastAPI
* SQLAlchemy
* Pydantic

**Database & AI**

* PostgreSQL
* Supabase
* OpenRouter for LLM access

## 🏗️ Architecture

```text
Business Owner
      |
      v
Next.js Web Application
      |
      v
FastAPI Backend
      |
      +------ Agent Management
      |
      +------ Business Knowledge
      |
      +------ AI / LLM Integration
      |
      v
PostgreSQL Database
```

The frontend communicates with the backend through API endpoints. The backend manages agent-related data, business knowledge, and integration with language models.

## 🧪 Current Development

RepreZ-AI is an actively developed project. Current work focuses on building the core backend and frontend workflows.

Areas of development include:

* Agent creation and management
* Business-specific knowledge storage
* Knowledge onboarding and preview
* Frontend-to-backend API integration
* LLM-powered business interactions

Features are being developed incrementally, so the repository represents a work in progress rather than a finished production platform.

## 🎯 What's Next

* Improve the reliability of knowledge-grounded responses.
* Build a smoother business onboarding experience.
* Connect business context to agent conversations.
* Introduce workflow-oriented agent capabilities.
* Add evaluation and testing for agent responses.
* Explore safeguards for incorrect or unsupported answers.

## 💻 Getting Started

### Prerequisites

* Python 3.10+
* Node.js and npm
* PostgreSQL or a configured Supabase database
* An LLM provider API key

### 1. Clone the repository

```bash
git clone https://github.com/Jaan2002/RepreZ-AI.git
cd RepreZ-AI
```

### 2. Configure the backend

Navigate to the backend directory and create a virtual environment:

```bash
cd backend
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the required environment variables in a local `.env` file, using the project's environment configuration as the source of truth.

### 3. Start the backend

```bash
uvicorn app.main:app --reload
```

Confirm the application import path matches the current backend structure. If configured, FastAPI's interactive API documentation is available at `/docs`.

### 4. Configure the frontend

In a separate terminal, navigate to the frontend directory:

```bash
cd frontend
npm install
```

Create a `.env.local` file and configure the backend URL:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

Start the development server:

```bash
npm run dev
```

Open `http://localhost:3000` in your browser.

*Note: Setup commands and environment variables may need adjustment to match the current repository configuration.*

## 🌱 Project Philosophy

I'm interested in building AI systems that do more than generate text.

I want to explore how AI representatives can understand context, use relevant knowledge, and eventually execute useful workflows while remaining predictable and reliable.

RepreZ-AI is my attempt to learn by building a practical product from the ground up.

## 📌 Status

**In active development.**

This project is being built incrementally, with an emphasis on practical AI applications, full-stack engineering, and agent-oriented workflows.

## 👩‍💻 Author

**Jaanvi**

GitHub: [@Jaan2002](https://github.com/Jaan2002)
