from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    CallbackQueryHandler,
)

# =========================
# SOZLAMALAR
# =========================

TOKEN = "8767423548:AAHTyZuT4jqUYprYgTExPiT_mbGm3GhPB"

ADMIN_ID = 8499593996

CHANNEL = "@urolov_service"


# =========================
# OBUNANI TEKSHIRISH
# =========================

async def is_subscribed(
    user_id,
    context
):

    try:

        member = await context.bot.get_chat_member(
            chat_id=CHANNEL,
            user_id=user_id
        )

        return member.status in [
            "member",
            "administrator",
            "creator"
        ]

    except Exception as e:

        print("OBUNANI TEKSHIRISHDA XATO:", e)

        return False


# =========================
# START
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    subscribed = await is_subscribed(
        user_id,
        context
    )

    if not subscribed:

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "📢 Kanalga obuna bo‘lish",
                    url="https://t.me/urolov_service"
                )
            ],
            [
                InlineKeyboardButton(
                    "✅ Obunani tekshirish",
                    callback_data="check_subscription"
                )
            ]
        ])

        await update.message.reply_text(
            "👋 Assalomu alaykum!\n\n"
            "🤖 AI Xizmatlari botiga xush kelibsiz!\n\n"
            "📢 Botdan foydalanish uchun avval "
            "kanalimizga obuna bo‘ling.\n\n"
            "1️⃣ Kanalga obuna bo‘ling\n"
            "2️⃣ «✅ Obunani tekshirish» tugmasini bosing.",
            reply_markup=keyboard
        )

        return

    await request_phone(
        update,
        context
    )


# =========================
# OBUNANI QAYTA TEKSHIRISH
# =========================

async def check_subscription(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    user_id = query.from_user.id

    subscribed = await is_subscribed(
        user_id,
        context
    )

    if not subscribed:

        await query.answer(
            "❌ Siz hali kanalga obuna bo‘lmagansiz!",
            show_alert=True
        )

        return

    await query.message.edit_text(
        "✅ Obuna tasdiqlandi!\n\n"
        "Endi telefon raqamingizni yuboring."
    )

    button = KeyboardButton(
        "📱 Telefon raqamimni yuborish",
        request_contact=True
    )

    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await query.message.reply_text(
        "📱 Buyurtma berishdan oldin "
        "telefon raqamingizni yuboring:",
        reply_markup=keyboard
    )


# =========================
# TELEFON RAQAMINI SO‘RASH
# =========================

async def request_phone(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if context.user_data.get("phone"):

        await show_menu(
            update
        )

        return

    button = KeyboardButton(
        "📱 Telefon raqamimni yuborish",
        request_contact=True
    )

    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_text(
        "📱 Buyurtma berishdan oldin "
        "telefon raqamingizni yuboring.",
        reply_markup=keyboard
    )


# =========================
# TELEFON RAQAMINI QABUL QILISH
# =========================

async def receive_contact(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    contact = update.message.contact

    user = update.effective_user

    if contact.user_id and contact.user_id != user.id:

        await update.message.reply_text(
            "⚠️ Iltimos, o‘zingizning "
            "telefon raqamingizni yuboring."
        )

        return

    phone = contact.phone_number

    context.user_data["phone"] = phone

    context.user_data["telegram_id"] = user.id

    username = (
        f"@{user.username}"
        if user.username
        else "Username mavjud emas"
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            "📱 YANGI MIJOZ!\n\n"
            f"👤 Ism: {user.full_name}\n"
            f"📱 Username: {username}\n"
            f"📞 Telefon: +{phone.lstrip('+')}\n"
            f"🆔 Telegram ID: {user.id}"
        )
    )

    await update.message.reply_text(
        "✅ Telefon raqamingiz qabul qilindi!\n\n"
        "Endi xizmatni tanlang."
    )

    await show_menu(
        update
    )


# =========================
# MENYU
# =========================

async def show_menu(
    update: Update
):

    keyboard = [
        [
            "🖼 AI Rasm yaratish",
            "🎬 AI Video yaratish"
        ],
        [
            "🎯 YouTube Thumbnail",
            "📢 Reklama rasmi"
        ],
        [
            "👤 AI Avatar",
            "💰 Narxlar"
        ],
        [
            "📞 Admin bilan bog‘lanish"
        ],
    ]

    await update.message.reply_text(
        "🤖 AI Xizmatlari botiga xush kelibsiz!\n\n"
        "👇 Kerakli xizmatni tanlang:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )


# =========================
# XIZMAT TANLASH
# =========================

async def request_service(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    service = update.message.text

    context.user_data["service"] = service

    context.user_data["waiting_order"] = True

    examples = {

        "🖼 AI Rasm yaratish":
            "Masalan:\n"
            "Qora kostyumdagi yigit, professional "
            "studiyada, realistik, premium sifat.",

        "🎬 AI Video yaratish":
            "Masalan:\n"
            "10 soniyalik cinematic video, "
            "mashina tungi shaharda harakatlanmoqda.",

        "🎯 YouTube Thumbnail":
            "Masalan:\n"
            "Minecraft 100 kun challenge uchun "
            "yorqin va professional thumbnail.",

        "📢 Reklama rasmi":
            "Masalan:\n"
            "AI kursi uchun premium Instagram "
            "reklama rasmi.",

        "👤 AI Avatar":
            "Masalan:\n"
            "Instagram uchun professional AI avatar.",
    }

    example = examples.get(
        service,
        ""
    )

    await update.message.reply_text(
        f"✅ Siz tanladingiz:\n"
        f"{service}\n\n"
        "📝 Endi buyurtmangizni batafsil yozing.\n\n"
        f"{example}\n\n"
        "👇 Buyurtmangizni shu yerga yuboring:"
    )


# =========================
# BUYURTMA QABUL QILISH
# =========================

async def receive_order(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not context.user_data.get(
        "waiting_order"
    ):

        return

    user = update.effective_user

    order_text = update.message.text

    service = context.user_data.get(
        "service",
        "Noma'lum xizmat"
    )

    phone = context.user_data.get(
        "phone",
        "Telefon raqami mavjud emas"
    )

    username = (
        f"@{user.username}"
        if user.username
        else "Username mavjud emas"
    )

    admin_message = (
        "🔔 YANGI BUYURTMA!\n\n"
        f"👤 Mijoz: {user.full_name}\n"
        f"📱 Username: {username}\n"
        f"📞 Telefon: +{phone.lstrip('+')}\n"
        f"🆔 Telegram ID: {user.id}\n\n"
        f"🛠 Xizmat: {service}\n\n"
        f"📝 Buyurtma:\n"
        f"{order_text}\n\n"
        "━━━━━━━━━━━━━━"
    )

    try:

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_message
        )

        await update.message.reply_text(
            "✅ Buyurtmangiz qabul qilindi!\n\n"
            "📩 Buyurtma adminimizga yuborildi.\n"
            "⏳ Tez orada siz bilan bog‘lanamiz."
        )

        context.user_data[
            "waiting_order"
        ] = False

    except Exception as e:

        print(
            "ADMINGA YUBORISHDA XATO:",
            e
        )

        await update.message.reply_text(
            "❌ Buyurtmani yuborishda xatolik yuz berdi."
        )


# =========================
# NARXLAR
# =========================

async def prices(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "💰 AI XIZMATLARI NARXLARI\n\n"
        "🖼 AI Rasm — 5 000–30 000 so‘m\n"
        "🎬 AI Video — 100 000–150 000 so‘m\n"
        "🎯 YouTube Thumbnail — 30 000–60 000 so‘m\n"
        "📢 Reklama rasmi — 50 000–150 000 so‘m\n"
        "👤 AI Avatar — 20 000 so‘m\n\n"
        "📌 Aniq narx buyurtma murakkabligiga qarab belgilanadi."
    )


# =========================
# ADMIN
# =========================

async def admin_contact(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "📞 ADMIN BILAN BOG‘LANISH\n\n"
        "👤 Admin: @shoxruz011\n\n"
        "Buyurtma yoki savollaringiz bo‘lsa yozishingiz mumkin."
    )


# =========================
# ASOSIY HANDLER
# =========================

async def message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.message.contact:

        await receive_contact(
            update,
            context
        )

        return

    if not update.message.text:

        return

    text = update.message.text

    services = [
        "🖼 AI Rasm yaratish",
        "🎬 AI Video yaratish",
        "🎯 YouTube Thumbnail",
        "📢 Reklama rasmi",
        "👤 AI Avatar",
    ]

    if text in services:

        if not context.user_data.get("phone"):

            await request_phone(
                update,
                context
            )

            return

        await request_service(
            update,
            context
        )

    elif text == "💰 Narxlar":

        await prices(
            update,
            context
        )

    elif text == "📞 Admin bilan bog‘lanish":

        await admin_contact(
            update,
            context
        )

    elif context.user_data.get(
        "waiting_order"
    ):

        await receive_order(
            update,
            context
        )

    else:

        await update.message.reply_text(
            "👇 Iltimos, menyudan kerakli "
            "xizmatni tanlang."
        )


# =========================
# BOTNI ISHGA TUSHIRISH
# =========================

def main():

    app = Application.builder().token(
        TOKEN
    ).build()

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            check_subscription,
            pattern="^check_subscription$"
        )
    )

    app.add_handler(
        MessageHandler(
            filters.ALL & ~filters.COMMAND,
            message_handler
        )
    )

    print(
        "🤖 AI Xizmatlari bot ishga tushdi!"
    )

    app.run_polling()


if __name__ == "__main__":

    main()