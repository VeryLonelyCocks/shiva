import uuid


class Notifier():

    def __init__(self, server, db):
        self.server = server
        self.table = self.db['notify_chats']

    def set_routes(self):
        chats = self.get_all_chats()
        for chat in chats:
            self.server.hooks.add(telegram.URI, tg_callback)

    def get_all_chats(self):
        return table.find()

    def get_chat_uri(self, key):
        return '/notify/{}'.format(key)


    def generate_id(self):
        return uuid.uuid4().hex[:8]

    def get_chat_by_key(self, key):
        chat = table.find_one({'key': key})
        if chat:
            return chat['key']
        return None

    def save_chat_to_db(self, chat_id):
        key = self.generate_id()

        chat_model = {
            'chat_id': chat_id,
            'key': key
        }

        return self.table.insert_one(chat_model)
