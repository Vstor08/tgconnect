from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsAdmin(BaseFilter):
    def __init__(self, admin_id: str):
        self.admin_id = admin_id

    async def __call__(self, message: Message) -> bool:
        return str(message.from_user.id) == self.admin_id

class Command(BaseFilter):
    def __init__(self, command: str):
        self.command = command

    async def __call__(self, message: Message) -> bool:
        if not message.text:
            return False
        return message.text.strip().startswith(f"/{self.command}")

class Text(BaseFilter):
    def __init__(self, text: str):
        self.text = text
    async def __call__(self,message: Message) -> bool:
        return message.text == self.text
