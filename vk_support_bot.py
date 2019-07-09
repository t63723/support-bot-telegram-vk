import os
import random
import logging

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType

from telegram import Bot

import dialogflow
from google.api_core.exceptions import InvalidArgument

from dotenv import load_dotenv

load_dotenv()

MONITORING_CHAT_ID = os.getenv('MONITORING_CHAT_ID')
MONITORING_TOKEN = os.getenv('MONITORING_TOKEN')
MONITORING_BOT = Bot(token=MONITORING_TOKEN)


class LoggerForTelegram(logging.Handler):

    def emit(self, record):
        log_entry = self.format(record)
        MONITORING_BOT.send_message(chat_id=MONITORING_CHAT_ID, text=log_entry)


logger = logging.getLogger("logger for telegram")
logger.setLevel(logging.DEBUG)
logger.addHandler(LoggerForTelegram())

DIALOGFLOW_PROJECT_ID = os.getenv('PROJECT_ID')
DIALOGFLOW_LANGUAGE_CODE = 'ru-RU'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv('GA-KEY-CLIENT')


def answer(event, vk_api):
    vk_user_id = event.user_id
    dialogflow_client = dialogflow.SessionsClient()
    dialogflow_session = dialogflow_client.session_path(DIALOGFLOW_PROJECT_ID, vk_user_id)

    text_to_be_analyzed = event.text
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)

    query_input = dialogflow.types.QueryInput(text=text_input)

    try:
        response = dialogflow_client.detect_intent(session=dialogflow_session, query_input=query_input)
    except InvalidArgument as err:
        logger.critical(err)
        raise

    if response.query_result.action != 'input.unknown':
        vk_api.messages.send(
            user_id=event.user_id,
            message=response.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":

    VK_TOKEN = os.getenv("VK")
    vk_session = VkApi(token=VK_TOKEN)
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer(event, vk_api)
