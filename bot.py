import telebot
from telebot import types
from config import BOT_TOKEN
from main import Trivia
from html import unescape

trivia = Trivia()
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    start = types.InlineKeyboardButton("Start 🤔❔", callback_data="start_game")
    markup.add(start)

    bot.reply_to(message, "Welcome to TriviaBot! Test your knowledge and have fun with exciting trivia challenges. Let the games begin! Press start to dive in!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "start_game")
def start_game(callback):
    chat_id = callback.message.chat.id

    questions, all_options, correct_option = trivia.get_questions()
    
    button_1_disp = all_options[0] 
    button_2_disp = all_options[1]
    button_3_disp = all_options[2]
    button_4_disp = all_options[3]
    
    buttons = [button_1_disp, button_2_disp, button_3_disp, button_4_disp]
    
    global correct_button
    
    for i in range(len(buttons)):
        if buttons[i] == correct_option[0]:
            correct_button = str(i + 1)

    button_1 = types.InlineKeyboardButton(button_1_disp, callback_data="button_1")
    button_2 = types.InlineKeyboardButton(button_2_disp, callback_data="button_2")
    button_3 = types.InlineKeyboardButton(button_3_disp, callback_data="button_3")
    button_4 = types.InlineKeyboardButton(button_4_disp, callback_data="button_4")
    
    answer_buttons = types.InlineKeyboardMarkup(row_width=2)
    answer_buttons.add(button_1, button_2, button_3, button_4)
    
    questions[0] = unescape(questions[0])
    bot.send_message(chat_id, questions[0], reply_markup=answer_buttons)


@bot.callback_query_handler(func=lambda call: call.data.startswith("button_"))
def handle_button_click(callback):
    again = types.InlineKeyboardButton("Another one❔", callback_data="start_game")
    
    answer_buttons = types.InlineKeyboardMarkup(row_width=1)
    answer_buttons.add(again)
    
    global score
    selected_option = callback.data[7:]

    if selected_option == correct_button:
        bot.send_message(callback.message.chat.id, "Correct! 🎉", reply_markup=answer_buttons)
    else:
        bot.send_message(callback.message.chat.id, "Incorrect! 😔", reply_markup=answer_buttons)


while True:
    try:
        bot.polling()
    except: 
        pass