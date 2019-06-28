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

monitoring_chat_id = os.getenv('monitoring_chat_id')
monitoring_token = os.getenv('monitoring_token')
monitoring_bot = Bot(token=monitoring_token)


class LoggerForTelegram(logging.Handler):

    def emit(self, record):
        log_entry = self.format(record)
        monitoring_bot.send_message(chat_id=monitoring_chat_id, text=log_entry)


logger = logging.getLogger("logger for telegram")
logger.setLevel(logging.DEBUG)
logger.addHandler(LoggerForTelegram())

DIALOGFLOW_PROJECT_ID = os.getenv('project_id')
DIALOGFLOW_LANGUAGE_CODE = 'ru-RU'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv('ga-key-client')


def echo(event, vk_api):
    session_id = event.user_id
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, session_id)

    text_to_be_analyzed = event.text
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)

    query_input = dialogflow.types.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument as err:
        logger.critical(err)
        raise

    if response.query_result.intent.display_name != 'Default Fallback Intent':
        vk_api.messages.send(
            user_id=event.user_id,
            message=response.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":

    vk_token = os.getenv("vk")
    vk_session = VkApi(token=vk_token)
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)
