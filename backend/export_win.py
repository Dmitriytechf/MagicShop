import os
import sys
import django
from django.core.management import call_command


# 1. Добавляем путь к проекту
project_path = r'C:\MyProgect\DjangoAdvance' # здесь ваш путь*
sys.path.append(project_path)

# 2. Указываем правильный модуль настроек
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bigcorp.settings')

# 3. Инициализируем Django
django.setup()

# 4. Ваш путь для сохранения файла с данными
output_path = os.path.join(project_path, 'backend', 'data.json')
print(f"Сохраняем в: {output_path}")

try:
    # Открываем файл и указываем кодировку
    with open(output_path, 'w', encoding='utf-8') as f:
        call_command(
            'dumpdata',
            exclude=['contenttypes', 'auth.Permission'], # исключаем эти таблицы
            indent=2, # форматирование JSON с отступами
            stdout=f # перенаправляем вывод в файл
        )
    print(f"✅ Успешно! Размер файла: {os.path.getsize(output_path)} байт")

except Exception as e:
    print(f"❌ Ошибка: {e}")
    if os.path.exists(output_path):
        os.remove(output_path)