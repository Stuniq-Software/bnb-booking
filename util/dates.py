from datetime import datetime


def calculate_nights(checkin_date: datetime.date, checkout_date: datetime.date) -> int:
    return (checkout_date - checkin_date).days - 1


