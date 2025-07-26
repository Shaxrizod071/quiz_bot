from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    CallbackQueryHandler,
)
from dotenv import load_dotenv
import os
from tinydb import TinyDB, Query

load_dotenv()

db = TinyDB("database.json")


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to the Quiz Bot! Use /quiz to start a quiz.")


def quiz(update: Update, context: CallbackContext) -> None:
    """Shows list of available quizzes."""
    lst = ["Quiz 1", "Quiz 2", "Quiz 3"]  # This should be fetched from the database
    key_list = []
    for i in lst:
        keyboard = InlineKeyboardButton(i, callback_data=i)
        key_list.append([keyboard])

    quiz_keyboard = InlineKeyboardMarkup(key_list)
    update.message.reply_text("Choose a quiz to start:", reply_markup=quiz_keyboard)


data = [
    {
        "quiz_name": "Quiz 1",
        "questions": [
            {
                "question": "What is the capital of France?",
                "A": "Paris",
                "B": "London",
                "C": "Berlin",
                "D": "Madrid",
                "correct_answer": "A",
            },
            {
                "question": "What is 2 + 2?",
                "A": "3",
                "B": "4",
                "C": "5",
                "D": "6",
                "correct_answer": "B",
            },
        ],
    }
]

index = 0  # Global index to track the current question


def handle_quiz_selection(update: Update, context: CallbackContext) -> None:
    """
    Handle the user's selection of a quiz.
    This function will fetch the quiz from the database and start the quiz.
    """
    global index
    index = 0  # Reset index for new quiz

    update.callback_query.answer()
    query = update.callback_query
    quiz_name = query.data

    variant = {}

    for quiz in data:
        if quiz["quiz_name"] == quiz_name:
            variant = quiz
            break

    # Fetch the quiz from the database
    text = f"""You have selected: {quiz_name}. Let's start the quiz!
question: {variant['questions'][index]['question']}
A: {variant['questions'][index]['A']}
B: {variant['questions'][index]['B']}
C: {variant['questions'][index]['C']}
D: {variant['questions'][index]['D']}
Please answer with A, B, C, or D.
"""
    inline_keyboard = InlineKeyboardButton("A", callback_data="A")
    inline_keyboard2 = InlineKeyboardButton("B", callback_data="B")
    inline_keyboard3 = InlineKeyboardButton("C", callback_data="C")
    inline_keyboard4 = InlineKeyboardButton("D", callback_data="D")
    keyboard = InlineKeyboardMarkup(
        [[inline_keyboard, inline_keyboard2, inline_keyboard3, inline_keyboard4]]
    )
    query.edit_message_text(text=text, reply_markup=keyboard)


def answer(update: Update, context: CallbackContext) -> None:
    """
    Handle user answers to quiz questions(a,b,c,d).
    This function will check the user's answer against the correct answer
    and gives next question or end the quiz.
    """
    print("answer")


def main() -> None:
    token = os.getenv("TOKEN")
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN not found in environment variables.")
        return

    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("quiz", quiz))
    dispatcher.add_handler(CallbackQueryHandler(handle_quiz_selection, pattern="Quiz"))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
