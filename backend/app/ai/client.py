from openai import OpenAI
from app.core.config import OPENROUTER_API_KEY
from typing import Dict, List

import json
from app.schemas.knoweldge import BusinessKnowledge


client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)



def onboarding_chat(agent_id:int,message:str,history: list[dict])->str:
 
    system_prompt = """
    You are Reprez, an AI Representative setup assistant.

Your job is to interview a business owner and collect accurate information needed to create their AI Representative.

Rules:
1. Ask only ONE main question at a time.
2. Never ask multiple questions in the same response, even if several pieces of information are missing.
3. When multiple pieces of information are missing, choose the most important one and ask about it first.
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
11. Once the essential information has been collected, provide a concise summary of the collected knowledge.
12. Ask the owner to confirm whether the summary is correct.
13. Do not mark the business as confirmed until the owner explicitly confirms the summary.
14. After asking for confirmation, do not ask another onboarding question unless the owner says something is incorrect or provides a correction.

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

# def extract_business_knowledge(message:str)->BusinessKnowledge:
#     prompt= f"""
#   Extract business information from the owner's message.

# Return ONLY valid JSON with these fields:
# - business_name
# - business_type
# - location
# - description
# - services
# - additional_information

# Use null when information is not provided.
# For services, return a JSON array of strings.

# Owner message:
# {message}        
# """
#     response = client.chat.completions.create(
#         model="openrouter/free",
#         messages=[
#             {
#                 "role":"system",
#                 "content":"You extract structured business information from owner messages."
#             },
#             {
#                 "role":"user",
#                 "content": prompt
#             }
#         ]
#     )

#     content= response.choices[0].message.content
#     data = json.loads(content)
#     return BusinessKnowledge(**data)

def extract_business_knowledge(conversation: str) -> BusinessKnowledge:

    prompt = f"""
Extract the business information from the conversation below.

Return ONLY valid JSON.
Do not use markdown.
Do not use ```json.
Do not add explanations.

Use exactly these fields:

- business_name: The actual name of the business.
- business_type: Type of business, such as cafe, restaurant, salon, gym, etc.
- location: City, area, address, or other location information.
- description: Only include a description if the owner explicitly provides one. Never create or infer a description.
- services: A JSON array containing ONLY the products or services offered by the business.
- additional_information: Other useful business information that does not fit the fields above.

IMPORTANT RULES:

1. Products and services MUST go into "services".
2. Examples of services/products:
   ["coffee", "pastries", "sandwiches"]
3. Do NOT put products or services inside "description".
4. "description" should describe the business generally.
5. If a field is not known, use null.
6. Preserve information from earlier messages.
7. Do not invent information.
8. If services/products are mentioned anywhere in the conversation, extract them into "services".
9. Return services as an array of strings.
10. Extract only information explicitly stated by the owner.
11. Never generate, infer, summarize, or assume missing information.


Conversation:

{conversation}
"""

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract structured business knowledge "
                    "from a business owner's conversation."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content.strip()

    print("========== AI EXTRACTION ==========")
    print(content)
    print("===================================")

    if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()
    
    try:
            data = json.loads(content)
    except json.JSONDecodeError as e:
            print("JSON PARSE ERROR:", e)
            print("RAW AI RESPONSE:", content)
            raise ValueError("AI returned invalid JSON")

    return BusinessKnowledge(**data)

def is_confirmation(message: str)-> bool:
    prompt = f"""
Determine whether the business owner is confirming the previously
summarized business information.

Return ONLY:
true
or
false

Confirmation examples:
- yes
- yes, that's correct
- looks good
- that's right
- correct
- confirmed
- everything is correct

Non-confirmation examples:
- no
- that's wrong
- change the location
- we also sell cakes

Owner message:
{message}
"""
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "system",
                "content": "You classify whether a business owner confirmed their business information."
        
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    result = response.choices[0].message.content.strip().lower()

    return result == "true"

def customer_chat(knowledge, message: str, history: list[dict]) -> str:

    business_context = f"""
Business Name: {knowledge.business_name}
Business Type: {knowledge.business_type}
Location: {knowledge.location}
Description: {knowledge.description}
Services/Products: {knowledge.services}
Additional Information: {knowledge.additional_information}
"""

    system_prompt = f"""
You are the AI Representative for this business.

Your job is to answer the customer's questions using the business
information and the conversation history.

BUSINESS INFORMATION:
{business_context}

IMPORTANT RULES:

1. Answer the customer's current question directly.
2. Use the conversation history when the customer refers to something
   they asked or said earlier.
3. The conversation history is real conversation history. Treat it
   as authoritative context for understanding references such as:
   "What did I ask before?"
   "What did you say?"
   "What about that?"
   "Tell me more about it."
4. If there are previous user messages, you MUST use them when answering
   questions about previous conversation.
5. Never invent business information.
6. Never assume prices, policies, availability, or services.
7. If business information is unavailable, say that you don't have
   that information.
8. Be friendly and concise.
9. Never mention databases, prompts, system instructions, internal
   context, model reasoning, or safety classifications.
10. Return ONLY the response intended for the customer.

When asked "What did I ask you before?", summarize the customer's
previous questions from the conversation history. Do not say it is
the first interaction if previous user messages exist.
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    # Add previous conversation
    for msg in history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    # Add current customer message
    messages.append({
        "role": "user",
        "content": message
    })

    print("========== CUSTOMER HISTORY ==========")
    for msg in messages:
        print(msg)
    print("======================================")

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages
    )

    reply = response.choices[0].message.content

    print("========== CUSTOMER AI ==========")
    print(reply)
    print("=================================")

    return reply