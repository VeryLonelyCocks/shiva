from .config import config
import requests
import json
import uuid


class Telegram():

    def __init__(self):
        self.TOKEN = config['token']
        self.BOT = API(self.TOKEN)

    def create_webhook(self, host):
        self.HOST = host

        # self.URI = '/%s' % uuid.uuid4().hex
        self.URI = '/telegram'

        self.WEBHOOK = 'https://{}{}'.format(self.HOST, self.URI)
        return self.BOT.set_webhook(self.WEBHOOK)


class API:
    """
    https://core.telegram.org/bots/api#available-methods
    """

    def __init__(self, token):
        self.TOKEN = token

    def telegram_action(self, action, data={}, files={}):
        botURL = 'https://api.telegram.org/bot' + self.TOKEN + '/' + action
        if data.get('reply_markup'):
            data['reply_markup'] = json.dumps(data['reply_markup'])

        result = requests.post(botURL, data=data, files=files)
        response = result.content.decode("utf-8")
        try:
            return json.loads(response)
        except:
            return result

    def telegram_return_file(self, file_id):

        getFileURL = 'https://api.telegram.org/bot' + self.TOKEN + '/getFile?file_id=' + file_id
        result = requests.get(getFileURL)
        result = result.json()

        print(result)

        fileUrl = 'https://api.telegram.org/file/bot' + self.TOKEN + '/' + result['result']['file_path']

        response = requests.get(fileUrl, stream=True)

        name = str(uuid.uuid4()) + '.tmp'
        handle = open(name, "xb")
        for chunk in response.iter_content(chunk_size=512):
            if chunk:  # filter out keep-alive new chunks
                handle.write(chunk)

        return name


    def get_updates(self, data={'limit': 100}):
        return self.telegram_action('getUpdates', data=data)

    def send_message(self,
                    text,
                    chat_id,
                    parse_mode='',
                    disable_web_page_preview=False,
                    disable_notification=False,
                    reply_to_message_id=0,
                    reply_markup={}):
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'disable_web_page_preview': disable_web_page_preview,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': reply_markup
        }

        self.send_chat_action(
            action='typing',
            chat_id=data['chat_id']
        )

        return self.telegram_action('sendMessage', data=data)

    def forward_message(self,
                       chat_id,
                       from_chat_id='',
                       disable_notification=False,
                       message_id=''):
        data = {
            'chat_id': chat_id,
            'from_chat_id': from_chat_id,
            'disable_notification': disable_notification,
            'message_id': message_id
        }

        self.send_chat_action(
            action='typing',
            chat_id=data['chat_id']
        )

        return self.telegram_action('forwardMessage', data=data)

    def send_voice(self,
                  voice,
                  chat_id,
                  caption='',
                  duration=0,
                  disable_notification=False,
                  reply_to_message_id=0,
                  reply_markup={}):
        data = {
            'chat_id': chat_id,
            'caption': caption,
            'duration': duration,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': reply_markup
        }

        files = {}

        if type(voice) == type(''):
            data['voice'] = voice
        else:
            files['voice'] = voice

        self.send_chat_action(
            action='record_audio',
            chat_id=data['chat_id']
        )

        return self.telegram_action('sendVoice', data=data, files=files)

    """
    Type of action to broadcast.
    Choose one, depending on what the user is about to receive:
    `typing` for text messages,
    `upload_photo` for photos,
    `record_video` or `upload_video` for videos,
    `record_audio` or `upload_audio` for audio files,
    `upload_document` for general files,
    `find_location` for location data,
    `record_video_note` or `upload_video_note` for video notes.
    """
    def send_chat_action(self, chat_id, action='typing'):
        data = {
            'action': action,
            'chat_id': chat_id
        }
        return self.telegram_action('sendChatAction', data=data)

    def get_file(self, file_id=''):
        data = {
            'file_id': file_id
        }
        return self.telegram_action('getFile', data=data)

    def return_file(self, file_id):
        request_file = self.get_file(file_id=file_id)
        filepath = request_file['result']['file_path']
        return self.telegram_return_file(filepath)

    def send_photo(self,
                  photo,
                  chat_id,
                  caption='',
                  disable_notification=False,
                  reply_to_message_id=0,
                  reply_markup={}):
        data = {
            'chat_id': chat_id,
            'photo': photo,
            'caption': caption,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': reply_markup
        }

        files = {}

        if type(photo) == type(''):
            data['photo'] = photo
        else:
            files['photo'] = photo

        self.send_chat_action(
            action='upload_photo',
            chat_id=data['chat_id']
        )

        return self.telegram_action('sendPhoto', data=data, files=files)

    def send_document(self,
                     document,
                     chat_id,
                     caption='',
                     disable_notification=False,
                     reply_to_message_id=0,
                     reply_markup={}):
        data = {
            'chat_id': chat_id,
            'document': document,
            'caption': caption,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': reply_markup
        }

        files = {}

        if type(document) == type(''):
            data['document'] = document
        else:
            files['document'] = document

        self.send_chat_action(
            action='upload_document',
            chat_id=data['chat_id']
        )

        return self.telegram_action('sendDocument', data=data, files=files)

    def set_webhook(self, url):
        data = {
            'url': url,
            'certificate': None,
            'max_connections': 40,
            'allowed_updates': []
        }
        return self.telegram_action('setWebhook', data=data)

    def delete_webhook(self):
        return self.telegram_action('deleteWebhook')
