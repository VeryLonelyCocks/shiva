from .Core import Core
from .config import config
import datetime
import json

core = Core(config['core'])

def log_event(event):
    table = core.db['events']
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    event_model = {
        'date': date,
        'event': event
    }
    table.insert_one(event_model)

def return_chat(chat_data):
    table = core.db['chats']
    chat = table.find_one({'id': chat_data['id']})
    if not chat:
        chat = table.insert_one(chat_data)
    return chat

async def tg_callback(request):
    try:
        ## get event and log it #
        event = await request.json()
        log_event(event)
        core.logger.info('Got a new event: %s' % event)
        ###

        message = event.get("message", "")
        if message:
            chat = return_chat(message['chat'])
            print(chat)
            response = "hello!"
            telegram.BOT.sendMessage(
                text=response,
                chat_id=chat['id']
            )

    except Exception as e:
        core.logger.error(e, exc_info=e)

    return {'text': 'OK'}

telegram = core.telegram
telegram.createWebhook(config['host'])
core.server.hooks.add(telegram.URI, tg_callback)

core.server.run()
