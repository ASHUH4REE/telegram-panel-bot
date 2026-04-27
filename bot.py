import os
import random
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8726860078:AAE9EkygEYB02GLM7ZKbli7bLNBLccMSOfo"

OWNER_USERNAME = "ASHUH4REEE"
ADMIN_PASSWORD = "A$huX991#"

users = set()
admin_logged = set()
waiting_password = set()
maintenance = False
cooldowns = {}

COOLDOWN = 10
VIP_LINK = "https://t.me/ASHUH4REEE"
REGISTER_LINK = "https://www.jaiclub41.com/#/register?invitationCode=76751105547"

BTN_SIGNAL = "🎯 GET SIGNAL"
BTN_VIP = "👑 VIP SIGNAL"

IST = ZoneInfo("Asia/Kolkata")

join_buttons = [
    [InlineKeyboardButton("🔥 Channel 1", url="https://t.me/+5-MI5unhqHs5OTBl")],
    [InlineKeyboardButton("💰 Channel 2", url="https://t.me/+CM7-2EZgLZw0MzU1")],
    [InlineKeyboardButton("🚀 Channel 3", url="https://t.me/ayulootersop")],
    [InlineKeyboardButton("👑 Channel 4", url="https://t.me/iglootsofficial")],
    [InlineKeyboardButton("✅ DONE", callback_data="done")]
]

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(BTN_SIGNAL, callback_data="signal")],
        [InlineKeyboardButton(BTN_VIP, url=VIP_LINK)],
        [InlineKeyboardButton("📝 REGISTER NOW", callback_data="register")]
    ])

def next_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎯 GET NEXT PREDICTION", callback_data="signal")],
        [InlineKeyboardButton("👑 VIP SIGNAL", url=VIP_LINK)],
        [InlineKeyboardButton("📝 REGISTER NOW", callback_data="register")]
    ])

admin_buttons = [
    [InlineKeyboardButton("📊 Stats", callback_data="stats")],
    [InlineKeyboardButton("📣 Broadcast", callback_data="broadcast")],
    [InlineKeyboardButton("✏️ Edit Buttons", callback_data="editbtn")],
    [InlineKeyboardButton("🛡 Maintenance", callback_data="maint")],
    [InlineKeyboardButton("⏱ Cooldown", callback_data="cool")],
    [InlineKeyboardButton("❌ Close", callback_data="close")]
]

edit_buttons = [
    [InlineKeyboardButton("🎯 Change Signal Button", callback_data="editsignal")],
    [InlineKeyboardButton("👑 Change VIP Button", callback_data="editvip")],
    [InlineKeyboardButton("🔙 Back", callback_data="backpanel")]
]

edit_mode = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global maintenance
    user = update.effective_user
    users.add(user.id)

    if maintenance and user.username != OWNER_USERNAME:
        await update.message.reply_text("⚠️ SYSTEM UNDER MAINTENANCE")
        return

    await update.message.reply_text(
"""⚡━━━━━━━━━━━━⚡
CYBER NEON BOT
━━━━━━━━━━━━
JOIN ALL CHANNELS
UNLOCK SIGNAL ACCESS
⚡━━━━━━━━━━━━⚡""",
        reply_markup=InlineKeyboardMarkup(join_buttons)
    )

async def panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.username != OWNER_USERNAME:
        return
    waiting_password.add(update.effective_user.id)
    await update.message.reply_text("🔐 ENTER ADMIN PASSWORD")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global BTN_SIGNAL, BTN_VIP
    uid = update.effective_user.id
    text = update.message.text

    if uid in waiting_password:
        if text == ADMIN_PASSWORD:
            waiting_password.remove(uid)
            admin_logged.add(uid)
            await update.message.reply_text(
                "⚡ ADMIN PANEL OPENED",
                reply_markup=InlineKeyboardMarkup(admin_buttons)
            )
        else:
            waiting_password.remove(uid)
            await update.message.reply_text("❌ WRONG PASSWORD")
        return

    if uid in edit_mode:
        mode = edit_mode[uid]
        if mode == "signal":
            BTN_SIGNAL = text
            await update.message.reply_text("✅ Signal Button Updated")
        elif mode == "vip":
            BTN_VIP = text
            await update.message.reply_text("✅ VIP Button Updated")
        del edit_mode[uid]

async def send_signal(msg):
    multi = round(random.uniform(1.25, 4.90), 2)
    sec = random.randint(5, 18)
    risk = random.choice(["LOW 🟢", "MEDIUM 🟡", "HIGH 🔴"])
    live = random.randint(180, 1500)
    current_time = datetime.now(IST).strftime("%H:%M:%S")

    await msg.edit_text(
f"""⚡ SIGNAL READY ⚡

⏰ Time: {current_time}
🚀 Next Round: {sec}s
💰 Cashout: {multi}x
📊 Risk: {risk}
👥 Live Users: {live}

👑 VIP: @ASHUH4REEE""",
        reply_markup=next_menu()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global maintenance, COOLDOWN

    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    if query.data == "done":
        await query.message.edit_text(
            "⚡ ACCESS GRANTED ⚡",
            reply_markup=main_menu()
        )

    elif query.data == "register":
        await query.message.reply_text(
            "📝 Register under our link for signal access ⚡",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📝 OPEN REGISTER LINK", url=REGISTER_LINK)]
            ])
        )

    elif query.data == "signal":
        now = time.time()

        if uid in cooldowns and now - cooldowns[uid] < COOLDOWN:
            left = int(COOLDOWN - (now - cooldowns[uid]))
            await query.message.reply_text(f"⏳ WAIT {left}s")
            return

        cooldowns[uid] = now

        msg = await query.message.reply_text("⚡ Scanning Server...")
        await msg.edit_text("📡 Reading Market...")
        await msg.edit_text("💎 Preparing Signal...")

        await send_signal(msg)

    elif uid in admin_logged:

        if query.data == "stats":
            await query.message.reply_text(f"📊 Users: {len(users)}")

        elif query.data == "broadcast":
            await query.message.reply_text("Use:\n/broadcast your message")

        elif query.data == "editbtn":
            await query.message.edit_text(
                "✏️ BUTTON SETTINGS",
                reply_markup=InlineKeyboardMarkup(edit_buttons)
            )

        elif query.data == "editsignal":
            edit_mode[uid] = "signal"
            await query.message.reply_text("Send New Signal Button Name")

        elif query.data == "editvip":
            edit_mode[uid] = "vip"
            await query.message.reply_text("Send New VIP Button Name")

        elif query.data == "backpanel":
            await query.message.edit_text(
                "⚡ ADMIN PANEL",
                reply_markup=InlineKeyboardMarkup(admin_buttons)
            )

        elif query.data == "maint":
            maintenance = not maintenance
            state = "ON" if maintenance else "OFF"
            await query.message.reply_text(f"🛡 Maintenance {state}")

        elif query.data == "cool":
            COOLDOWN = 5 if COOLDOWN == 10 else 10
            await query.message.reply_text(f"⏱ Cooldown {COOLDOWN}s")

        elif query.data == "close":
            admin_logged.remove(uid)
            await query.message.reply_text("🔒 PANEL CLOSED")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in admin_logged:
        return

    msg = " ".join(context.args)
    if not msg:
        return

    sent = 0
    for uid in users:
        try:
            await context.bot.send_message(uid, msg)
            sent += 1
        except:
            pass

    await update.message.reply_text(f"📣 SENT TO {sent} USERS")

app = (
    Application.builder()
    .token(TOKEN)
    .connect_timeout(60)
    .read_timeout(60)
    .write_timeout(60)
    .pool_timeout(60)
    .build()
)

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("panel", panel))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

print("Railway Bot Running Full Upgrade...")
app.run_polling()