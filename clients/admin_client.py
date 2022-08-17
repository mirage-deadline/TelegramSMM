from typing import Union
from data import config
from clients.base_client import BaseClient
from pyrogram.types import ChatPrivileges


class AdminClient(BaseClient):

    def __init__(self) -> None:
        super().__init__(config.ADMIN_NUMBER)

    async def make_admin(self, user_id: Union[str, int], chat_id: Union[str, int]) -> bool:
        self.active_client = await self.activate()
        self.active_client.get_chat_members('+P4O2JTA3DXo1N2U6')
        try:
            await self.active_client.promote_chat_member(
                chat_id, 
                user_id, 
                privileges= ChatPrivileges(
                    can_invite_users=True
                ))
            return True
        except TypeError:
            return False

AdminClientSinglton = AdminClient()
