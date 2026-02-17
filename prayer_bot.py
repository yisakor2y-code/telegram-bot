from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "8351637214:AAFjEqsushuk7Bw4UezM1bp__8BT98V0APM"
ADMIN_ID = 873346173
CHANNEL_ID = -1003604224872


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🕊 Welcome.\n\n"
        "Send your story freely.\n"
        "Your identity will remain anonymous."
    )


async def receive_story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    message_id = update.message.message_id

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"approve:{message_id}"),
            InlineKeyboardButton("❌ Cancel", callback_data=f"cancel:{message_id}")
        ]
    ])

    # Store message globally
    context.bot_data[message_id] = user_text

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📩 *New anonymous submission:*\n\n{user_text}",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )


async def decision_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, msg_id = query.data.split(":")
    msg_id = int(msg_id)

    story = context.bot_data.get(msg_id)

    if not story:
        await query.edit_message_text("⚠️ Message not found or already handled.")
        return

    if action == "approve":
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=f"🕊 *Anonymous message:*\n\n{story}",
            parse_mode="Markdown"
        )
        await query.edit_message_text("✅ Approved and posted.")

    else:
        await query.edit_message_text("❌ Message cancelled.")

    del context.bot_data[msg_id]


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_story))
    app.add_handler(CallbackQueryHandler(decision_handler))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
