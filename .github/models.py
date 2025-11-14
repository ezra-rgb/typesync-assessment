from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# ============================================================================
# EAS-20 Assessment Model
# ============================================================================

class EAS20Assessment(Base):
    """
    Environmental Assessment Scale - 20 items
    Stores assessment results for EAS-20
    """
    __tablename__ = 'eas20_assessments'
    
    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(String(255), unique=True, index=True, nullable=False)
    responses = Column(Text)  # JSON array of 20 responses
    scores = Column(Text)     # JSON object with archetype scores
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<EAS20Assessment {self.assessment_id}>'

# ============================================================================
# AAS Assessment Model
# ============================================================================

class AASAssessment(Base):
    """
    Archetype Assessment Scale
    Stores assessment results for AAS
    """
    __tablename__ = 'aas_assessments'
    
    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(String(255), unique=True, index=True, nullable=False)
    responses = Column(Text)  # JSON array of responses
    scores = Column(Text)     # JSON object with archetype scores
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<AASAssessment {self.assessment_id}>'
