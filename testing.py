import os
import json
#this is useful when the email is has nit arrived yet and if we put any strict schema may throw error
from typing import Optional #used for llm_output and parsed_result if it dont exist initially
from pydantic import BaseModel

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END, START
#stategraph creates an workflow engine or creates workflow graph

from config import GROQ_API_KEY, MODEL_NAME

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

action_file = os.path.join(BASE_DIR,"emails_action.txt")
info_file = os.path.join(BASE_DIR,"emails_info.txt")

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=MODEL_NAME,
    temperature=0.2
)

prompt = ChatPromptTemplate.from_messages([
    ("system",
     """
You are a professional enterprise email classification engine.

Rules:
1. category:
   - actionable → needs reply, approval, task, or decision
   - informative → FYI, newsletters, promotions, alerts

2. priority:
   - high, medium, low

3. sentiment:
   - positive, neutral, negative

4. urgency_score:
   - integer from 1 to 10

5. recommended_action:
   - clear next step or 'No action required'

6. reason:
   - short justification

Respond ONLY with valid JSON.
No markdown.
No explanation text.

JSON FORMAT:
{{
  "category": "actionable | informative",
  "priority": "high | medium | low",
  "sentiment": "positive | neutral | negative",
  "urgency_score": 5,
  "recommended_action": "string",
  "reason": "string"
}}
"""
    ),
    ("human",
     """
From: {sender}
Subject: {subject}

Email Content:
{body}
"""
    )
])


class EmailState(BaseModel):
    sender: str
    subject: str
    body: str
    received_time: str

    llm_output: Optional[str] = None
    parsed_result: Optional[dict] = None


#initialization of node1 = classify
def classify_email(state: dict):

    chain = prompt | llm

    response = chain.invoke({
        "sender": state["sender"],
        "subject": state["subject"],
        "body": state["body"]
    })

    state["llm_output"] = response.content
    return state


#makes the data usable convert string to dictionary
#node 2
def parse_json(state: dict):

    state["parsed_result"] = json.loads(state["llm_output"])
    return state

#node 3
def save_by_category(state: dict):

    result = state["parsed_result"]

    category = result.get("category", "").upper()
    priority = result.get("priority", "").upper()
    urgency = result.get("urgency_score", "")

    formatted_text = f"""
==================================================
CATEGORY       : {category}
PRIORITY       : {priority}
URGENCY SCORE  : {urgency}
RECEIVED TIME  : {state["received_time"]}

FROM           : {state["sender"]}
SUBJECT        : {state["subject"]}

EMAIL BODY:
{state["body"]}

--------------------------------------------------

"""

    if category.lower() == "actionable":
        target_file = action_file
    else:
        target_file = info_file

    with open(target_file, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    return state

builder = StateGraph(dict)

builder.add_node("classify", classify_email)
builder.add_node("parse", parse_json)
builder.add_node("save", save_by_category)

builder.add_edge(START, "classify")
builder.add_edge("classify","parse")
builder.add_edge("parse","save")
builder.add_edge("save", END)

graph = builder.compile()


def process_email(sender, subject, body, received_time):

    initial_state = {
        "sender": sender,
        "subject": subject,
        "body": body,
        "received_time": received_time,
        "llm_output": None,
        "parsed_result": None
    }

    final_state = graph.invoke(initial_state)

    return final_state["parsed_result"]
