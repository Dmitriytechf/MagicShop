# Project: *MagicShop*

Проект представляет собой **реализацию интернет-магазина**, написанного на Django. Далее описан основной **стек технологий** и **функциональные возможности** сайта. Основной целью данной работы является совершенствование профессиональных навыков (*hard skills*) и возможность творческой самореализации (конечно, звучит пафосно, но всё же!). Приоритетными направлениями развития проекта остаются **оптимизация** и **масштабируемость**, а уже затем — дизайн и визуальная составляющая.

## Описание

### 🚀 Возможности и развитие
-✅ Интернет магазин со всеми основными возможностями
-✅ Активная разработка фронтенд-части (HTMX, JavaScript, AJAX)
-✅ Подключенное REST API с Swagger/OpenAPI документацией
-✅ Гибкая система оплаты (Stripe, Webhook)
-✅ Интеграция с Docker, Nginx и CI/CD (GitHub Actions)

### 📊 Основной функционал для пользователя
- Добавление и удаление товара в корзине
- Категории продуктов
- Детальный разбор товара, похожие товары
- Создание и управление акаунтом
- Редактирование профиля(добавление фото, смена пароля и т.д.)
- Оплата с помощью stripe
- Доступ к товарам через API
- Пагинация и удобный вывод
- Поиск по товару или описанию

### ⚙️ Основной функционал работы с проектом для разработчика и администратора
- Работа с API
- Возможность добавления продуктов и категорий
- Получение pdf-счетов заказов
- Docker-контейнеризация
-  Асинхронные задачи через Celery

## 🛠️ Стек технологий
### Основные технологии
- Django
- Django REST
- HTML и CSS
- HTMX
- Celery
- Redis
- Webhook
- Bootstrap
- Ajax
- Github Action
- Docker
- Nginx

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django&logoColor=white)
![Django REST](https://img.shields.io/badge/Django_REST-3.14-ff1709?logo=django&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![HTMX](https://img.shields.io/badge/HTMX-1.9.0-5C1D8A?logo=htmx&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=white)
![Webhook](https://img.shields.io/badge/Webhook-6B2C85?logo=webhooks&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?logo=bootstrap&logoColor=white)
![Ajax](https://img.shields.io/badge/Ajax-0088CC?logo=ajax&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?logo=nginx&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?logo=javascript&logoColor=black)


## 🚀 Установка
1. Клонируйте репозиторий:
```bash
git clone <название-репозитория>
cd <название-репозитория>
```

2. Создать и активировать виртуальную среду:
```bash
python -m venv venv
source venv/Scripts/activate
```

3. Установить зависимости из файла requirements.txt:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```
4. Выполнить миграции:
```bash
python manage.py migrate
```

5. Запустить проект:
```bash
python manage.py runserver
```

### Дополнительно:

**Тестирование**
Команда для тестов:
```
python manage.py test
```

## API
*Ниже приведены примеры запросов к API*

#### 📄 Получение конкретной публикации
`http://127.0.0.1:8000/api/v1/products/{id}/` - адрес
**Вывод**
```
{
"id": 0,
"title": "string",
"slug": "string",
"brand": "string",
"category": "string",
"price": "string",
"image": "http://example.com",
"available": true,
"discount": 100,
"created_at": "2019-08-24T14:15:22Z",
"update_at": "2019-08-24T14:15:22Z"
}
```
(Можно задать параметры *limit* при get запросах)

## 📚 Документация к API
После применения миграций `python manage.py migrate `  и запуска проекта командной `python manage.py runserver` можно перейти на локальный сервер. Там Вам будет доступна документация проекта по ссылке
`http://127.0.0.1:8000/api/v1/redoc/` или `http://127.0.0.1:8000/api/v1/swagger/ `. В ней **подробно** расипсаны все способы запросов к API.

## 👨‍💻 Автор
[Дмитрий] - [https://github.com/Dmitriytechf]
