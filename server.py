from telegram_bot_helper.api import TelegramAPIHelper
from telegram_bot_helper.message_processor import MessageProcessor

from time import sleep


class VacasBotServer():
    JOBS_FILE = 'jobs.json'

    TOKEN = ""
    BOT_ID = ""
    BOT_NAME = ""

    SLEEP_TIME = 5

    last_message_timestamp = {}

    def run(self):
        self.telegram = TelegramAPIHelper(self.TOKEN, self.BOT_NAME)
        self.message_processor = MessageProcessor(self.JOBS_FILE)
        self._discard_previous_unattended_messages()
        while True:
            self.telegram.update_offset()
            for message in self.telegram.get_new_messages():
                self._process_message(message)

            sleep(self.SLEEP_TIME)

    def _discard_previous_unattended_messages(self):
        self.telegram.get_new_messages()
        self.telegram.update_offset()

    def _process_message(self, message):
        answer = self.message_processor.get_answer(message)
        if answer:
            self.telegram.send_message(message.chat_id, answer)
