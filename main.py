import telebot
import Menu
from telebot import types

TOKEN = '1426242640:AAFVJRVKXlC_notspSzrJgWIw4BaG5xPvv8' # Токен телеграм бота
bot = telebot.TeleBot(TOKEN) # Обращаемся к боту по данныому токену

#***
admin1 = '719779899'
admin2 = '947104288'
#*** Id админов в которые бот посылает сообщение о заказе


print('good')# Проверка что скрипт начал работать
data = []
zakaz = []

#***
all_commands = ['Сделать заказ', 'Закончить выбор', 'Назад', 'Отменить заказ', 'Удалить последний заказ', 'Правильные данные', '/start', 'Правильный номер']
#*** Нужные обрабатываемые строки, чтобы мы могли следить на какую кнопку нажимал Юсер
commands = ['0']

def format_for_FIO(zakaz,message): # Добавляет ФИО который написал Юсер
    zakaz.append("Данные:")
    zakaz.append("\n---------------------\n")
    zakaz.append(str(message.text + "\n"))
    return zakaz

def type_of_zakaz(menuTypes, message):# метод для того чтобы на экран вывел Все типы Меню
    do_zakaz_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) # создание кнопки,  указываем resize_keyboard=True
    # чтобы размеры кнопки могли меняться, например можно будет положить в один ряд 2 кнокпи
    for x in menuTypes:# подбираем строки внутри массива MenuTypes
        item = types.KeyboardButton(x)# превращаем их в кнопки
        do_zakaz_markup.add(item)# добавляем его в список возвращаемых кнопок
    #**
    bot.send_message(message.chat.id, "<b>Выберите тип заказа!</b>", parse_mode='html', reply_markup=do_zakaz_markup)
    #** отправка сообщения Юсеру и возвращать ему список определенных кнопок
def end_of_zakaz(user,message):#Здесь мы готовим сообщение о заказе для админов и для Юсера
    zakaz_to_str = ""#сообщение будет отправлено Админам
    tff = 1
    list_of_zakaz = "Ваш заказ:\n+-------------------------------+\n"#сообщение будет отправлено Юсеру
    for z in user['zakaz']:#Здесь мы перебираем по циклу заказы Юсера, и показываем что добавить к сообщению Юсеру и Админу
        zakaz_to_str += z
        if z == 'Данные:':
            tff = 0
        if tff != 0:
            list_of_zakaz += z
    sum_str = '\nСумма заказа: ' + str(user['SUMMA']) + 'тг\n' # Добавляет сумму заказа
    print(sum_str)
    zakaz_to_str += sum_str
    sum = 0
    #***
    bot.send_message(admin1, zakaz_to_str)
    bot.send_message(admin2, zakaz_to_str)
    #*** отправка сообщения админам
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) # Создание листа возвращаемых кнопок
    to_start = types.KeyboardButton("/start")
    markup.add(to_start)# Добавление кнопки в список
    list_of_zakaz += "\n+-------------------------------+\n" + message.text + sum_str
    list_of_zakaz += "Заказ пошел в обработку(Отменить заказ после отправки невозможно), \nждите звонка оператора!"
    #***
    bot.send_message(message.chat.id, list_of_zakaz, parse_mode='html', reply_markup=markup)
    #** отправка сообщения Юсеру
    return []

def do_zakaz(menuTypes, itMenu, message):#проесс заказа еды
    for x in menuTypes:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if x == message.text:# проверяем выбрал ли человек какой то тип Еды
            final = types.KeyboardButton("Закончить выбор")
            cancel = types.KeyboardButton("Отменить заказ")
            delete = types.KeyboardButton("Удалить последний заказ")
            back = types.KeyboardButton("Назад")
            foods = itMenu.it_menu(message.text)#Возвращает кнопки тех блюд которые принадлежат типу который Юсер выбрал
            for food in foods:
                markup.add(food)# Добавление кнопки в возвращаемые кнопки
            markup.add(final, cancel)# Вот здесь мы в одну строку возвращаем 2 кнопки
            markup.add(delete, back)
            if message.text == 'Комбо':# Если юсер выбрал Тип Комбо
                kombos = "/home/muratbekovyerassyl/kombos.jpg"
                bot.send_photo(message.chat.id, photo=open(kombos, "rb"))# Мы отправляем ему фото о Комбо заказах
            bot.send_message(message.chat.id, "<b>Выберите заказ!</b>", parse_mode='html',
                             reply_markup=markup)

def delete_last_zakaz(user, message):#функция для удаления последнего заказа
    try:
        s = user['zakaz'][len(user['zakaz']) - 1]# Если список заказов у пользователя не пуста то
        # выбираем последний элемент из списка заказов
        print("last_zakaz: ", s)#Выводим его на экран чтобы могли увидеть работоспособность функции
        user['zakaz'] = user['zakaz'][:len(user['zakaz']) - 1]# Идет удаление последнего заказа
        print(zakaz)
        cost = s.find(' - ')
        tg = s.find('тг')
        user['SUMMA'] -= int(s[cost + 3:tg])#Идет вычет из Суммы заказов стоимость последнего заказа
        bot.send_message(message.chat.id, "ok", parse_mode='html')# Сообщаем клиенту что мы успешно удалили
        return user
    except:# Ну если Юсер еще не делал никаких заказов У нас будет ошибка и мы отправляем сообщение Юсеру
        bot.send_message(message.chat.id, "Вы еще не сделали заказ", parse_mode='html')
        return user

idxs = []#Здесь будет храниться все пользователи

@bot.message_handler(commands=['start'])#Работа при комманде старт
def welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать на наш ТелеграмБот ,{0.first_name}!  Нажмите на кнопку <b>'CДЕЛАТЬ ЗАКАЗ'</b> если хотите сделать заказ!".format(message.from_user), parse_mode='html')
    #keyboard
    global idxs
    tf = 0
    for i in range(len(idxs)):#Проверяем из списка Делал ли этот клиент заказ и не завершил его
        if idxs[i]['chat_id'] == message.chat.id:#Если есть такой пользователь мы создаем его как нового пользователя
            idxs[i] = {
                "id": i,
                "chat_id": message.chat.id,
                "commands": ['0'],
                "zakaz": [],
                "SUMMA": 0
            }
            tf = 1
            break
    if tf == 0:#Если такого пользователя нету мы также создаем его
        iterator = max(len(idxs) - 1, 0)
        idxs.append({
            "id": iterator,
            "chat_id": message.chat.id,
            "commands": ['0'],
            "zakaz": [],
            "SUMMA": 0
        })
    #**
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Сделать Заказ")
    item2 = types.KeyboardButton("Написать потом")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Сделать Заказ/Написать потом", parse_mode='html', reply_markup=markup)
    #** Уже описал Дамир мнаны озин жаз устиге карап


#**Мнанын барине озин коммент жаз адемилеп мен саган бастап бердим адемилеп
@bot.message_handler(content_types=['text'])# Функция которая выполняется при написании иного смса
def whatever(message):
    tf = 0
    kr = 0
    iterator = -1
    global idxs, commands
    if message.chat.type == 'private':
        for i in range(len(idxs)):
            iterator = i
            if idxs[i]['chat_id'] == message.chat.id:
                tf = 1
                break
        if tf == 0:
            bot.send_message(message.chat.id, "Чтобы начать работать с ботом, нажмите на <a>/start</a>", parse_mode='html')
            return
       # print(iterator)
        #print(idxs[iterator])
       # print(idxs[iterator]['commands'])
        #print(idxs[iterator]['commands'][len(commands)-1])

        itMenu = Menu.myMenu
        menuTypes = ['Сеты', 'Роллы', 'Пицца', 'Донер', 'Бургеры', 'Салаты', 'К чаю', 'Напитки', 'Комбо']
### Выбор типа заказа
        do_zakaz(menuTypes, itMenu, message)
###
        if message.text == 'Сделать Заказ':
            type_of_zakaz(menuTypes, message)
            kr = 1

        if message.text == 'Назад':
            type_of_zakaz(menuTypes, message)
            kr = 1

        if message.text == 'Отменить заказ':
            bot.send_message(message.chat.id, "Жаль! Заходи еще, мы ждем тебя)", parse_mode='html')
            idxs.pop(iterator)
            return
        if message.text == 'Закончить выбор':
            bot.send_message(message.chat.id, "Напишите фамилию и имя:", parse_mode='html')
            kr = 1
        if idxs[iterator]['commands'][len(idxs[iterator]['commands'])-1] == 'Закончить выбор':
            idxs[iterator]['zakaz'] = format_for_FIO(idxs[iterator]['zakaz'], message)
            bot.send_message(idxs[iterator]['chat_id'], "номер сот.телефона:(Напишите в формате: +77XXXXXXXXX) ",
                                parse_mode='html')
            message.text = 'Правильные данные'
            kr = 1
        if idxs[iterator]['commands'][len(idxs[iterator]['commands'])-1] == 'Правильные данные' and len(message.text) == 12 and message.text[:3] == '+77':

            idxs[iterator]['zakaz'].append(str("номер: " + message.text + "\n"))
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Доставка")
            item2 = types.KeyboardButton("Самовывоз")
            markup.add(item1, item2)
            bot.send_message(message.chat.id, "Доставка/Самовывоз", parse_mode='html', reply_markup=markup)
            message.text = 'Правильные данные2'
            #commands = ['0']
            kr = 1


        if idxs[iterator]['commands'][len(idxs[iterator]['commands'])-1] == 'Правильные данные2' and (message.text == 'Доставка' or message.text == 'Самовывоз'):

            if message.text == 'Доставка':
                if idxs[iterator]['SUMMA'] >= 5000:
                    message.text += " бесплатная\n"
                else:
                    message.text += " - 500тг"
                    idxs[iterator]['SUMMA'] += 500
            idxs[iterator]['zakaz'].append(message.text)
            idxs[iterator]['zakaz'].append("\n---------------------")
            idxs[iterator]['zakaz'] = end_of_zakaz(idxs[iterator], message)
            idxs.pop(iterator)
            return
        if message.text == 'Удалить последний заказ':
            idxs[iterator] = delete_last_zakaz(idxs[iterator], message)
            kr = 1
        tt = 0
        if len(idxs[iterator]['zakaz']) > 0:
            for item in itMenu.all_menu():
                if str(item.text + "\n") == idxs[iterator]['zakaz'][len(idxs[iterator]['zakaz'])-1]:
                    tt = 1
                    break
        else:
            tt = 1
        if tt == 1:
            for item in itMenu.all_menu():
                if item.text == message.text:
                    idxs[iterator]['zakaz'].append(str(message.text + "\n"))
                    cost = message.text.find(' - ')
                    tg = message.text.find('тг')
                    idxs[iterator]['SUMMA'] += int(message.text[cost+3:tg])

        if kr == 1:
            idxs[iterator]['commands'].append(message.text)
        #print(idxs[0])
        for x in idxs:
            print(x)


# RUN
bot.polling(none_stop=True)
