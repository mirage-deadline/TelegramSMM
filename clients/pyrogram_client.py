from datetime import datetime
import json
import os
from pathlib import Path
from typing import Union
from data import config
from datetime import datetime
from errors.custom_errors import ZeroAttemtsLeftError
from logger import logger
from pyrogram import Client
from pyrogram.types import ChatMember
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram.errors.exceptions.forbidden_403 import UserPrivacyRestricted
from pyrogram.errors.exceptions.bad_request_400 import PeerFlood, UserNotMutualContact


class PyrogramClient:

    __slots__ = ('client', 'invite_attempts', 'get_members_attemts', 'storage_members_path')

    def __init__(self, phone_number: str) -> None:
        self.client = Client(
            name=phone_number, 
            api_id=config.API_ID, 
            api_hash=config.API_HASH, 
            phone_number=phone_number, 
            workdir=self.sessions_folder)
    
    async def login(self):
        self.client = await self.client.start()
        return self

    async def join_channel(self, chanels: Union[list[str], str]):
        """Join client to channel

        Args:
            chanels (Union[list[str], str]): _description_
        """
        if isinstance(chanels, str):
            chanels = [chanels,]
        for chanel in chanels:
            await self.client.join_chat(chanel)
        return self
        
    async def left_channel(self, chanels: Union[list[str], str]):
        """Left client to channel

        Args:
            chanels (Union[list[str], str]): _description_
        """
        if isinstance(chanels, str):
            chanels = [chanels,]
        for chanel in chanels:
            await self.client.leave_chat(chanel)

    async def invite_user_to_group(self, chat_id: Union[str, int], user_id: Union[str, int]):
        try:
            chat_id = (await self.client.get_chat(chat_id)).id
            await self.client.add_chat_members(chat_id=chat_id, user_ids=user_id)
            logger.info(f'User with id {user_id} successfully added to {chat_id}')
        except (PeerFlood, FloodWait):
            logger.warning(f'Account banned for time. Use it for next day. Used account: {self.client.name}')
            raise ZeroAttemtsLeftError
        except UserNotMutualContact:
            logger.info(f'Not mutual. ID: {user_id}')

    async def load_members_list(self, chat_id: Union[int, str]):
        """Load and save parsed data if not exist else read from cache file

        Args:
            chat_id (Union[int, str]): _description_

        Returns:
            _type_: _description_
        """
        files_storage = Path(__file__).parent.parent / 'chat_members_data' / str(datetime.now().date())
        self.storage_members_path = os.path.join(files_storage, f'{chat_id}.json')
        if not os.path.exists(self.storage_members_path):
            Path(files_storage).mkdir(parents=True, exist_ok=True)
        return await self._load_new_data(chat_id)

    @staticmethod
    def _load_from_static(path_to_file: Path) -> list:
        """Load from local cache

        Args:
            path_to_file (Path): _description_

        Returns:
            _type_: _description_
        """
        with open(path_to_file, 'r') as file:
            data = json.load(file)
        return data

    async def _load_new_data(self, chat_id: Union[str, int]):
        return await self._format_requested_data(self.client.get_chat_members(chat_id))

    async def _format_requested_data(self, members_list: list[ChatMember]):
        all_data = []
        member: ChatMember
        async for member in members_list:
            if member.user.username not in ('yaskravviy', 'kurgan_smp', 'evdokiya_mr'):
                all_data.append({
                    'status': member.status.value,
                    'user_meta': {
                        'user_id': member.user.id,
                        'is_self': member.user.is_self,
                        'is_contact': member.user.is_contact,
                        'status': member.user.status.value if member.user.status else None,
                        'username': member.user.username,
                        'last_name': member.user.last_name,
                        'is_premium': member.user.is_premium,
                        'is_sapport': member.user.is_support,
                        'is_bot': member.user.is_bot,
                        'is_verified': member.user.is_verified
                    }
                })
        with open(self.storage_members_path, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=4)

        return all_data

    @property
    def sessions_folder(self) -> str:
        sessions_path = Path(__file__).parent.parent / 'sessions'
        if not sessions_path.exists():
            sessions_path.mkdir(parents=True, exist_ok=True)
        return sessions_path
    
    @property
    def client_phone(self) -> str:
        return self.client.name
