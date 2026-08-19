from openai import OpenAI
from app.core.config import OPENROUTER_API_KEY
from typing import Dict, List

import json
from app.schemas.knoweldge import BusinessKnowledge
client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

conversation_history: Dict[int, List[dict]] = {}

def onboarding_chat(agent_id:int,message:str)->str:
    history= conversation_history.setdefault(agent_id,[])
    system_prompt = """
    You are Reprez, an AI Representative setup assistant.

Your job is to interview a business owner and collect accurate information needed to create their AI Representative.

Rules:
1. Ask only ONE main question at a time.
2. Keep responses concise and natural.
3. Never invent, assume, or speculate about the business.
4. Never assume local preferences, customer behavior, payment methods, products, or policies.
5. Use information already provided by the business owner and never ask the same question again.
6. Ask follow-up questions when an answer is incomplete or ambiguous.
7. Prioritize information that the AI Representative will need to answer customer questions.
8. Collect information such as:
   - Business name and location
   - Products/services
   - Prices
   - Opening hours
   - Ordering process
   - Payment methods
   - Delivery options
   - Reservations
   - Policies
   - Frequently asked questions
   - Special offers or important business information
9. Do not overwhelm the owner with a long questionnaire.
10. Do not add unnecessary explanations or generic business advice.
11. Once enough information has been collected, summarize the collected knowledge and ask the owner to confirm it.
12. Only after confirmation should the information be considered ready for the AI Representative's knowledge base.

Conversation style:
- Friendly
- Professional
- Concise
- Conversational
- One question at a time

Example:

User: "We are a cafe in Bangalore."

Assistant:
"Great! Let's set up your AI Representative. ☕

First, what is your cafe's name and which area of Bangalore is it located in?"
    """
    messages = [
        {
            "role":"system",
            "content": system_prompt
        },
        *history,
        {
            "role":"user",
            "content": message
        }
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages
    )

    reply = response.choices[0].message.content

    history.append({
        "role":"user",
        "content": message
    })

    history.append({
            "role":"assistant",
            "content": reply
    })

    return reply

def ask_ai(message: str)->str:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "system",
                "content": (
                   "You are the onboarding assistant for Reprez. "
                   "Your job is to learn about a business from its owner "
                    "and ask useful follow-up questions."
                ),
            },
            {
             "role": "user",
             "content": message,
            },
        ],
    )
    return response.choices[0].message.content

def extract_business_knowledge(message:str)->BusinessKnowledge:
    prompt= f"""
  Extract business information from the owner's message.

Return ONLY valid JSON with these fields:
- business_name
- business_type
- location
- description
- services
- additional_information

Use null when information is not provided.
For services, return a JSON array of strings.

Owner message:
{message}        
"""
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role":"system",
                "content":"You extract structured business information from owner messages."
            },
            {
                "role":"user",
                "content": prompt
            }
        ]
    )

    content= response.choices[0].message.content
    data = json.loads(content)
    return BusinessKnowledge(**data)