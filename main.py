from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8478445732:AAExzCN-vAwxZnnhGfhUjZ5EEZSjFtBYbxc"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Add Task", switch_inline_query_current_chat="/add")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("مرحبًا! اختر إجراء:", reply_markup=reply_markup)

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("اكتب المهمة بعد /add")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.run_webhook(
        listen="0.0.0.0",
        port=8080,
        webhook_url="https://your-bot-name.onrender.com/webhook"
    )

if __name__ == "__main__":
    main()