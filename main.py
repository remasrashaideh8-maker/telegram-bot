from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = "8478445732:AAExzCN-vAwxZnnhGfhUjZ5EEZSjFtBYbxc"
WEBHOOK_URL = "https://telegram-bot-1d3c.onrender.com/webhook"
TASKS_FILE = "tasks.txt"

# /start مع أزرار
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("➕ إضافة مهمة", callback_data="add")],
        [InlineKeyboardButton("📋 عرض المهام", callback_data="list")],
        [InlineKeyboardButton("✅ أتممت مهمة", callback_data="done")]
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

    elif query.data == "done":
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                tasks = f.readlines()
            if tasks:
                keyboard = [
                    [InlineKeyboardButton(t.strip(), callback_data=f"complete:{i}")]
                    for i, t in enumerate(tasks)
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.message.reply_text("اختر المهمة التي أتممتها:", reply_markup=reply_markup)
            else:
                await query.message.reply_text("📭 لا توجد مهام.")
        else:
            await query.message.reply_text("📭 لا يوجد ملف مهام.")

    elif query.data.startswith("complete:"):
        index = int(query.data.split(":")[1])
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            tasks = f.readlines()
        if 0 <= index < len(tasks):
            completed = tasks.pop(index)
            with open(TASKS_FILE, "w", encoding="utf-8") as f:
                f.writelines(tasks)
            await query.message.reply_text(f"✅ تم إنهاء المهمة: {completed.strip()}")
        else:
            await query.message.reply_text("❌ رقم المهمة غير صالح.")

# /add لإضافة مهمة
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if args:
        task = " ".join(args)
        with open(TASKS_FILE, "a", encoding="utf-8") as f:
            f.write(f"{task}\n")
        await update.message.reply_text(f"📌 تم إضافة المهمة: {task}")
    else:
        await update.message.reply_text("❗ استخدم الأمر بهذا الشكل:\n/add المهمة التي تريد إضافتها")

# /list أو عرض المهام من زر
async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_target = (
        update.message if update.message
        else update.callback_query.message
    )
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            tasks = f.readlines()
        if tasks:
            message = "📋 المهام الحالية:\n" + "".join(f"- {t}" for t in tasks)
        else:
            message = "📭 لا توجد مهام بعد."
    else:
        message = "📭 لا يوجد ملف مهام حتى الآن."
    await message_target.reply_text(message)

# /remind لتفعيل التذكير الخارجي
async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            tasks = f.readlines()
        if tasks:
            message = "⏰ تذكير بالمهام:\n" + "".join(f"- {t}" for t in tasks)
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
    app.add_handler(CommandHandler("remind", remind))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.run_webhook(
        listen="0.0.0.0",
        port=8080,
        url_path="webhook",
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    main()
