from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8478445732:AAExzCN-vAwxZnnhGfhUjZ5EEZSjFtBYbxc"
WEBHOOK_PATH = "webhook"
WEBHOOK_URL = f"https://telegram-bot-3u3r.onrender.com/{WEBHOOK_PATH}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت يعمل!")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_webhook(
        listen="0.0.0.0",
        port=8080,
        url_path=WEBHOOK_PATH,
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    main()
