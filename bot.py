import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.client.bot import DefaultBotProperties

API_TOKEN = "7478788701:AAH0QzJSV4BPVywo9V4AGEU-YwBv917Pplw"
CHANNEL_ID = -1002519824012
CHANNEL_LINK = "https://t.me/+kB5yMneuZko4ZWQ0"
REGISTRATION_LINK = "https://1wzyuh.com/casino/list?open=register&p=j47j"
PROMO_CODE = "AMG1WIN"

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
user_data = {}

def get_main_menu(lang: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🚀Lucky Jet", callback_data="game_Lucky Jet")],
        [InlineKeyboardButton(text="💣Mines", callback_data="game_CaveMines")],
        [InlineKeyboardButton(text="🔥Rocet Queen", callback_data="game_Rocet Queen")],
        [InlineKeyboardButton(text="🚘Speed & Cash", callback_data="game_Speed & Cash")],
        [InlineKeyboardButton(text="👾Rocket X", callback_data="game_Rocket X")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def is_subscribed(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ("member", "administrator", "creator")
    except Exception:
        return False

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    lang_keyboard = InlineKeyboardMarkup(inline_keyboard=[[ 
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en")
    ]])
    await message.answer("<b>Установите язык / Set the language.</b>", reply_markup=lang_keyboard)

@dp.callback_query(F.data.startswith("lang_"))
async def language_selected(callback: types.CallbackQuery):
    lang = callback.data.split("_")[1]
    user_data[callback.from_user.id] = {"lang": lang}

    text = {
        "ru": "<b>Чтобы воспользоваться ботом, подпишитесь на канал.</b>",
        "en": "<b>To use the bot, subscribe to the channel.</b>"
    }[lang]

    subscribe_btn = InlineKeyboardButton(
        text={"ru": "Подписаться", "en": "Subscribe"}[lang],
        url=CHANNEL_LINK
    )
    check_btn = InlineKeyboardButton(
        text={"ru": "Проверить подписку", "en": "Check Subscription"}[lang],
        callback_data=f"check_sub_{lang}"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [subscribe_btn],
        [check_btn]
    ])

    await callback.message.delete()

    await callback.message.answer(text, reply_markup=keyboard)

@dp.callback_query(F.data.startswith("check_sub_"))
async def check_subscription(callback: types.CallbackQuery):
    lang = callback.data.split("_")[-1]
    user_data[callback.from_user.id] = {"lang": lang}
    subscribed = await is_subscribed(callback.from_user.id)

    if subscribed:
        msg = {"ru": "Выберите игру:", "en": "Choose a game:"}[lang]

        await callback.message.delete()

        await callback.message.answer(msg, reply_markup=get_main_menu(lang))
    else:
        await callback.answer({
            "ru": "Вы не подписаны на канал!",
            "en": "You are not subscribed to the channel!"
        }[lang], show_alert=True)

@dp.callback_query(F.data.startswith("game_"))
async def game_selected(callback: types.CallbackQuery):
    lang = user_data.get(callback.from_user.id, {}).get("lang", "ru")
    name = callback.from_user.full_name

    text = {
        "ru": (
            "<b>Для получения сигналов вам необходимо подключить новый аккаунт 1win.</b>\n"
            "1. При регистрации введите промокод \"AMG1WIN\".\n"
            "2. Внесите депозит от 1000₽\n"
            "3. После регистрации нажмите на кнопку \"Проверить регистрацию\".\n"
        ),
        "en": (
            "<b>To receive the signals, you need to connect a new 1win account.</b>\n"
            "1. When registering, enter the promo code \"AMG1WIN\".\n"
            "2. Make a deposit of 10$\n"
            "3. After registration, click on the \"Check registration\" button.\n"
        )
    }[lang]

    buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text={"ru": "Регистрация", "en": "Register"}[lang], url=REGISTRATION_LINK)],
        [InlineKeyboardButton(text={"ru": "Проверить регистрацию", "en": "Check registration"}[lang], callback_data="check_reg")]
    ])

    await callback.message.delete()

    await callback.message.answer(text, reply_markup=buttons)

@dp.callback_query(F.data == "check_reg")
async def check_registration(callback: types.CallbackQuery):
    lang = user_data.get(callback.from_user.id, {}).get("lang", "ru")
    if lang not in ["ru", "en"]:
        lang = "ru"
    
    messages = {
        "ru": (
            "Ошибка синхронизации аккаунта!\n\n"
            "Возможные причины:\n"
            "- Используется старый аккаунт.\n"
            "- Промокод не был введен.\n"
            "- Депозит не был внесен."
        ),
        "en": (
            "Account synchronization error!\n\n"
            "Possible causes:\n"
            "- The old account is being used.\n"
            "- The promocode was not entered.\n"
            "- No deposit has been made."
        )
    }
    await callback.answer(messages[lang], show_alert=True)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
