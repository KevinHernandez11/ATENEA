from fastapi import APIRouter
from fastapi import Depends
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
def checkout(purchase: PurchaseRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        # Stripe requires the amount to be in the smallest currency unit (e.g., cents for USD).
        # Since COP does not use fractional units, we can pass the amount directly.
        intent = stripe.PaymentIntent.create(
            amount=int(purchase.amount),  # Monto en pesos colombianos directamente
            currency="cop",
            payment_method=purchase.payment_method_id,
            confirm=True
        )

        charge = intent.charges.data[0]

        transaction = Purchase(
            user_id=user.id,
            book_id=purchase.Book_id,
            stripe_payment_id=intent.id,
            amount=purchase.amount,
            currency=intent.currency,
            status=intent.status,
            method=intent.payment_method_types[0],
            card_last4=charge.payment_method_details.card.last4,
            card_brand=charge.payment_method_details.card.brand,
            created_at=datetime.fromtimestamp(intent.created),
            metadata=intent.metadata
        )

        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return {"message": "Pago exitoso", "payment_id": intent.id}

    except stripe.error.StripeError as e:
        return {"error": str(e)}

    

