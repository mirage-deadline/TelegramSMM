import asyncio
import json
import sys
from errors.custom_errors import ZeroAttemtsLeftError
from logger import logger
from clients.pyrogram_client import PyrogramClient
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram.errors.exceptions.forbidden_403 import UserPrivacyRestricted
from pyrogram.errors.exceptions.bad_request_400 import PeerFlood, UserNotMutualContact


class ClientManager:

    def __init__(self, clients: list[PyrogramClient], count_of_new_users: int, chat_from: str, chat_to: str) -> None:
        self.clients = clients
        self.count_of_new_users = count_of_new_users
        self.chat_from = chat_from
        self.chat_to = chat_to
    
    async def upgrade_group_count(self):

        client_generator = self.clients_generator()
        client = await (await next(client_generator).login()).join_channel([self.chat_from, self.chat_to])
        
        members = await self.get_members(client)

        success_invites = 0

        for user_id in members:
            
            try:
                if self.count_of_new_users == success_invites:
                    sys.exit('Target added quantity received')
                await client.invite_user_to_group(chat_id=self.chat_to, user_id=user_id)
                success_invites += 1
                logger.info(f'{user_id} -> ADDED. Total invited {success_invites}')
            except PeerIdInvalid as pii:
                logger.error(f'Theory about same ids of my acc. {user_id}. Exceptrion {pii}')
            except UserPrivacyRestricted as _ex:
                logger.info(f'{user_id} -> Privicy policy not allowed to add him. {_ex}')
            except ZeroAttemtsLeftError:
                client = await (await next(client_generator).login()).join_channel([self.chat_from, self.chat_to])
                await client.load_members_list(self.chat_from)
                logger.info(f'New client activated {client.client_phone}')
            await asyncio.sleep(3)
            
    
    async def login_client(self, base_client: PyrogramClient) -> PyrogramClient:
        client = await base_client.login()
        for channel in (self.chat_from, self.chat_to):
            await client.join_channel(channel)
        return client

    async def left_from_groups(self, client: PyrogramClient):
        for channel in (self.chat_from, self.chat_to):
            await client.left_channel(channel)

    def clients_generator(self):

        client: PyrogramClient
        for client in self.clients:
            yield client
    
    async def get_members(self, client: PyrogramClient, status_filter=['member', ], online_filter=('recently', 'online', 'offline')):
        valid_data = []
        all_data = await client.load_members_list(self.chat_from)
        for row in all_data:
            if row['status'] in status_filter:
                if row['user_meta']['status'] in online_filter:
                    valid_data.append(row['user_meta']['user_id'])
        return valid_data
