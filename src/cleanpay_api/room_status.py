from dataclasses import dataclass
import logging

from cleanpay_api.cleanpay import CleanPay

from .util import (
    safely_get_json_value,
)

_LOGGER = logging.getLogger(__name__)

@dataclass(kw_only=True)
class Washer():
    label_id: str
    satus: str
    status_text: str
    left_time: str
    sub_type: str

class Dryer():
    pass


class RoomStatus():
    wash_total: int = 0
    wash_available: int = 0

    dryer_total: int = 0
    dryer_available: int = 0

    washers: list[Washer] = []
    dryers: list[Dryer] = []

    def __init__(self, api: CleanPay, location_id: str):
        self.api = api
        self.location_id = location_id

    async def refesh(self):
        token = await self.api.login()
        state = await self.api.room_status(token, self.location_id)

        _LOGGER.debug(f"update local state: {self.location_id}, {state}")

        self.wash_total = safely_get_json_value(state, "wash_total", int)
        self.wash_available = safely_get_json_value(state, "wash_available", int)

        self.dryer_total = safely_get_json_value(state, "dryer_total", int)
        self.dryer_available = safely_get_json_value(state, "dryer_available", int)

        self.washers = safely_get_json_value(state, "washers", lambda washers: [Washer(**w) for w in washers])
        self.dryers = safely_get_json_value(state, "dryers")

    def __repr__(self):
        return {
            "wash_total": self.wash_total,
            "wash_available": self.wash_available,
            "dryer_total": self.dryer_total,
            "dryer_available": self.dryer_available,
            "washers": self.washers,
            "dryers": self.dryers
        }

    def __str__(self):
        return f"{self.__repr__()}"