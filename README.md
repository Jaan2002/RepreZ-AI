backend/
│
├── app/
│   │
│   ├── api/              # FastAPI endpoints
│   │
│   ├── core/             # App configuration
│   │
│   ├── schemas/          # Request & Response models
│   │
│   ├── agents/           # Everything related to AI Agents
│   │
│   ├── ai/               # LLMs, prompts, embeddings, RAG
│   │
│   ├── memory/           # Agent memory & knowledge
│   │
│   ├── integrations/     # OpenRouter, ElevenLabs, Tavily, etc.
│   │
│   ├── database/         # Database connection & models
│   │
│   ├── utils/
│   │
│   └── main.py
│
├── uploads/
├── tests/
├── .env
├── requirements.txt
└── README.md