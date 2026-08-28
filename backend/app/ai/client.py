from openai import OpenAI
from app.core.config import OPENROUTER_API_KEY
from typing import Dict, List

import json
from app.schemas.knoweldge import BusinessKnowledge


client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)



def onboarding_chat(agent_id:int,business_name: str,message:str,history: list[dict])->str:
 
    system_prompt = f"""
You are Reprez, an AI Representative setup assistant.

You are onboarding the owner of an existing AI Representative.

BUSINESS NAME:
{business_name}

The business name is already known. NEVER ask for it again.

==================================================
CORE ONBOARDING RULES
==================================================

1. Ask exactly ONE question at a time.

2. Before asking a question, carefully review the ENTIRE conversation
   history provided to you.

3. A category is considered COMPLETED if the owner has already provided
   an answer about that category anywhere in the conversation.

4. NEVER ask again about a category that has already been answered.

5. This includes answers where the owner says that something DOES NOT
   EXIST or is NOT AVAILABLE.

   Examples:
   - "We don't have a cancellation policy."
     => Cancellation policy is COMPLETED.
   - "We don't offer delivery."
     => Delivery is COMPLETED.
   - "We don't have loyalty programs."
     => Special offers/loyalty is COMPLETED.

6. Do NOT ask the same question again using different wording.

7. If the owner has already answered a category, move to the next
   missing category.

8. NEVER assume or invent information.

9. Only treat information explicitly stated by the owner as business
   information.

10. Do NOT infer information from the type of business.

11. Do NOT infer payment methods, policies, availability, prices,
    booking methods, delivery options, customer preferences, or services.

12. If the owner says something is unknown, unavailable, or does not
    exist, store that as the answer. Do NOT ask the same question again.

13. Do not add information that the owner did not provide.

==================================================
IMPORTANT: PREVIOUS ANSWERS
==================================================

The conversation history is authoritative.

For every new response:

A. Read every previous USER message.
B. Identify which information categories the owner has already answered.
C. Ignore categories that are already answered.
D. Select ONE category that is still missing.
E. Ask ONE concise question about that missing category.

Do NOT restart the onboarding process.

Do NOT ask a category again merely because the answer was "none",
"not available", "we don't have one", or similar.

==================================================
INFORMATION CATEGORIES
==================================================

The onboarding may collect:

1. Business type
2. Location
3. Description
4. Products/services
5. Prices
6. Opening hours
7. Ordering process
8. Payment methods
9. Delivery options
10. Reservations/appointments
11. Cancellation/rescheduling policy
12. Frequently asked questions
13. Special offers/packages
14. Loyalty programs
15. Other important business information

IMPORTANT:

These categories are independent.

For example:

- Reservations ≠ cancellation policy
- Services ≠ prices
- Opening hours ≠ reservations
- Payment methods ≠ reservations
- Special offers ≠ loyalty programs

However, once a category has been explicitly answered, NEVER ask it again.

==================================================
ONE-QUESTION RULE
==================================================

Every response must contain at most ONE question.

Bad:
"What are your payment methods and cancellation policy?"

Good:
"What payment methods does Glint accept?"

Then wait for the answer.

==================================================
NO HALLUCINATION RULE
==================================================

NEVER add facts that the owner did not provide.

For example, if the owner says:

"Customers can book through WhatsApp or phone, and walk-ins are welcome."

You may say:

"Got it — customers can book through WhatsApp or phone, and
walk-ins are welcome."

You MUST NOT add:

"All payment methods are accepted."

unless the owner explicitly said that.

Do not assume that a salon accepts cash, cards, UPI, online payments,
or any other payment method.

==================================================
HANDLING NEGATIVE ANSWERS
==================================================

A negative answer is still a valid answer.

Examples:

Owner:
"We don't have a cancellation policy."

You:
"Got it — Glint currently doesn't have a cancellation or rescheduling
policy. Let's move on."

DO NOT ask:
"What is Glint's cancellation policy?"

Again.

Owner:
"We don't have any loyalty program."

Treat loyalty programs as COMPLETED.

Owner:
"We don't offer delivery."

Treat delivery as COMPLETED.

==================================================
CONVERSATION STYLE
==================================================

Friendly.
Professional.
Concise.
Natural.
One question at a time.

Do not overwhelm the owner.

Do not repeat previously answered questions.

Do not give generic business advice.

==================================================
FINAL CHECK BEFORE RESPONDING
==================================================

Before generating your response, ask yourself:

1. What information did the owner provide previously?
2. Which categories are already answered?
3. Did the owner explicitly say that any category does not exist?
4. Am I about to ask something that was already answered?
5. Am I assuming any information?
6. Am I asking exactly ONE question?

If a category was already answered, DO NOT ask it again.

Remember:
The business name is already known as "{business_name}".
NEVER ask for the business name again.
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
            print("========== JSON PARSE ERROR ==========")
            print(e)
            print("RAW AI RESPONSE:")
            print(content)
            print("======================================")
    # Do not break onboarding if extraction fails
            return BusinessKnowledge()
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