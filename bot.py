import telebot
import config 
from telebot import types
bot = telebot.TeleBot(config.TOKEN)

user_data = {}
class User:
    def __init__(self, first_name):
        self.first_name = first_name 
        self.last_name = ''
@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
 
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    item1 = types.KeyboardButton("Реклама")
    item2 = types.KeyboardButton("Додати рекламодавця")
    item3 = types.KeyboardButton("Додати клієнта")
    item4 = types.KeyboardButton("Додати товар до клієнта")
    item5 = types.KeyboardButton("Статистика")
    markup.add(item1, item2, item3, item4, item5)

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == 'Реклама':
                markup = types.InlineKeyboardMarkup(row_width=2)
                button1 = types.InlineKeyboardButton("Реклама спрацювала", callback_data='Yes')
                button2 = types.InlineKeyboardButton("Реклама не спрацювала", callback_data='No') 
                markup.add(button1, button2)
                bot.send_message(message.chat.id, 'Чи спрацювала реклама?', reply_markup=markup)        
        elif message.text == 'Додати рекламодавця':
            def ttt(message):
                msg1 = bot.send_message(message.chat.id,"Введіть прізвище рекламодавця: ")
                bot.register_next_step_handler(msg1, process_firstname_step_rekl)                                                                                                  
            def process_firstname_step_rekl(message):  
                user_id = message.from_user.id
                user_data[user_id] = User(message.text)
                msg1 = bot.send_message(message.chat.id,"Введіть ім'я рекламодавця: ")
                bot.register_next_step_handler(msg1, process_lastname_step_rekl) 

            def process_lastname_step_rekl(message):
                    user_id = message.from_user.id
                    user = user_data[user_id]
                    user.last_name = message.text
                    bot.send_message(message.chat.id, "Ви успішно зареєстрували рекламодавця")                     

            ttt(message)

        elif message.text == 'Додати клієнта':      
            def rrr(message):
                msg2 = bot.send_message(message.chat.id,"Введіть прізвище клієнта: ")
                bot.register_next_step_handler(msg2, process_firstname_step_client)
            def process_firstname_step_client(message):  
                user_id = message.from_user.id
                user_data[user_id] = User(message.text)

                msg2 = bot.send_message(message.chat.id,"Введіть ім'я клієнта: ")
                bot.register_next_step_handler(msg2, process_lastname_step_client)   
            def process_lastname_step_client(message): 
                    user_id = message.from_user.id
                    user = user_data[user_id]
                    user.last_name = message.text
                    bot.send_message(message.chat.id, "Ви успішно зареєстрували клієнта")
            rrr(message)
        elif message.text == 'Додати товар до клієнта':                                 
            def lll(message):
                msg3 = bot.send_message(message.chat.id,"Введіть прізвище клієнта: ")
                bot.register_next_step_handler(msg3, process_firstname_step_client)                                
            def process_firstname_step_client(message):  
                user_id = message.from_user.id
                user_data[user_id] = User(message.text)

                msg3 = bot.send_message(message.chat.id,"Введіть ім'я клієнта: ")
                bot.register_next_step_handler(msg3, process_lastname_step_client)   
            def process_lastname_step_client(message): 
                user_id = message.from_user.id
                user = user_data[user_id]
                user.last_name = message.text

                markup = types.InlineKeyboardMarkup(row_width=2)
                lutton1 = types.InlineKeyboardButton("Перший", callback_data='first')
                lutton2 = types.InlineKeyboardButton("Другий", callback_data='second') 
                lutton3 = types.InlineKeyboardButton("Третій", callback_data='third')
                lutton4 = types.InlineKeyboardButton("Четвертий", callback_data='fourth')
                markup.add(lutton1, lutton2, lutton3, lutton4)
                bot.send_message(message.chat.id, 'Який товар купив клієнт?', reply_markup=markup)
            lll(message)
        else:
            bot.send_message(message.chat.id, 'Я не знаю що відповісти😢')
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'first':
                bot.send_message(call.message.chat.id, 'Товар додано до клієнта😊')
            elif call.data == 'second':
                bot.send_message(call.message.chat.id, 'Товар додано до клієнта😊')
            elif call.data == 'third':
                bot.send_message(call.message.chat.id, 'Товар додано до клієнта😊')
            elif call.data == 'fourth':
                bot.send_message(call.message.chat.id, 'Товар додано до клієнта😊')
 
            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Який товар купив клієнт?",
                reply_markup=None)

    except Exception as e:
        print(repr(e)) 
    try:
        if call.message:
            if call.data == 'Yes':
                bot.send_message(call.message.chat.id, 'Додано оплату за спрацьовану рекламу')
            elif call.data == 'No':
                bot.send_message(call.message.chat.id, 'Додано оплату за неспрацьовану рекламу')
 
            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Чи спрацювала реклама?",
                reply_markup=None)

    except Exception as e:
        print(repr(e))                                                                                                                     
 
# RUN
bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
if __name__ == '__main__':
    bot.polling(none_stop=True)
