
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
import random
import uuid

app = FastAPI()

# Разрешаем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Report(BaseModel):
    id: str
    title: str
    created_at: str
    status: str
    value: float

@app.get("/reports", response_model=List[Report])
def get_reports():
    statuses = ["pending", "completed", "failed"]
    reports = [
        Report(
            id=str(uuid.uuid4()),
            title=f"Report {i + 1}",
            created_at=datetime.utcnow().isoformat(),
            status=random.choice(statuses),
            value=round(random.uniform(1000, 5000), 2)
        )
        for i in range(5)
    ]
    return reports

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
