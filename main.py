import asyncio
import shutil
from clients.client_manager import ClientManager
from clients.pyrogram_client import PyrogramClient
from data import config
from pathlib import Path


def remove_old_sessions():
    sessions_folder = Path(__file__).parent / 'sessions'
    shutil.rmtree(sessions_folder)
    sessions_folder.mkdir(parents=True, exist_ok=True)


async def main():
    clients = [PyrogramClient(number) for number in config.AVAIBLE_CLIENTS]
    inviter = ClientManager(clients=clients, count_of_new_users=30, chat_from=config.FROM_CHANNEL, chat_to=config.TO_CHANNEL)
    await inviter.upgrade_group_count()


if __name__ == '__main__':
    remove_old_sessions()
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())