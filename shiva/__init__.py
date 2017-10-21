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
            # response = process_message(message, chat)
            response = "halo"
            telegram.BOT.sendMessage(
                text=response,
                chat_id=chat
            )

            # start(message['chat']['id'])
            stop(message['chat']['id'])

    except Exception as e:
        core.logger.error(e, exc_info=e)

    return {'text': 'OK'}

def getJobId(label, chat_id):
    job_id = "{}:{}".format(chat_id, label)
    return job_id

def test_notify(chat_id):
    message = 'privet'
    telegram.BOT.sendMessage(
        text=message,
        chat_id=chat_id
    )

def start(chat_id):
    core.scheduler.addJob(
        label='test_notify',
        func_args=[chat_id],
        trigger='cron',
        trigger_params={'second': '*/5'},
        job_id=getJobId('test_notify', chat_id)
    )
    return '🔔 Ежедневные уведомления включены.'

def stop(chat_id):
    core.scheduler.removeJob(getJobId('test_notify', chat_id))
    return '🔕 Ежедневные уведомления выключены.'



core.scheduler.setFunctions({
    'test_notify': test_notify
})
core.scheduler.restoreJobs()

telegram = core.telegram
telegram.createWebhook(config['host'])
core.server.hooks.add(telegram.URI, tg_callback)

core.server.run()
