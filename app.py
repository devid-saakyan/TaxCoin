import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

MINI_APP_URL = "https://front.taxco-in.com/auth/signup"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    telegram_id = user.id

    referral_code = context.args[0] if context.args else None

    url = f"{MINI_APP_URL}?telegram_id={telegram_id}"
    if referral_code:
        url += f"&referral_id={referral_code}"

    keyboard = [
        [InlineKeyboardButton("Открыть мини-приложение", web_app=WebAppInfo(url=url))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Привет! Нажми на кнопку ниже, чтобы открыть мини-приложение.",
        reply_markup=reply_markup
    )


def main():
    application = Application.builder().token("7519340984:AAEy9LrrojQnhNx70dmi-pSm0bpxFvib-60").build()

    application.add_handler(CommandHandler("start", start))

    application.run_polling()


if __name__ == '__main__':
    main()