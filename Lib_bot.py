import asyncio

import aioschedule as aioschedule
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_polling
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, ContentType
from db import create_session, User, global_init, trade, Book
import datetime
from pydub import AudioSegment as am
import json
import requests
import pydub

for_admin = 'asdjk;laskjnvajllkajsdlkj'

TOKEN = '2027076146:AAF71gnNupo1gGYlBXAcJdQc6XJJLHsIusg'
close = {'rus': InlineKeyboardButton('❌ Закрыть', callback_data='close'),
         'tat': InlineKeyboardButton('❌ Ябырга', callback_data='close')}
back = {'rus': InlineKeyboardButton('🏘 Вернуться в главное меню', callback_data='menu'),
        'tat': InlineKeyboardButton('🏘 Баш менюне ачырга', callback_data='menu')}
inline_btn_1 = {'rus': InlineKeyboardButton('📚 Список всех книг', callback_data='list_of_all'),
                'tat': InlineKeyboardButton('📚 Барлык китаплар исемлеге', callback_data='list_of_all')}
inline_btn_2 = {'rus': InlineKeyboardButton('📓 Книги которые я должен', callback_data='my_duty'),
                'tat': InlineKeyboardButton('📓 Мин бурычлы китаплар', callback_data='my_duty')}
inline_btn_3 = {'rus': InlineKeyboardButton('🔎 Книги по жанрам', callback_data='genres'),
                'tat': InlineKeyboardButton('🔎 Жанр буенча китаплар', callback_data='genres')}
fr_book_genre = {'rus': InlineKeyboardButton('📖 Свободные книги', callback_data='fr_book_genre'),
                 'tat': InlineKeyboardButton('📖 Ирекле китаплар', callback_data='fr_book_genre')}
al_book_genre = {'rus': InlineKeyboardButton('🔓 Все книги', callback_data='al_book_genre'),
                 'tat': InlineKeyboardButton('🔓 Барлык китаплар', callback_data='al_book_genre')}
fr_book = {'rus': InlineKeyboardButton('📖 Свободные книги', callback_data='fr_book'),
           'tat': InlineKeyboardButton('📖 Ирекле китаплар', callback_data='fr_book')}
al_book = {'rus': InlineKeyboardButton('🔓 Все книги', callback_data='al_book'),
           'tat': InlineKeyboardButton('🔓 Барлык китаплар', callback_data='al_book')}
prof = {'rus': InlineKeyboardButton('🏠 Профиль', callback_data='prof'),
        'tat': InlineKeyboardButton('🏠 Профиль', callback_data='prof')}
chit_dnev = {'rus': InlineKeyboardButton('📖 Читательский дневник', callback_data='chit_dnev'),
             'tat': InlineKeyboardButton('📖 Уку көндәлеге', callback_data='chit_dnev')}

sib1 = {'rus': InlineKeyboardMarkup(row_width=1).add(fr_book['rus'], al_book['rus'], back['rus']),
        'tat': InlineKeyboardMarkup(row_width=1).add(fr_book['tat'], al_book['tat'], back['tat'])}
sib2 = {'rus': InlineKeyboardMarkup(row_width=1).add(fr_book_genre['rus'], al_book_genre['rus'], back['rus']),
        'tat': InlineKeyboardMarkup(row_width=1).add(fr_book_genre['tat'], al_book_genre['tat'], back['tat'])}
main_menu = {
    'rus': InlineKeyboardMarkup(row_width=1).add(prof['rus'], inline_btn_1['rus'], inline_btn_3['rus'], close['rus']),
    'tat': InlineKeyboardMarkup(row_width=1).add(prof['tat'], inline_btn_1['tat'], inline_btn_3['tat'], close['tat'])}

see_debtor = KeyboardButton('Посмотреть должников 👀')
add_book = KeyboardButton('Добавить новую книгу 🔄')
adm_keyb = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(see_debtor, add_book)

tes = {'rus': (ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(KeyboardButton('⬅️ Назад'),
                                                                          KeyboardButton('Дальше ➡️'),
                                                                          KeyboardButton(
                                                                              'Вернуться в главное меню 🏘'))),
       'tat': (ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(KeyboardButton('⬅️ Артка'),
                                                                          KeyboardButton('Алга ➡️'),
                                                                          KeyboardButton('Баш менюне ачырга 🏘')))}
chanel = -1001509319502


class Login(StatesGroup):
    login = State()
    phone = State()


class AddBook(StatesGroup):
    name = State()
    genre = State()
    author = State()
    description = State()
    amount = State()
    sog = State()


class SeeBook(StatesGroup):
    al = State()
    genre = State()


import requests
from bs4 import BeautifulSoup

import requests


def by_link(url):
    payload = {}
    headers = {
        'authority': 'www.litres.ru',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-US;q=0.6',
    }

    res = requests.request("GET", url, headers=headers, data=payload)
    soup = BeautifulSoup(res.text, 'lxml')
    name = soup.find('h1', itemprop="name").text[:-5]
    author = soup.find('a', class_="biblio_book_author__link").text
    genre = soup.find('a', class_="biblio_info__link").text
    description = soup.find('div', itemprop="description").text
    data = {}
    data['name'] = name
    data['author'] = author
    data['genre'] = genre
    data['description'] = description
    return data


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

import soundfile as sf


def convert_to_wav(filepath):
    data, samplerate = sf.read(filepath)
    sf.write(filepath, data, samplerate)


@dp.callback_query_handler(lambda callback_query: callback_query.data and callback_query.data.startswith('close'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


@dp.callback_query_handler(lambda callback_query: callback_query.data and 'ponim' in callback_query.data)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    if callback_query.data == 'ponim':
        await bot.edit_message_text('Мы очень рады 🥳', callback_query.message.chat.id,
                                    callback_query.message.message_id)
    elif callback_query.data == 'neponim':
        h = InlineKeyboardMarkup().add(InlineKeyboardButton('Посмотреть 👀', url='https://t.me/lyceum_library'))
        await bot.edit_message_text('Мы скинули в канал, надеемся вам помогут', callback_query.message.chat.id,
                                    callback_query.message.message_id, reply_markup=h)
        f = open("sample.wav", "rb")
        await bot.send_voice(chanel, f)


@dp.callback_query_handler(lambda callback_query: callback_query.data and callback_query.data.startswith('lang'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    if callback_query.data == 'lang':
        lkj = InlineKeyboardMarkup().add(InlineKeyboardButton('Русский 🇷🇺', callback_data='lang_rus'),
                                         InlineKeyboardButton('Татарский 🏳️', callback_data='lang_tat'))
        await  bot.edit_message_text('Выберите нужный язык 🎯', callback_query.message.chat.id,
                                     callback_query.message.message_id, reply_markup=lkj, )
    elif callback_query.data == 'lang_rus':
        session = create_session()
        user = session.query(User).filter(User.tg_id == callback_query.message.chat.id).first()
        user.lang = 'rus'
        session.add(user)
        session.commit()
        text = {'rus': 'Здравствуйте', 'tat': 'Исэнмесез'}
        await bot.edit_message_text(f"{text[user.lang]}, {user.name} ✌️", callback_query.message.chat.id,
                                    callback_query.message.message_id, reply_markup=main_menu[user.lang])
    elif callback_query.data == 'lang_tat':
        session = create_session()
        user = session.query(User).filter(User.tg_id == callback_query.message.chat.id).first()
        user.lang = 'tat'
        session.add(user)
        session.commit()
        text = {'rus': 'Здравствуйте', 'tat': 'Исэнмесез'}
        await bot.edit_message_text(f"{text[user.lang]}, {user.name} ✌️", callback_query.message.chat.id,
                                    callback_query.message.message_id, reply_markup=main_menu[user.lang])


def query(filename):
    headers = {"Authorization": f"Bearer api_dWmEmEvSoqvicaaeOySxMfRESevEWjTaVa"}
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.request("POST",
                                "https://api-inference.huggingface.co/models/anton-l/wav2vec2-large-xlsr-53-tatar"
                                , headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))


def translate(text):
    url = "http://byhackathon.translate.tatar/translate?lang=1&text="
    response = requests.get(url + text)
    text = response.text
    if "<responseType>" in response.text:
        text = response.text.split("<translation>")[1].split("</translation>")[0]
    return text


@dp.message_handler(content_types=['voice'])
async def voice_processing(message):
    file_info = await bot.get_file(message.voice.file_id)
    file_path = file_info.file_path
    await bot.download_file(file_path, 'sample.wav')
    data = query('sample.wav')
    data = dict(data)
    print(data)
    data = translate(data['text'])
    nnkl = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton('Понятно ✅', callback_data='ponim'),
                                                 InlineKeyboardButton('Не подходит ❌', callback_data='neponim'))
    if len(data) == 0:
        await bot.send_message(message.chat.id, 'Мы не распознали вашу речь 😢\nПопробуйте ещё раз 😉')
    else:
        await bot.send_message(message.chat.id, data[0].upper() + data[1::], reply_markup=nnkl)


@dp.callback_query_handler(lambda callback_query: callback_query.data and callback_query.data.startswith('daa'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await bot.edit_message_text('aklsdfj;laksdj',
                                callback_query.message.chat.id,
                                callback_query.message.message_id)


@dp.callback_query_handler(lambda callback_query: callback_query.data and callback_query.data.startswith('tradefinish'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    trade_id = callback_query.data.split('_')[1]
    session = create_session()
    user = session.query(User).filter(User.tg_id == callback_query.message.chat.id).first()
    trade_info = session.query(trade).filter(trade.trade_id == trade_id).first()
    if user.role != 'admin':
        main_menu_button = back[user.lang]
        adm_keyb = InlineKeyboardMarkup(row_width=1, resize_keyboard=True).add(main_menu_button)
        text = {'rus': "Ждем решения библиотекаря", 'tat': 'Китапханәченең карарын көтәбез җавап'}
        await bot.edit_message_text(text[user.lang],
                                    callback_query.message.chat.id,
                                    callback_query.message.message_id, reply_markup=adm_keyb)
        admin = session.query(User).filter(User.role == 'admin').first().tg_id
        main_menu_button1 = InlineKeyboardButton('✅ Принять книгу', callback_data=f'tradefinish_{trade_id}_yes')
        main_menu_button2 = InlineKeyboardButton('❌ Отказать', callback_data=f'tradefinish_{trade_id}_no')
        main_menu = InlineKeyboardMarkup(row_width=2, resize_keyboard=True).add(main_menu_button1,
                                                                                main_menu_button2)
        await bot.send_message(admin,
                               f'Пользователь {user.name} возвращает книгу {trade_info.book_name}',
                               reply_markup=main_menu)
    else:
        user = session.query(User).filter(User.tg_id == trade_info.user_id).first()
        main_menu_button = back[user.lang]
        main_menu = InlineKeyboardMarkup(row_width=1, resize_keyboard=True).add(main_menu_button)
        if callback_query.data.split('_')[-1] == 'yes':
            book = session.query(Book).filter(Book.book_id == trade_info.book_id).first()
            book.amount += 1
            trade_info.status = "worked"
            session.commit()
            user = session.query(User).filter(User.tg_id == trade_info.user_id).first()
            # c = user.xp
            # user.xp = int(user.xp) + 5
            session.add(user)
            session.commit()
            text = {'rus': f'{user.name}, вы успешно сдали книгу {trade_info.book_name}\nХотите пройти тест и получить баллы? 😏',
                    'tat': f'{user.name}, сез китапны тапшырдыгыз {trade_info.book_name}\nТест ясарга һәм баллар алырга телисезме? 😏'}
            lkjh = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton('Да ✅', callback_data='daa'),
                                                         InlineKeyboardButton('Нет ❌', callback_data='nno'))
            await bot.send_message(user.tg_id,
                                   text[user.lang],
                                   reply_markup=lkjh)
            await bot.edit_message_text(f"Пользователь {user.name} успешно сдал книгу {trade_info.book_name}",
                                        callback_query.message.chat.id,
                                        callback_query.message.message_id)
        else:
            text = {'rus': f'{user.name}, вам отказано в возврате книги {trade_info.book_name}',
                    'tat': f'{user.name}, сез китап тапшырмадыгыз {trade_info.book_name}'}
            await bot.send_message(user.tg_id, text[user.lang],
                                   reply_markup=main_menu)
            await bot.edit_message_text(f"Вы не приняли книгу у {user.name}",
                                        callback_query.message.chat.id,
                                        callback_query.message.message_id)


@dp.callback_query_handler(lambda callback_query: callback_query.data and callback_query.data.startswith('tradeyes'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    trade_id = callback_query.data.split('_')[1]
    session = create_session()
    trade_info = session.query(trade).filter(trade.trade_id == trade_id).first()
    book = session.query(Book).filter(Book.book_id == trade_info.book_id).first()
    user = session.query(User).filter(User.tg_id == trade_info.user_id).first()
    book.amount = int(book.amount) - 1
    trade_info.status = 'working'
    session.commit()
    main_menu_button = back[user.lang]
    main_menu = InlineKeyboardMarkup(row_width=1, resize_keyboard=True).add(main_menu_button)
    await bot.edit_message_text(
        f"Вы успешно выдали книгу *{trade_info.book_name}* пользователю {user.name} {user.surname} из {user.clas}",
        callback_query.message.chat.id,
        callback_query.message.message_id, parse_mode=ParseMode.MARKDOWN)
    text = {
        'rus': f'Вы взяли книгу {trade_info.book_name}. Напоминаем что книгу необходимо вернуть до {trade_info.date_return}.'
        ,
        'tat': f'Сез {trade_info.book_name} китапны алдыгыз. хәтерегездә тотыгыз, китапны  {trade_info.date_return} кадәр кайтарырга кирәк..'}
    await bot.send_message(trade_info.user_id,
                           f'Вы взяли книгу {trade_info.book_name}. Напоминаем что книгу необходимо вернуть до {trade_info.date_return}.',
                           reply_markup=main_menu)


@dp.callback_query_handler(lambda callback_query: callback_query.data and callback_query.data.startswith('tradeno'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    trade_id = callback_query.data.split('_')[1]
    session = create_session()
    trade_info = session.query(trade).filter(trade.trade_id == trade_id).first()
    user = session.query(User).filter(trade_info.user_id == User.tg_id).first()
    main_menu_button = back[user.lang]
    main_menu = InlineKeyboardMarkup(row_width=1, resize_keyboard=True).add(main_menu_button)
    await bot.edit_message_text(
        f"Вы отказали в выдаче книги *{trade_info.book_name}* пользователю {user.name} {user.surname} из {user.clas}",
        callback_query.message.chat.id,
        callback_query.message.message_id, parse_mode=ParseMode.MARKDOWN)
    text = {'rus': f'Вам отказано в выдаче книги {trade_info.book_name}.',
            'tat': f'Сезгә {trade_info.book_name} китабын бирмәделәр'}
    await bot.send_message(trade_info.user_id,
                           text[user.lang], reply_markup=main_menu)
    session.delete(trade_info)
    session.commit()


@dp.callback_query_handler(lambda callback_query: callback_query.data and callback_query.data.startswith('date_choose'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    book_id = callback_query.data.split('_')[-1]
    print(callback_query.data)
    session = create_session()
    book = session.query(Book).filter(Book.book_id == book_id).first()
    user = session.query(User).filter(User.tg_id == callback_query.message.chat.id).first()
    if book.amount != 0 and book.amount != '0':
        await callback_query.answer('Выберите период в течении которого вы прочитаете книгу ⬇️')
        text = {'rus': '1 день', 'tat': '1 көн'}
        btn1 = InlineKeyboardButton(text[user.lang], callback_data=f'take_{book_id}_1')
        text = {'rus': '3 день', 'tat': '3 көн'}
        btn2 = InlineKeyboardButton(text[user.lang], callback_data=f'take_{book_id}_3')
        text = {'rus': '1 неделя', 'tat': '1 атна'}
        btn3 = InlineKeyboardButton(text[user.lang], callback_data=f'take_{book_id}_7')
        adm_keyb = InlineKeyboardMarkup(row_width=2, resize_keyboard=True).row(btn1, btn2)
        adm_keyb.add(btn3)
        text = {'rus': 'Выберите период, в течении которого вы сможете вернуть книгу. 📆️',
                'tat': 'Китапны кайчан кире кайтарасыз? 📆️'}
        await bot.edit_message_text(text[user.lang],
                                    callback_query.message.chat.id,
                                    callback_query.message.message_id, reply_markup=adm_keyb)
    else:
        user = session.query(User).filter(User.tg_id == callback_query.message.chat.id).first()
        if user.hurry < 3:
            user.hurry += 1
            session.add(user)
            session.commit()
            tr = session.query(trade).filter(trade.book_id == book_id).filter(trade.status == 'working').all()
            for i in tr:
                await bot.send_message(i.user_id, 'Пожалуйста поскорее возращайте книгу ' + i.book_name + ' 🙏')
            await callback_query.answer('Мы поторопили владельца книги 🏎')
        else:
            await callback_query.answer('В день можно торопить только три раза', show_alert=True)


@dp.callback_query_handler(lambda callback_query: callback_query.data and callback_query.data.startswith('take_'),
                           state=None)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer('Отлично! Осталось дождаться подтверждения')
    book_id = callback_query.data.split('_')[1]
    period = callback_query.data.split('_')[2]
    session = create_session()
    book = session.query(Book).filter(Book.book_id == book_id).first()
    if int(book.amount) > 0:
        admin = session.query(User).filter(User.role == 'admin').first().tg_id
        user = session.query(User).filter(User.tg_id == callback_query.message.chat.id).first()
        main_menu_button = back[user.lang]
        main_menu = InlineKeyboardMarkup(row_width=1, resize_keyboard=True).add(main_menu_button)
        text = {'rus': 'Ждём подтверждения от библиотекаря. ⏳\nВы будете уведомлены после подтверждения. 🔔️',
                'tat': 'Китапханәченең рөхсәтен көтәбез'}
        await bot.edit_message_text(text[user.lang],
                                    callback_query.message.chat.id,
                                    callback_query.message.message_id, reply_markup=main_menu)
        data = await state.get_data()
        if data.get('0') != None:
            for i in range(int(data.get('0'))):
                i += 1
                c = data.get(str(i))
                if str(data.get(str(i))) != str(callback_query.message.message_id):
                    await bot.delete_message(callback_query.message.chat.id, data.get(str(i)))
            await bot.delete_message(callback_query.message.chat.id, data.get('mainMes'))
        new_trade = trade()
        new_trade.user_id = callback_query.message.chat.id
        new_trade.book_id = book_id
        new_trade.status = 'waiting'
        new_trade.book_name = book.name
        new_trade.date_taking = datetime.date.today().strftime("%d-%m-%Y")
        new_trade.date_return = (datetime.date.today() + datetime.timedelta(int(period))).strftime("%d-%m-%Y")
        session.add(new_trade)
        session.commit()
        btn1 = InlineKeyboardButton('✅ Выдать книгу', callback_data=f'tradeyes_{new_trade.trade_id}')
        btn2 = InlineKeyboardButton('❌ Отказать', callback_data=f'tradeno_{new_trade.trade_id}')
        adm_keyb = InlineKeyboardMarkup(row_width=2, resize_keyboard=True).row(btn1, btn2)
        await bot.send_message(admin,
                               f'Пользователь {user.name} {user.surname} из {user.clas} собирается взять книгу {book.name}',
                               reply_markup=adm_keyb)
        session.commit()
    else:
        await callback_query.answer('Данная книга уже занята 😔\nМы уже поторопили владельца книги')


@dp.callback_query_handler(lambda callback_query: callback_query.data and callback_query.data.startswith('duty_'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await  bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=False,
                                     text="Загружаем информацию о задолженности...️")
    duty_id = callback_query.data.split('_')[1]
    session = create_session()
    user = session.query(User).filter(User.tg_id == callback_query.message.chat.id).first()
    duty_info = session.query(trade).filter(trade.trade_id == duty_id).first()
    duties = InlineKeyboardMarkup(row_width=2)
    btnn1 = {'rus': InlineKeyboardButton(f'◀️ Назад', callback_data=f'my_duty'),
             'tat': InlineKeyboardButton(f'◀️ Артка', callback_data=f'my_duty')}
    btnn2 = {'rus': InlineKeyboardButton(f'✅ Вернуть книгу', callback_data=f'tradefinish_{duty_info.trade_id}'),
             'tat': InlineKeyboardButton(f'✅ Китап кайтару', callback_data=f'tradefinish_{duty_info.trade_id}')}
    duties.add(btnn1[user.lang],
               btnn2[user.lang])
    text = {
        'rus': f"Вы взяли книгу *{duty_info.book_name}* {duty_info.date_taking}.️ Дата возврата: {duty_info.date_return}",
        'tat': f"Сез *{duty_info.book_name}* китапны алдыгыз {duty_info.date_taking}.️ Кире кайтару датасы: {duty_info.date_return}", }
    await bot.edit_message_text(text[user.lang],
                                callback_query.message.chat.id,
                                callback_query.message.message_id, reply_markup=duties, parse_mode=ParseMode.MARKDOWN)


@dp.callback_query_handler(state=None)
async def main_buttons(callback_query: types.CallbackQuery, state: FSMContext):
    session = create_session()
    user = session.query(User).filter(User.tg_id == callback_query.message.chat.id).first()
    if callback_query.data == 'my_duty':
        await  bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=False,
                                         text="Загружаем список задолженостей ⏳")
        session = create_session()
        books = session.query(trade).filter(trade.user_id == callback_query.message.chat.id).filter(
            trade.status == 'working').all()
        user = session.query(User).filter(User.tg_id == callback_query.message.chat.id).first()
        duties = InlineKeyboardMarkup(row_width=1)
        if len(books) < 1:
            duties.add(back[user.lang])
            text = {'rus': 'У вас нет задолжностей', 'tat': 'Сездә китаплар юк'}
            await bot.edit_message_text(text[user.lang], callback_query.message.chat.id,
                                        callback_query.message.message_id, reply_markup=duties)
        else:
            for i in books:
                duties.add(InlineKeyboardButton(f'{i.book_name}', callback_data=f'duty_{i.trade_id}'))
            duties.add(back[user.lang])
            text = {'rus': 'Выбирете книгу из списка ниже 👇', 'tat': 'Китапны сайлагыз 👇'}
            await bot.edit_message_text(text[user.lang], callback_query.message.chat.id,
                                        callback_query.message.message_id, reply_markup=duties)
    elif callback_query.data == 'menu':
        await  bot.answer_callback_query(callback_query_id=callback_query.id, show_alert=False,
                                         text="Возвращаемся в главное меню 🚶‍♀️")
        session = create_session()
        user = session.query(User).filter(User.tg_id == callback_query.message.chat.id).first()
        if user != None:
            if user.role == 'admin':
                pass
            else:
                text = {'rus': 'Здравствуйте', 'tat': 'Исэнмесез'}
                await bot.edit_message_text(f"{text[user.lang]}, {user.name} ✌️", callback_query.message.chat.id,
                                            callback_query.message.message_id, reply_markup=main_menu[user.lang])
    elif callback_query.data == 'list_of_all':
        await callback_query.answer('Выберете тип книг из списка ниже ⬇️')
        text = {'rus': 'Какие книги вы хотите увидеть?', 'tat': 'Нинди китаплар сез күрергә теләсәгез?'}
        await bot.edit_message_text(text[user.lang],
                                    callback_query.message.chat.id,
                                    callback_query.message.message_id, parse_mode=ParseMode.MARKDOWN,
                                    reply_markup=sib1[user.lang])
        # async with state.proxy() as data:
        #     data['genre'] = None
        session = create_session()
        user = session.query(User).filter(User.tg_id == callback_query.message.chat.id).first()
        user.genre = None
        session.add(user)
        session.commit()
    elif callback_query.data == 'genres':
        await callback_query.answer('Выберете тип книг из списка ниже ⬇️')
        text = {'rus': 'Какие книги вы хотите увидеть?', 'tat': 'Нинди китаплар сез күрергә теләсәгез?'}
        await bot.edit_message_text(text[user.lang],
                                    callback_query.message.chat.id,
                                    callback_query.message.message_id, parse_mode=ParseMode.MARKDOWN,
                                    reply_markup=sib2[user.lang])
    elif callback_query.data == 'al_book':
        await callback_query.answer('Загружаем список всех книг 🔎')
        session = create_session()
        books = session.query(Book).all()
        # async with state.proxy() as data:
        #     data['page'] = 1
        # async with state.proxy() as data:
        #     data['free'] = False
        count = 0
        user = session.query(User).filter(User.tg_id == callback_query.message.chat.id).first()
        user.fre = False
        user.page = '1'
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        text = {'rus': 'Используйте клавиатуру для перелистывания 😉', 'tat': 'Эзләү өчен клавиатураны кулланыгыз 😉'}
        a = await bot.send_message(callback_query.message.chat.id, text[user.lang],
                                   reply_markup=tes[user.lang])
        user.mainMes = a.message_id
        for i in books:
            count += 1
            more = {'rus': InlineKeyboardButton('Подробнее 🧐', url=i.link),
                    'tat': InlineKeyboardButton('Тәфсилле 🧐', url=i.link)}
            take = {'rus': InlineKeyboardButton('🤲🏻 Взять', callback_data=f'date_choose_{i.book_id}'),
                    'tat': InlineKeyboardButton('🤲🏻 Алырга', callback_data=f'date_choose_{i.book_id}')}
            hurry = {'rus': InlineKeyboardButton('🚴‍♀️ Поторопить', callback_data=f"date_choose_{i.book_id}"),
                     'tat': InlineKeyboardButton('🚴‍♀️ Ашыктыру', callback_data=f"date_choose_{i.book_id}")}
            if i.amount != 0 and i.amount != '0':
                kl = InlineKeyboardMarkup(row_width=2).add(take[user.lang], more[user.lang])
            else:
                kl = InlineKeyboardMarkup(row_width=2).add(hurry[user.lang], more[user.lang])
            a = await bot.send_message(callback_query.message.chat.id, str(count) + ' - '
                                                                                    '*Название:* ' + i.name + '\n*      Жанр:* ' + i.genre + '\n*      Автор:* ' + i.author,
                                       parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
            if count == 1:
                user.one = a.message_id
            if count == 2:
                user.two = a.message_id
            if count == 3:
                user.three = a.message_id
            if count == 3:
                break
        user.ziro = str(count)
        session.add(user)
        session.commit()
    elif callback_query.data == 'fr_book':
        await callback_query.answer('Загружаем свободные книги 🔍')
        session = create_session()
        books = session.query(Book).filter(Book.amount != 0).filter(Book.amount != '0').all()
        user = session.query(User).filter(User.tg_id == callback_query.message.chat.id).first()
        user.page = '1'
        user.fre = True
        count = 0
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        text = {'rus': 'Используйте клавиатуру для перелистывания 😉', 'tat': 'Эзләү өчен клавиатураны кулланыгыз 😉'}
        a = await bot.send_message(callback_query.message.chat.id, text[user.lang],
                                   reply_markup=tes[user.lang])
        user.mainMes = a.message_id
        for i in books:
            count += 1
            more = {'rus': InlineKeyboardButton('Подробнее 🧐', url=i.link),
                    'tat': InlineKeyboardButton('Тәфсилле 🧐', url=i.link)}
            take = {'rus': InlineKeyboardButton('🤲🏻 Взять', callback_data=f'date_choose_{i.book_id}'),
                    'tat': InlineKeyboardButton('🤲🏻 Алырга', callback_data=f'date_choose_{i.book_id}')}
            hurry = {'rus': InlineKeyboardButton('🚴‍♀️ Поторопить', callback_data=f"date_choose_{i.book_id}"),
                     'tat': InlineKeyboardButton('🚴‍♀️ Ашыктыру', callback_data=f"date_choose_{i.book_id}")}
            if i.amount != 0 and i.amount != '0':
                kl = InlineKeyboardMarkup(row_width=2).add(take[user.lang], more[user.lang])
            else:
                kl = InlineKeyboardMarkup(row_width=2).add(hurry[user.lang], more[user.lang])
            a = await bot.send_message(callback_query.message.chat.id, str(count) + ' - '
                                                                                    '*Название:* ' + i.name + '\n*      Жанр:* ' + i.genre + '\n*      Автор:* ' + i.author,
                                       parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
            if count == 1:
                user.one = a.message_id
            if count == 2:
                user.two = a.message_id
            if count == 3:
                user.three = a.message_id
            if count == 3:
                break
            if count == 3:
                break
        user.ziro = str(count)
        session.add(user)
        session.commit()
    elif callback_query.data == 'al_book_genre':
        await callback_query.answer('Выберете жанр книги 📖')
        session = create_session()
        books = session.query(Book).all()
        user = session.query(User).filter(User.tg_id == callback_query.message.chat.id).first()
        user.fre = False
        sp = []
        for i in books:
            if i.genre not in sp:
                sp.append(i.genre)
        kl = InlineKeyboardMarkup(row_width=2)
        c = 0
        for i in range(len(sp)):
            if i != len(sp) - 1 and i % 2 == 0:
                kl.add(InlineKeyboardButton(sp[i], callback_data=sp[i]),
                       InlineKeyboardButton(sp[i + 1], callback_data=sp[i + 1]))
        if len(sp) % 2 != 0:
            kl.add(InlineKeyboardButton(sp[-1], callback_data=sp[-1]))
        kl.add(back[user.lang])
        text = {'rus': 'Выберите нужный жанр 🎯', 'tat': 'Сайлагыз жанры 🎯'}
        a = await bot.edit_message_text(text[user.lang], callback_query.message.chat.id,
                                        callback_query.message.message_id,
                                        reply_markup=kl)
        user.mainMes = a.message_id
        session.add(user)
        session.commit()
    elif callback_query.data == 'fr_book_genre':
        await callback_query.answer('Выберете жанр книги 📖')
        session = create_session()
        books = session.query(Book).filter(Book.amount != 0).filter(Book.amount != '0').all()
        user = session.query(User).filter(User.tg_id == callback_query.message.chat.id).first()
        user.fre = True
        sp = []
        for i in books:
            if i.genre not in sp:
                sp.append(i.genre)
        kl = InlineKeyboardMarkup(row_width=2)
        c = 0
        for i in range(len(sp)):
            if i != len(sp) - 1 and i % 2 == 0:
                kl.add(InlineKeyboardButton(sp[i], callback_data=sp[i]),
                       InlineKeyboardButton(sp[i + 1], callback_data=sp[i + 1]))
        if len(sp) % 2 != 0:
            kl.add(InlineKeyboardButton(sp[-1], callback_data=sp[-1]))
        kl.add(back[user.lang])
        text = {'rus': 'Выберите нужный жанр 🎯', 'tat': 'Сайлагыз жанры 🎯'}
        a = await bot.edit_message_text(text[user.lang], callback_query.message.chat.id,
                                        callback_query.message.message_id,
                                        reply_markup=kl)
        user.mainMes = a.message_id
        session.add(user)
        session.commit()
    else:
        if callback_query.data == 'prof':
            session = create_session()
            must = len(session.query(trade).filter(trade.status == 'working').filter(
                trade.user_id == callback_query.message.chat.id).all())
            proch = len(session.query(trade).filter(trade.status == 'worked').filter(
                trade.user_id == callback_query.message.chat.id).all())
            user = session.query(User).filter(User.tg_id == callback_query.message.chat.id).first()
            nkl = InlineKeyboardMarkup(row_width=1).add(
                InlineKeyboardButton('Язык 🇷🇺/ Тел  🏳️', callback_data='lang'))
            nkl.add(inline_btn_2[user.lang], chit_dnev[user.lang], back[user.lang])
            user = session.query(User).filter(User.tg_id == callback_query.message.chat.id).first()
            xx = user.xp
            lvl = 1
            c = 10
            while xx >= c:
                xx -= c
                lvl += 1
                c *= 1.2
                c = int(c)
            text_rus = 'Приветствуем вас 🙋\n' + 'Вы должны библиотеке ' + str(must) + ' 📕\n' + 'Вы прочитали ' + str(
                proch) + ' 📘\n' + 'Ваш уровень равен *' + str(lvl) + '* 🏰 вам осталось *' + str(
                c - xx) + ' xp* до нового уровня'
            text_tat = 'Исэнмесез 🙋\n' + 'Хәзер сездә ' + str(must) + ' китап 📕\n' + 'Сез ' + str(
                proch) + 'китап укыдыгыз 📘\n' + 'Сездә *' + str(lvl) + '* уровень\n 🏰 Сезгә *' + str(
                c - xx) + ' xp* яңа уровень өчен кирәк'
            text12 = {'rus': text_rus, 'tat': text_tat}
            await bot.edit_message_text(text12[user.lang],
                                        callback_query.message.chat.id,
                                        callback_query.message.message_id, reply_markup=nkl,
                                        parse_mode=ParseMode.MARKDOWN)
        elif callback_query.data == 'chit_dnev':
            session = create_session()
            proch = len(session.query(trade).filter(trade.status == 'worked').filter(
                trade.user_id == callback_query.message.chat.id).all())
            if proch != 0:
                proch = session.query(trade).filter(trade.status == 'worked').filter(
                    trade.user_id == callback_query.message.chat.id).all()
                kl = InlineKeyboardMarkup(row_width=1)
                for i in proch:
                    kl.add(InlineKeyboardButton(i.book_name, callback_data=i.book_name))
                kl.add(back[user.lang])
                await bot.edit_message_text('Выберите книгу и посмотрите ваши записи или добавьте их 🦸‍♂️',
                                            callback_query.message.chat.id,
                                            callback_query.message.message_id, reply_markup=kl)
            else:
                await bot.edit_message_text('К сожалению вы ещё ничего не прочитали 😕', callback_query.message.chat.id,
                                            callback_query.message.message_id,
                                            reply_markup=InlineKeyboardMarkup(row_width=1).add(back[user.lang]))
        else:
            session = create_session()
            user = session.query(User).filter(User.tg_id == callback_query.message.chat.id).first()
            if user.fre == True:
                books = session.query(Book).filter(Book.amount != 0).filter(Book.amount != '0').filter(
                    Book.genre == callback_query.data).all()
                user.page = '1'
                count = 0
                user.genre = callback_query.data
                session.add(user)
                session.commit()
                await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
                text = {'rus': 'Используйте клавиатуру для перелистывания 😉',
                        'tat': 'Эзләү өчен клавиатураны кулланыгыз 😉'}
                a = await bot.send_message(callback_query.message.chat.id, text[user.lang],
                                           reply_markup=tes[user.lang])
                user.mainMes = a.message_id
                for i in books:
                    count += 1
                    more = {'rus': InlineKeyboardButton('Подробнее 🧐', url=i.link),
                            'tat': InlineKeyboardButton('Тәфсилле 🧐', url=i.link)}
                    take = {'rus': InlineKeyboardButton('🤲🏻 Взять', callback_data=f'date_choose_{i.book_id}'),
                            'tat': InlineKeyboardButton('🤲🏻 Алырга', callback_data=f'date_choose_{i.book_id}')}
                    hurry = {'rus': InlineKeyboardButton('🚴‍♀️ Поторопить', callback_data=f"date_choose_{i.book_id}"),
                             'tat': InlineKeyboardButton('🚴‍♀️ Ашыктыру', callback_data=f"date_choose_{i.book_id}")}
                    if i.amount != 0 and i.amount != '0':
                        kl = InlineKeyboardMarkup(row_width=2).add(take[user.lang], more[user.lang])
                    else:
                        kl = InlineKeyboardMarkup(row_width=2).add(hurry[user.lang], more[user.lang])
                    a = await bot.send_message(callback_query.message.chat.id, str(count) + ' - '
                                                                                            '*Название:* ' + i.name + '\n*      Жанр:* ' + i.genre + '\n*      Автор:* ' + i.author,
                                               parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
                    if count == 1:
                        user.one = a.message_id
                    if count == 2:
                        user.two = a.message_id
                    if count == 3:
                        user.three = a.message_id
                    if count == 3:
                        break
                    if count == 3:
                        break
                user.ziro = str(count)
                session.add(user)
                session.commit()
            else:
                session = create_session()
                books = session.query(Book).filter(
                    Book.genre == callback_query.data).all()
                async with state.proxy() as data:
                    data['page'] = 1
                user = session.query(User).filter(User.tg_id == callback_query.message.chat.id).first()
                user.page = '1'
                user.genre = callback_query.data
                session.add(user)
                session.commit()
                count = 0
                await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
                text = {'rus': 'Используйте клавиатуру для перелистывания 😉',
                        'tat': 'Эзләү өчен клавиатураны кулланыгыз 😉'}
                a = await bot.send_message(callback_query.message.chat.id, text[user.lang],
                                           reply_markup=tes[user.lang])
                user.mainMes = a.message_id
                for i in books:
                    count += 1
                    more = {'rus': InlineKeyboardButton('Подробнее 🧐', url=i.link),
                            'tat': InlineKeyboardButton('Тәфсилле 🧐', url=i.link)}
                    take = {'rus': InlineKeyboardButton('🤲🏻 Взять', callback_data=f'date_choose_{i.book_id}'),
                            'tat': InlineKeyboardButton('🤲🏻 Алырга', callback_data=f'date_choose_{i.book_id}')}
                    hurry = {'rus': InlineKeyboardButton('🚴‍♀️ Поторопить', callback_data=f"date_choose_{i.book_id}"),
                             'tat': InlineKeyboardButton('🚴‍♀️ Ашыктыру', callback_data=f"date_choose_{i.book_id}")}
                    if i.amount != 0 and i.amount != '0':
                        kl = InlineKeyboardMarkup(row_width=2).add(take[user.lang], more[user.lang])
                    else:
                        kl = InlineKeyboardMarkup(row_width=2).add(hurry[user.lang], more[user.lang])
                    a = await bot.send_message(callback_query.message.chat.id, str(count) + ' - '
                                                                                            '*Название:* ' + i.name + '\n*      Жанр:* ' + i.genre + '\n*      Автор:* ' + i.author,
                                               parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
                    if count == 1:
                        user.one = a.message_id
                    if count == 2:
                        user.two = a.message_id
                    if count == 3:
                        user.three = a.message_id
                    if count == 3:
                        break
                    if count == 3:
                        break
                user.ziro = str(count)
                session.add(user)
                session.commit()


@dp.message_handler(commands=['start'], state=None)
async def process_start_command(message: types.Message):
    session = create_session()
    user = session.query(User).filter(User.tg_id == message.chat.id).first()
    if user != None:
        if user.role == 'admin':
            if 'take_book' in message.get_args():
                book_id = message.get_args().split('_')[-1]
                if book_id != '':
                    trade_info = session.query((trade)).filter(book_id == trade.book_id).filter(
                        trade.status == 'working').first()
                    book = session.query(Book).filter(Book.book_id == trade_info.book_id).first()
                    book.amount += 1
                    trade_info.status = "worked"
                    user = session.query(User).filter(User.tg_id == trade_info.user_id).first()
                    # c = user.xp
                    # user.xp = int(user.xp) + 5
                    session.add(user)
                    session.add(trade_info)
                    session.commit()
                    lkjh = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton('Да ✅', callback_data='daa'),
                                                                 InlineKeyboardButton('Нет ❌', callback_data='nno'))
                    text = {'rus': f'{user.name}, вы успешно сдали книгу {trade_info.book_name}',
                            'tat': f'{user.name}, сез китапны тапшырдыгыз {trade_info.book_name}'}
                    await bot.send_message(user.tg_id,
                                           text[user.lang] + '\n'
                                                             'Вы хотите пройти тест и полчить баллы? 😏',
                                           reply_markup=lkjh)
                    await bot.send_message(message.chat.id, f"Пользователь успешно сдал книгу {trade_info.book_name}",
                                           )
            else:
                user.for_admin = '0'
                session.add(user)
                session.commit()
                see_debtor = KeyboardButton('Посмотреть должников 👀')
                add_book = KeyboardButton('Добавить новую книгу 🔄')
                adm_keyb = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(see_debtor, add_book)
                await bot.send_message(message.chat.id, "Доброе время суток", reply_markup=adm_keyb)
        else:
            if 'take_book' in message.get_args():
                book_id = message.get_args().split('_')[-1]
                if book_id != '':
                    book = session.query(Book).filter(Book.book_id == int(book_id)).first()
                    text = {'rus': '1 день', 'tat': '1 көн'}
                    btn1 = InlineKeyboardButton(text[user.lang], callback_data=f'take_{book_id}_1')
                    text = {'rus': '3 день', 'tat': '3 көн'}
                    btn2 = InlineKeyboardButton(text[user.lang], callback_data=f'take_{book_id}_3')
                    text = {'rus': '1 неделя', 'tat': '1 атна'}
                    btn3 = InlineKeyboardButton(text[user.lang], callback_data=f'take_{book_id}_7')
                    adm_keyb = InlineKeyboardMarkup(row_width=2, resize_keyboard=True).row(btn1, btn2)
                    adm_keyb.add(btn3)
                    text = {
                        'rus': f"Вы собираетесь взять книгу *{book.name}*.\n\nВыберите период, в течении которого вы сможете вернуть книгу. 📆️",
                        'tat': f"Сез *{book.name}* китапны аласыз.\n\nКитапны кайчан кире кайтарасыз? 📆️"}
                    await bot.send_message(message.chat.id, text[user.lang],
                                           reply_markup=adm_keyb, parse_mode=ParseMode.MARKDOWN)
            else:
                text = {'rus': 'Здравствуйте', 'tat': 'Исэнмесез'}
                await bot.send_message(message.chat.id, f"{text[user.lang]}, {user.name} ✌️",
                                       reply_markup=main_menu[user.lang])
    else:
        await bot.send_message(message.chat.id,
                               "Привет! 👋\nДля продолжения необходимо указать свои данные\nВ следущем сообщении введите своё имя, фамилию и класс через пробел в формате *Иванов Иван 10А.*",
                               parse_mode=ParseMode.MARKDOWN)
        await Login.login.set()


@dp.message_handler(state=None)
async def just_message(msg: types.Message, state: FSMContext):
    session = create_session()
    user = session.query(User).filter(User.tg_id == msg.chat.id).first()
    if msg.text == for_admin:
        user.role = 'admin'
        user.for_admin = '0'
        await bot.send_message(msg.chat.id, "Доброе время суток, теперь у вас есть права админа", reply_markup=adm_keyb)
        session.add(user)
        session.commit()
    elif user.role == 'admin':
        if msg.text == 'Добавить новую книгу 🔄':
            await bot.send_message(msg.chat.id,
                                   'Начинаем процесс добавления книги 📘\nЕсли вы допустили ошибку, продолжите, в конце вы можете отменить операцию\nНапишите только *название* книги или отправьте ссылку на литрес.',
                                   parse_mode=ParseMode.MARKDOWN)
            await AddBook.name.set()
        elif msg.text == 'Посмотреть должников 👀':
            books = session.query(trade).filter(trade.status == 'working').all()
            if len(books) < 1:
                await bot.send_message(msg.chat.id, "Пока нет должников 👍")
            else:
                ms = ''
                c = 1
                for i in books:
                    ms += str(c) + '. '
                    sid = i.user_id
                    us = session.query(User).filter(User.tg_id == sid).first()
                    ms += us.name + ' ' + us.surname + ' ' + us.clas + ' должен вам книгу ' + i.book_name + ' +' + str(
                        us.phone)
                    ms += '\n'
                    c += 1
                await bot.send_message(msg.chat.id, ms)
    else:
        if msg.text == 'Вернуться в главное меню 🏘' or msg.text == 'Баш менюне ачырга 🏘':
            session = create_session()
            user = session.query(User).filter(User.tg_id == msg.chat.id).first()
            text = {'rus': 'Здравствуйте', 'tat': 'Исэнмесез'}
            await bot.send_message(msg.chat.id, f"{text[user.lang]}, {user.name} ✌️",
                                   reply_markup=main_menu[user.lang])
            if user.ziro != None:
                for i in range(int(user.ziro)):
                    if i == 0:
                        await bot.delete_message(msg.chat.id, user.one)
                    elif i == 1:
                        await bot.delete_message(msg.chat.id, user.two)
                    elif i == 2:
                        await bot.delete_message(msg.chat.id, user.three)
                #                                  text="Возвращаемся в главное меню 🚶‍♀️")
                await bot.delete_message(msg.chat.id, msg.message_id)
                await bot.delete_message(msg.chat.id, user.mainMes)

        else:
            # data = await state.get_data()
            if msg.text == '⬅️ Назад' or msg.text == '⬅️ Артка':
                # print(data.get('page'))
                if str(user.page) == '1':
                    # await bot.edit_message_text('Вы долистали до нижней границы 😔', msg.chat.id, data.get('main'))
                    pass
                else:
                    page = user.page
                    page = int(page) - 1
                    # async with state.proxy() as data:
                    #     data['page'] = str(int(data.get('page')) - 1)
                    user.page = str(page)
                    for i in range(int(user.ziro)):
                        if i == 0:
                            await bot.delete_message(msg.chat.id, user.one)
                        elif i == 1:
                            await bot.delete_message(msg.chat.id, user.two)
                        elif i == 2:
                            await bot.delete_message(msg.chat.id, user.three)
                    if user.genre == None:
                        if user.fre == True:
                            books = session.query(Book).filter(Book.amount != 0).filter(Book.amount != '0').all()
                        else:
                            books = session.query(Book).all()
                    else:
                        if user.fre == True:
                            books = session.query(Book).filter(Book.amount != 0).filter(Book.amount != '0').filter(
                                Book.genre == user.genre).all()
                        else:
                            books = session.query(Book).filter(Book.genre == user.genre).all()
                    count = 0
                    c = 0
                    for i in books:
                        count += 1
                        if (page - 1) * 3 < count and page * 3 >= count:
                            c += 1
                            more = {'rus': InlineKeyboardButton('Подробнее 🧐', url=i.link),
                                    'tat': InlineKeyboardButton('Тәфсилле 🧐', url=i.link)}
                            take = {
                                'rus': InlineKeyboardButton('🤲🏻 Взять', callback_data=f'date_choose_{i.book_id}'),
                                'tat': InlineKeyboardButton('🤲🏻 Алырга', callback_data=f'date_choose_{i.book_id}')}
                            hurry = {'rus': InlineKeyboardButton('🚴‍♀️ Поторопить',
                                                                 callback_data=f"date_choose_{i.book_id}"),
                                     'tat': InlineKeyboardButton('🚴‍♀️ Ашыктыру',
                                                                 callback_data=f"date_choose_{i.book_id}")}
                            if i.amount != 0 and i.amount != '0':
                                kl = InlineKeyboardMarkup(row_width=2).add(take[user.lang], more[user.lang])
                            else:
                                kl = InlineKeyboardMarkup(row_width=2).add(hurry[user.lang], more[user.lang])
                            a = await bot.send_message(msg.chat.id, str(count) + ' - '
                                                                                 '*Название:* ' + i.name + '\n*      Жанр:* ' + i.genre + '\n*      Автор:* ' + i.author,
                                                       parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
                            if c == 1:
                                user.one = a.message_id
                            if c == 2:
                                user.two = a.message_id
                            if c == 3:
                                user.three = a.message_id
                            if c == 3:
                                break
                    # async with state.proxy() as data:
                    #     data['0'] = str(c)
                    user.ziro = str(c)
                await bot.delete_message(msg.chat.id, msg.message_id)
                session.add(user)
                session.commit()
            elif msg.text == 'Дальше ➡️' or msg.text == 'Алга ➡️':
                session = create_session()
                user = session.query(User).filter(User.tg_id == msg.chat.id).first()
                # page = data.get('page')
                if user.genre == None:
                    if user.fre == True:
                        books = session.query(Book).filter(Book.amount != 0).filter(Book.amount != '0').all()
                    else:
                        books = session.query(Book).all()
                else:
                    if user.fre == True:
                        books = session.query(Book).filter(Book.amount != 0).filter(Book.amount != '0').filter(
                            Book.genre == user.genre).all()
                        # print(data.get('genre'))
                    else:
                        books = session.query(Book).filter(Book.genre == user.genre).all()
                        # print(data.get('genre'))

                if int(user.page) * 3 >= len(books):
                    # await bot.edit_message_text('Вы долистали до нижней границы 😔', msg.chat.id, data.get('main'))
                    # await bot.delete_message(msg.chat.id, msg.message_id)
                    pass
                else:
                    for i in range(int(user.ziro)):
                        if i == 0:
                            await bot.delete_message(msg.chat.id, user.one)
                        elif i == 1:
                            await bot.delete_message(msg.chat.id, user.two)
                        elif i == 2:
                            await bot.delete_message(msg.chat.id, user.three)
                    page = user.page
                    page = int(page) + 1
                    # async with state.proxy() as data:
                    #     data['page'] = str(int(data.get('page')) + 1)
                    user.page = page
                    count = 0
                    c = 0
                    for i in books:
                        count += 1
                        if (page - 1) * 3 < count and page * 3 >= count:
                            # if i.genre == user.genre or user.genre == None:
                            c += 1
                            more = {'rus': InlineKeyboardButton('Подробнее 🧐', url=i.link),
                                    'tat': InlineKeyboardButton('Тәфсилле 🧐', url=i.link)}
                            take = {
                                'rus': InlineKeyboardButton('🤲🏻 Взять', callback_data=f'date_choose_{i.book_id}'),
                                'tat': InlineKeyboardButton('🤲🏻 Алырга', callback_data=f'date_choose_{i.book_id}')}
                            hurry = {'rus': InlineKeyboardButton('🚴‍♀️ Поторопить',
                                                                 callback_data=f"date_choose_{i.book_id}"),
                                     'tat': InlineKeyboardButton('🚴‍♀️ Ашыктыру',
                                                                 callback_data=f"date_choose_{i.book_id}")}
                            if i.amount != 0 and i.amount != '0':
                                kl = InlineKeyboardMarkup(row_width=2).add(take[user.lang], more[user.lang])
                            else:
                                kl = InlineKeyboardMarkup(row_width=2).add(hurry[user.lang], more[user.lang])
                            a = await bot.send_message(msg.chat.id, str(count) + ' - '
                                                                                 '*Название:* ' + i.name + '\n*      Жанр:* ' + i.genre + '\n*      Автор:* ' + i.author,
                                                       parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
                            # async with state.proxy() as data:
                            #     data[str(count - (page - 1) * 3)] = a.message_id
                            if c == 1:
                                user.one = a.message_id
                            if c == 2:
                                user.two = a.message_id
                            if c == 3:
                                user.three = a.message_id
                            if c == 3:
                                break
                    # async with state.proxy() as data:
                    #     data['0'] = str(c)
                    user.ziro = str(c)
                    session.add(user)
                    session.commit()
                await bot.delete_message(msg.chat.id, msg.message_id)
            else:

                books = session.query(Book).filter(Book.name == msg.text).first()
                if books == None:
                    await bot.send_message(msg.chat.id, 'К сожелению у нас нет такой книги 😔')
                else:
                    more = {'rus': InlineKeyboardButton('Подробнее 🧐', url=books.link),
                            'tat': InlineKeyboardButton('Тәфсилле 🧐', url=books.link)}
                    take = {
                        'rus': InlineKeyboardButton('🤲🏻 Взять', callback_data=f'date_choose_{books.book_id}'),
                        'tat': InlineKeyboardButton('🤲🏻 Алырга', callback_data=f'date_choose_{books.book_id}')}
                    hurry = {'rus': InlineKeyboardButton('🚴‍♀️ Поторопить',
                                                         callback_data=f"date_choose_{books.book_id}"),
                             'tat': InlineKeyboardButton('🚴‍♀️ Ашыктыру',
                                                         callback_data=f"date_choose_{books.book_id}")}
                    if books.amount != '0' and books.amount != 0:
                        kl = InlineKeyboardMarkup(row_width=2).add(take[user.lang], more[user.lang])
                    else:
                        kl = InlineKeyboardMarkup(row_width=2).add(hurry[user.lang], more[user.lang])
                    await bot.send_message(msg.chat.id,
                                           'Кажется у нас есть то, что вы ищете 🥳\n' + '1 - ' + '*Название:* ' + books.name + '\n*      Жанр:* ' + books.genre + '\n*      Автор:* ' + books.author,
                                           parse_mode=ParseMode.MARKDOWN, reply_markup=kl)
                await bot.delete_message(msg.chat.id, msg.message_id)


@dp.message_handler(state=Login.login)
async def login(msg: types.Message, state: FSMContext):
    login = msg.text.split()
    if msg.text == for_admin:
        session = create_session()
        user = User()
        user.role = 'admin'
        user.for_admin = '0'
        await bot.send_message(msg.chat.id, "Доброе время суток, теперь у вас есть права админа", reply_markup=adm_keyb)
        session.add(user)
        session.commit()
        return
    elif login[2].lower() == 'учитель' or login[2].lower() == 'воспитатель':
        async with state.proxy() as data:
            data['login'] = login
        markup_request = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
            KeyboardButton('Поделиться своим номером ☎️', request_contact=True)
        )
        await bot.send_message(msg.chat.id,
                               f"Отлично, {login[1]}️. ☺\nОсталось отправить свой номер телефона. Для этого нажмите кнопку ниже.️",
                               reply_markup=markup_request)
        await Login.phone.set()
    elif (len(login) != 3) or (not login[0].isalpha()) or (not login[1].isalpha()) or not login[2][:-1].isdigit() or not \
            login[2][-1].isalpha():
        await bot.send_message(msg.chat.id,
                               'Видимо вы ошиблись в введённых данных. 😔 \nНапоминаю, что необходимо ввести своё имя, фамилию и класс через пробел в формате *Иван Иванов 10А.*',
                               parse_mode=ParseMode.MARKDOWN)
    else:
        async with state.proxy() as data:
            data['login'] = login
        markup_request = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
            KeyboardButton('Поделиться своим номером ☎️', request_contact=True)
        )
        await bot.send_message(msg.chat.id,
                               f"Отлично, {login[1]}️. ☺\nОсталось отправить свой номер телефона. Для этого нажмите кнопку ниже.️",
                               reply_markup=markup_request)
        await Login.phone.set()


@dp.message_handler(state=Login.phone, content_types=ContentType.CONTACT)
async def getting_password(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    login = data.get('login')
    name = login[1]
    surname = login[0]
    clas = login[2]
    session = create_session()
    new_user = User()
    new_user.tg_id = msg.chat.id
    new_user.name = name
    new_user.surname = surname
    new_user.clas = clas
    new_user.phone = msg.contact.phone_number
    new_user.role = 'user'
    new_user.hurry = 0
    new_user.xp = 0
    session.add(new_user)
    session.commit()
    await state.finish()
    text = {'rus': 'Здравствуйте', 'tat': 'Исэнмесез'}
    await bot.edit_message_text(f"{text[new_user.lang]}, {new_user.name} ✌️", reply_markup=main_menu)
    # await Us.use.set()


@dp.message_handler(state=AddBook.name)
async def ad(msg: types.Message, state: FSMContext):
    name = msg.text
    if 'litres.ru' in name:
        data1 = by_link(msg.text)
        async with state.proxy() as data:
            data['name'] = data1['name']
            data['genree'] = data1['genre']
            data['author'] = data1['author']
            data['description'] = data1['description']
        await AddBook.amount.set()
        await bot.send_message(msg.chat.id, 'Напишите пожалуйста *количество* книг',
                               parse_mode=ParseMode.MARKDOWN)
    else:
        async with state.proxy() as data:
            data['name'] = name
        await AddBook.genre.set()
        await bot.send_message(msg.chat.id, 'Напишите пожалуйста *жанр* книги',
                               parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(state=AddBook.genre)
async def ad(msg: types.Message, state: FSMContext):
    genre = msg.text
    async with state.proxy() as data:
        data['genree'] = genre
    await AddBook.author.set()
    await bot.send_message(msg.chat.id, 'Напишите пожалуйста *автора* книги',
                           parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(state=AddBook.author)
async def ad(msg: types.Message, state: FSMContext):
    author = msg.text
    async with state.proxy() as data:
        data['author'] = author
    await AddBook.description.set()
    await bot.send_message(msg.chat.id, 'Напишите пожалуйста *небольшое описание* для книги',
                           parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(state=AddBook.description)
async def ad(msg: types.Message, state: FSMContext):
    description = msg.text
    async with state.proxy() as data:
        data['description'] = description
    await AddBook.amount.set()
    await bot.send_message(msg.chat.id, 'Напишите пожалуйста *количество* книг',
                           parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(state=AddBook.amount)
async def ad(msg: types.Message, state: FSMContext):
    amount = msg.text
    async with state.proxy() as data:
        data['amount'] = amount
    await AddBook.sog.set()
    sog = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(KeyboardButton('Да ✅'),
                                                                     KeyboardButton('Нет ❌'))
    new_book = Book()
    data = await state.get_data()
    new_book.name = data.get('name')
    new_book.genre = data.get('genree')
    new_book.author = data.get('author')
    new_book.description = data.get('description')
    new_book.amount = data.get('amount')
    await bot.send_message(msg.chat.id,
                           f'Название книги: {new_book.name}\n\nЖанр: {new_book.genre}\n\nАвтор: {new_book.author}\n\nОписание: {new_book.description}\n\nКоличество книг: {new_book.amount}')
    await bot.send_message(msg.chat.id, 'Подтверждаем операцию?',
                           reply_markup=sog)


@dp.message_handler(state=AddBook.sog)
async def ad(msg: types.Message, state: FSMContext):
    sog = msg.text
    if sog == 'Да ✅':
        session = create_session()
        new_book = Book()
        data = await state.get_data()
        new_book.name = data.get('name')
        new_book.genre = f"{data.get('genree')[0].upper()}{data.get('genree')[1:]}"
        new_book.author = data.get('author')
        new_book.description = data.get('description')
        new_book.amount = data.get('amount')
        session.add(new_book)
        session.commit()
        chn = await bot.send_message(chanel,
                                     f'Добавлена новая книга! 🎉\n\n*{new_book.name}*\n\n{new_book.description}\n\n*Автор*: {new_book.author}\n*Жанр*: {new_book.genre}\n\n Взять книгу можно по [этой ссылке](https://t.me/SchoolLibraryLi1_bot?start=take_book_{new_book.book_id})',
                                     parse_mode=ParseMode.MARKDOWN)
        new_book.link = f"https://t.me/lyceum_library/{chn.message_id}"
        new_book.mes_id = chn.message_id
        session.add(new_book)
        session.commit()
        await bot.send_message(msg.chat.id, 'Операция успешно выполнена', reply_markup=adm_keyb)
    else:
        await bot.send_message(msg.chat.id, 'Операция успешно отменена', reply_markup=adm_keyb)
    await state.finish()


async def hurryz():
    session = create_session()
    users = session.query(User).all()
    for i in users:
        i.hurry = 0
        session.add(i)
    session.commit()


async def scheduler():
    aioschedule.every().day.at('00:00').do(hurryz)
    while True:
        await asyncio.sleep(1)
        await aioschedule.run_pending()


async def on_startup(x):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    global_init("db.sqlite")
    start_polling(dp, on_startup=on_startup)

# Мы школьники
