import stripe
import os


stripe.api_key = os.getenv("STRIPE_API_KEY")


def create_payment_id(amount: float, currency: str, description: str, booking_id: str) -> str:
    intent = stripe.PaymentIntent.create(
        amount=int(amount*100),
        currency=currency,
        description=description,
        metadata={"booking_id", booking_id},
        payment_method_types=["card"],
        confirm=True
    )
    return intent['id']

