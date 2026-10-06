# RepreZ-AI

> **AI representatives for businesses — built to learn, understand, and interact with customers.**

RepreZ-AI is an AI agent platform that lets businesses create their own AI representative, teach it about their business through conversational onboarding, and use that knowledge to interact with customers.

The goal is to move beyond a generic chatbot toward an **AI representative with business-specific knowledge, state, and future actions.**

---

## 🚀 What RepreZ Does

A business can create an AI representative and provide information about the business through a conversational onboarding flow.

The agent then uses that business-specific knowledge when interacting with customers.

```text
Business Owner
      │
      ▼
Create Business / Agent
      │
      ▼
Conversational Onboarding
      │
      ▼
Business Knowledge
      │
      ▼
AI Representative
      │
      ▼
Customer Interaction
```

### Example

A salon owner creates an agent for their business:

> **Maya Salon — Bangalore**

The agent can learn information such as:

* Services
* Pricing
* Opening hours
* Location
* Business-specific information

A customer can then ask:

> "Does Maya Salon offer bridal makeup?"

The agent can use the business's stored knowledge to respond.

---

## 🧠 Why I Built It

I wanted to explore a question:

> **What happens when an AI agent is designed to represent a specific business rather than simply act as a general-purpose chatbot?**

That led to building the system around three core ideas:

**Conversation → Knowledge → Agent**

The business provides information conversationally, the system stores that information as business knowledge, and the AI representative uses that knowledge during customer interactions.

---

## 🏗️ Architecture Evolution

The first version of RepreZ used a fixed business knowledge schema:

```text
Business
├── Name
├── Location
├── Services
├── Opening Hours
└── Additional Information
```

While testing different business types, I found that this approach did not generalize well.

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

Different businesses naturally have different types of information.

Instead of adding more fields to the database for every new business type, the architecture is evolving toward separating:

```text
Business Profile
        +
Flexible Knowledge Entries
        ↓
   AI Representative
```

This allows business knowledge to evolve without requiring a predefined database field for every possible business category.

> **Current status:** The repository contains the working V1 implementation while the flexible knowledge architecture is being developed as the next iteration.

---

## 🛠️ Tech Stack

| Layer            | Technologies          |
| ---------------- | --------------------- |
| Frontend         | Next.js · TypeScript  |
| Backend          | FastAPI · Python      |
| API / Validation | Pydantic              |
| ORM              | SQLAlchemy            |
| Database         | PostgreSQL · Supabase |
| AI               | LLM APIs · OpenRouter |

---

## 🔑 Current Capabilities

* AI agent creation
* Business onboarding
* Conversational information collection
* Business-specific knowledge
* LLM API integration
* Customer interaction flow
* Persistent backend state
* Initial knowledge architecture

---

## 🔭 What's Next

The current development focus is on making RepreZ more capable of supporting different business types and more useful real-world interactions.

Planned improvements include:

* Flexible knowledge extraction
* Improved knowledge retrieval
* More robust agent workflows
* Agent actions and tool usage
* Voice interaction
* Additional customer interaction channels

---

## 📂 Project Structure

```text
RepreZ-AI/
│
├── frontend/
│   └── Next.js application
│
├── backend/
│   ├── FastAPI application
│   ├── Agent logic
│   ├── Business models
│   └── API endpoints
│
└── README.md
```

---

## 📈 Status

**Active development**

RepreZ-AI is an evolving AI-agent project focused on building business-specific representatives that can learn from businesses and interact with their customers.

The project is being developed iteratively, with the architecture evolving based on real product and engineering constraints discovered during development.

---

## 👩‍💻 Built By

**Jaanvi**

Software engineering graduate building AI-native products and exploring the intersection of **AI agents, product engineering, and application security**.
