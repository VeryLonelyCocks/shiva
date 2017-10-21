from .core import Core
from .config import config
import datetime
from .commands import TelegramCommands

core = Core(config)
telegramHandler = TelegramCommands(core)

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
        chat = table.find_one({'id': chat_data['id']})
    return chat

async def tg_callback(request):
    try:
        ## get event and logs it #
        event = await request.json()
        log_event(event)
        core.logger.info('Got a new event: %s' % event)
        ###

        selectel = core.selectel

        message = event.get("message", "")
        chat = {}
        text = ''

        if message:
            chat = message['chat']
            text = message.get('text', '')
        #     selectel.auth_by_chat_id(chat['id'])
        #
        # if text.startswith('/auth'):
        #     cmd, user, password = text.split(' ')
        #
        #     telegram.storage_auth(chat['id'], user, password)
        #
        # if text.startswith('/new_container'):
        #     cmd, name = text.split(' ')
        #
        #     telegram.create_container(name)
        #
        # if text.startswith('/containers'):
        #     containers = telegram.get_containers_list()
        #
        #     response = ''
        #     for container in containers:
        #         response += container['name'] + '\n'
        #
        #     core.telegram.BOT.send_message(text=response, chat_id=chat['id'])
        #
        # if text.startswith('/files'):
        #     cmd, container = text.split(' ')
        #     files = telegram.get_files_list(container)
        #
        #     response = ''
        #     for file in files:
        #         response += file['name'] + '\n'
        #
        #     core.telegram.BOT.send_message(text=response, chat_id=chat['id'])
        #
        # if text.startswith('/delete'):
        #     cmd, container, file_name = text.split(' ')
        #
        #     telegram.delete_file(container, file_name)
        #
        # if text.startswith('/download'):
        #     cmd, container, file_name = text.split(' ')
        #     file = telegram.download_file(container, file_name)
        #     core.telegram.BOT.send_document(file, chat['id'])
        #
        # document = message.get('document', '')
        #
        # if document:
        #     caption = message.get('caption', '')
        #
        #     if caption.startswith('/upload'):
        #         cmd, container, file_name = caption.split(' ')
        #         file = core.telegram.BOT.return_file(document['file_id'])
        #         telegram.upload_file(container, file_name, file)

        # if message.startswith('/upload')

        if text.startswith('/notifier'):
            # core.telegram.BOT.send_document(file, chat['id'])
            return core.notifier.process_start(chat['id'], 'telegram')

        # process_start

        # if message:
        #     chat = return_chat(message['chat'])
        #     print(chat)
        #     response = "hello!"
        #     telegram.BOT.send_message(
        #         text=response,
        #         chat_id=chat['id']
        #     )

    except Exception as e:
        core.logger.error(e, exc_info=e)

    return {'text': 'ok'}

telegram = core.telegram
telegram.create_webhook(config['host'])
core.server.hooks.add(telegram.URI, telegramHandler.telegram_callback)

core.server.run()
