import requests
import json
import uuid


class Telegram():

    def __init__(self, token):
        self.TOKEN = token
        self.BOT = API(self.TOKEN)

    def createWebhook(self, host):
        self.HOST = host
        self.URI = '/%s' % uuid.uuid4().hex
        self.WEBHOOK = 'https://{}{}'.format(self.HOST, self.URI)
        return self.BOT.setWebhook(self.WEBHOOK)

"""
https://core.telegram.org/bots/api#available-methods
"""
class API:

    def __init__(self, token):
        self.TOKEN = token

    def telegramAction(self, action, data={}, files={}):
        botURL = 'https://api.telegram.org/bot' + self.TOKEN + '/' + action
        result = requests.post(botURL, data=data, files=files)
        response = result.content.decode("utf-8")
        return json.loads(response)

    def telegramReturnFile(self, file_path):
        fileURL = 'https://api.telegram.org/file/bot' + self.TOKEN + '/' + file_path
        result = requests.get(fileURL)
        response = result.content
        return response


    def getUpdates(self, data={'limit': 100}):
        return self.telegramAction('getUpdates', data=data)

    ## send message
    def sendMessage(self,
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

        self.sendChatAction(
            action='typing',
            chat_id=data['chat_id']
            )

        return self.telegramAction('sendMessage', data=data)

    ## send message
    def forwardMessage(self,
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

        self.sendChatAction(
            action='typing',
            chat_id=data['chat_id']
            )

        return self.telegramAction('forwardMessage', data=data)

    def sendVoice(self,
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

        self.sendChatAction(
            action='record_audio',
            chat_id=data['chat_id']
            )

        return self.telegramAction('sendVoice', data=data, files=files)

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
    def sendChatAction(self, chat_id, action='typing'):
        data = {
            'action': action,
            'chat_id': chat_id
        }
        return self.telegramAction('sendChatAction', data=data)

    def getFile(self, file_id=''):
        data = {
            'file_id': file_id
        }
        return self.telegramAction('getFile', data=data)

    def returnFile(self, file_id):
        request_file = self.getFile(file_id=file_id)
        filepath = request_file['result']['file_path']
        return self.telegramReturnFile(filepath)

    def sendPhoto(self,
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

        self.sendChatAction(
            action='upload_photo',
            chat_id=data['chat_id']
            )

        return self.telegramAction('sendPhoto', data=data, files=files)

    def sendDocument(self,
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

        self.sendChatAction(
            action='upload_document',
            chat_id=data['chat_id']
            )

        return self.telegramAction('sendDocument', data=data, files=files)


    def setWebhook(self, url):
        data = {
            'url': url,
            'certificate': None,
            'max_connections': 40,
            'allowed_updates': []
        }
        return self.telegramAction('setWebhook', data=data)

    def deleteWebhook(self):
        return self.telegramAction('deleteWebhook')
