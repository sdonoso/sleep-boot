import logging

import requests
from telegram import Update
from telegram.ext import CallbackContext, Updater
from telegram.ext import CommandHandler, ConversationHandler, Filters, MessageHandler

from scriptBot.botSettings import BACKEND_URL, KEY
from scriptBot.messages import ALREADY_REGISTERED_MSG, GENERAL_ERROR, NOT_REGISTERED_ANSWER, REGISTRATION_CANCEL_MSG, \
    REGISTRATION_SUCCESSFUL_MSG, START_MSG, OFF_CONTEXT_CANCEL

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    """ Manages the start command """
    # https://python-telegram-bot.readthedocs.io/en/stable/telegram.user.html
    user = update.effective_user
    result = 1
    response = requests.get(BACKEND_URL + "persons/" + str(user["id"]))
    if response.status_code == 200:
        result = -1
        username = response.json()["name"]
        message = ALREADY_REGISTERED_MSG.format(name=username)
        context.bot.send_message(chat_id=user['id'], text=message)
    elif response.status_code == 404:
        context.bot.send_message(chat_id=user['id'], text=START_MSG)
    else:
        result = -1
        context.bot.send_message(chat_id=user['id'], text=GENERAL_ERROR)
        response_error(response)
    return result


def cancel_register(update: Update, context: CallbackContext):
    """ Manages the cancel command, when sent inside a registration """
    user = update.effective_user
    result = -1
    context.bot.send_message(chat_id=user['id'], text=REGISTRATION_CANCEL_MSG)
    return result


def ask_name(update: Update, context: CallbackContext):
    """ Manages the registering of a new user after asking it's name """
    user = update.effective_user
    result = -1
    new_user = {
        'name': update.message.text,
        'id_telegram': user['id'],
    }
    response = requests.post(BACKEND_URL + "persons/", data=new_user)
    if response.status_code == 201:
        context.bot.send_message(chat_id=update.message.chat_id, text=REGISTRATION_SUCCESSFUL_MSG)
    else:
        result = 1
        context.bot.send_message(chat_id=user['id'], text=GENERAL_ERROR)
        response_error(response)
    return result


def cancel_out_of_context(update: Update, context: CallbackContext):
    """ Manages the cancel command, when out of context """
    user = update.effective_user
    context.bot.send_message(chat_id=user['id'], text=OFF_CONTEXT_CANCEL)


def unrecognized_answer(update: Update, context: CallbackContext):
    """ Manages unrecognized answers """
    user = update.effective_user
    context.bot.send_message(chat_id=user['id'], text=NOT_REGISTERED_ANSWER)


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def response_error(response):
    """Log Errors caused by unexpected responses from the backend REST API"""
    logger.warning(
        'Received unexpected server response with code "%s", response: "%s"',
        response.status_code,
        response
    )


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(KEY, use_context=True)
    # Get the dispatcher to register handlers
    flag = 0
    dp = updater.dispatcher

    # Handler for the start conversation
    # https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.conversationhandler.html
    start_handler = ConversationHandler(
        [CommandHandler('start', start), CommandHandler('register', start)],
        {1: [MessageHandler(Filters.text, ask_name)]},
        [CommandHandler('cancel', cancel_register), MessageHandler(Filters.all, unrecognized_answer)],
    )

    dp.add_handler(start_handler)

    # Handler for the /cancel command when out of context. This has to be after all the CommandHandlers of the bot
    dp.add_handler(CommandHandler('cancel', cancel_out_of_context))

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
