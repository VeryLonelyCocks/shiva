class Notifier:

    def __init__(self, core):
        self.core = core
        self.telegram = core.telegram.BOT
        self.sdk = core.notifier

        self.commands = {
            'notifier': self.notifier_start
        }

    def notifier_start(self, message):
        chat = message.get('chat')

        response = self.sdk.process_start(chat['id'], 'telegram')

        if response:
            self.telegram.send_message(
                text=response,
                chat_id=chat['id']
            )

        return {'text': 'ok'}