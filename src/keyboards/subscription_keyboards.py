from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def subscription_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Подписаться", callback_data="subscribe"),
                InlineKeyboardButton(text="Отписаться", callback_data="unsubscribe")
            ],
            [
                InlineKeyboardButton(text="В меню", callback_data="back_to_main_menu")
            ]
        ]
    )
