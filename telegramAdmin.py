from telegram import Bot, ChatMember
from telegram.constants import ChatMemberStatus
import asyncio

TOKEN = '7519340984:AAEy9LrrojQnhNx70dmi-pSm0bpxFvib-60'
CHANNEL_ID = '@crypt0scamm'
bot = Bot(token=TOKEN)
loop = asyncio.get_event_loop()

async def check_membership(telegram_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=telegram_id)
        return member.status in {ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER}
    except Exception as e:
        print(f"Ошибка: {e}")
        return False


def is_user_in_channel(telegram_id: int) -> bool:
    return loop.run_until_complete(check_membership(telegram_id))