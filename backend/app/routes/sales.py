from fastapi import APIRouter
from fastapi import Depends, HTTPException
from app.services.auth_service import get_current_user
from app.models.user import User
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.purchase import Purchase
from app.schemas.purchase import PurchaseRequest
from datetime import datetime
from dotenv import load_dotenv

# from google.oauth2 import service_account
import stripe
import os

purchase = APIRouter()

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@purchase.post("/checkout")
def checkout(purchase: PurchaseRequest, db: Session = Depends(get_db)):
    user = "580c40c2-5327-47fd-a5ec-ab3e42d79cbb"  # For testing purposes, replace with actual user retrieval logic
    try:
        # Stripe requires the amount to be in the smallest currency unit (e.g., cents for USD).
        # Since COP does not use fractional units, we can pass the amount directly.
        intent = stripe.PaymentIntent.create(
            amount=int(purchase.amount),  # Monto en pesos colombianos directamente
            currency="cop",
            payment_method=purchase.payment_method_id,
            confirm=True,
            automatic_payment_methods={
                "enabled": True,
                "allow_redirects": "never"
            },
        #     expand=["charges"]
        )

        # charges = intent.get("charges", {}).get("data", [])
        # if not charges:
        #     raise HTTPException(status_code=400, detail="No se generó ningún cargo")

        # charge = charges[0]

        transaction = Purchase(
            user_id=user,
            stripe_payment_id=intent.id,
            amount=purchase.amount,
            currency=intent.currency,
            status=intent.status,
            method=intent.payment_method_types[0],
            card_last4=None,
            card_brand=None,
            created_at=datetime.fromtimestamp(intent.created),
            metadata=intent.metadata
        )

        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return {"message": "Pago exitoso", "payment_id": intent.id}

    except stripe.error.StripeError as e:
        return {"error": str(e)}

    

