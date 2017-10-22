import io
import os


class Selectel:

    def __init__(self, core):
        self.core = core
        self.telegram = core.telegram.BOT

        self.commands = {
            'auth': self.storage_auth,
            'containers': self.send_container_list,
            'select_container': self.select_container,
            'upload_file': self.upload_file,
            'select_file': self.select_file,
            'download_file': self.download_file,
            'delete_file': self.delete_file,
            'file_link': self.file_link,
            'files': self.get_files,
            'new_container': self.create_container,
            'del_container': self.del_container,
            'cloudstorage': self.send_container_list
        }

    def storage_auth(self, message):
        text = message.get('text')
        chat = message.get('chat')

        try:
            cmd, user, password = text.split(' ', 2)
        except:
            self.telegram.send_message('Введите логин и пароль в формате /auth {login} {pass}', chat_id=chat['id'])
            return

        self.sdk.storage_auth(chat['id'], user, password)

        self.send_container_list(message)

    def send_container_list(self, message):

        chat = message.get('chat')

        containers = self.sdk.get_containers_list()

        if len(containers) == 0:
            self.telegram.send_message('Доступных контейнеров нет', chat_id=chat['id'])
            return

        buttons = []

        for container in containers:
            name = container.get('name')

            row = [{
                'text': name,
                'callback_data': '{}|{}'.format('select_container', name)
            }]
            buttons.append(row)

        message = 'Выбирете контейнер, с которым хотите работать:'

        self.telegram.send_message(message, chat_id=chat['id'], reply_markup={'inline_keyboard': buttons})

    def select_container(self, callback_query):
        data = callback_query.get('data')
        message = callback_query.get('message')
        chat = message.get('chat')

        cmd, container = data.split('|', 1)

        self.core.states.push(chat['id'], {'type': 'container', 'container': container})
        self.get_files(message)

    def upload_file(self, message):
        document = message['document']
        chat = message['chat']

        file = self.telegram.telegram_return_file(document['file_id'])

        state = self.core.states.get(chat['id'])

        container = state.get('container')
        name = document.get('file_name')

        code = self.sdk.upload_file(container, name, file, document.get('mime_type'), document.get('file_size'))

        if 199 < code < 300:
            message = 'Файл успешно загружен'
        else:
            message = 'Ошибка при загрузке файла'

        self.telegram.send_message(message, chat['id'])

    def select_file(self, callback_query):
        data = callback_query.get('data')
        chat = callback_query['message']['chat']

        cmd, container, file = data.split('|', 2)

        buttons = [[{
            'text': 'Скачать',
            'callback_data': 'download_file|{}|{}'.format(container, file)
        }],
        [{
            'text': 'Ссылка',
            'callback_data': 'file_link|{}|{}'.format(container, file)
        }],
        [{
            'text': 'Удалить',
            'callback_data': 'delete_file|{}|{}'.format(container, file)
        }]]

        self.telegram.send_message(file, chat_id=chat['id'], reply_markup={'inline_keyboard': buttons})

    def download_file(self, callback_query):
        data = callback_query.get('data')
        chat = callback_query['message']['chat']

        cmd, container, file = data.split('|', 2)

        buffer = self.sdk.download_file(container, file)

        response = self.telegram.send_document(buffer.getvalue(), chat['id'])

        if hasattr(response, 'states_code') and response.status_code == 413:
            self.telegram.send_message('Файл слишком большой, воспользуйтесь ссылкой', chat_id=chat['id'])

    def delete_file(self, callback_query):
        data = callback_query.get('data')
        chat = callback_query['message']['chat']

        cmd, container, file = data.split('|', 2)

        self.sdk.delete_file(container, file)
        self.telegram.send_message('Файл удален', chat_id=chat['id'])

    def file_link(self, callback_query):
        data = callback_query.get('data')
        chat = callback_query['message']['chat']

        cmd, container, file = data.split('|', 2)

        link = self.sdk.get_file_link(chat['id'], container, file)

        share_button = [[{
            'text': '',
            'url': 'https://t.me/share/url?url={}'.format(link)
        }]]

        if link:
            self.telegram.send_message(link, chat_id=chat['id'], reply_markup={'inline_keyboard': share_button})
        else:
            self.telegram.send_message('К сожалению, у вас нет доступа к созданию ссылок для данного хранилища', chat_id=chat['id'])

    def get_files(self, message):

        chat = message.get('chat')

        state = self.core.states.get(chat['id']) or {}
        container = state.get('container')

        if not container:
            self.telegram.send_message('Пожалуйста, выберите контейнер. \n'
                                       'Список доступных контейнеров — /containers')
            return

        files = self.sdk.get_files_list(container)
        buttons = []

        message = 'Для загрузки файла, прикрепите его в сообщении.'

        if len(files) is not 0:
            message += ' Для скачивания файла, выберите его из списка:'

            for file in files:
                name = file.get('name')

                row = [{
                    'text': name,
                    'callback_data': '{}|{}|{}'.format('select_file', container, name)
                }]
                buttons.append(row)

        print(self.telegram.send_message(message, chat_id=chat['id'], reply_markup={'inline_keyboard': buttons}))

    def create_container(self, message):
        text = message.get('text')
        chat = message.get('chat')

        try:
            cmd, container = text.split(' ', 1)
        except:
            self.telegram.send_message('Введите команду в формате /new_container {name}', chat_id=chat['id'])
            return

        self.sdk.create_container(container)

        self.telegram.send_message('Контейнер создан', chat_id=chat['id'])

    def del_container(self, message):
        text = message.get('text')
        chat = message.get('chat')

        try:
            cmd, container = text.split(' ', 1)
        except:
            self.telegram.send_message('Введите команду в формате /del_container {name}', chat_id=chat['id'])
            return

        self.sdk.delete_container(container)

        self.telegram.send_message('Контейнер удален', chat_id=chat['id'])

    def auth(self, chat_id):
        if not self.sdk.authorized:
            self.sdk.storage_auth(chat_id)

        if not self.sdk.authorized:
            return False

        return True

    def request_auth(self, chat_id):
        self.telegram.send_message('Пожалуйста, авторизуйтесь c помощью команы /auth', chat_id=chat_id)

    def process_command(self, cmd, message):

        self.sdk = self.core.selectel(self.core.db)

        document = message.get('document')
        chat = message.get('chat')

        if not self.auth(chat['id']) and cmd != 'auth':
            self.request_auth(chat['id'])
            return

        state = self.core.states.get(chat['id'])

        if document and state.get('type') == 'container':
            self.commands['upload_file'](message)
        else:
            self.commands[cmd](message)

    def process_callback_query(self, cmd, callback_query):

        self.sdk = self.core.selectel(self.core.db)

        chat = callback_query['message'].get('chat')

        if not self.auth(chat['id']):
            self.request_auth(chat['id'])
            return

        self.commands[cmd](callback_query)
