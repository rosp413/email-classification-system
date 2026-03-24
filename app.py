from fastapi import FastAPI # type: ignore
from pydantic import BaseModel

# import the separate LLM processor module
from testing import process_email # type: ignore

app = FastAPI()

class EmailPayload(BaseModel):
    from_: str
    subject: str
    body: str
    received_time: str
    message_id: str

@app.post("/email")
def receive_email(payload: EmailPayload):
    print("📩 NEW EMAIL RECEIVED")
    print("From:", payload.from_)
    print("Subject:", payload.subject)
    print("Received:", payload.received_time)
    print("Body:", payload.body[:300])  # preview

    # ---- LLM processing (NEW PART) ----
    try:
        result = process_email(
            sender=payload.from_,
            subject=payload.subject,
            body=payload.body,
            received_time=payload.received_time
        )
    except Exception as e:
        print("❌ LLM processing failed:", str(e))
        return {"status": "error", "message": str(e)}

    print("✅ EMAIL CLASSIFIED")
    print("Category:", result["category"])
    print("Priority:", result["priority"])

    return {
        "status": "processed",
        "category": result["category"],
        "priority": result["priority"],
        "urgency_score": result["urgency_score"]
    }
