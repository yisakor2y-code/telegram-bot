pending_message = {}
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

TOKEN = "8351637214:AAFjEqsushuk7Bw4UezM1bp__8BT98V0APM"
ADMIN_ID = 873346173  # your telegram user id
CHANNEL_ID = -1003604224872  # your channel id

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Send your prayer request or testimony.")

def receive_message(update, context):
    user_message = update.message.text
    message_id = update.message.message_id

    pending_messages[message_id] = user_message

    keyboard = [[
        InlineKeyboardButton("Approve", callback_data=f"approve_{message_id}"),
        InlineKeyboardButton("Cancel", callback_data=f"cancel_{message_id}")
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"New anonymous message:\n\n{user_message}",
        reply_markup=reply_markup
    )

    update.message.reply_text("Your message has been sent for approval.")

def button(update, context):
    query = update.callback_query
    data = query.data

    if data.startswith("approve_"):
        msg_id = int(data.split("_")[1])
        message = pending_messages.get(msg_id)

        if message:
            context.bot.send_message(chat_id=CHANNEL_ID, text=message)
            query.edit_message_text("Message approved and posted.")

    elif data.startswith("cancel_"):
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





