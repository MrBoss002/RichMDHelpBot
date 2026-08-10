from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
import config
from database import add_user

router = Router()

def get_main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📖 Formatting Guides", callback_query_data="menu_guides"),
                InlineKeyboardButton(text="📢 Channel Settings", callback_query_data="menu_channel")
            ],
            [
                InlineKeyboardButton(text="ℹ️ About Bot", callback_query_data="menu_about"),
                InlineKeyboardButton(text="⚙️ Settings", callback_query_data="menu_settings")
            ]
        ]
    )

def get_back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Back to Main Menu", callback_query_data="menu_main")]
        ]
    )

@router.message(CommandStart())
async def cmd_start(message: Message):
    await add_user(message.from_user.id)
    welcome_text = (
        f"👋 Welcome <b>{message.from_user.full_name}</b> to <b>RichMDHelpBot</b>!\n\n"
        "Send me any text formatted in Markdown or HTML to generate instant rich messages, "
        "or link your channels to enable auto-formatting and custom footers.\n\n"
        "Use the menu below to explore features and guides:"
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard(), parse_mode="HTML")

@router.message(Command("about"))
async def cmd_about(message: Message):
    await show_about(message)

async def show_about(target: Message | CallbackQuery):
    about_text = (
        "🤖 <b>Rich Text Formatting Bot</b>\n\n"
        "Transform standard text into beautifully formatted Telegram posts with headers, "
        "code blocks, custom footers, and rich media blocks.\n\n"
        "👨‍💻 <b>Admin:</b> @MrBoss002\n"
        "📢 <b>Dev Channel:</b> @MrBossTG\n"
        "🛠 <b>Language / Stack:</b> Python 3.11+ (aiogram 3.x)\n"
        f"🔗 <b>GitHub Repository:</b> <a href='{config.REPO_URL}'>RichMDHelpBot</a>\n"
        "🎓 <b>Video Tutorials:</b> <i>Coming Soon</i>\n\n"
        "Built for clean channel management and rapid message design."
    )
    
    keyboard = get_back_keyboard()
    
    if isinstance(target, CallbackQuery):
        await target.message.edit_text(about_text, reply_markup=keyboard, parse_mode="HTML", disable_web_page_preview=True)
    else:
        await target.answer(about_text, reply_markup=keyboard, parse_mode="HTML", disable_web_page_preview=True)

@router.callback_query(F.data == "menu_main")
async def cb_main_menu(call: CallbackQuery):
    welcome_text = (
        f"👋 Welcome <b>{call.from_user.full_name}</b> to <b>RichMDHelpBot</b>!\n\n"
        "Send me any text formatted in Markdown or HTML to generate instant rich messages, "
        "or link your channels to enable auto-formatting and custom footers."
    )
    await call.message.edit_text(welcome_text, reply_markup=get_main_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "menu_about")
async def cb_about_menu(call: CallbackQuery):
    await show_about(call)

@router.callback_query(F.data == "check_fsub")
async def cb_check_fsub(call: CallbackQuery):
    await call.answer("✅ Verification successful!", show_alert=True)
    await cb_main_menu(call)
