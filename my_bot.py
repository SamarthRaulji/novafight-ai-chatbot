import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

# Load env
load_dotenv()

telegram_token = os.getenv("telegram_token")
gemini_apikey = os.getenv("gemini_apikey")

client = genai.Client(api_key=gemini_apikey)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 NovaFightBot is ready! Ask anything 🚀")


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=user_message

        )

        await update.message.reply_text(response.text)

    except Exception as e:
        print("Error:", e)
        await update.message.reply_text("Error Occur")

app = ApplicationBuilder().token(telegram_token).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("Bot running...")
app.run_polling()