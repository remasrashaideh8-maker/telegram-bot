from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8478445732:AAExzCN-vAwxZnnhGfhUjZ5EEZSjFtBYbxc"
WEBHOOK_URL = "https://telegram-bot-1d3c.onrender.com/webhook"

# أمر /start مع أزرار
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("➕ إضافة مهمة", callback_data="add")],
        [InlineKeyboardButton("📋 عرض المهام", callback_data="list")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("مرحبًا! اختر إجراء:", reply_markup=reply_markup)

# التعامل مع ضغط الأزرار
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "add":
        await query.message.reply_text("❗ استخدم الأمر بهذا الشكل:\n/add المهمة التي تريد إضافتها")
    elif query.data == "list":
        await list_tasks(update, context)

# أمر /add
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if args:
        task = " ".join(args)
        with open("tasks.txt", "a", encoding="utf-8") as f:
            f.write(f"{task}\n")
        await update.message.reply_text(f"📌 تم إضافة المهمة: {task}")
    else:
        await update.message.reply_text("❗ استخدم الأمر بهذا الشكل:\n/add المهمة التي تريد إضافتها")

# أمر /list
async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open("tasks.txt", "r", encoding="utf-8") as f:
            tasks = f.readlines()
        if tasks:
            message = "📋 المهام الحالية:\n" + "".join(f"- {t}" for t in tasks)
        else:
            message = "📭 لا توجد مهام بعد."
    except FileNotFoundError:
        message = "📭 لا يوجد ملف مهام حتى الآن."
    await update.message.reply_text(message)

# تشغيل البوت باستخدام Webhook
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list_tasks))
    app.add_handler(telegram.ext.CallbackQueryHandler(handle_button))
    app.run_webhook(
        listen="0.0.0.0",
        port=8080,
        url_path="webhook",
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    main()
