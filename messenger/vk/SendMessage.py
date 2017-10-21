from messenger.vk.VKAPIRequest import VKRequest


class VKBot:
    def __init__(self, user_id):
        self.user_id = user_id

    def send_text(self, text):
        url = VKRequest.get_request_url(method='messages.send', message=text, user_id=self.user_id)
        VKRequest.get_request(url)

        return 'ok'

    def send_photo(self, file_name, message=''):
        photo = VKRequest.get_upload_photos(user_id=self.user_id, file_name=file_name)
        attachment = 'photo{owner_id}_{picture_id}'.format(owner_id=photo['owner_id'], picture_id=photo['id'])

        url = VKRequest.get_request_url('messages.send', user_id=self.user_id, message=message, attachment=attachment)

        VKRequest.get_request(url)

        return 'ok'
