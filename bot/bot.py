import logging
from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook
from keyboards import standard_keyboard
from settings import (BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT)
from parsing import get_pools, get_balance


logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(text='Start')
async def cmd_balance(message: types.Message):
    await message.answer("Hi this is autostake bot\nYou can get balance or pools", reply_markup=standard_keyboard())


@dp.message_handler(text='Balance')
async def cmd_balance(message: types.Message):
    await message.answer("Getting balance, please wait", reply_markup=standard_keyboard())
    balance = get_balance("Beefy")
    for row in balance:
        await message.answer(row, reply_markup=standard_keyboard())


@dp.message_handler(text='Pools')
async def cmd_pools(message: types.Message):
    await message.answer("Getting pools, please wait", reply_markup=standard_keyboard())
    min_apy = 10000
    min_tvl = 100
    pools = get_pools(min_apy=min_apy, min_tvl=min_tvl)
    await message.answer(f"Total pools ={len(pools)}", reply_markup=standard_keyboard())
    for pool in pools:
        await message.answer(pool, reply_markup=standard_keyboard())


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )