# RepreZ-AI

> **AI representatives for businesses — create, train, and interact through a web interface.**

RepreZ-AI is an AI agent platform that allows businesses to create an AI representative, provide business-specific information, and use the agent for customer interactions.

---

## 🧩 How It Works

```text
┌──────────────────┐
│   Business Owner │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   Create Agent   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Onboard & Train  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Business Knowledge│
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   AI Agent       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Customer Chat    │
└──────────────────┘
```

## 🚀 Version 1

The initial version used a **fixed business knowledge schema**:

```text
Business
├── Name
├── Location
├── Services
├── Opening Hours
└── Additional Information
```

This allowed us to build the initial agent creation, onboarding, training, and customer interaction flow.

## 🔍 Problem We Found

While testing different business use cases, we found that a fixed schema does not generalize well.

For example:

```text
Salon
├── Services
├── Appointments
└── Opening Hours

EdTech
├── Courses
├── Batches
├── Instructors
└── Eligibility
```

Different businesses have fundamentally different types of information.

This became an architectural problem rather than simply a UI problem.

## 🏗️ Architecture Evolution

We are redesigning the knowledge layer to separate:

**Business Profile**
→ stable information about the business

**Knowledge Entries**
→ flexible, business-specific information

This allows the agent's knowledge to evolve without requiring the database schema to contain a predefined field for every possible business type.

> **Current repository:** The public repository contains the Version 1 implementation. The flexible knowledge architecture is the current development direction.

---

## 🛠️ Tech Stack

| Layer      | Technologies          |
| ---------- | --------------------- |
| Frontend   | Next.js · TypeScript  |
| Backend    | FastAPI · Python      |
| ORM        | SQLAlchemy            |
| Validation | Pydantic              |
| Database   | PostgreSQL · Supabase |
| AI         | LLM APIs · OpenRouter |

## 📌 Current Focus

* [x] AI agent creation
* [x] Business onboarding
* [x] Initial knowledge structure
* [x] LLM API integration
* [ ] Flexible knowledge architecture
* [ ] Improved knowledge extraction
* [ ] More robust customer interactions
* [ ] Voice and additional interaction channels

## 📈 Status

**Active development**

RepreZ-AI is being developed iteratively, with the architecture evolving from a fixed business model toward a more flexible knowledge system that can support different business types.
