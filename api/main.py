import os
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import PyJWKClient
from pydantic import BaseModel
from typing import List
from datetime import datetime
import random
import uuid
import requests

security = HTTPBearer()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

KEYCLOAK_URL = "http://keycloak:8080"
KEYCLOAK_REALM = "reports-realm"
KEYCLOAK_CERTS_URL = KEYCLOAK_URL + "/realms/" + KEYCLOAK_REALM + "/protocol/openid-connect/certs"
ALGORITHM = "RS256"
REQUIRED_ROLE = "prothetic_user"

@app.get("/reports", response_model=List[Report])
def get_reports(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        jwks_client = PyJWKClient(KEYCLOAK_CERTS_URL)
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(token, signing_key.key, algorithms=[ALGORITHM])
        roles: List[str] = payload.get("realm_access", {}).get("roles", [])
        if REQUIRED_ROLE not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
                )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

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
