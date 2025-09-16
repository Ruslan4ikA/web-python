from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

# Данные прямо в коде
CATEGORIES = [
    'Politic',
    'Sport',
    'Science',
    'Techno',
    'Health',
    'Business'
]

LANGUAGES = {
    'ru': 'Rus',
    'en': 'Engl',
    'de': 'Deutsch'
}

# Пример новостей
NEWS_DATA = [
    {
        'title': 'Новые технологии меняют мир',
        'content': 'Описание новости про технологии...',
        'category': 'Techno',
        'image': '/static/images/tech.jpg'
    },
    {
        'title': 'Победа в чемпионате мира',
        'content': 'Команда одержала победу...',
        'category': 'Sport',
        'image': '/static/images/sport.jpg'
    },
    {
        'title': 'Открытие в области медицины',
        'content': 'Учёные сделали важное открытие...',
        'category': 'Health',
        'image': '/static/images/health.jpg'
    }
]

def index(request):
    # Получаем куки
    selected_categories = request.COOKIES.get('categories', '')
    lang = request.COOKIES.get('language', 'ru')

    # Разбираем категории
    if selected_categories:
        selected_list = selected_categories.split(',')
    else:
        selected_list = []

    # Фильтруем новости
    filtered_news = [
        news for news in NEWS_DATA
        if not selected_list or news['category'] in selected_list
    ]

    context = {
        'categories': CATEGORIES,
        'languages': LANGUAGES,
        'news_list': filtered_news,
        'selected_lang': lang,
        'current_lang_name': LANGUAGES.get(lang, 'Русский'),
        'selected_categories': selected_list
    }

    response = render(request, 'index.html', context)

    # Сохраняем язык интерфейса, если его нет
    if not request.COOKIES.get('language'):
        response.set_cookie('language', 'ru', max_age=365*24*60*60)  # 1 год

    return response


def save_preferences(request):
    if request.method == 'POST':
        categories = request.POST.getlist('categories')
        language = request.POST.get('language', 'ru')

        response = redirect('home')
        # Сохраняем в куках
        response.set_cookie('categories', ','.join(categories), max_age=365*24*60*60)
        response.set_cookie('language', language, max_age=365*24*60*60)

        messages.success(request, 'Настройки успешно сохранены!')
        return response

    return redirect('home')