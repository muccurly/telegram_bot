import json
from telegram import Update, LabeledPrice, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, PreCheckoutQueryHandler, MessageHandler, filters, ContextTypes
from flask import Flask, request

# Конфигурация
TELEGRAM_TOKEN = '7446262616:AAEUrocdS7wrmw4HYXoTaDyBr4DZ4-_ZuhM'
PROVIDER_TOKEN = '5740929568:TEST:638563210960780616'

# Данные заказа
TITLE = "Авторский курс от Huga"
DESCRIPTION = "Создание концепции с помощью ИИ"
PAYLOAD = "1"
CURRENCY = "KZT"
PRICE = 37800 * 100  # Сумма указывается в копейках: 37800 тг

PRICES = [LabeledPrice("Тенге", PRICE)]

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌟 Привет всем! Меня зовут Хуга, (https://www.instagram.com/hugastyle) и я прошел путь от международного дизайнера одежды к погружению в мир Искусственного интеллекта. За последние два месяца мой Инстаграм привлек более 100,000 подписчиков со всего мира благодаря моему новому подходу к дизайну, созданному с применением ИИ.\n\n"
        "🚀 Сейчас моя жизнь и мое видение кардинально изменились, и я готов поделиться этим с вами! Представляю вам мой авторский курс по созданию дизайна и концепции с использованием Искусственного интеллекта."
    )
    await update.message.reply_text(
        "🎓 В этом курсе вы освоите:\n\n"
        "Все, что я узнал за свои 8 лет работы в индустрии моды и 2 года в области ИИ.\n"
        "Шаг за шагом от регистрации до создания собственных уникальных дизайнов на моем уровне.\n"
        "💡 Подключитесь к волне будущего прямо сейчас и измените свою жизнь и карьеру!\n\n"
        "💥 Цена курса: $79 / 6980₽ / 37,800тг\n\n"
        "📩 После оплаты вы моментально получите доступ к материалам курса.\n\n"
        "🎯 Ваше внимание очень важно! Присоединяйтесь прямо сейчас и станьте лидером в новой эпохе дизайна с Искусственным интеллектом!\n\n"
        "https://drive.google.com/drive/folders/1-FgiuyA8N3V3RV9xYuaiBMgCQt9IbLie\n"
        "Договор оферты и Политика конфиденциальности",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Оплатить", callback_data="pay")]
        ])
    )

# Обработчик нажатия кнопки "Оплатить"
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat.id

    invoice = {
        "chat_id": chat_id,
        "title": TITLE,
        "description": DESCRIPTION,
        "payload": PAYLOAD,
        "provider_token": PROVIDER_TOKEN,
        "currency": CURRENCY,
        "prices": PRICES,
        "provider_data": json.dumps({
            "InvoiceId": 100,
            "Receipt": {
                "sno": "osn",
                "items": [
                    {
                        "name": TITLE,
                        "quantity": 1,
                        "sum": PRICE,
                        "tax": "vat10",
                        "payment_method": "full_payment",
                        "payment_object": "commodity"
                    }
                ]
            }
        })
    }

    await context.bot.send_invoice(**invoice)

# Обработчик pre_checkout_query
async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query

    if query.invoice_payload != PAYLOAD:
        await query.answer(ok=False, error_message="Что-то пошло не так...")
    else:
        await query.answer(ok=True)

# Обработчик successful_payment
async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    successful_payment = update.message.successful_payment
    await update.message.reply_text("Оплата прошла успешно! Можешь по этой ссылке вступить в группу: https://t.me/+B_me4k9U1WdmNjEy")

application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button_callback, pattern="pay"))
application.add_handler(PreCheckoutQueryHandler(precheckout_callback))
application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), application.bot)
        application.process_update(update)
        return 'ok'
    except Exception as e:
        print(f"Error: {e}")
        return 'error', 500

if __name__ == '__main__':
    app.run()
