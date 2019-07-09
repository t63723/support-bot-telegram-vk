import os
import logging

import dialogflow
from google.api_core.exceptions import InvalidArgument

from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

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


def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Здравствуйте!')


def answer(bot, update):
    telegram_id = update.update_id
    dialogflow_client = dialogflow.SessionsClient()
    dialogflow__session = dialogflow_client.session_path(DIALOGFLOW_PROJECT_ID, telegram_id)

    text_to_be_analyzed = update.message.text
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)

    query_input = dialogflow.types.QueryInput(text=text_input)

    try:
        response = dialogflow_client.detect_intent(session=dialogflow__session, query_input=query_input)
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

    TOKEN = os.getenv("TELEGRAM_TOKEN")
    updater = Updater(TOKEN)

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
