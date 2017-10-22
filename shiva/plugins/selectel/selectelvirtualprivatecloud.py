from .sdk.sdk.virtualprivatecloud import VirtualPrivateCloud


class SelectelVirtualPrivateCloud:

    def __init__(self, db):
        self._db = db

    def vpc_auth(self, chat_id, token):

        table = self._db['virtualprivatecloud_tokens']

        self._sdk = VirtualPrivateCloud(token)

        table.insert_one({
            'chat_id': chat_id,
            'token': token
        })

    def auth_by_chat_id(self, chat_id):

        if hasattr(self, '_sdk'):
            return

        table = self._db['virtualprivatecloud_tokens']

        saved_user = table.find_one({'chat_id': chat_id})

        if saved_user:
            self._sdk = VirtualPrivateCloud(saved_user['token'])

    def get_list_projects(self):

        if not hasattr(self, '_sdk'):
            return

        return self._sdk.get_list_projects()

    def get_configuration_about_project(self, project_id):

        if not hasattr(self, '_sdk'):
            return

        return self._sdk.get_configuration_about_project(project_id)

    def get_quotas(self):

        if not hasattr(self, '_sdk'):
            return

        return self._sdk.get_quotas()

    def get_free_quotas(self):

        if not hasattr(self, '_sdk'):
            return

        return self._sdk.get_free_quotas()

    def get_quotas_for_all_projects(self):

        if not hasattr(self, '_sdk'):
            return

        return self._sdk.get_quotas_for_all_projects()

    def get_quotas_for_project(self, project_id):

        if not hasattr(self, '_sdk'):
            return

        return self._sdk.get_quotas_for_project(project_id)

    def get_traffic(self):

        if not hasattr(self, '_sdk'):
            return

        return self._sdk.get_traffic()

    def get_users(self):

        if not hasattr(self, '_sdk'):
            return

        return self._sdk.get_users()