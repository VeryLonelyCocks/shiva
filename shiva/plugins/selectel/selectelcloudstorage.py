import random
import string

from .sdk.sdk.cloudstorage import CloudStorage


class SelectelCloudStorage:

    def __init__(self, db):
        self.db = db
        self.authorized = False
        self.link_key = None


    def storage_auth(self, chat_id, user=None, password=None):

        table = self.db['cloudstorage_tokens']

        saved_user = table.find_one({'chat_id': chat_id})

        if saved_user and user is None and password is None:
            self.sdk = CloudStorage(saved_user['token'])
            self.sdk.set_storage_url(saved_user['storage_url'])
            self.authorized = True
            return

        self.sdk = CloudStorage(user, password)
        self.authorized = True

        table.insert_one({
            'user': user,
            'chat_id': chat_id,
            'token': self.sdk.auth_token,
            'storage_url': self.sdk.storage_url
        })

    def create_container(self, name, type='private'):

        if not self.authorized:
            return False

        self.sdk.new_container(name, type)

    def get_containers_list(self):

        if not self.authorized:
            return []

        return self.sdk.containers_list()

    def get_files_list(self, container, limit=None, marker=None, format='json'):

        if not self.authorized:
            return []

        return self.sdk.get_files(container, limit=limit, marker=marker, format=format)

    def upload_file(self, container, file_name, file, file_type, file_size):

        if not self.authorized:
            return

        return self.sdk.upload(container, file_name, file, file_type, file_size)

    def download_file(self, container, file_name):

        if not self.authorized:
            return

        return self.sdk.download(container, file_name)

    def delete_file(self, container, file_name):

        if not self.authorized:
            return

        self.sdk.delete(container, file_name)

    def set_link_key(self, chat_id, key):

        response = self.sdk.set_link_key(key)

        if response.status_code == 403:
            return False

        self.link_key = key
        collection = self.db['cloudstorage_link_keys']
        collection.insert_one({'chat_id': chat_id, 'key': key})

        return True


    def get_file_link(self, chat_id, container, file):
        sig = self.link_key

        if not hasattr(self, 'link_key') or not self.link_key:
            collection = self.db['cloudstorage_link_keys']
            saved = collection.find_one({'chat_id': chat_id})

            from time import time  # данные для генерации ссылки
            expires = int(time()) + 60 * 60 * 24  # срок действия ссылки (60 секунд)
            path = "/{}/{}".format(container, file)  # полный путь к файлу в хранилище

            if not saved:

                import hmac
                from hashlib import sha1
                method = "GET"

                s = string.ascii_lowercase + string.digits
                link_secret_key = ''.join(random.sample(s, 10))
                hmac_body = '%s\n%s\n%s' % (method, expires, path)

                a = bytearray()
                a.extend(map(ord, link_secret_key))

                b = bytearray()
                b.extend(map(ord, hmac_body))

                sig = hmac.new(a, b, sha1).hexdigest()  # ключ доступа

                if not self.set_link_key(chat_id, link_secret_key):
                    return False

            else:
                sig = saved['key']

        link = self.sdk.storage_url + path \
               + '?temp_url_sig=' + sig \
               + '&temp_url_expires=' + str(expires)

        return link
