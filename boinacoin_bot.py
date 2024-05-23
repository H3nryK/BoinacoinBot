import logging
from telegram import Update, Poll, PollAnswer, ChatPermissions
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, PollAnswerHandler, 
    ContextTypes, filters, ChatMemberHandler, JobQueue, CallbackContext
)
from datetime import time
from telegram.constants import ParseMode
from flask import Flask, request, jsonify

app = Flask(__name__)
application = app

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Dummy database for subscriptions
subscribers = []

# Define the command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am Boinacoin Bot. How can I assist you today? Type /help for the list of commands.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Available commands:\n'
        '/start - Start the bot\n'
        '/help - Get help information\n'
        '/about - Learn about Boinacoin\n'
        '/roadmap - View the project roadmap\n'
        '/goals - Understand our goals\n'
        '/team - Meet the team\n'
        '/tokenomics - Learn about our tokenomics\n'
        '/subscribe - Subscribe to updates\n'
        '/unsubscribe - Unsubscribe from updates\n'
        '/poll - Participate in a poll\n'
        '/tendies - Get ready for gains!\n'
        '/gainz - HODL for massive gains\n'
        '/mcnugget - Wow much nugget, so crypto\n'
        '/borkbork - 1 boinacoin = 1 boinacoin\n'
        "/pizzatime - It's pizza time!\n"
        '/buythedig - boinacoin to the moon!\n'
        "/fomo - Don't let FOMO get you\n"
        '/shitcoin - boinacoin is no shitcoin\n'
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Boinacoin is a cryptocurrency designed to reward culinary experiences and support local food businesses.')

async def roadmap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Our roadmap:\nQ3 2024: Project Launch\nQ4 2024: Core Development\nQ1 2025: Exchange Listing\nQ2 2025: Global Adoption')

async def goals(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Our goals include promoting culinary diversity, supporting local businesses, and creating a global community of food lovers.')

async def team(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Our team consists of experienced professionals from the fields of blockchain technology, culinary arts, and business development.')

async def tokenomics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Boinacoin tokenomics:\nTotal Supply: 1,000,000,000 BOINA\nDistribution: 50% Public Sale, 20% Team, 20% Ecosystem, 10% Reserve')

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    if user.id not in subscribers:
        subscribers.append(user.id)
        await update.message.reply_text('You have been subscribed to updates.')
    else:
        await update.message.reply_text('You are already subscribed.')

async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    if user.id in subscribers:
        subscribers.remove(user.id)
        await update.message.reply_text('You have been unsubscribed from updates.')
    else:
        await update.message.reply_text('You are not subscribed.')

async def send_update(context: ContextTypes.DEFAULT_TYPE) -> None:
    for subscriber_id in subscribers:
        try:
            await context.bot.send_message(chat_id=subscriber_id, text='Here is your regular update from Boinacoin!')
        except Exception as e:
            logger.error(f"Error sending update to {subscriber_id}: {e}")

async def announce(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.chat.type != 'private':
        await update.message.reply_text("This command can only be used in a private chat.")
        return
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /announce <message>")
        return
    message = ' '.join(context.args)
    chat_id = -1002005569292  # Replace with your group chat ID
    try:
        await context.bot.send_message(chat_id=chat_id, text=message)
        await update.message.reply_text("Announcement sent.")
    except Exception as e:
        logger.error(f"Error sending announcement: {e}")
        await update.message.reply_text("Failed to send announcement.")

async def poll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    questions = ["What is your favorite feature of Boinacoin?", "How did you hear about us?", "Are you planning to invest in Boinacoin?"]
    options = [["Rewards", "Community", "Support for local businesses"], ["Social Media", "Friend", "Event"], ["Yes", "No", "Undecided"]]
    question_index = 0  # Just an example, you could choose a random question
    question = questions[question_index]
    choices = options[question_index]
    await context.bot.send_poll(
        chat_id=update.message.chat_id,
        question=question,
        options=choices,
        is_anonymous=False,
    )

async def handle_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    answer = update.poll_answer
    user = answer.user
    poll_id = answer.poll_id
    option_ids = answer.option_ids
    logger.info(f"User {user} answered poll {poll_id} with options {option_ids}")
        
# Define the daily post function
async def daily_post(context: CallbackContext) -> None:
    chat_id = -1002005569292  # Replace with your group chat ID
    message = (
        "Follow us on our socials for the latest updates:\n"
        "Twitter: https://twitter.com/boinacoin\n"
        "Instagram: https://instagram.com/boinacoin"
    )
    image_path = 'media/logo.png'
    logger.info(f"Attempting to send daily post to chat ID {chat_id}")

    if os.path.exists(image_path):
        try:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=open(image_path, 'rb'),
                caption=message,
                parse_mode=ParseMode.HTML
            )
            logger.info("Daily post sent successfully.")
        except Exception as e:
            logger.error(f"Error sending daily post: {e}")
    else:
        logger.error(f"Image not found at {image_path}")


# Group management handlers
async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for member in update.message.new_chat_members:
        await update.message.reply_text(f"Welcome {member.full_name} to the Boinacoin group!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Here you can add custom message handling logic
    text = update.message.text.lower()
    if "spam" in text:
        await update.message.reply_text("Please refrain from spamming the group.")
        await context.bot.restrict_chat_member(
            chat_id=update.message.chat_id,
            user_id=update.message.from_user.id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=None  # Ban indefinitely
        )
        
async def tendies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_animation(chat_id=update.effective_chat.id, animation=open('media/chicken.gif', 'rb'))
    await update.message.reply_text("Gains incoming! 🚀💰")

async def gainz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("💪 HODL for massive boinacoin gainz!")

async def mcnugget(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('media/Doge_meme.jpg', 'rb'))
    await update.message.reply_text("Wow much nugget, so crypto")

async def borkbork(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_animation(chat_id=update.effective_chat.id, animation=open('media/funny.gif', 'rb'))
    await update.message.reply_text("1 boinacoin = 1 boinacoin")

async def pizzatime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('media/pizza.jpg', 'rb'))

async def buythedig(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('media/astronaut.jpg', 'rb'))
    await update.message.reply_text("You guys are buying fiat? No no, boinacoin to the moon! 🚀")

async def fomo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_animation(chat_id=update.effective_chat.id, animation=open('meida/miss.gif', 'rb'))
    await update.message.reply_text("Don't let FOMO get you, stack boinacoin now!")

async def shitcoin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('media/kermit.jpg', 'rb'))
    await update.message.reply_text("boinacoin is no shitcoin, it's the dankest crypto out there")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)

def main() -> None:
    # Replace 'YOUR_BOT_TOKEN' with your actual Bot Token
    application = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

    job_queue = JobQueue()
    job_queue.set_application(application)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("roadmap", roadmap))
    application.add_handler(CommandHandler("goals", goals))
    application.add_handler(CommandHandler("team", team))
    application.add_handler(CommandHandler("tokenomics", tokenomics))
    application.add_handler(CommandHandler("subscribe", subscribe))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe))
    application.add_handler(CommandHandler("poll", poll))
    application.add_handler(CommandHandler("announce", announce))
    application.add_handler(CommandHandler("tendies", tendies))
    application.add_handler(CommandHandler("gainz", gainz))
    application.add_handler(CommandHandler("mcnugget", mcnugget))
    application.add_handler(CommandHandler("borkbork", borkbork))
    application.add_handler(CommandHandler("pizzatime", pizzatime))
    application.add_handler(CommandHandler("buythedig", buythedig))
    application.add_handler(CommandHandler("fomo", fomo))
    application.add_handler(CommandHandler("shitcoin", shitcoin))
    application.add_handler(PollAnswerHandler(handle_poll_answer))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(ChatMemberHandler(welcome_new_member, ChatMemberHandler.MY_CHAT_MEMBER))
    application.add_handler(ChatMemberHandler(welcome_new_member, ChatMemberHandler.CHAT_MEMBER))


    # Schedule a daily update for subscribers
    job_queue.run_daily(send_update, time=time(11, 0, 0)) 
    
    job_queue.run_daily(daily_post, time=time(9, 0, 0))   
    job_queue.run_daily(daily_post, time=time(10, 57, 0))  
    job_queue.run_daily(daily_post, time=time(21, 0, 0)) 
    logger.info("Job queue set up for daily posts at 9 AM, 11 AM, and 7 PM.")

    # Start the JobQueue
    job_queue.start()

    application.run_polling()
    
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.json, bot)
    dispatcher.process_update(update)
    return jsonify({'status': 'ok'})

def run_bot():
    global bot, dispatcher
    bot, dispatcher = main()
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
