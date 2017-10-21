from .sdk.sdk.cloudstorage import CloudStorage

class SelectelCloudStorage:

    def __init__(self, db):
        self.db = db
        self.authorized = False

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
