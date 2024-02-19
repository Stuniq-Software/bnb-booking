import stripe
import os
from datetime import datetime


stripe.api_key = os.getenv("STRIPE_API_KEY")


def create_payment_id(
        amount: float, 
        currency: str, 
        description: str, 
        booking_id: str, 
        stay_id: str, 
        user_id: str, 
        checkout_date: datetime
    ) -> str:
    print(f"Creating payment intent for {amount} {currency} for booking {booking_id}")
    intent = stripe.PaymentIntent.create(
        amount=int(amount*100),
        currency=currency.lower(),
        description=description,
        automatic_payment_methods={"enabled": True}
    )

    stripe.PaymentIntent.modify(
        intent["id"], 
        metadata={
            "booking_id": booking_id, 
            "stay_id": stay_id, 
            "user_id": user_id,
            "checkout_date": checkout_date
        }
    )

    return intent['id']

