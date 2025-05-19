import asyncio
import logging

from handlers import routers
from bot import dp, bot
from utils.scheduler import scheduler


async def main():
    scheduler.start()
    for router in routers:
        dp.include_router(router)
    await asyncio.gather(
        dp.start_polling(bot),
    )


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')