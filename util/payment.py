import stripe
import os


stripe.api_key = os.getenv("STRIPE_API_KEY")


def create_payment_id(amount: float, currency: str, description: str, booking_id: str) -> str:
    print(f"Creating payment intent for {amount} {currency} for booking {booking_id}")
    intent = stripe.PaymentIntent.create(
        amount=int(amount*100),
        currency=currency.lower(),
        description=description,
        automatic_payment_methods={"enabled": True}
    )

    stripe.PaymentIntent.modify(intent["id"], metadata={"booking_id": booking_id})

    return intent['id']

