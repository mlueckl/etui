import httpx
import logging
import asyncio
from typing import Dict

logger = logging.getLogger(__name__)


class Request:
    header = {}

    # TODO: Improve Auth handling
    def __init__(self, base_url: str, auth_token: str = "", timeout: float = 30.0, semaphore: int = 100) -> None:
        """Request class to handle HTTP requests

        Args:
            base_url (str): Base URL
            auth_token (str): Encrypted auth token
            timeout (float, optional): Timeout for request. Defaults to 30.0.
            semaphore (int, optional): How many concurrent async calls. Defaults to 100.
        """
        self.base_url = base_url
        self.auth_token = auth_token
        self.timeout = timeout
        self.semaphore = asyncio.Semaphore(semaphore)

    def _set_headers(self, additional_headers: Dict[str, str]) -> Dict[str, str]:
        self.header = {
            "Authorization": f"{self.auth_token}",
            "Accept": "application/json",
        }

        if additional_headers != {}:
            self.header.update(additional_headers)

    def _handle_response_codes(self, response: httpx._models.Response):
        if response.status_code == 500:
            logger.warning(f"{response.request} - {response.text}")

        return response

    def call(
        self,
        endpoint: str,
        method: str,
        parameters: Dict[str, str] = {},
        data: Dict[str, str] = {},
        additional_headers: Dict[str, str] = {},
    ) -> httpx._models.Response:
        self._set_headers(additional_headers)
        if method == "PUT":
            self.header["Content-Type"] = "application/json-patch+json"

        try:
            r = httpx.request(
                method,
                f"{self.base_url}/{endpoint}",
                params=parameters,
                data=data,
                headers=self.header,
                timeout=httpx.Timeout(
                    self.timeout,
                    read=None,
                ),
            )

            self._handle_response_codes(r)

            return r
        except httpx.ConnectTimeout:
            logger.warning(f"ConnectionTimeout: {endpoint}")

    async def call_async(
        self,
        endpoint: str,
        method: str,
        parameters: Dict[str, str] = {},
        data: Dict[str, str] = {},
        additional_headers: Dict[str, str] = {},
    ) -> httpx._models.Response:
        self._set_headers(additional_headers)
        if method == "PUT":
            self.header["Content-Type"] = "application/json-patch+json"

        try:
            async with httpx.AsyncClient() as client:
                async with self.semaphore:
                    r = await client.request(
                        method,
                        f"{self.base_url}/{endpoint}",
                        params=parameters,
                        data=data,
                        headers=self.header,
                        timeout=httpx.Timeout(
                            self.timeout,
                            read=None,
                        ),
                    )

                    self._handle_response_codes(r)

                    return r
        except httpx.ConnectTimeout:
            logger.warning(f"ConnectionTimeout: {endpoint}")
