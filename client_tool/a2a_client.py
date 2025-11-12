# client_tool/a2a_client.py
# --------------------------------------------------------------
# Minimal, standalone PaymentRemoteA2aClient – no common/ needed
# --------------------------------------------------------------

import httpx
import logging
import uuid
from typing import Set

from a2a import types as a2a_types
from a2a.client.card_resolver import A2ACardResolver
from a2a.client.client import Client, ClientConfig
from a2a.client.client_factory import ClientFactory
from a2a.client.client_task_manager import ClientTaskManager

DEFAULT_TIMEOUT = 600.0
HTTP_EXTENSION_HEADER = "X-A2A-Extensions"
# Change if your remote agents require extensions
EXTENSION_URI = "http://example.com/extensions"


class PaymentRemoteA2aClient:
    """Wrapper identical to AP2 sample – no external imports."""
    def __init__(
        self,
        name: str,
        base_url: str,
        required_extensions: Set[str] | None = None,
    ):
        self._httpx_client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout=DEFAULT_TIMEOUT)
        )
        self._factory = ClientFactory(ClientConfig(httpx_client=self._httpx_client))
        self._name = name
        self._base_url = base_url.rstrip("/")
        self._agent_card = None
        self._required_extensions = required_extensions or set()

    async def get_agent_card(self) -> a2a_types.AgentCard:
        if self._agent_card is None:
            resolver = A2ACardResolver(
                httpx_client=self._httpx_client,
                base_url=self._base_url,
            )
            self._agent_card = await resolver.get_agent_card()
        return self._agent_card

    async def send_a2a_message(self, message: a2a_types.Message) -> a2a_types.Task:
        client: Client = await self._get_a2a_client()
        task_manager = ClientTaskManager()

        async for event in client.send_message(message):
            if isinstance(event, tuple):
                event = event[0]
            await task_manager.process(event)

        task = task_manager.get_task()
        if task is None:
            raise RuntimeError(f"No response from {self._name}")

        logging.info(
            "Response from %s (context_id=%s, task_id=%s)",
            self._name, task.context_id, task.id,
        )
        return task

    async def _get_a2a_client(self) -> Client:
        await self.get_agent_card()
        if self._required_extensions:
            self._httpx_client.headers[HTTP_EXTENSION_HEADER] = ", ".join(
                self._required_extensions
            )
        return self._factory.create(self._agent_card)

    def create_message(self, text: str) -> a2a_types.Message:
        return a2a_types.Message(
            message_id=uuid.uuid4().hex,
            parts=[a2a_types.Part(root=a2a_types.TextPart(text=text))],
            role=a2a_types.Role.agent,
        )