from .Core import Core
from .config import config
from aiohttp import web
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

async def vk_callback(request):
    """
    Web App function for processing callback
    """
    try:
        data = await request.json()
        print(data)

        if data['type'] == 'confirmation':
            return {'text': '2bc41420'}

        if data['type'] == 'message_new':
            vk.send_photo(data['object']['user_id'], "E:\GitHubRep\shiva\shiva\messengers\\vk\ii5hpvRVF24.jpg")
    except Exception as e:
        print("Message process error: [%s]" % e)

    return {'text': 'ok'}

telegram = core.telegram
telegram.createWebhook(config['host'])
core.server.hooks.add(telegram.URI, tg_callback)

vk = core.vk
core.server.hooks.add(vk.get_web_hook(), vk_callback)

core.server.run()
