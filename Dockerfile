FROM python

# хост базы данных для докера
ENV DATABASE_HOST=database
# хост сайта
ENV SITE_HOST=0.0.0.0

# установка рабочей директории
WORKDIR /

# установка зависимостей
COPY requirements.txt .
RUN pip install -r requirements.txt
# копирование проекта
COPY Fastapi_Games .