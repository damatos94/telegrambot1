import telebot
from telebot import types
import random
import time
import requests
import json
import base64
from datetime import datetime, timedelta
import hashlib
import urllib.parse
import os  # ← для переменных окружения Bothost

# ====================== ТОКЕНЫ ИЗ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ (Bothost) ======================
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден! Добавь переменную BOT_TOKEN в настройках Bothost.")

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    print("⚠️ OPENAI_API_KEY не найден. Чат с AI будет отключён.")

# Создаем экземпляр бота
bot = telebot.TeleBot(BOT_TOKEN)

# =============== РАСШИРЕННЫЕ ВИКТОРИНЫ ===============
history_quiz = [
    {"question": "В каком году началась Вторая мировая война?", "options": ["1938", "1939", "1940", "1941"], "correct": 1},
    {"question": "Кто был первым президентом США?", "options": ["Джордж Вашингтон", "Томас Джефферсон", "Авраам Линкольн", "Джон Адамс"], "correct": 0},
    {"question": "В каком году пал Берлин?", "options": ["1944", "1945", "1946", "1947"], "correct": 1},
    {"question": "Кто был последним императором России?", "options": ["Александр II", "Александр III", "Николай I", "Николай II"], "correct": 3},
    {"question": "В каком году началась Первая мировая война?", "options": ["1913", "1914", "1915", "1916"], "correct": 1},
    {"question": "Столица Византийской империи?", "options": ["Афины", "Рим", "Константинополь", "Александрия"], "correct": 2},
    {"question": "В каком году была открыта Америка?", "options": ["1491", "1492", "1493", "1494"], "correct": 1},
    {"question": "Кто построил первую пирамиду в Египте?", "options": ["Хеопс", "Джосер", "Хефрен", "Микерин"], "correct": 1},
]
geography_quiz = [
    {"question": "Какая самая длинная река в мире?", "options": ["Амазонка", "Нил", "Миссисипи", "Янцзы"], "correct": 1},
    {"question": "Столица Австралии?", "options": ["Сидней", "Мельбурн", "Канберра", "Перт"], "correct": 2},
    {"question": "Самая высокая гора в мире?", "options": ["К2", "Эверест", "Аннапурна", "Макалу"], "correct": 1},
    {"question": "В какой стране находится город Мачу-Пикчу?", "options": ["Боливия", "Перу", "Эквадор", "Колумбия"], "correct": 1},
    {"question": "Самое глубокое озеро в мире?", "options": ["Байкал", "Танганьика", "Каспийское море", "Верхнее"], "correct": 0},
    {"question": "Сколько часовых поясов в России?", "options": ["9", "10", "11", "12"], "correct": 2},
    {"question": "Столица Канады?", "options": ["Торонто", "Ванкувер", "Монреаль", "Оттава"], "correct": 3},
    {"question": "Самая маленькая страна в мире?", "options": ["Монако", "Ватикан", "Сан-Марино", "Лихтенштейн"], "correct": 1},
]
science_quiz = [
    {"question": "Сколько хромосом у человека?", "options": ["44", "46", "48", "50"], "correct": 1},
    {"question": "Химический символ золота?", "options": ["Go", "Gd", "Au", "Ag"], "correct": 2},
    {"question": "Скорость света в вакууме?", "options": ["300,000 км/с", "299,792,458 м/с", "300,000,000 м/с", "Все варианты верны"], "correct": 3},
    {"question": "Кто открыл пенициллин?", "options": ["Луи Пастер", "Александр Флеминг", "Мария Кюри", "Грегор Мендель"], "correct": 1},
    {"question": "Самый твердый природный материал?", "options": ["Алмаз", "Кварц", "Корунд", "Графит"], "correct": 0},
    {"question": "Какая планета ближайшая к Солнцу?", "options": ["Венера", "Земля", "Меркурий", "Марс"], "correct": 2},
    {"question": "Формула воды?", "options": ["H2O", "CO2", "NaCl", "CH4"], "correct": 0},
    {"question": "Единица измерения электрического тока?", "options": ["Вольт", "Ампер", "Ом", "Ватт"], "correct": 1},
]
it_quiz = [
    {"question": "Кто создал язык программирования Python?", "options": ["Линус Торвальдс", "Гвидо ван Россум", "Деннис Ритчи", "Джеймс Гослинг"], "correct": 1},
    {"question": "Что означает HTML?", "options": ["Hypertext Markup Language", "High Tech Modern Language", "Home Tool Markup Language", "Hyperlink Text Management Language"], "correct": 0},
    {"question": "В каком году был создан JavaScript?", "options": ["1993", "1995", "1997", "1999"], "correct": 1},
    {"question": "Что такое API?", "options": ["Application Programming Interface", "Advanced Programming Instructions", "Automated Program Integration", "Application Process Indicator"], "correct": 0},
    {"question": "Кто основал компанию Microsoft?", "options": ["Стив Джобс", "Билл Гейтс", "Ларри Пейдж", "Марк Цукерберг"], "correct": 1},
    {"question": "Какой порт использует HTTP по умолчанию?", "options": ["21", "22", "80", "443"], "correct": 2},
    {"question": "Что означает SQL?", "options": ["Structured Query Language", "Simple Query Language", "System Query Language", "Standard Query Language"], "correct": 0},
    {"question": "В каком году был создан Linux?", "options": ["1989", "1991", "1993", "1995"], "correct": 1},
]
literature_quiz = [
    {"question": "Кто написал 'Войну и мир'?", "options": ["Достоевский", "Толстой", "Тургенев", "Чехов"], "correct": 1},
    {"question": "Главный герой романа 'Преступление и наказание'?", "options": ["Раскольников", "Безухов", "Онегин", "Печорин"], "correct": 0},
    {"question": "Кто автор 'Гамлета'?", "options": ["Байрон", "Шекспир", "Мильтон", "Шелли"], "correct": 1},
    {"question": "В каком году родился Пушкин?", "options": ["1798", "1799", "1800", "1801"], "correct": 1},
    {"question": "Кто написал 'Мастер и Маргарита'?", "options": ["Булгаков", "Пастернак", "Солженицын", "Шолохов"], "correct": 0},
    {"question": "Автор 'Анны Карениной'?", "options": ["Тургенев", "Толстой", "Гончаров", "Лесков"], "correct": 1},
    {"question": "Кто написал 'Евгений Онегин'?", "options": ["Лермонтов", "Пушкин", "Некрасов", "Фет"], "correct": 1},
    {"question": "Автор 'Отцы и дети'?", "options": ["Толстой", "Достоевский", "Тургенев", "Гоголь"], "correct": 2},
]
all_quizzes = {
    "🏛️ История": history_quiz,
    "🌍 География": geography_quiz,
    "🔬 Наука": science_quiz,
    "💻 IT": it_quiz,
    "📚 Литература": literature_quiz
}

# =============== РАСШИРЕННЫЕ ЦИТАТЫ ===============
motivational_quotes = [
    "Не откладывайте на завтра то, что можете сделать сегодня! 💪",
    "Каждый день - это новая возможность стать лучше! ✨",
    "Верьте в себя, и все остальное встанет на свои места! 🌟",
    "Успех - это не конечная точка, а путешествие! 🚀",
    "Самый трудный шаг - это первый шаг! 👣",
    "Мечты не имеют срока годности! 🌈",
    "Будьте собой, все остальные роли уже заняты! 🎭",
    "Падать не страшно, страшно не вставать! 💥",
    "Возможности не приходят, их создают! ⚡",
    "Единственный способ делать великие дела - любить то, что ты делаешь! ❤️",
    "Не ждите идеального момента, берите момент и делайте его идеальным! ⏰",
    "Сильные люди делают трудный выбор и принимают его последствия! 💎",
    "Ваше время ограничено, не тратьте его, живя чужой жизнью! ⌛",
    "Препятствия не должны останавливать вас! 🔥",
    "Неудача - это просто возможность начать заново, но уже более разумно! 🧠"
]
wisdom_quotes = [
    "Знание - сила, но знание того, как применить его - мудрость! 🧭",
    "Не судите человека по его успехам, судите по тому, как он преодолевает неудачи! ⚖️",
    "Жизнь - это 10% того, что с вами происходит, и 90% того, как вы на это реагируете! 📊",
    "Лучшее время посадить дерево было 20 лет назад. Второе лучшее время - сейчас! 🌳",
    "Мудрость приходит не с возрастом, а с принятием ответственности! 🎯",
    "Не бойтесь медленно идти, бойтесь стоять на месте! 🚶‍♂️",
    "Самая большая комната в мире - это комната для улучшений! 🏠",
    "Образование - это то, что остается после того, как забываешь все, чему учился в школе! 🎓",
]
funny_quotes = [
    "Программист - это человек, который решает проблемы, о которых вы не знали! 👨‍💻",
    "Кофе и код - все, что нужно для счастья! ☕",
    "Багов нет, это фичи! 🐛",
    "Работает на моей машине! 🖥️",
    "99 багов в коде, исправил один баг, стало 127 багов в коде! 🔢",
    "Лучший способ отладить код - объяснить его резиновой уточке! 🦆",
    "Искусственный интеллект - это когда компьютер думает, что он умнее человека! 🤖",
    "Два типа людей: те, кто делает бэкапы, и те, кто будет их делать! 💾"
]

# =============== ИГРЫ И РАЗВЛЕЧЕНИЯ ===============
riddles = [
    {"question": "Что можно сломать, даже не касаясь?", "answer": "обещание", "hint": "Это не физический объект"},
    {"question": "Что имеет ключи, но не может открыть замки?", "answer": "пианино", "hint": "Музыкальный инструмент"},
    {"question": "Что растет вниз головой?", "answer": "сосулька", "hint": "Зимнее явление"},
    {"question": "Что можно поймать, но нельзя бросить?", "answer": "насморк", "hint": "Связано со здоровьем"},
    {"question": "У кого есть шея, но нет головы?", "answer": "бутылка", "hint": "Емкость для жидкости"},
    {"question": "Что бежит, но никогда не устает?", "answer": "время", "hint": "Абстрактное понятие"},
    {"question": "Что всегда идет, но никогда не приходит?", "answer": "завтра", "hint": "Временной период"},
    {"question": "Что можно увидеть с закрытыми глазами?", "answer": "сон", "hint": "Происходит ночью"}
]
jokes = [
    "- Доктор, у меня проблемы с памятью!\n- С каких пор?\n- С каких пор что? 🤔",
    "Программист ложится спать в 3 ночи и ставит на тумбочку два стакана: один с водой на случай, если захочется пить, второй пустой - на случай, если не захочется! 💤",
    "- Как дела в IT?\n- Как в больнице: работает только реанимация! 🏥",
    "Жена программиста просит:\n- Дорогой, сходи в магазин за хлебом, а если будут яйца - купи десяток.\nПрограммист приходит домой с 10 батонами хлеба! 🍞",
    "- Почему программисты путают Хэллоуин и Рождество?\n- Потому что Oct 31 = Dec 25! 🎃",
    "Системный администратор - это человек, который приходит в ваш офис, чтобы починить принтер, и случайно сломать интернет! 🖨️",
    "- В чем разница между программистом и пользователем?\n- Программист думает, что стакан наполовину полон. Пользователь думает, что стакан сломан! 🥤"
]
facts = [
    "🐙 У осьминога три сердца и голубая кровь!",
    "🦒 Жираф может обойтись без воды дольше верблюда!",
    "🧠 Человеческий мозг содержит около 86 миллиардов нейронов!",
    "🌍 За одну секунду Земля проходит 30 километров вокруг Солнца!",
    "🐝 Пчелы могут видеть ультрафиолетовые цвета!",
    "🦘 Кенгуру не могут ходить назад!",
    "🌙 Луна удаляется от Земли на 3.8 см каждый год!",
    "🐧 Пингвины могут прыгать на высоту до 3 метров!",
    "🦈 Акулы существуют дольше деревьев!",
    "🍯 Мед никогда не портится!",
    "🐘 Слоны боятся пчел!",
    "🌈 Морковь изначально была фиолетового цвета!",
    "🧊 Горячая вода замерзает быстрее холодной!",
    "🦎 Гекконы могут бегать по воде!",
    "🌋 На Венере день длиннее года!"
]

# =============== УТИЛИТЫ ===============
translation_dict = {
    "hello": "привет", "goodbye": "до свидания", "thank you": "спасибо",
    "please": "пожалуйста", "yes": "да", "no": "нет", "water": "вода",
    "food": "еда", "house": "дом", "car": "машина", "book": "книга",
    "time": "время", "money": "деньги", "work": "работа", "love": "любовь",
    "friend": "друг", "family": "семья", "cat": "кот", "dog": "собака"
}

def generate_simple_qr_link(text):
    encoded_text = urllib.parse.quote(text)
    return f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={encoded_text}"

def calculate(expression):
    try:
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in expression):
            return "❌ Недопустимые символы в выражении"
        result = eval(expression)
        return f"🧮 {expression} = {result}"
    except ZeroDivisionError:
        return "❌ Деление на ноль!"
    except:
        return "❌ Ошибка в выражении"

def get_free_weather(city):
    try:
        url = f"http://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            temp = current['temp_C']
            feels_like = current['FeelsLikeC']
            humidity = current['humidity']
            desc = current['weatherDesc'][0]['value']
            wind = current['windspeedKmph']
            pressure = current['pressure']
            weather_code = int(current['weatherCode'])
            if weather_code in [113]:
                emoji = "☀️"
            elif weather_code in [116, 119, 122]:
                emoji = "⛅"
            elif weather_code in [143, 248, 260]:
                emoji = "🌫️"
            elif weather_code in [176, 263, 266, 281, 284, 293, 296, 299, 302, 305, 308, 311, 314, 317, 320, 323, 326, 329, 332, 335, 338, 350, 353, 356, 359, 362, 365, 368, 371, 374, 377, 386, 389, 392, 395]:
                emoji = "🌧️"
            elif weather_code in [179, 182, 185, 227, 230, 323, 326, 329, 332, 335, 338, 368, 371, 374, 377, 392, 395]:
                emoji = "🌨️"
            else:
                emoji = "☁️"
            return f"""
{emoji} Погода в {city}
🌡️ Температура: {temp}°C (ощущается как {feels_like}°C)
📝 Описание: {desc}
💧 Влажность: {humidity}%
🌪️ Ветер: {wind} км/ч
🔽 Давление: {pressure} мбар
"""
        else:
            return "❌ Город не найден или сервис недоступен"
    except:
        return "❌ Ошибка получения данных о погоде"

def chat_gpt(message_text):
    if not OPENAI_API_KEY:
        return "❌ Чат с AI временно недоступен (API-ключ не настроен в Bothost)."
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": message_text}]
        }
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"❌ Ошибка OpenAI: {response.status_code}"
    except Exception as e:
        return f"❌ Ошибка: {str(e)}"

# =============== ХРАНИЛИЩЕ ДАННЫХ ===============
user_data = {}

# =============== ОБРАБОТЧИКИ КОМАНД ===============
@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "Друг"
    if user_id not in user_data:
        user_data[user_id] = {
            'name': user_name,
            'quiz_scores': {name: 0 for name in all_quizzes.keys()},
            'total_score': 0,
            'commands_used': 0,
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'riddles_solved': 0,
            'calculations_done': 0,
            'chat_interactions': 0
        }
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        "🎯 Викторины", "💡 Мотивация", "🎲 Случайное число", "📊 Статистика",
        "🌤 Погода", "🧩 Загадки", "😂 Анекдоты", "🤓 Факты",
        "🧮 Калькулятор", "🔤 Переводчик", "📱 QR код", "🎮 Игры",
        "ℹ️ Помощь", "🔮 Гадание", "🤖 Чат с AI"
    ]
    for i in range(0, len(buttons), 2):
        markup.row(buttons[i], buttons[i+1] if i+1 < len(buttons) else "")
    welcome_text = f"""
🤖 Добро пожаловать, {user_name}!
🎉 Я - супер-бот с множеством функций:
🎯 Викторины по 5 темам (история, география, наука, IT, литература)
🌤 Бесплатная погода для любого города
💡 Мотивационные цитаты и мудрость
🧩 Загадки и головоломки
😂 Анекдоты и интересные факты
🧮 Калькулятор и переводчик
📱 Генератор QR кодов
🎮 Мини-игры и развлечения
🔮 Гадания и предсказания
🤖 Чат с искусственным интеллектом
Выберите что вас интересует! ⬇️
"""
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_message(message):
    help_text = """
📋 Полный список команд:
🎯 ВИКТОРИНЫ:
/quiz - выбрать викторину
/history - викторина по истории
/geography - викторина по географии
/science - викторина по науке
/it - викторина по IT
/literature - викторина по литературе
🌤 ПОГОДА:
/weather - актуальная погода
/forecast - прогноз погоды
💡 МОТИВАЦИЯ:
/motivation - мотивационная цитата
/wisdom - мудрая мысль
/joke - анекдот
🎮 РАЗВЛЕЧЕНИЯ:
/riddle - загадка
/fact - интересный факт
/random - случайное число
/dice - бросить кубик
/coin - подбросить монетку
/fortune - гадание
🛠 УТИЛИТЫ:
/calc - калькулятор
/translate - переводчик
/qr - генератор QR кода
/stats - ваша статистика
/chat - чат с AI
Или просто используйте кнопки меню! 🎯
"""
    bot.send_message(message.chat.id, help_text)

# =============== ВИКТОРИНЫ ===============
@bot.message_handler(commands=['quiz'])
def quiz_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = []
    for quiz_name in all_quizzes.keys():
        callback_data = f"select_quiz_{quiz_name.split()[1].lower()}"
        buttons.append(types.InlineKeyboardButton(quiz_name, callback_data=callback_data))
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            markup.row(buttons[i], buttons[i+1])
        else:
            markup.row(buttons[i])
    markup.row(types.InlineKeyboardButton("🎲 Случайная викторина", callback_data="select_quiz_random"))
    bot.send_message(message.chat.id, "🎯 Выберите тему викторины:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('select_quiz_'))
def select_quiz(call):
    quiz_type = call.data.replace('select_quiz_', '')
    if quiz_type == 'random':
        quiz_name = random.choice(list(all_quizzes.keys()))
    else:
        quiz_map = {
            'история': '🏛️ История',
            'география': '🌍 География',
            'наука': '🔬 Наука',
            'it': '💻 IT',
            'литература': '📚 Литература'
        }
        quiz_name = quiz_map.get(quiz_type, '🏛️ История')
    start_quiz(call.message, quiz_name)
    bot.answer_callback_query(call.id)

def start_quiz(message, quiz_type):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {
            'quiz_scores': {name: 0 for name in all_quizzes.keys()},
            'total_score': 0,
            'commands_used': 0,
            'chat_interactions': 0
        }
    questions = all_quizzes[quiz_type]
    question_data = random.choice(questions)
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = []
    for i, option in enumerate(question_data['options']):
        callback_data = f"quiz_{i}_{question_data['correct']}_{quiz_type}"
        buttons.append(types.InlineKeyboardButton(option, callback_data=callback_data))
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            markup.row(buttons[i], buttons[i+1])
        else:
            markup.row(buttons[i])
    bot.send_message(message.chat.id, f"{quiz_type}\n\n❓ {question_data['question']}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('quiz_') and len(call.data.split('_')) >= 4)
def quiz_callback(call):
    try:
        user_id = call.from_user.id
        data = call.data.split('_')
        selected_answer = int(data[1])
        correct_answer = int(data[2])
        quiz_type = '_'.join(data[3:])
        if user_id not in user_data:
            user_data[user_id] = {
                'quiz_scores': {name: 0 for name in all_quizzes.keys()},
                'total_score': 0,
                'commands_used': 0,
                'chat_interactions': 0
            }
        if selected_answer == correct_answer:
            user_data[user_id]['quiz_scores'][quiz_type] += 1
            user_data[user_id]['total_score'] += 1
            bot.answer_callback_query(call.id, "✅ Правильно! +1 балл")
            result_text = "🎉 Отлично! Правильный ответ!"
            emoji = "🎯"
        else:
            bot.answer_callback_query(call.id, "❌ Неправильно")
            result_text = "😔 Неправильно. Но не сдавайтесь!"
            emoji = "💪"
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        markup = types.InlineKeyboardMarkup()
        btn_again = types.InlineKeyboardButton(f"🔄 Еще {quiz_type}", callback_data=f"select_quiz_{quiz_type.split()[1].lower()}")
        btn_menu = types.InlineKeyboardButton("📚 Другая тема", callback_data="select_quiz_menu")
        markup.row(btn_again, btn_menu)
        bot.send_message(
            call.message.chat.id,
            f"{emoji} {result_text}\n\nВаш счет в {quiz_type}: {user_data[user_id]['quiz_scores'][quiz_type]}\nОбщий счет: {user_data[user_id]['total_score']}",
            reply_markup=markup
        )
    except Exception as e:
        bot.answer_callback_query(call.id, "❌ Ошибка обработки ответа")
        bot.send_message(call.message.chat.id, "😔 Произошла ошибка. Попробуйте еще раз!")

@bot.callback_query_handler(func=lambda call: call.data == 'select_quiz_menu')
def back_to_quiz_menu(call):
    quiz_menu(call.message)
    bot.answer_callback_query(call.id)

# =============== ПОГОДА ===============
@bot.message_handler(commands=['weather'])
def weather_command(message):
    bot.send_message(message.chat.id, "🌤 Введите название города:")
    bot.register_next_step_handler(message, get_weather_city)

def get_weather_city(message):
    city = message.text.strip()
    if not city:
        bot.send_message(message.chat.id, "❌ Пожалуйста, введите название города!")
        return
    weather_info = get_free_weather(city)
    bot.send_message(message.chat.id, weather_info)

# =============== МОТИВАЦИЯ И ЦИТАТЫ ===============
@bot.message_handler(commands=['motivation'])
def motivation_command(message):
    quote = random.choice(motivational_quotes)
    bot.send_message(message.chat.id, f"💡 {quote}")

@bot.message_handler(commands=['wisdom'])
def wisdom_command(message):
    quote = random.choice(wisdom_quotes)
    bot.send_message(message.chat.id, f"🧠 {quote}")

@bot.message_handler(commands=['joke'])
def joke_command(message):
    joke = random.choice(jokes)
    bot.send_message(message.chat.id, f"😂 {joke}")

# =============== РАЗВЛЕЧЕНИЯ ===============
@bot.message_handler(commands=['riddle'])
def riddle_command(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {
            'name': message.from_user.first_name or "Друг",
            'quiz_scores': {name: 0 for name in all_quizzes.keys()},
            'total_score': 0,
            'commands_used': 0,
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'riddles_solved': 0,
            'calculations_done': 0,
            'chat_interactions': 0
        }
    riddle = random.choice(riddles)
    user_data[user_id]['current_riddle'] = riddle
    user_data[user_id]['riddle_attempts'] = 0
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📝 Подсказка", callback_data="riddle_hint"))
    markup.add(types.InlineKeyboardButton("🙌 Сдаться", callback_data="riddle_giveup"))
    bot.send_message(
        message.chat.id,
        f"🧩 Загадка:\n{riddle['question']}\n\nНапишите ответ или используйте кнопки:",
        reply_markup=markup
    )
    bot.register_next_step_handler(message, check_riddle_answer)

def check_riddle_answer(message):
    user_id = message.from_user.id
    if user_id not in user_data or 'current_riddle' not in user_data[user_id]:
        bot.send_message(message.chat.id, "❌ Нет активной загадки! Используйте /riddle")
        return
    user_answer = message.text.strip().lower()
    correct_answer = user_data[user_id]['current_riddle']['answer'].lower()
    user_data[user_id]['riddle_attempts'] += 1
    if user_answer == correct_answer:
        user_data[user_id]['riddles_solved'] += 1
        user_data[user_id]['total_score'] += 2
        bot.send_message(
            message.chat.id,
            f"🎉 Правильно! Ответ: {correct_answer}\n+2 балла!\nРешено загадок: {user_data[user_id]['riddles_solved']}"
        )
        del user_data[user_id]['current_riddle']
        del user_data[user_id]['riddle_attempts']
    else:
        if user_data[user_id]['riddle_attempts'] >= 3:
            bot.send_message(
                message.chat.id,
                f"😔 Вы исчерпали попытки! Правильный ответ: {correct_answer}"
            )
            del user_data[user_id]['current_riddle']
            del user_data[user_id]['riddle_attempts']
        else:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("📝 Подсказка", callback_data="riddle_hint"))
            markup.add(types.InlineKeyboardButton("🙌 Сдаться", callback_data="riddle_giveup"))
            bot.send_message(
                message.chat.id,
                f"❌ Неправильно! Попробуйте еще раз (попыток осталось: {3 - user_data[user_id]['riddle_attempts']}):",
                reply_markup=markup
            )
            bot.register_next_step_handler(message, check_riddle_answer)

@bot.callback_query_handler(func=lambda call: call.data in ['riddle_hint', 'riddle_giveup'])
def riddle_callback(call):
    user_id = call.from_user.id
    if user_id not in user_data or 'current_riddle' not in user_data[user_id]:
        bot.send_message(call.message.chat.id, "❌ Нет активной загадки! Используйте /riddle")
        bot.answer_callback_query(call.id)
        return
    if call.data == 'riddle_hint':
        bot.send_message(
            call.message.chat.id,
            f"📝 Подсказка: {user_data[user_id]['current_riddle']['hint']}"
        )
        bot.answer_callback_query(call.id)
        bot.register_next_step_handler(call.message, check_riddle_answer)
    else:
        correct_answer = user_data[user_id]['current_riddle']['answer']
        bot.send_message(
            call.message.chat.id,
            f"🙌 Вы сдались! Правильный ответ: {correct_answer}"
        )
        bot.answer_callback_query(call.id)
        del user_data[user_id]['current_riddle']
        del user_data[user_id]['riddle_attempts']

@bot.message_handler(commands=['fact'])
def fact_command(message):
    fact = random.choice(facts)
    bot.send_message(message.chat.id, f"🤓 {fact}")

@bot.message_handler(commands=['random'])
def random_command(message):
    number = random.randint(1, 100)
    bot.send_message(message.chat.id, f"🎲 Случайное число: {number}")

@bot.message_handler(commands=['dice'])
def dice_command(message):
    dice = random.randint(1, 6)
    bot.send_message(message.chat.id, f"🎲 Выпало: {dice}")

@bot.message_handler(commands=['coin'])
def coin_command(message):
    result = random.choice(["Орел 🦅", "Решка 🪙"])
    bot.send_message(message.chat.id, f"🪙 {result}")

@bot.message_handler(commands=['fortune'])
def fortune_command(message):
    fortunes = [
        "🔮 Сегодня вас ждет приятный сюрприз!",
        "🌟 Удача на вашей стороне, действуйте смело!",
        "⚖️ Принимайте решения с умом, и все получится!",
        "🌙 Ночь принесет важные мысли!",
        "💫 Встреча с новым человеком изменит ваш день!",
        "🛤️ Новый путь уже ждет вас!",
        "🌈 Радость придет оттуда, откуда не ждали!",
        "⚡ Энергия дня поможет вам свернуть горы!"
    ]
    fortune = random.choice(fortunes)
    bot.send_message(message.chat.id, fortune)

# =============== УТИЛИТЫ ===============
@bot.message_handler(commands=['calc'])
def calc_command(message):
    bot.send_message(message.chat.id, "🧮 Введите математическое выражение (например, 2+2):")
    bot.register_next_step_handler(message, process_calc)

def process_calc(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {
            'name': message.from_user.first_name or "Друг",
            'quiz_scores': {name: 0 for name in all_quizzes.keys()},
            'total_score': 0,
            'commands_used': 0,
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'riddles_solved': 0,
            'calculations_done': 0,
            'chat_interactions': 0
        }
    expression = message.text.strip()
    result = calculate(expression)
    user_data[user_id]['calculations_done'] += 1
    user_data[user_id]['commands_used'] += 1
    bot.send_message(message.chat.id, result)

@bot.message_handler(commands=['translate'])
def translate_command(message):
    bot.send_message(message.chat.id, "🔤 Введите слово на английском для перевода на русский:")
    bot.register_next_step_handler(message, process_translation)

def process_translation(message):
    word = message.text.strip().lower()
    translation = translation_dict.get(word, "❌ Слово не найдено в словаре")
    bot.send_message(message.chat.id, f"🔤 {word} → {translation}")

@bot.message_handler(commands=['qr'])
def qr_command(message):
    bot.send_message(message.chat.id, "📱 Введите текст или ссылку для создания QR-кода:")
    bot.register_next_step_handler(message, process_qr)

def process_qr(message):
    text = message.text.strip()
    if not text:
        bot.send_message(message.chat.id, "❌ Пожалуйста, введите текст или ссылку!")
        return
    qr_url = generate_simple_qr_link(text)
    bot.send_message(message.chat.id, "📱 Ваш QR-код:")
    bot.send_photo(message.chat.id, qr_url)

@bot.message_handler(commands=['stats'])
def stats_command(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {
            'name': message.from_user.first_name or "Друг",
            'quiz_scores': {name: 0 for name in all_quizzes.keys()},
            'total_score': 0,
            'commands_used': 0,
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'riddles_solved': 0,
            'calculations_done': 0,
            'chat_interactions': 0
        }
    stats = user_data[user_id]
    quiz_stats = "\n".join([f"{name}: {score} баллов" for name, score in stats['quiz_scores'].items()])
    stats_text = f"""
📊 Статистика для {stats['name']}:
🎯 Общий счет: {stats['total_score']}
🧩 Решено загадок: {stats['riddles_solved']}
🧮 Вычислений: {stats['calculations_done']}
🤖 Чатов с AI: {stats['chat_interactions']}
📜 Команд использовано: {stats['commands_used']}
📅 Дата регистрации: {stats['start_date']}
🏅 Результаты викторин:
{quiz_stats}
"""
    bot.send_message(message.chat.id, stats_text)

# =============== ЧАТ С AI ===============
@bot.message_handler(commands=['chat'])
def chat_command(message):
    bot.send_message(message.chat.id, "🤖 Задайте вопрос или напишите, о чем хотите поговорить:")
    bot.register_next_step_handler(message, process_chat)

def process_chat(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {
            'name': message.from_user.first_name or "Друг",
            'quiz_scores': {name: 0 for name in all_quizzes.keys()},
            'total_score': 0,
            'commands_used': 0,
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'riddles_solved': 0,
            'calculations_done': 0,
            'chat_interactions': 0
        }
    response = chat_gpt(message.text.strip())
    user_data[user_id]['chat_interactions'] = user_data[user_id].get('chat_interactions', 0) + 1
    user_data[user_id]['commands_used'] += 1
    bot.send_message(message.chat.id, response)

# =============== ОБРАБОТЧИК КНОПОК МЕНЮ ===============
@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {
            'name': message.from_user.first_name or "Друг",
            'quiz_scores': {name: 0 for name in all_quizzes.keys()},
            'total_score': 0,
            'commands_used': 0,
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'riddles_solved': 0,
            'calculations_done': 0,
            'chat_interactions': 0
        }
    user_data[user_id]['commands_used'] += 1
    text = message.text.strip()
    commands = {
        "🎯 Викторины": quiz_menu,
        "💡 Мотивация": motivation_command,
        "🎲 Случайное число": random_command,
        "📊 Статистика": stats_command,
        "🌤 Погода": weather_command,
        "🧩 Загадки": riddle_command,
        "😂 Анекдоты": joke_command,
        "🤓 Факты": fact_command,
        "🧮 Калькулятор": calc_command,
        "🔤 Переводчик": translate_command,
        "📱 QR код": qr_command,
        "🎮 Игры": lambda msg: bot.send_message(msg.chat.id, "🎮 Выберите игру:\n/coin - подбросить монетку\n/dice - бросить кубик"),
        "ℹ️ Помощь": help_message,
        "🔮 Гадание": fortune_command,
        "🤖 Чат с AI": chat_command
    }
    command = commands.get(text)
    if command:
        command(message)
    else:
        bot.send_message(message.chat.id, "❓ Неизвестная команда. Используйте кнопки меню или /help")

# =============== ЗАПУСК БОТА ===============
if __name__ == "__main__":
    print("Бот запущен...")
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(10)
        bot.infinity_polling()
