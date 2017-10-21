import requests
from messenger.vk.config import access_token


def vk_requests_url(method, **kwargs):
    attacments = ''

    for arg in kwargs:
        attacments += arg+'='+str(kwargs[arg])+"&"

    attacments = attacments[0:-1]
    url = """https://api.vk.com/method/{method}?{attacments}&access_token={access_token}&v=5.53\
    """.replace(" ", "").format(method=method, attacments=attacments, access_token=access_token)

    return url


def vk_api_upload_server_response(user_id):
    url = vk_requests_url('photos.getMessagesUploadServer', peer_id=user_id)

    q = requests.get(url)

    return q.json()['response']['upload_url']


def vk_api_upload_photo(url, file_name):
    files = {'file': open(file_name, 'rb')}

    q = requests.post(url, files=files)

    return q.json()


def vk_api_save_photo(server, photo, hash):
    url = vk_requests_url('photos.saveMessagesPhoto', server=server, photo=photo, hash=hash)

    q = requests.get(url)

    return q.json()


def vk_upload_photos(user_id, file_name):
    server_response = vk_api_upload_server_response(user_id)
    upload_response = vk_api_upload_photo(server_response, file_name)

    photo = upload_response['photo']
    server = upload_response['server']
    hash = upload_response['hash']

    photo = vk_api_save_photo(server, photo, hash)['response'][-1]

    return photo
