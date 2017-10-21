import requests


class VKRequest:

    @staticmethod
    def get_request_url(method, token, **kwargs):
        attacments = ''

        for arg in kwargs:
            attacments += arg+'='+str(kwargs[arg])+"&"

        attacments = attacments[0:-1]
        url = """https://api.vk.com/method/{method}?{attacments}&access_token={access_token}&v=5.53\
        """.replace(" ", "").format(method=method, attacments=attacments, access_token=token)

        return url

    @staticmethod
    def get_request(url):
        q = requests.get(url)

        return q.json()

    @staticmethod
    def post_request(url, files=None):
        if files is None:
            q = requests.post(url)
        else:
            q = requests.post(url, files=files)

        return q.json()

    @staticmethod
    def _api_upload_server_response(user_id, token):
        url = VKRequest.get_request_url('photos.getMessagesUploadServer', token=token, peer_id=user_id)

        q = VKRequest.get_request(url)

        return q['response']['upload_url']

    @staticmethod
    def _api_upload_photo(url, file_name):
        files = {'file': open(file_name, 'rb')}

        q = VKRequest.post_request(url, files=files)

        return q

    @staticmethod
    def _api_save_photo(server, photo, hash, token):
        url = VKRequest.get_request_url('photos.saveMessagesPhoto', token=token, server=server, photo=photo, hash=hash)

        q = VKRequest.get_request(url)

        return q

    @staticmethod
    def get_upload_photos(user_id, file_name, token):
        server_response = VKRequest._api_upload_server_response(user_id, token)
        upload_response = VKRequest._api_upload_photo(server_response, file_name)

        photo = upload_response['photo']
        server = upload_response['server']
        hash = upload_response['hash']

        photo = VKRequest._api_save_photo(server, photo, hash, token)['response'][-1]

        return photo
