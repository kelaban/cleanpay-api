import logging
from typing import Optional

from aiohttp import ClientSession, ClientResponse, ClientError, __version__, formdata
from aiohttp.hdrs import USER_AGENT

from .util_http import request_with_logging

_LOGGER = logging.getLogger(__name__)

API_URL: str = "https://express.kiosoft.com/api/"


class CleanPay:
    def __init__(self, api_key: str, userid: str, client_session: Optional[ClientSession] = None):
        self.api_key = api_key
        self.userid = userid

        if client_session is None:
            self.api_session = ClientSession(raise_for_status=True)
        else:
            self.api_session = client_session
        _LOGGER.debug(f"api_session_version: {__version__}")

    async def cleanup_client_session(self):
        await self.api_session.close()

    @request_with_logging
    async def _post_request_with_logging_and_errors_raised(
        self, url: str, json_body: dict 
    ) -> ClientResponse:
        headers = {}
        headers["X-API-Key"] = self.api_key
        return await self.api_session.post(url=url, json=json_body, headers=headers)

    @request_with_logging
    async def _post_form_request_with_logging_and_errors_raised(
        self, url: str, data: dict
    ) -> ClientResponse:
        headers = { }
        headers["X-API-Key"] = self.api_key

        return await self.api_session.request(url=url, data=formdata.FormData(data), headers=headers, method="POST")

    @request_with_logging
    async def _get_request_with_logging_and_errors_raised(
        self, url: str, params: Optional[dict] = None
    ) -> ClientResponse:
        headers = {}
        headers["X-API-Key"] = self.api_key
        return await self.api_session.get(url=url, headers=headers, params=params)

    async def login(self) -> str:
        url = API_URL + "auth/third_login"
        data = {
            "app_version": "3.6.1",
            "language": 1, 
            "source": 2,
            "userid": self.userid,
        }
        response: ClientResponse = (
            await self._post_form_request_with_logging_and_errors_raised(
                url=url, data=data
            )
        )
        response_json = await response.json()
        return response_json["token"]

    async def room_status(self, auth_token: str, location_id: str):
        url = API_URL + "rooms/room_status"
        params = {"location_id": location_id, "room_number": 1, "token": auth_token}
        response: ClientResponse = (
            await self._get_request_with_logging_and_errors_raised(
                url=url, params=params
            )
        )
        response_json = await response.json()
        return response_json["data"]

    async def location_via_srcode(self, srcode: str):
        url = API_URL + "locations/get_location_via_srcode"
        params = {"language": 1, "srcode": srcode}
        response: ClientResponse = (
            await self._get_request_with_logging_and_errors_raised(
                url=url, params=params
            )
        )
        response_json = await response.json()
        return response_json