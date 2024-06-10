import logging
import asyncio
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, PollAnswerHandler, 
    ContextTypes, filters, JobQueue, CallbackContext
)
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Dummy database for subscriptions
subscribers = []

# Define your bot token here
TOKEN = ""

# Define your start message
START_MESSAGE = "Hey buddy, what do you want to order today?"

# Define your welcome message
WELCOME_MESSAGE = "Welcome to BoinaCoin! We're glad you joined us. Remember to follow us on X for more updates: https://x.com/BoinaCoin"

# Define the command handlers
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(START_MESSAGE)

# Function to handle new members joining
async def welcome_new_member(update: Update, context: CallbackContext) -> None:
    new_member = update.message.new_chat_members[0]
    await update.message.reply_text(f"Hey {new_member.first_name}! {WELCOME_MESSAGE}")

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

async def tendies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    await context.bot.send_animation(chat_id=update.effective_chat.id, animation=open('media/chicken.gif', 'rb'))
    await update.message.reply_text("Gains incoming! 🚀💰")

async def gainz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("💪 HODL for massive boinacoin gainz!")

async def mcnugget(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('media/Doge_meme.jpg', 'rb'))
    await update.message.reply_text("Wow much nugget, so crypto")

async def borkbork(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    await context.bot.send_animation(chat_id=update.effective_chat.id, animation=open('media/funny.gif', 'rb'))
    await update.message.reply_text("1 boinacoin = 1 boinacoin")

async def pizzatime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('media/pizza.jpg', 'rb'))

async def buythedig(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('media/astronaut.jpg', 'rb'))
    await update.message.reply_text("You guys are buying fiat? No no, boinacoin to the moon! 🚀")

async def shitcoin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('media/kermit.jpg', 'rb'))
    await update.message.reply_text("boinacoin is no shitcoin, it's the dankest crypto out there")

# Function to send frequent messages
# In the send_frequent_message function
async def send_frequent_message(context: CallbackContext) -> None:
    message = "Hey everyone! How's your day going?\nDon't forget to follow our X community to stay updated.You might get the juice. Tell a friend to tell a friend.\n\n https://x.com/BoinaCoin"
    chat_id = # Replace with your group chat ID
    try:
        await context.bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        logger.error(f"Error sending frequent message: {e}")

# Function to send frequent updates
async def send_frequent_update(context: CallbackContext) -> None:
    message = ("Hey BoinaCoin fam! 🚀 \nJust a reminder that every dip is an opportunity "
               "for a comeback! Keep hodling strong and remember, the journey to the moon "
               "is full of twists and turns, but together, we'll reach our destination. "
               "Let's spread positivity, support each other, and keep the BoinaCoin spirit alive! "
               "\n💪💎 #BoinaFam #ToTheMoon")
    chat_id =  # Replace with your group chat ID
    try:
        await context.bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        logger.error(f"Error sending frequent message: {e}")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)

def main() -> None:
    # Replace 'YOUR_BOT_TOKEN' with your actual Bot Token
    application = ApplicationBuilder().token(TOKEN).build()

    job_queue = application.job_queue

    # Create an APScheduler scheduler
    scheduler = AsyncIOScheduler()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("roadmap", roadmap))
    application.add_handler(CommandHandler("goals", goals))
    application.add_handler(CommandHandler("team", team))
    application.add_handler(CommandHandler("tokenomics", tokenomics))
    application.add_handler(CommandHandler("subscribe", subscribe))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe))
    application.add_handler(CommandHandler("announce", announce))
    application.add_handler(CommandHandler("poll", poll))
    application.add_handler(PollAnswerHandler(handle_poll_answer))
    application.add_handler(CommandHandler("tendies", tendies))
    application.add_handler(CommandHandler("gainz", gainz))
    application.add_handler(CommandHandler("mcnugget", mcnugget))
    application.add_handler(CommandHandler("borkbork", borkbork))
    application.add_handler(CommandHandler("pizzatime", pizzatime))
    application.add_handler(CommandHandler("buythedig", buythedig))
    application.add_handler(CommandHandler("shitcoin", shitcoin))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    
    # Scheduling the frequent message on a 24hr loop
    job = job_queue.run_repeating(send_frequent_message, interval=86400, first=66600)

    # Scheduling the frequent update on a 24hr loop
    job = job_queue.run_repeating(send_frequent_message, interval=86400, first=57600)

    # Start the scheduler
    scheduler.start()

    application.run_polling()

if __name__ == "__main__":
    main()
