FROM python:3.10

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /aiogram_guess_bot

ADD . /aiogram_guess_bot

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]

