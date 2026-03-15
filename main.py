"""
Telegram Verification Bot
=========================

HOW TO SET UP:
--------------

1. GET YOUR BOT TOKEN:
   - Open Telegram and search for @BotFather
   - Send /newbot and follow the instructions
   - BotFather will give you a token like: 7123456789:AAFxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   - Paste it below where it says TOKEN = "YOUR_BOT_TOKEN_HERE"

2. GET YOUR GROUP CHAT ID:
   - Add your bot to the Telegram group as a member
   - Also add @userinfobot or @RawDataBot to the group temporarily
   - Send any message in the group — the bot will reply with the chat ID
   - The group chat ID looks like: -1001234567890  (note the minus sign!)
   - Paste it below where it says GROUP_ID = YOUR_GROUP_ID_HERE
   - You can remove @userinfobot/@RawDataBot from the group after getting the ID

   Alternative method:
   - Send a message in the group
   - Open this URL in your browser (replace YOUR_TOKEN with your actual token):
     https://api.telegram.org/botYOUR_TOKEN/getUpdates
   - Look for "chat":{"id": ...} in the response — that number is your GROUP_ID

3. MAKE SURE YOUR BOT IS AN ADMIN of the group (or at least has permission to send messages)

4. RUN THE BOT:
   - Run this file with: python main.py
"""

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# =============================================
# PASTE YOUR BOT TOKEN HERE (from @BotFather)
# =============================================
TOKEN = "8703946447:AAFp0anD4-zDxcbxzas56tEq90scUEsd0cE"

# =============================================
# PASTE YOUR GROUP CHAT ID HERE
# (usually starts with a minus sign, e.g. -1001234567890)
# =============================================
GROUP_ID = -7809528036  # <-- Replace this with your actual group ID


# This message is sent when a user types /start
WELCOME_MESSAGE = """Hello! / Привіт!

Verification Form / Форма верифікації

Where are you from? / Від куди ви?

Which factions are you in? / В яких ви фракціях?

What is your language? / Яка ваша мова?

How much are you ready to tap for us? / Скільки ви готові за нас тапати?

Send your profile on CanvasPixels or Pixmap. / Киньте ваш профіль на CanvasPixels або Pixmap."""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command — send the welcome/verification message."""
    await update.message.reply_text(WELCOME_MESSAGE)


async def forward_to_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Forward every user message to the group chat."""
    user = update.message.from_user

    # Build a forwarded message with sender info
    username = f"@{user.username}" if user.username else user.first_name
    forwarded_text = (
        f"Message from {username} (ID: {user.id}):\n\n"
        f"{update.message.text}"
    )

    await context.bot.send_message(chat_id=GROUP_ID, text=forwarded_text)

    # Confirm receipt to the user
    await update.message.reply_text("Your message has been received!")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Handle /start command
    app.add_handler(CommandHandler("start", start))

    # Handle all regular text messages (not commands)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_group))

    print("Bot is running... Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()