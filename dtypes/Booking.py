from typing import List, Optional


class Booking:
    id: str
    user_id: str
    stay_id: str
    checkin_date: str
    checkout_date: str
    nights: int
    total_amount: float
    payment_id: str
    is_paid: bool
    status: str
    created_at: Optional[str]
    updated_at: Optional[str]

    def __init__(self):
        self.id = ""
        self.user_id = ""
        self.stay_id = ""
        self.checkin_date = ""
        self.checkout_date = ""
        self.nights = 0
        self.total_amount = 0.0
        self.payment_id = ""
        self.is_paid = False
        self.status = ""
        self.created_at = None
        self.updated_at = None

    @staticmethod
    def from_tuple(booking_tuple: tuple):
        booking = Booking()
        booking.id = booking_tuple[0]
        booking.user_id = booking_tuple[1]
        booking.stay_id = booking_tuple[2]
        booking.checkin_date = booking_tuple[3]
        booking.checkout_date = booking_tuple[4]
        booking.nights = booking_tuple[5]
        booking.total_amount = booking_tuple[6]
        booking.payment_id = booking_tuple[7]
        booking.is_paid = booking_tuple[8]
        booking.status = booking_tuple[9]
        booking.created_at = booking_tuple[10]
        booking.updated_at = booking_tuple[11]
        return booking

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "stay_id": self.stay_id,
            "checkin_date": self.checkin_date,
            "checkout_date": self.checkout_date,
            "nights": self.nights,
            "total_amount": self.total_amount,
            "payment_id": self.payment_id,
            "is_paid": self.is_paid,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
