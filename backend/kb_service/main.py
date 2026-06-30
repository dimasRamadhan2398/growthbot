from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, Base, get_db

app = FastAPI(title="KB Service")

@app.on_event("startup")
def startup_db():
    Base.metadata.create_all(bind=engine)

def require_tenant_id(x_tenant_id: str = Header(None)):
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-ID header missing")
    return x_tenant_id

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "kb_service"}

@app.get("/api/kb-files", response_model=List[schemas.KBFileOut])
def get_kb_files(tenant_id: str = Depends(require_tenant_id), db: Session = Depends(get_db)):
    return db.query(models.KBFile).filter(models.KBFile.tenant_id == tenant_id).all()

@app.post("/api/kb-files", response_model=schemas.KBFileOut)
def create_kb_file(kb_file: schemas.KBFileCreate, tenant_id: str = Depends(require_tenant_id), db: Session = Depends(get_db)):
    new_file = models.KBFile(**kb_file.dict(), tenant_id=tenant_id)
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file

@app.delete("/api/kb-files/{file_id}")
def delete_kb_file(file_id: int, tenant_id: str = Depends(require_tenant_id), db: Session = Depends(get_db)):
    db_file = db.query(models.KBFile).filter(models.KBFile.id == file_id, models.KBFile.tenant_id == tenant_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File metadata not found")
    db.delete(db_file)
    db.commit()
    return {"message": "Deleted successfully"}
