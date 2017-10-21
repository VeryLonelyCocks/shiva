from .core import Core
from .config import config
import datetime
from .commands import TelegramCommands

core = Core(config)
telegramHandler = TelegramCommands(core)

# def log_event(event):
#     table = core.db['events']
#     date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     event_model = {
#         'date': date,
#         'event': event
#     }
#     table.insert_one(event_model)
#
# def return_chat(chat_data):
#     table = core.db['chats']
#     chat = table.find_one({'id': chat_data['id']})
#     if not chat:
#         chat = table.insert_one(chat_data)
#         chat = table.find_one({'id': chat_data['id']})
#     return chat

# async def tg_callback(request):
#     try:
#         ## get event and logs it #
#         event = await request.json()
#         log_event(event)
#         core.logger.info('Got a new event: %s' % event)
#         ###

telegram = core.telegram
telegram.create_webhook(config['host'])
core.server.hooks.add(telegram.URI, telegramHandler.telegram_callback)

core.server.run()
