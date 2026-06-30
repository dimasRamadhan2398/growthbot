from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, Base, get_db

app = FastAPI(title="CRM Service")

@app.on_event("startup")
def startup_db():
    Base.metadata.create_all(bind=engine)

def require_tenant_id(x_tenant_id: str = Header(None)):
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-ID header missing")
    return x_tenant_id

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "crm_service"}

@app.get("/api/leads", response_model=List[schemas.LeadOut])
def get_leads(tenant_id: str = Depends(require_tenant_id), db: Session = Depends(get_db)):
    return db.query(models.Lead).filter(models.Lead.tenant_id == tenant_id).all()

@app.post("/api/leads", response_model=schemas.LeadOut)
def create_lead(lead: schemas.LeadCreate, tenant_id: str = Depends(require_tenant_id), db: Session = Depends(get_db)):
    new_lead = models.Lead(**lead.dict(), tenant_id=tenant_id)
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    return new_lead

@app.put("/api/leads/{lead_id}", response_model=schemas.LeadOut)
def update_lead(lead_id: int, lead_update: schemas.LeadUpdate, tenant_id: str = Depends(require_tenant_id), db: Session = Depends(get_db)):
    db_lead = db.query(models.Lead).filter(models.Lead.id == lead_id, models.Lead.tenant_id == tenant_id).first()
    if not db_lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    if lead_update.column_name:
        db_lead.column_name = lead_update.column_name

    db.commit()
    db.refresh(db_lead)
    return db_lead

@app.delete("/api/leads/{lead_id}")
def delete_lead(lead_id: int, tenant_id: str = Depends(require_tenant_id), db: Session = Depends(get_db)):
    db_lead = db.query(models.Lead).filter(models.Lead.id == lead_id, models.Lead.tenant_id == tenant_id).first()
    if not db_lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    db.delete(db_lead)
    db.commit()
    return {"message": "Deleted successfully"}

@app.get("/api/agents", response_model=List[schemas.AgentOut])
def get_agents(tenant_id: str = Depends(require_tenant_id), db: Session = Depends(get_db)):
    return db.query(models.Agent).filter(models.Agent.tenant_id == tenant_id).all()

@app.post("/api/agents", response_model=schemas.AgentOut)
def create_agent(agent: schemas.AgentCreate, tenant_id: str = Depends(require_tenant_id), db: Session = Depends(get_db)):
    new_agent = models.Agent(**agent.dict(), tenant_id=tenant_id)
    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)
    return new_agent

@app.put("/api/agents/{agent_id}", response_model=schemas.AgentOut)
def update_agent(agent_id: int, agent_update: schemas.AgentUpdate, tenant_id: str = Depends(require_tenant_id), db: Session = Depends(get_db)):
    db_agent = db.query(models.Agent).filter(models.Agent.id == agent_id, models.Agent.tenant_id == tenant_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    if agent_update.status:
        db_agent.status = agent_update.status
    if agent_update.messages is not None:
        db_agent.messages = agent_update.messages

    db.commit()
    db.refresh(db_agent)
    return db_agent
