from environs import Env


env = Env()
env.read_env()


API_HASH = env.str('API_HASH')
API_ID = env.int('API_ID')
AVAIBLE_CLIENTS = env.list('AVAIBLE_CLIENTS')
ADMIN_NUMBER = env.str('ADMIN_NUMBER')
FROM_CHANNEL = env.str('FROM_CHANNEL')
TO_CHANNEL = env.str('TO_CHANNEL')
