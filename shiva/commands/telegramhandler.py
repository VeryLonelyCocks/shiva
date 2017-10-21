from .telegram import Selectel


class TelegramCommands:

    def __init__(self, core):
        self.core = core
        self.commands = {}
        self.load_pluigns()

    def load_pluigns(self):
        self.selectel = Selectel(self.core)

        for command,callback in self.selectel.commands.items():
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


        if callback_query:
            data = callback_query.get('data')
            cmd, other_data = data.split('|', 1)

            if cmd in self.selectel.commands:
                self.selectel.process_callback_query(cmd, callback_query)