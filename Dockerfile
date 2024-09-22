# Используем официальный образ Python 3.12
FROM python:3.12.5

# Отключаем кеширование bytecode
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта
COPY . /app/

# Открываем порт для приложения
EXPOSE 8000

# Запускаем сервер
CMD ["python", "web_auto_server/web_auto/manage.py", "runserver", "0.0.0.0:8000"]
