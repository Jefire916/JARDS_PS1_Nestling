"""
Nestling Decision Engine API
Hackathon: AI-gnition — Problem Statement 1
Author: Devanshi (Customer Data & Decision Engine Lead)
Features:
- REST API powered by FastAPI
- Confidence-weighted consent validation:
    confidence(consent_opted_in) > (confidence(consent_opted_out) + confidence(OPT_OUT))
- Dynamic calculation of:
    * Diaper & wipes replenishment schedules
    * User-requested snoozes (3 or 7 days)
    * Inactivity winback (Free delivery if inactive > 30 days)
    * Baby birthday month free delivery perk
    * Stage-based size-up for Diapers, Clothing (0-18M), Toys (Sets 1-4 & Play Mat), and Formula
    * Strict WHO Code compliance guardrails for infant formula Stage 1 & 2
- MantaGO OpenAPI webhook compatibility
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime, date, timedelta
import uvicorn
app = FastAPI(
    title="Nestling Decision Engine API",
    description="Automated customer data evaluation and reminder dispatch engine for Nest Helper",
    version="1.0.0"
)
# ---------------------------------------------------------
# DATA MODELS
# ---------------------------------------------------------
class CustomerEvaluationRequest(BaseModel):
    customer_id: str
    parent_name: str
    baby_name: str
    baby_birth_date: Optional[str] = None  # YYYY-MM-DD
    last_order_date: str                   # YYYY-MM-DD
    last_product_purchased: str
    last_category: str                     # Diapers, Wipes, Clothing, Toys, Formula
    last_interaction_date: Optional[str] = None # YYYY-MM-DD
    snooze_until: Optional[str] = None     # YYYY-MM-DD (e.g. from 3 or 7-day request)
