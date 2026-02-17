from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

TOKEN = "8351637214:AAFjEqsushuk7Bw4UezM1bp__8BT98V0APM"
ADMIN_ID = 123456789  # your telegram user id
CHANNEL_ID = -1003604224872  # your channel id

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Send your anonymous message.")

def receive_message(update: Update, context: CallbackContext):
    user_message = update.message.text

    keyboard = [
        [
            InlineKeyboardButton("Approve", callback_data=f"approve|{user_message}"),
            InlineKeyboardButton("Cancel", callback_data="cancel")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"New anonymous message:\n\n{user_message}",
        reply_markup=reply_markup
    )

    update.message.reply_text("Your message has been sent for approval.")

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    data = query.data

    if data.startswith("approve"):
        message = data.split("|")[1]
        context.bot.send_message(chat_id=CHANNEL_ID, text=message)
        query.edit_message_text("Message approved and posted.")

    elif data == "cancel":
        query.edit_message_text("Message canceled.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, receive_message))
    dp.add_handler(CallbackQueryHandler(button))

    print("Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()


