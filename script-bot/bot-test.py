import logging
from telegram.ext import Updater
from messages import START_TEXT, REGISTRATION_TEXT
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

new_user = {}



def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=START_TEXT)
    new_user['chat_id'] = update.message.chat_id
    return 1


def ask_name(bot, update):
    new_user['name'] = update.message
    bot.send_message(chat_id=update.message.chat_id, text=REGISTRATION_TEXT)
    # Todo: send new_user to django url for create new user
    return -1


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("KEY")
    # Get the dispatcher to register handlers
    flag = 0
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, ask_name))

    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

#TODO falta hacer que el bot no vuelva a responder despues  que se le manda el nombre
if __name__ == '__main__':
    main()