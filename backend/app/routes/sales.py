from typing import Any, Dict
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.purchase import Purchase
from app.schemas.purchase import PurchaseRequest
from app.services.auth_service import get_current_user
from app.models.user import User
import stripe
import logging

logger = logging.getLogger(__name__)
purchase = APIRouter()

@purchase.post("/checkout")
def checkout(purchase_req: PurchaseRequest,db: Session = Depends(get_db),current_user: User = Depends(get_current_user),) -> Dict[str, Any]:
    
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(purchase_req.amount),
            currency="cop",
            payment_method=purchase_req.payment_method_id,
            confirm=True,
            automatic_payment_methods={"enabled": True, "allow_redirects": "never"},
        )
        status_code = intent.status

        if status_code == "succeeded":
            transaction = Purchase(
                user_id=current_user.id,
                stripe_payment_id=intent.id,
                amount=float(purchase_req.amount),
                currency=intent.currency,
                status=status_code,
                method=intent.payment_method_types[0],
                card_last4=(intent.charges.data[0].payment_method_details.card.last4
                            if intent.charges.data else None),
                card_brand=(intent.charges.data[0].payment_method_details.card.brand
                            if intent.charges.data else None),
                created_at=datetime.fromtimestamp(intent.created),
                extra_metadata=intent.metadata or {},
            )
            db.add(transaction)
            db.commit()
            db.refresh(transaction)
            return {"message": "Pago exitoso", "payment_id": intent.id}

        if status_code == "requires_action":
            return {
                "message": "Pago requiere acción adicional",
                "payment_intent_id": intent.id,
                "client_secret": intent.client_secret,
                "status": status_code,
            }

        if status_code == "requires_payment_method":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El método de pago fue rechazado o es inválido",
            )

        logger.warning("Intent de Stripe en estado inesperado %s", status_code,
                       extra={"intent_id": intent.id})
        raise HTTPException(status_code=500, detail="Estado de pago desconocido")

    except stripe.error.CardError as exc:
        logger.info("CardError de Stripe: %s", exc.user_message)
        raise HTTPException(status_code=400, detail=exc.user_message)

    except stripe.error.StripeError as exc:
        logger.exception("Error de Stripe: %s", exc)
        raise HTTPException(status_code=502,
                            detail="No se pudo procesar el pago, inténtalo más tarde")

    except Exception as exc:
        logger.exception("Error no controlado en checkout", exc_info=exc)
        raise HTTPException(status_code=500, detail="Error interno")
