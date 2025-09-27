from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8478445732:AAExzCN-vAwxZnnhGfhUjZ5EEZSjFtBYbxc"  # توكن البوت الحقيقي
WEBHOOK_URL = "https://telegram-bot-1d3c.onrender.com/webhook"  # رابط البوت من Render

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Add Task", switch_inline_query_current_chat="/add")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("مرحبًا! اختر إجراء:", reply_markup=reply_markup)

# أمر /add
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("اكتب المهمة بعد /add")

# تشغيل البوت باستخدام Webhook
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.run_webhook(
        listen="0.0.0.0",
        port=8080,
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    main()
