from openai import OpenAI
from app.core.config import OPENROUTER_API_KEY
from typing import Dict, List

import json
from app.schemas.knoweldge import BusinessKnowledge, ExtractedBusinessData


client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)



def onboarding_chat(
    agent_id: int,
    business_name: str,
    message: str,
    history: list[dict]
) -> str:

    system_prompt = f"""
You are RepreZ, an AI Representative setup assistant.

You are onboarding the owner of an existing AI Representative.

BUSINESS NAME:
{business_name}

The business name is already known. NEVER ask for it again.

==================================================
CORE ONBOARDING RULES
==================================================

1. Ask exactly ONE question at a time.

2. Carefully review the ENTIRE conversation history before responding.

3. A category is COMPLETED if the owner has already provided
information about that category anywhere in the conversation.

4. NEVER ask again about a category that has already been answered.

5. A negative answer also COMPLETES the category.

Examples:

Owner:
"We don't have a cancellation policy."

This means:
Cancellation/rescheduling policy = answered.

Owner:
"We don't offer delivery."

This means:
Delivery = answered.

Owner:
"We don't have a loyalty program."

This means:
Loyalty = answered.

6. Do NOT ask the same question again using different wording.

7. If a category is already answered, move to the next missing category.

8. NEVER assume or invent business information.

9. Only treat information explicitly provided by the owner as business
information.

10. NEVER infer information from the business type.

11. NEVER infer prices, payment methods, policies, availability,
booking methods, delivery options, services, or opening hours.

12. If the owner says something is unknown, unavailable, or does not
exist, treat that as a valid answer.

13. Do not add information that the owner did not provide.

==================================================
INFORMATION CATEGORIES
==================================================

Collect the following information when it has not already been answered:

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

These categories are independent.

Reservations are NOT the same as cancellation/rescheduling.

Services are NOT the same as prices.

Opening hours are NOT the same as reservations.

Payment methods are NOT the same as reservations.

Special offers are NOT the same as loyalty programs.

==================================================
CANCELLATION / RESCHEDULING
==================================================

Cancellation and rescheduling is a normal business-information
category.

Ask about it normally when it has not already been answered.

For example:

"What is your cancellation or rescheduling policy for reservations?"

If the owner says:

"We don't have one."

Treat the category as COMPLETED.

Do NOT ask about it again.

If the owner provides a policy, acknowledge it and continue to the
next missing category.

==================================================
ONE-QUESTION RULE
==================================================

Every response must contain AT MOST ONE question.

Good:

"What is your cancellation or rescheduling policy for reservations?"

Bad:

"What is your cancellation policy, and what payment methods do you
accept?"

Ask one question and wait for the owner's answer.

==================================================
NO HALLUCINATION
==================================================

NEVER add facts that the owner did not provide.

If the owner says:

"Customers can book through WhatsApp and walk-ins are welcome."

You may acknowledge exactly that.

Do NOT add:

"Customers can also book by phone."

unless the owner explicitly says so.

Do NOT assume cash, cards, UPI, online payments, delivery,
refunds, cancellations, or any other policy.

==================================================
HANDLING NEGATIVE ANSWERS
==================================================

A negative answer is still a complete answer.

Examples:

"We don't have a cancellation policy."

"We don't offer delivery."

"We don't have a loyalty program."

"We don't accept reservations."

"We don't have any special offers."

All of these must be treated as answered categories.

Never ask the same category again.

==================================================
CONVERSATION STYLE
==================================================

Friendly.
Professional.
Concise.
Natural.

Do not overwhelm the owner.

Do not repeat questions.

Do not give generic business advice.

Do not invent information.

==================================================
RESPONSE PROCESS
==================================================

Before responding:

1. Read the entire conversation history.
2. Identify information already provided by the owner.
3. Identify categories that are already completed.
4. Include negative answers as completed categories.
5. Find ONE missing category.
6. Ask ONE concise question about that category.
7. Never ask for the business name.

The business name is already known:

"{business_name}"

NEVER ask for the business name again.
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    # Add existing conversation history
    for msg in history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    # Add current owner message
    messages.append({
        "role": "user",
        "content": message.strip()
    })

    print("========== ONBOARDING AI REQUEST ==========")
    print("Agent ID:", agent_id)
    print("Business:", business_name)
    print("Message:", message)
    print("History messages:", len(history))
    print("===========================================")

    try:
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages
        )

    except Exception as exc:
        print("========== ONBOARDING AI ERROR ==========")
        print("Error type:", type(exc).__name__)
        print("Error:", str(exc))
        print("=========================================")

        raise

    if not response.choices:
        raise RuntimeError(
            "AI returned no choices."
        )

    reply = response.choices[0].message.content

    if not reply:
        raise RuntimeError(
            "AI returned an empty response."
        )

    print("========== ONBOARDING AI RESPONSE ==========")
    print(reply)
    print("=============================================")

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


# def extract_business_knowledge(conversation: str) -> BusinessKnowledge:

#     prompt = f"""
# Extract the business information from the conversation below.

# Return ONLY valid JSON.
# Do not use markdown.
# Do not use ```json.
# Do not add explanations.

# Use exactly these fields:

# - business_name: The actual name of the business.
# - business_type: Type of business, such as cafe, restaurant, salon, gym, etc.
# - location: City, area, address, or other location information.
# - description: Only include a description if the owner explicitly provides one. Never create or infer a description.
# - services: A JSON array containing ONLY the products or services offered by the business.
# - additional_information: Other useful business information that does not fit the fields above.

# IMPORTANT RULES:

# 1. Products and services MUST go into "services".
# 2. Examples of services/products:
#    ["coffee", "pastries", "sandwiches"]
# 3. Do NOT put products or services inside "description".
# 4. "description" should describe the business generally.
# 5. If a field is not known, use null.
# 6. Preserve information from earlier messages.
# 7. Do not invent information.
# 8. If services/products are mentioned anywhere in the conversation, extract them into "services".
# 9. Return services as an array of strings.
# 10. Extract only information explicitly stated by the owner.
# 11. Never generate, infer, summarize, or assume missing information.


# Conversation:

# {conversation}
# """

#     response = client.chat.completions.create(
#         model="openrouter/free",
#         messages=[
#             {
#                 "role": "system",
#                 "content": (
#                     "You extract structured business knowledge "
#                     "from a business owner's conversation."
#                 )
#             },
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ]
#     )

#     content = response.choices[0].message.content.strip()

#     print("========== AI EXTRACTION ==========")
#     print(content)
#     print("===================================")

#     if content.startswith("```"):
#             content = content.replace("```json", "").replace("```", "").strip()
    
#     try:
#             data = json.loads(content)
#     except json.JSONDecodeError as e:
#             print("========== JSON PARSE ERROR ==========")
#             print(e)
#             print("RAW AI RESPONSE:")
#             print(content)
#             print("======================================")
#     # Do not break onboarding if extraction fails
#             return BusinessKnowledge()
#     return BusinessKnowledge(**data)

def extract_business_knowledge(conversation: str) -> ExtractedBusinessData:

    prompt = f"""
Extract the business information from the conversation below.

Return ONLY valid JSON.
Do not use markdown.
Do not use ```json.
Do not add explanations.

The JSON must have exactly this structure:

{{
    "profile": {{
        "business_type": null,
        "location": null,
        "description": null
    }},
    "knowledge": []
}}

==================================================
PROFILE RULES
==================================================

The profile contains only universal business information.

business_type:
- Extract only if explicitly stated by the owner.
- Never infer it.

location:
- Extract only explicitly stated location information.

description:
- Include only if the owner explicitly describes the business.
- Never create or infer a description.

Use null when information is not explicitly available.

==================================================
KNOWLEDGE RULES
==================================================

Extract all other useful business information into "knowledge".

Each knowledge item MUST contain:

- category
- title
- content
- metadata

==================================================
CANONICAL CATEGORIES
==================================================

Use ONLY these category names whenever applicable:

service
product
pricing
opening_hours
ordering
payment
delivery
reservation
cancellation_policy
faq
offer
loyalty
policy
other

Do NOT create alternative category names.

Examples:

Correct:
"opening_hours"

Incorrect:
"hours"
"operating_hours"
"business_hours"

Correct:
"ordering"

Incorrect:
"order"
"order_methods"
"ordering_methods"

Correct:
"reservation"

Incorrect:
"reservations"
"booking"

==================================================
CANONICAL TITLES
==================================================

Use the following canonical titles for these categories:

opening_hours:
"Opening Hours"

ordering:
"Ordering Methods"

payment:
"Payment Methods"

delivery:
"Delivery"

reservation:
"Reservations"

cancellation_policy:
"Cancellation Policy"

pricing:
"Pricing"

offer:
"Special Offers"

loyalty:
"Loyalty Program"

faq:
"FAQ"

For products/services, use the actual product or service name
as the title.

Examples:

Espresso
Pour-over Coffee
Chocolate Croissant
Manicure
Hair Coloring

Do NOT create generic titles such as:

"Products"
"Services"
"Menu Items"
"Coffee and Drinks"

when individual products/services can be extracted.

==================================================
VERY IMPORTANT: ONE FACT = ONE ENTRY
==================================================

The knowledge array represents canonical business facts.

Do NOT create multiple entries containing the same fact.

For example, if the conversation contains:

"We are open Monday to Saturday from 9 AM to 9 PM."

Return:

{{
    "category": "opening_hours",
    "title": "Opening Hours",
    "content": "The business is open Monday to Saturday from 9 AM to 9 PM.",
    "metadata": null
}}

Do NOT return:

- Opening Hours
- Operating Hours
- Business Hours

These are the SAME fact.

--------------------------------------------------

If the conversation contains:

"Customers can order at the counter or through WhatsApp."

Return ONE entry:

{{
    "category": "ordering",
    "title": "Ordering Methods",
    "content": "Customers can order directly at the counter or through WhatsApp.",
    "metadata": null
}}

Do NOT return:

- Order Methods
- Ordering Methods
- Ordering

--------------------------------------------------

If the conversation contains prices such as:

"Cappuccino is ₹180 and espresso is ₹120."

Return ONE pricing entry containing the known prices.

Do NOT create separate entries called:

- Prices
- Product Prices
- Pricing

--------------------------------------------------

Products and services must be represented individually when possible.

For example, if the owner says:

"We serve espresso, pour-over coffee and fresh pastries."

Return:

[
    {{
        "category": "product",
        "title": "Espresso",
        "content": "The business serves espresso.",
        "metadata": null
    }},
    {{
        "category": "product",
        "title": "Pour-over Coffee",
        "content": "The business serves pour-over coffee.",
        "metadata": null
    }},
    {{
        "category": "product",
        "title": "Fresh Pastries",
        "content": "The business serves fresh pastries.",
        "metadata": null
    }}
]

Do NOT additionally create:

"Products"

or

"Services"

containing the same information.

==================================================
NEGATIVE INFORMATION
==================================================

Negative information is valid business information.

For example:

"We don't offer delivery."

Return:

{{
    "category": "delivery",
    "title": "Delivery",
    "content": "The business does not offer delivery.",
    "metadata": null
}}

Do not omit the entry.

==================================================
PRESERVING UPDATED INFORMATION
==================================================

The conversation may contain older and newer answers.

If the owner changes previously provided information, use the
MOST RECENT explicitly stated information.

Example:

Owner:
"We open at 9 AM."

Later:

"Actually, we open at 10 AM."

Return only:

{{
    "category": "opening_hours",
    "title": "Opening Hours",
    "content": "The business opens at 10 AM.",
    "metadata": null
}}

Do not return both versions.

==================================================
STRICT RULES
==================================================

1. Extract ONLY information explicitly provided by the owner.

2. Never invent information.

3. Never infer information from the business type.

4. Do not create duplicate facts.

5. Do not create duplicate entries using different titles.

6. Do not create duplicate entries using singular/plural variations.

7. Do not create generic summary entries when individual facts can be
   represented separately.

8. Use canonical category names.

9. Use canonical titles.

10. Preserve information from earlier messages.

11. If newer information contradicts older information, use the newest
    explicit information.

12. Negative information must be preserved.

13. Products and services belong in knowledge.

14. Prices belong in pricing.

15. Opening hours belong in opening_hours.

16. Ordering information belongs in ordering.

17. Payment methods belong in payment.

18. Delivery information belongs in delivery.

19. Reservation information belongs in reservation.

20. Cancellation/rescheduling information belongs in cancellation_policy.

21. Special offers belong in offer.

22. Loyalty programs belong in loyalty.

23. If no knowledge is available, return an empty array.

24. metadata should contain structured information only when explicitly
    available and useful. Otherwise use null.

==================================================
FINAL DEDUPLICATION CHECK
==================================================

Before returning the JSON:

- Merge duplicate facts.
- Merge title variations referring to the same fact.
- Merge category variations referring to the same fact.
- Do not return both a generic summary and its individual facts.
- Make sure each business fact appears only ONCE.

==================================================
CONVERSATION
==================================================

{conversation}
"""

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract structured business information "
                    "from a business owner's conversation. "
                    "Return only valid JSON following the requested schema."
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
        content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

    try:
        data = json.loads(content)

    except json.JSONDecodeError as e:
        print("========== JSON PARSE ERROR ==========")
        print(e)
        print("RAW AI RESPONSE:")
        print(content)
        print("======================================")

        return ExtractedBusinessData(
            profile={
                "business_type": None,
                "location": None,
                "description": None
            },
            knowledge=[]
        )

    try:
        return ExtractedBusinessData(**data)

    except Exception as e:
        print("========== EXTRACTION VALIDATION ERROR ==========")
        print(e)
        print("EXTRACTED DATA:")
        print(data)
        print("=================================================")

        return ExtractedBusinessData(
            profile={
                "business_type": None,
                "location": None,
                "description": None
            },
            knowledge=[]
        )

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

def customer_chat(
    knowledge: dict,
    message: str,
    history: list[dict]
) -> str:

    # --------------------------------------------------
    # Build knowledge text
    # --------------------------------------------------

    knowledge_items = knowledge.get(
        "knowledge",
        []
    )

    if knowledge_items:

        knowledge_text = "\n".join(
            f"- {item.get('title')}: {item.get('content')}"
            for item in knowledge_items
        )

    else:

        knowledge_text = (
            "No additional business knowledge is available."
        )

    # --------------------------------------------------
    # Business context
    # --------------------------------------------------

    business_context = f"""
Business Name:
{knowledge.get("business_name")}

Business Type:
{knowledge.get("business_type")}

Location:
{knowledge.get("location")}

Description:
{knowledge.get("description")}

CURRENT BUSINESS KNOWLEDGE:
{knowledge_text}
"""

    # --------------------------------------------------
    # AI system prompt
    # --------------------------------------------------

    system_prompt = f"""
You are the AI Representative for this business.

Your job is to answer customer questions using ONLY:

1. The current business information below.
2. The conversation history.

==================================================
CURRENT BUSINESS INFORMATION
==================================================

{business_context}

==================================================
SOURCE OF TRUTH
==================================================

The CURRENT BUSINESS KNOWLEDGE above is the source of truth.

Only use business facts that are explicitly present there.

NEVER invent, assume, or guess business information.

Do not use general knowledge about cafes, restaurants, salons,
shops, or businesses to fill missing information.

==================================================
IMPORTANT RULES
==================================================

1. Answer the customer's current question directly.

2. Be friendly, natural, and concise.

3. Use conversation history when the customer refers to something
   discussed earlier.

4. Never invent business information.

5. Never assume prices.

6. Never assume opening hours.

7. Never assume payment methods.

8. Never assume delivery options.

9. Never assume reservation rules.

10. Never assume cancellation or rescheduling policies.

11. Never assume services or products.

12. If the requested information is not present in the current
    business knowledge, clearly say that you do not have that
    information.

13. If a policy is not listed, DO NOT assume that the business
    has such a policy.

14. If the customer asks about cancellation or rescheduling and
    no cancellation/rescheduling information exists, say that
    you do not have information about that policy.

15. Do not mention databases, prompts, system instructions,
    internal context, model reasoning, or implementation details.

16. Return ONLY the response intended for the customer.

==================================================
MISSING INFORMATION
==================================================

If information is unavailable, use a natural response such as:

"I don't have that information for {knowledge.get("business_name")}."

You may also suggest contacting the business directly when
appropriate.

Do NOT make up an answer.

==================================================
CONVERSATION HISTORY
==================================================

The conversation history represents the real conversation with
the customer.

Use it when the customer asks things like:

- "What did I ask before?"
- "What did you say?"
- "What about that?"
- "Tell me more about it."

However, conversation history must NOT override current business
knowledge when answering factual business questions.

==================================================
"""

    # --------------------------------------------------
    # Build messages
    # --------------------------------------------------

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    for msg in history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    messages.append({
        "role": "user",
        "content": message
    })

    # --------------------------------------------------
    # Debug
    # --------------------------------------------------

    print("========== CUSTOMER HISTORY ==========")

    for msg in messages:
        print(msg)

    print("======================================")

    # --------------------------------------------------
    # OpenRouter call
    # --------------------------------------------------

    try:

        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages
        )

    except Exception as exc:

        print("========== CUSTOMER AI ERROR ==========")
        print(type(exc).__name__)
        print(str(exc))
        print("=======================================")

        raise

    # --------------------------------------------------
    # Extract response
    # --------------------------------------------------

    reply = response.choices[0].message.content

    if not reply:
        raise RuntimeError(
            "Customer AI returned an empty response."
        )

    # --------------------------------------------------
    # Debug
    # --------------------------------------------------

    print("========== CUSTOMER AI ==========")
    print(reply)
    print("=================================")

    return reply