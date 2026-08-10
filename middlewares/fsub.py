from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ChatMemberStatus
import config

class ForceSubMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any]
    ) -> Any:
        # Extract user_id and chat context
        user = data.get("event_from_user")
        if not user:
            return await handler(event, data)

        # Skip check for admins
        if user.id == config.ADMIN_ID:
            return await handler(event, data)

        bot = data["bot"]
        
        try:
            member = await bot.get_chat_member(chat_id=config.FSUB_CHANNEL_ID, user_id=user.id)
            if member.status in [ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
                return await handler(event, data)
        except Exception as e:
            # If bot is not admin in the channel or fails to check, continue execution gracefully
            return await handler(event, data)

        # User is NOT subscribed -> Block action and show Join button
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="📢 Join Channel", url=config.FSUB_CHANNEL_LINK)
                ],
                [
                    InlineKeyboardButton(text="🔄 Try Again", callback_query_data="check_fsub")
                ]
            ]
        )

        fsub_text = (
            "⚠️ <b>Access Denied!</b>\n\n"
            "To use this bot, you must first subscribe to our official channel."
        )

        if isinstance(event, Message):
            await event.answer(fsub_text, reply_markup=keyboard, parse_mode="HTML")
        elif isinstance(event, CallbackQuery):
            await event.answer("⚠️ Please join the channel first!", show_alert=True)
            await event.message.answer(fsub_text, reply_markup=keyboard, parse_mode="HTML")

        return
