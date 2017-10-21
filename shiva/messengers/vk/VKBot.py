from .VKAPIRequest import VKRequest
from .config import config


class VKBot:
    def __init__(self):
        self._token = config['vk_token']

    @staticmethod
    def get_web_hook():
        return config['vk_webhook']

    def send_text(self, user_id, text):
        url = VKRequest.get_request_url(method='messages.send', token=self._token, message=text, user_id=user_id)
        VKRequest.get_request(url)

    def send_photo(self, user_id, file_name, message=''):
        photo = VKRequest.get_upload_photos(user_id=user_id, file_name=file_name, token=self._token)
        attachment = 'photo{owner_id}_{picture_id}'.format(owner_id=photo['owner_id'], picture_id=photo['id'])

        url = VKRequest.get_request_url('messages.send', user_id=user_id, token=self._token,
                                        message=message, attachment=attachment)

        VKRequest.get_request(url)
