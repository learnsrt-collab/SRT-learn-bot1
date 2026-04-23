from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

from database import add_user, add_score, get_score
from quiz import quiz_data

TOKEN = "8502156429:AAFUYWw6VAiJEzmfKdn7LCUrc6eoGAMrq9w"

# Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.first_name)

    keyboard = [["Maths", "Science"], ["ICT", "Quiz"], ["Score"]]
    await update.message.reply_text(
        "📚 Welcome to O/L Education Bot",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# Quiz
async def send_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = []
    for item in quiz_data["options"]:
        buttons.append([InlineKeyboardButton(item, callback_data=item)])

    await update.message.reply_text(
        quiz_data["question"],
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Button answer
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == quiz_data["answer"]:
        add_score(query.from_user.id)
        await query.edit_message_text("✅ Correct!")
    else:
        await query.edit_message_text("❌ Wrong Answer")

# Messages
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if text == "quiz":
        await send_quiz(update, context)

    elif text == "score":
        score = get_score(update.effective_user.id)
        await update.message.reply_text(f"🏆 Your Score: {score}")

    elif "pythagoras" in text:
        await update.message.reply_text("a² + b² = c²")

    elif "dna" in text:
        await update.message.reply_text("DNA carries genetic information.")

    elif "විදුලිය" in text:
        await update.message.reply_text("විදුලිය යනු ආරෝපණ ගමන් කිරීමයි.")

    else:
        await update.message.reply_text("Send your O/L question.")

# Admin command
async def announce(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = 123456789  # replace with your telegram id
    if update.effective_user.id != admin_id:
        return

    msg = " ".join(context.args)
    await update.message.reply_text("📢 Announcement saved:\n" + msg)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("announce", announce))
app.add_handler(CallbackQueryHandler(button_click))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

print("Bot Running...")
app.run_polling()
