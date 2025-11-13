from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import os
import json
import uuid
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'sqlite:///./typesync.db'
)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI app
app = FastAPI(
    title='TypeSync Landing API',
    description='Minimal API for EAS-20 and AAS assessments'
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Import models
from models import Base, EAS20Assessment, AASAssessment

# Create tables
Base.metadata.create_all(bind=engine)

# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get('/api/assessments/all')
def get_all_assessments(db: Session = Depends(get_db)):
    """Get all assessment IDs"""
    eas20 = db.query(EAS20Assessment).all()
    aas = db.query(AASAssessment).all()
    
    return {
        'eas20_count': len(eas20),
        'aas_count': len(aas),
        'eas20_ids': [a.assessment_id for a in eas20],
        'aas_ids': [a.assessment_id for a in aas]
    }

@app.get('/')
def root():
    """Root endpoint"""
    return {
        'message': 'TypeSync Landing API',
        'version': '1.0.0',
        'status': 'running'
    }

@app.get('/health')
def health():
    """Health check endpoint"""
    return {
        'status': 'ok',
        'timestamp': datetime.utcnow().isoformat()
    }

# ============================================================================
# EAS-20 ENDPOINTS
# ============================================================================

@app.post('/api/assessments/eas20/save')
def save_eas20(
    data: dict,
    db: Session = Depends(get_db)
):
    """
    Save EAS-20 assessment results
    
    Expected data structure:
    {
        "responses": [1, 2, 3, 4, 5, ...],  // 20 ratings
        "scores": {
            "Strategist": 85,
            "Guardian": 70,
            ...
        }
    }
    """
    try:
        # Generate unique assessment ID
        assessment_id = str(uuid.uuid4())
        
        # Create assessment record
        assessment = EAS20Assessment(
            assessment_id=assessment_id,
            responses=json.dumps(data.get('responses', [])),
            scores=json.dumps(data.get('scores', {})),
            created_at=datetime.utcnow()
        )
        
        db.add(assessment)
        db.commit()
        db.refresh(assessment)
        
        logger.info(f'EAS-20 assessment saved: {assessment_id}')
        
        return {
            'success': True,
            'assessment_id': assessment_id,
            'type': 'EAS-20',
            'results_url': f'/results/{assessment_id}'
        }
    except Exception as e:
        db.rollback()
        logger.error(f'Error saving EAS-20: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/assessments/eas20/{assessment_id}')
def get_eas20(
    assessment_id: str,
    db: Session = Depends(get_db)
):
    """Retrieve EAS-20 assessment results"""
    try:
        assessment = db.query(EAS20Assessment).filter(
            EAS20Assessment.assessment_id == assessment_id
        ).first()
        
        if not assessment:
            raise HTTPException(status_code=404, detail='Assessment not found')
        
        return {
            'type': 'EAS-20',
            'assessment_id': assessment.assessment_id,
            'scores': json.loads(assessment.scores),
            'responses': json.loads(assessment.responses),
            'created_at': assessment.created_at.isoformat()
        }
    except Exception as e:
        logger.error(f'Error retrieving EAS-20: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# AAS ENDPOINTS
# ============================================================================

@app.post('/api/assessments/aas/save')
def save_aas(
    data: dict,
    db: Session = Depends(get_db)
):
    """
    Save AAS assessment results
    
    Expected data structure:
    {
        "responses": [1, 2, 3, ...],
        "scores": {
            "Strategist": 90,
            "Guardian": 65,
            ...
        }
    }
    """
    try:
        # Generate unique assessment ID
        assessment_id = str(uuid.uuid4())
        
        # Create assessment record
        assessment = AASAssessment(
            assessment_id=assessment_id,
            responses=json.dumps(data.get('responses', [])),
            scores=json.dumps(data.get('scores', {})),
            created_at=datetime.utcnow()
        )
        
        db.add(assessment)
        db.commit()
        db.refresh(assessment)
        
        logger.info(f'AAS assessment saved: {assessment_id}')
        
        return {
            'success': True,
            'assessment_id': assessment_id,
            'type': 'AAS',
            'results_url': f'/results/{assessment_id}'
        }
    except Exception as e:
        db.rollback()
        logger.error(f'Error saving AAS: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/assessments/aas/{assessment_id}')
def get_aas(
    assessment_id: str,
    db: Session = Depends(get_db)
):
    """Retrieve AAS assessment results"""
    try:
        assessment = db.query(AASAssessment).filter(
            AASAssessment.assessment_id == assessment_id
        ).first()
        
        if not assessment:
            raise HTTPException(status_code=404, detail='Assessment not found')
        
        return {
            'type': 'AAS',
            'assessment_id': assessment.assessment_id,
            'scores': json.loads(assessment.scores),
            'responses': json.loads(assessment.responses),
            'created_at': assessment.created_at.isoformat()
        }
    except Exception as e:
        logger.error(f'Error retrieving AAS: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# UNIFIED RESULTS ENDPOINT
# ============================================================================

@app.get('/api/results/{assessment_id}')
def get_results(
    assessment_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve assessment results from either EAS-20 or AAS
    """
    try:
        # Try EAS-20 first
        eas20 = db.query(EAS20Assessment).filter(
            EAS20Assessment.assessment_id == assessment_id
        ).first()
        
        if eas20:
            return {
                'type': 'EAS-20',
                'assessment_id': eas20.assessment_id,
                'scores': json.loads(eas20.scores),
                'responses': json.loads(eas20.responses),
                'created_at': eas20.created_at.isoformat()
            }
        
        # Try AAS
        aas = db.query(AASAssessment).filter(
            AASAssessment.assessment_id == assessment_id
        ).first()
        
        if aas:
            return {
                'type': 'AAS',
                'assessment_id': aas.assessment_id,
                'scores': json.loads(aas.scores),
                'responses': json.loads(aas.responses),
                'created_at': aas.created_at.isoformat()
            }
        
        raise HTTPException(status_code=404, detail='Assessment not found')
    except Exception as e:
        logger.error(f'Error retrieving results: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )
