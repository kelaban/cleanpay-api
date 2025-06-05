from cleanpay_api.room_status import RoomStatus
from cleanpay_api.util import safely_get_json_value
from .cleanpay import CleanPay

from .room_status import Washer, Dryer


async def get_room_status(api: CleanPay, srcode: str) -> RoomStatus:
    location_data = await api.location_via_srcode(srcode)
    return RoomStatus(api, safely_get_json_value(location_data, "rooms.0.id"))