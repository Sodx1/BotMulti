import logging
from aiogram  import executor
from create_bot import dp
from handlers.register import register_handlers


logging.basicConfig(level=logging.INFO)
register_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)