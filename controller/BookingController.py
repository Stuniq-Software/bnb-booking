from fastapi import APIRouter, Response, Request, Query
from repository import BookingRepository
from util import Database, RedisSession
from dtypes import APIResponse, HttpStatus
from datetime import datetime

router = APIRouter(prefix="/api/v1/booking", tags=["Booking"])
booking_service = BookingRepository(
    db_session=Database(),
    redis_session=RedisSession()
)


@router.post("/")
async def create_booking(request: Request, response: Response):
    body = await request.json()
    user_id = body['user_id']
    stay_id = body['stay_id']
    checkin_date = datetime.fromisoformat(body['checkin_date'])
    checkout_date = datetime.fromisoformat(body['checkout_date'])
    success, details = booking_service.create_booking(user_id, stay_id, checkin_date, checkout_date)
    if success:
        api_response = APIResponse(
            status=HttpStatus.CREATED,
            data=details,
            message="Booking created successfully"
        )
        response.status_code = api_response.status.value
        return api_response.to_dict()
    api_response = APIResponse(
        status=HttpStatus.INTERNAL_SERVER_ERROR,
        data=None,
        message="Error creating booking"
    )
    response.status_code = api_response.status.value
    return api_response.to_dict()


@router.get("/{uid}")
async def get_booking(
        uid: str,
        response: Response,
        id_type=Query(None, alias="type", description="Type of id", regex="user|booking")):
    if id_type == "user":
        success, booking = booking_service.get_bookings_by_user(uid)
    elif id_type == "booking":
        success, booking = booking_service.get_booking(uid)
    else:
        api_response = APIResponse(
            status=HttpStatus.BAD_REQUEST,
            data=None,
            message="Invalid id type"
        )
        response.status_code = api_response.status.value
        return api_response.to_dict()
    if success:
        api_response = APIResponse(
            status=HttpStatus.OK,
            data=booking,
            message="Booking found"
        )
        response.status_code = api_response.status.value
        return api_response.to_dict()
    api_response = APIResponse(
        status=HttpStatus.NOT_FOUND,
        data=None,
        message="Booking not found"
    )
    response.status_code = api_response.status.value
    return api_response.to_dict()


@router.put("/{booking_id}")
async def update_booking(booking_id: str, request: Request, response: Response):
    body = await request.json()
    status = body['status']
    is_paid = body['is_paid']
    cancel = body.get('cancel', False)
    success, message = booking_service.update_booking(booking_id, status, is_paid, cancel)
    if success:
        api_response = APIResponse(
            status=HttpStatus.OK,
            data=None,
            message=message
        )
        response.status_code = api_response.status.value
        return api_response.to_dict()
    api_response = APIResponse(
        status=HttpStatus.INTERNAL_SERVER_ERROR,
        data=None,
        message="Error updating booking"
    )
    response.status_code = api_response.status.value
    return api_response.to_dict()
