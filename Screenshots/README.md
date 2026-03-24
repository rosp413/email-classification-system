# 📧 AI Email Classification System  
### 🚀 Power Automate + FastAPI + LangGraph + Groq LLM

---

## 🌟 Overview

An **AI-powered email automation system** that intelligently processes incoming emails and classifies them into:

✅ **Actionable Emails** – Require reply, approval, or action  
📘 **Informational Emails** – Updates, newsletters, notifications  

This system integrates **Microsoft Power Automate**, **FastAPI**, **LangGraph**, and **Groq LLM** to create a fully automated, real-time pipeline.

---

## 🎯 Problem Statement

Managing emails manually leads to:

- ❌ Missed important emails  
- ❌ Time-consuming sorting  
- ❌ No prioritization  

---

## 💡 Solution

This project automates email handling by:

- 📩 Capturing incoming emails  
- 🤖 Using AI to analyze content  
- ⚡ Classifying emails instantly  
- 📊 Assigning priority & urgency  
- 📁 Storing results in structured format  

---

## 🧠 Architecture

```text
📩 Outlook Email
        ↓
⚡ Power Automate Trigger
        ↓
🌐 HTTP Request
        ↓
🔗 ngrok Tunnel
        ↓
🚀 FastAPI Backend (/email)
        ↓
🧠 LangGraph Workflow
   ├── classify (LLM)
   ├── parse (JSON)
   └── save (file)
        ↓
🤖 Groq LLM
        ↓
📄 emails_action.txt / emails_info.txt
```

---

## 🔄 Workflow

```text
Start
 ↓
New Email Arrives
 ↓
Power Automate Trigger
 ↓
Send HTTP Request
 ↓
FastAPI Receives Data
 ↓
LangGraph Executes
 ↓
LLM Classifies Email
 ↓
Parse JSON Output
 ↓
Save to File
 ↓
End
```

---
## Workflow of the Power Automate
<img width="786" height="594" alt="image" src="https://github.com/user-attachments/assets/f91389fb-6769-43fc-bb66-570a47fb75f6" />

## ⚙️ Tech Stack

| Technology | Role |
|-----------|------|
| 🐍 Python | Backend |
| ⚡ FastAPI | API server |
| 🔗 LangGraph | Workflow engine |
| 🧠 LangChain | LLM integration |
| 🤖 Groq | AI model |
| 🔄 Power Automate | Automation |
| 🌐 ngrok | Public tunnel |
| 📦 Pydantic | Validation |

---

## 📂 Project Structure

```text
email_flow_python/
│
├── app.py                # FastAPI server
├── testing.py            # LangGraph workflow
├── config.py             # API configuration
│
├── emails_action.txt     # Actionable emails
├── emails_info.txt       # Informational emails
│
├── requirements.txt
└── README.md
```

---

## 🔑 Configuration

Create `config.py`:

```python
GROQ_API_KEY = "your_api_key"
MODEL_NAME = "llama3-70b-8192"
```

🔗 Get API key: https://console.groq.com/keys

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

### 1️⃣ Activate Virtual Environment

```bash
.venv\Scripts\activate
```

---

### 2️⃣ Start FastAPI Server

```bash
python -m uvicorn app:app --port 8000 --reload
```

📍 Runs at:  
http://127.0.0.1:8000  

📄 Swagger Docs:  
http://127.0.0.1:8000/docs  

---

### 3️⃣ Start ngrok

```bash
ngrok http 8000
```

🔗 Example URL:

```
https://abc123.ngrok-free.app
```

---

### 4️⃣ Configure Power Automate

- Trigger: **When a new email arrives (V3)**  
- HTTP Action:

| Field | Value |
|------|------|
| Method | POST |
| URL | https://ngrok-url/email |

---

### 📤 Request Body

```json
{
  "from_": "@{triggerOutputs()?['body/from']}",
  "subject": "@{triggerOutputs()?['body/subject']}",
  "body": "@{triggerOutputs()?['body/body']}",
  "received_time": "@{triggerOutputs()?['body/receivedDateTime']}",
  "message_id": "@{triggerOutputs()?['body/id']}"
}
```

---

## 🧪 Testing API

👉 Open:

```
http://127.0.0.1:8000/docs
```

Use:

```
POST /email
```

---

## 📄 Output Example

### 🔴 Actionable Email

```
==================================================
CATEGORY       : ACTIONABLE
PRIORITY       : HIGH
URGENCY SCORE  : 9

FROM           : manager@company.com
SUBJECT        : Approval Required

EMAIL BODY:
Please approve immediately.
--------------------------------------------------
```

---

### 📘 Informational Email

```
==================================================
CATEGORY       : INFORMATIONAL
PRIORITY       : LOW

FROM           : newsletter@company.com
SUBJECT        : Monthly Update

EMAIL BODY:
Here are the latest updates.
--------------------------------------------------
```

---

## 🐛 Troubleshooting

### ❌ 405 Method Not Allowed
➡ Use POST, not browser

---

### ❌ ngrok not working
➡ Restart ngrok

---

### ❌ Flow not triggering
➡ Turn OFF → ON

---

## 🚀 Future Enhancements

- 📊 Dashboard UI  
- 🗄️ Database integration  
- 🔔 Slack/Teams notifications  
- 📈 Priority-based sorting  
- 🧠 Vector search  

---

## ⭐ Key Highlights

✔ Event-driven architecture  
✔ Real-time processing  
✔ AI-powered classification  
✔ Scalable workflow design  
✔ Cloud + Local integration  

---

## 📜 License

MIT License

---

## 💡 Author

Developed by **Roshni Poojary** 🚀

---
