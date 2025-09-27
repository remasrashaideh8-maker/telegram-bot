from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = "8478445732:AAExzCN-vAwxZnnhGfhUjZ5EEZSjFtBYbxc"
WEBHOOK_URL = "https://telegram-bot-1d3c.onrender.com/webhook"
TASKS_FILE = "tasks.txt"

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت يعمل! استخدم /add لإضافة مهمة.")

# أمر /add
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if args:
        task = " ".join(args)
        with open(TASKS_FILE, "a", encoding="utf-8") as f:
            f.write(f"{task}\n")
        await update.message.reply_text(f"📌 تم إضافة المهمة: {task}")
    else:
        await update.message.reply_text("❗ استخدم الأمر بهذا الشكل:\n/add المهمة التي تريد إضافتها")

# أمر /list
async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            tasks = f.readlines()
        if tasks:
            message = "📋 المهام الحالية:\n" + "".join(f"- {t}" for t in tasks)
        else:
            message = "📭 لا توجد مهام بعد."
    else:
        message = "📭 لا يوجد ملف مهام حتى الآن."
    await update.message.reply_text(message)

# تشغيل البوت باستخدام Webhook
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list_tasks))
    app.run_webhook(
        listen="0.0.0.0",
        port=8080,
        url_path="webhook",
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    main()
