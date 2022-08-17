import asyncio
from clients.client_manager import ClientManager
from clients.pyrogram_client import PyrogramClient
from data import config


async def main():
    clients = []
    for number in config.AVAIBLE_CLIENTS:
        obj = PyrogramClient(number)
        await (await obj.login()).join_channel(chanels=[config.FROM_CHANNEL, config.TO_CHANNEL])
        clients.append(obj)

    inviter = ClientManager(clients=clients, count_of_new_users=60, chat_from=config.FROM_CHANNEL, chat_to=config.TO_CHANNEL)
    await inviter.upgrade_group_count()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())