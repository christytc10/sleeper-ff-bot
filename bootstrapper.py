from discord_bot import chat_bot, bot2
from notifications import bot as notifications_bot
import threading


notifications_thread = threading.Thread(target=notifications_bot.run_notifications, args=())
notifications_thread.daemon = True  # Daemonize thread
notifications_thread.start()  # Start the execution

bot2_thread = threading.Thread(target=bot2.start_bot(), args=())
bot2_thread.daemon = True  # Daemonize thread
bot2_thread.start()  # Start the execution

chat_bot.start_bot()
