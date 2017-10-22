from .telegram import Selectel
from .telegram import Notifier
from .telegram import Main

class TelegramCommands:

    def __init__(self, core):
        self.core = core
        self.commands = {}

        self.load_plugins()

    def load_plugins(self):
        self.selectel = Selectel(self.core)
        for command,callback in self.selectel.commands.items():
            self.commands[command] = callback

        self.notifier = Notifier(self.core)
        for command,callback in self.notifier.commands.items():
            self.commands[command] = callback

        self.main = Main(self.core)
        for command,callback in self.main.commands.items():
            self.commands[command] = callback

    async def telegram_callback(self, request):

        event = await request.json()
        print(event)

        message = event.get('message')
        callback_query = event.get('callback_query')

        if message:
            text = message.get('text')
            entities = message.get('entities')

            if entities and entities[0]['type'] == 'bot_command' and entities[0]['offset'] == 0:
                command = text[1:entities[0]['length']]

                if command in self.selectel.commands:
                    self.selectel.process_command(command, message)

                if command in self.notifier.commands:
                    self.commands[command](message)

                if command in self.main.commands:
                    self.commands[command](message)

        if callback_query:
            data = callback_query.get('data')
            cmd, other_data = data.split('|', 1)

            if cmd in self.selectel.commands:
                self.selectel.process_callback_query(cmd, callback_query)
