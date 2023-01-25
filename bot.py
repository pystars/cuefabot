import json
import logging

import boto3
from telebot import TeleBot
from telebot.types import InlineQueryResultArticle, InputTextMessageContent, \
    InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '5893559533:AAEC611IodpKNXTqqWST64biBGrECDsrDBs'
bot = TeleBot(TOKEN)

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def answer_inline_query(inline_query_id):
    markup = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton('Rock', callback_data='rock'),
            InlineKeyboardButton('Paper', callback_data='paper'),
            InlineKeyboardButton('Scissors', callback_data='scissors')
        ]]
    )
    input_message = InputTextMessageContent('Сыграть в камень-ножницы-бумага')
    args = input_message, markup
    bot.answer_inline_query(
        inline_query_id,
        [
            InlineQueryResultArticle(
                'rock',
                'Rock',
                *args
            ),
            InlineQueryResultArticle(
                'paper',
                'Paper',
                *args
            ),
            InlineQueryResultArticle(
                'scissors',
                'Scissors',
                *args
            ),
        ],
    )


def handler(event, context):
    print(event)
    body = json.loads(event['body'])
    print(body)
    if 'inline_query' in body:
        answer_inline_query(body['inline_query']['id'])
    elif 'chosen_inline_result' in body:
        print(body['chosen_inline_result']['inline_message_id'])
        print(body['chosen_inline_result']['result_id'])
    elif 'callback_query' in body:
        cbq = body['callback_query']
        print(cbq)
        bot.edit_message_reply_markup(
            inline_message_id=cbq['inline_message_id'])
        # print(cbq['inline_message_id'])
        # print(cbq['result_id'])
    return {
        'statusCode': 200,
        'body': '',
    }
