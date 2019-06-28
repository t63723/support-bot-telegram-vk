import os
import logging

import dialogflow
from google.api_core.exceptions import InvalidArgument

from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

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


def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Здравствуйте!')


def answer(bot, update):
    session_id = update.update_id
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, session_id)

    text_to_be_analyzed = update.message.text
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)

    query_input = dialogflow.types.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument as err:
        logger.critical(err)
        raise

    update.message.reply_text(response.query_result.fulfillment_text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""

    logger.info('bot started')

    token = os.getenv("telegram_token")
    updater = Updater(token)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, answer))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
