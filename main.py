#!/usr/bin/env python3
"""
Telegram Bot for Uzbek Food Map
Compatible with python-telegram-bot 21.x
"""

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ========== CONFIGURATION ==========
# Get token from environment variable (safer than hardcoding)
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN environment variable not set!")

# Your GitHub Pages Mini App URL
MINI_APP_URL = "https://cat-k235.github.io/tashkent-food-telegram-app/"

# Logging configuration
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ========== COMMAND HANDLERS ==========

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command"""
    user = update.effective_user

    keyboard = [
        [InlineKeyboardButton("🗺️ OPEN FOOD MAP", web_app={"url": MINI_APP_URL})],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        f"🍽️ *Assalomu alaykum, {user.first_name or 'foydalanuvchi'}!*\n\n"
        "*O'zbekiston Oziq-ovqat Xaritasi* ga xush kelibsiz!\n\n"
        "✅ *Qanday foydalanish:*\n"
        "1. Quyidagi tugmani bosing\n"
        "2. Xaritadan ovqatlanish joylarini toping\n"
        "3. Telefon raqamlarini ko'ring\n"
        "4. To'g'ridan-to'g'ri qo'ng'iroq qiling\n\n"
        "📍 *Toshkent shahridagi barcha restoranlar, kafelar va tez ovqat joylari*"
    )

    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /help command"""
    help_text = (
        "🆘 *Yordam:*\n\n"
        "*/start* — Botni ishga tushirish\n"
        "*/help* — Yordam olish\n"
        "*/map* — Xaritani ochish\n\n"
        "📍 *Agar muammo bo‘lsa:*\n"
        "1. Internet aloqangizni tekshiring\n"
        "2. Botni qayta ishga tushiring: /start\n"
        "3. @yourusername ga murojaat qiling"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def map_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /map command — directly opens the Mini App"""
    keyboard = [[InlineKeyboardButton("🗺️ Hozir ochish", web_app={"url": MINI_APP_URL})]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Toshkent oziq-ovqat xaritasi ochilmoqda...", reply_markup=reply_markup
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles callback button presses"""
    query = update.callback_query
    await query.answer()
    # No extra buttons for now; HTML handles filtering
    await query.message.reply_text(
        "🗺️ Xarita ochish uchun pastdagi tugmani bosing",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🗺️ OPEN FOOD MAP", web_app={"url": MINI_APP_URL})]]
        ),
    )


# ========== MAIN BOT INITIALIZATION ==========

def main():
    """Runs the Telegram bot"""
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("map", map_command))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Global error logging
    async def error_handler(update, context):
        logger.error("Exception while handling update:", exc_info=context.error)

    application.add_error_handler(error_handler)

    logger.info("🤖 Uzbek Food Map Bot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()
