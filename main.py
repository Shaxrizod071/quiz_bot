from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
import os
from tinydb import TinyDB, Query

load_dotenv()

db = TinyDB('db.json')

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to the Quiz Bot! Use /quiz to start a quiz.')

def quiz(update: Update, context: CallbackContext) -> None:
    """Shows list of available quizzes."""
    pass

def handle_quiz_selection(update: Update, context: CallbackContext) -> None:
    """
    Handle the user's selection of a quiz.
    This function will fetch the quiz from the database and start the quiz.
    """
    pass

def answer(update: Update, context: CallbackContext) -> None:
    """
    Handle user answers to quiz questions(a,b,c,d).
    This function will check the user's answer against the correct answer
    and gives next question or end the quiz.
    """
    pass

def main() -> None:
    token = os.getenv('TOKEN')
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN not found in environment variables.")
        return
    
    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("quiz", quiz))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    