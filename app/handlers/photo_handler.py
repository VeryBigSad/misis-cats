from aiogram import Bot, F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MessageOriginHiddenUser,
    MessageOriginUser,
)

from config.settings import ADMIN_CHAT_ID, CHANNEL_CHAT_ID
from constants.texts import (
    PHOTO_RECEIVED_MESSAGE,
    SINGLE_PHOTO_REQUEST,
    FORWARDED_PHOTO_DECLINED,
)

router = Router()


class PhotoCallback(CallbackData, prefix="photo"):
    action: str
    message_id: int


@router.message(F.media_group_id)
async def handle_media_group(message: types.Message):
    await message.answer(SINGLE_PHOTO_REQUEST)


@router.message(F.photo)
async def handle_photo(message: types.Message):
    if isinstance(
        message.forward_origin, (types.MessageOriginChannel, types.MessageOriginChat)
    ):
        await message.answer(FORWARDED_PHOTO_DECLINED)
        return

    keyboard = create_admin_keyboard(message)
    await forward_to_admin(message, keyboard)
    await message.answer(PHOTO_RECEIVED_MESSAGE)


# Обработчик для кнопок
@router.callback_query(PhotoCallback.filter())
async def handle_photo_callback(
    callback_query: types.CallbackQuery, callback_data: PhotoCallback
):
    action = callback_data.action
    message_id = callback_data.message_id
    bot = callback_query.bot

    if action.startswith("approve"):
        await approve_photo(bot, callback_query, action, message_id)
    elif action == "skip":
        await skip_photo(callback_query)

    await callback_query.answer()


def create_admin_keyboard(message: types.Message) -> InlineKeyboardMarkup:
    buttons = []
    if message.caption:
        buttons.append(
            [create_button("✅ С комментарием", "approve_with_comment", message)]
        )
    buttons.extend(
        [
            [create_button("✅ Без комментария", "approve_without_comment", message)],
            [create_button("⏭️ Пропустить", "skip", message)],
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_button(
    text: str, action: str, message: types.Message
) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=text,
        callback_data=PhotoCallback(
            action=action, message_id=message.message_id
        ).pack(),
    )


async def forward_to_admin(message: types.Message, keyboard: InlineKeyboardMarkup):
    await message.bot.send_chat_action(chat_id=ADMIN_CHAT_ID, action="upload_photo")
    forwarded_msg = await message.forward(ADMIN_CHAT_ID)
    await message.bot.send_message(
        ADMIN_CHAT_ID,
        "Ревью фото:",
        reply_markup=keyboard,
        reply_to_message_id=forwarded_msg.message_id,
    )


async def approve_photo(
    bot: Bot, callback_query: types.CallbackQuery, action: str, message_id: int
):
    admin_message = callback_query.message
    original_message = admin_message.reply_to_message

    if original_message and original_message.forward_origin:
        caption = original_message.caption if action == "approve_with_comment" else None
        photo_id = original_message.photo[-1].file_id

        if isinstance(original_message.forward_origin, MessageOriginUser):
            user = original_message.forward_origin.sender_user
            if user.username:
                user_mention = (
                    f'<a href="https://t.me/{user.username}">{user.full_name}</a>'
                )
            else:
                user_mention = user.full_name
        elif isinstance(original_message.forward_origin, MessageOriginHiddenUser):
            user_mention = original_message.forward_origin.sender_user_name
        else:
            admin_message.edit_caption(
                "что-то не так - сообщение переслано не от юзера(?)"
            )

        full_caption = f"<i>Фото от {user_mention}</i>"
        if caption:
            full_caption += f"\n\n{caption}"

        await bot.send_photo(
            CHANNEL_CHAT_ID,
            parse_mode=ParseMode.HTML,
            photo=photo_id,
            caption=full_caption,
        )
        await admin_message.edit_text("Фото одобрено и отправлено в канал.")
    else:
        await admin_message.edit_text(
            "Ошибка: не удалось получить информацию о сообщении."
        )


async def skip_photo(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text("Фото пропущено.")
