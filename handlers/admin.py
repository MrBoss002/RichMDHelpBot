import asyncio
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter
import config
from database import get_total_users, get_all_users

router = Router()

# Admin Filter Helper
def is_admin(user_id: int) -> bool:
    return user_id == config.ADMIN_ID

@router.message(Command("stats"))
async def cmd_stats(message: Message):
    if not is_admin(message.from_user.id):
        return  # Ignore command for non-admins

    total_users = await get_total_users()
    stats_text = (
        "📊 <b>Bot Analytics & Statistics</b>\n\n"
        f"👤 <b>Total Registered Users:</b> {total_users}\n"
        f"⚙️ <b>Environment Status:</b> Operational"
    )
    await message.answer(stats_text, parse_mode="HTML")

@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message):
    if not is_admin(message.from_user.id):
        return  # Ignore command for non-admins

    # The broadcast message should be either replied to or provided after the command
    if message.reply_to_message:
        broadcast_msg = message.reply_to_message
    else:
        # Extract text after /broadcast
        command_args = message.text.split(maxsplit=1)
        if len(command_args) < 2:
            await message.answer(
                "⚠️ <b>Broadcast Usage:</b>\n\n"
                "1. Reply to any message with <code>/broadcast</code>\n"
                "2. Or type <code>/broadcast Your message text here</code>",
                parse_mode="HTML"
            )
            return
        broadcast_text = command_args[1]
        broadcast_msg = None

    users = await get_all_users()
    if not users:
        await message.answer("⚠️ No users found in the database to broadcast to.")
        return

    status_msg = await message.answer(f"⏳ <i>Broadcasting message to {len(users)} users...</i>", parse_mode="HTML")

    success_count = 0
    blocked_count = 0
    failed_count = 0

    for user_id in users:
        try:
            if broadcast_msg:
                await broadcast_msg.copy_to(chat_id=user_id)
            else:
                await message.bot.send_message(chat_id=user_id, text=broadcast_text, parse_mode="HTML")
            success_count += 1
            await asyncio.sleep(0.05)  # Rate limiting delay (~20 msgs/sec)
        except TelegramForbiddenError:
            blocked_count += 1
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            try:
                if broadcast_msg:
                    await broadcast_msg.copy_to(chat_id=user_id)
                else:
                    await message.bot.send_message(chat_id=user_id, text=broadcast_text, parse_mode="HTML")
                success_count += 1
            except Exception:
                failed_count += 1
        except Exception:
            failed_count += 1

    report_text = (
        "📢 <b>Broadcast Completed</b>\n\n"
        f"✅ <b>Successfully Delivered:</b> {success_count}\n"
        f"🚫 <b>Blocked/Deactivated:</b> {blocked_count}\n"
        f"❌ <b>Failed Deliveries:</b> {failed_count}"
    )
    await status_msg.edit_text(report_text, parse_mode="HTML")
