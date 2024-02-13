from util import Database, RedisSession, create_payment_id, calculate_nights, calculate_total_price
from typing import Optional, Tuple
from datetime import datetime


class BookingRepository:
    db_session: Database
    redis_session: RedisSession

    def __init__(self, db_session: Database, redis_session: RedisSession):
        self.db_session = db_session
        self.redis_session = redis_session

    def get_booking(self, booking_id: str) -> Tuple[bool, Optional[dict]]:
        query = "SELECT * FROM bookings WHERE id = %s"
        success, err = self.db_session.execute_query(query, (booking_id,))
        if success:
            return success, self.db_session.get_cursor().fetchone()
        return success, err

    def create_booking(
            self,
            user_id: str,
            stay_id: str,
            checkin_date: datetime.date,
            checkout_date: datetime.date
    ) -> Tuple[bool, Optional[dict]]:
        nights = calculate_nights(checkin_date, checkout_date)
        total_price = calculate_total_price(stay_id, nights)
        payment_id = create_payment_id(
            total_price,
            "INR",
            f"Booking for stay {stay_id}\nFrom {checkin_date} to {checkout_date}"
        )
        query = ("INSERT INTO bookings (user_id, stay_id, checkin_date, checkout_date, nights, total_amount, "
                 "payment_id) VALUES (%s, %s, %s, %s, %s, %s, %s)")

        success, err = self.db_session.execute_query(query, (
            user_id, stay_id, checkin_date, checkout_date, nights, total_price, payment_id), True)
        if success:
            return success, {
                "user_id": user_id,
                "stay_id": stay_id,
                "payment_id": payment_id,
                "nights": nights,
                "total_amount": total_price,
                "status": "booked",
                "is_paid": False,
                "checkin_date": checkin_date,
                "checkout_date": checkout_date
            }
        return success, err

    def update_booking(
            self,
            booking_id: str,
            status: str = 'booked',
            is_paid: bool = False,
            cancel: bool = False
    ) -> Tuple[bool, Optional[str]]:
        query = "UPDATE bookings SET status = %s, is_paid = %s WHERE id = %s"
        success, err = self.db_session.execute_query(query, (status, is_paid, booking_id))
        if success:
            if cancel:
                return success, "Booking cancelled"
            return success, "Booking updated"
        return success, err

    def get_bookings_by_user(self, user_id: str) -> Tuple[bool, Optional[list]]:
        query = "SELECT * FROM bookings WHERE user_id = %s"
        success, err = self.db_session.execute_query(query, (user_id,))
        if success:
            return success, self.db_session.get_cursor().fetchall()
        return success, err

    def get_bookings_by_stay(self, stay_id: str) -> Tuple[bool, Optional[list]]:
        query = "SELECT * FROM bookings WHERE stay_id = %s"
        success, err = self.db_session.execute_query(query, (stay_id,))
        if success:
            return success, self.db_session.get_cursor().fetchall()
        return success, err