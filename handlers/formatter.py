from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest

router = Router()

def get_guides_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📝 Markdown Guide", callback_query_data="guide_md"),
                InlineKeyboardButton(text="🌐 HTML Guide", callback_query_data="guide_html")
            ],
            [
                InlineKeyboardButton(text="🖼 Media & Tags", callback_query_data="guide_media"),
                InlineKeyboardButton(text="📢 Channel Features", callback_query_data="guide_channel")
            ],
            [
                InlineKeyboardButton(text="⬅️ Back to Main Menu", callback_query_data="menu_main")
            ]
        ]
    )

def get_back_to_guides_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Back to Guides", callback_query_data="menu_guides")]
        ]
    )

# --- Guide Handlers ---

@router.callback_query(F.data == "menu_guides")
async def cb_guides_menu(call: CallbackQuery):
    guide_text = (
        "📖 <b>Formatting Guides & Cheatsheets</b>\n\n"
        "Select a topic below to learn how to structure rich messages, expandable text, formulas, and media links."
    )
    await call.message.edit_text(guide_text, reply_markup=get_guides_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "guide_md")
async def cb_guide_md(call: CallbackQuery):
    text = (
        "📝 <b>Markdown Formatting Guide</b>\n\n"
        "<b>Basic Styles:</b>\n"
        "• <code>*bold text*</code> → <b>bold text</b>\n"
        "• <code>_italic text_</code> → <i>italic text</i>\n"
        "• <code>~strikethrough~</code> → <s>strikethrough</s>\n"
        "• <code>||spoiler||</code> → <tg-spoiler>spoiler</tg-spoiler>\n"
        "• <code>`inline code`</code> → <code>inline code</code>\n\n"
        "<b>Code Block:</b>\n"
        "```python\nprint('Hello World')\n```\n\n"
        "<b>Blockquote:</b>\n"
        "<code>> This is a quote message</code>\n\n"
        "Send any Markdown-formatted text to the bot to test it live!"
    )
    await call.message.edit_text(text, reply_markup=get_back_to_guides_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "guide_html")
async def cb_guide_html(call: CallbackQuery):
    text = (
        "🌐 <b>HTML Tags Guide</b>\n\n"
        "Telegram supports a clean subset of HTML tags:\n\n"
        "• <code>&lt;b&gt;bold&lt;/b&gt;</code> → <b>bold</b>\n"
        "• <code>&lt;i&gt;italic&lt;/i&gt;</code> → <i>italic</i>\n"
        "• <code>&lt;u&gt;underline&lt;/u&gt;</code> → <u>underline</u>\n"
        "• <code>&lt;s&gt;strikethrough&lt;/s&gt;</code> → <s>strikethrough</s>\n"
        "• <code>&lt;tg-spoiler&gt;spoiler&lt;/tg-spoiler&gt;</code> → <tg-spoiler>spoiler</tg-spoiler>\n"
        "• <code>&lt;code&gt;code&lt;/code&gt;</code> → <code>code</code>\n"
        "• <code>&lt;a href='URL'&gt;Link Text&lt;/a&gt;</code> → Hyperlink\n"
        "• <code>&lt;blockquote&gt;Quote&lt;/blockquote&gt;</code> → Quote box"
    )
    await call.message.edit_text(text, reply_markup=get_back_to_guides_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "guide_media")
async def cb_guide_media(call: CallbackQuery):
    text = (
        "🖼 <b>Media Embedding & Custom Tags</b>\n\n"
        "<b>Hyperlinked Media (Invisible Preview):</b>\n"
        "You can embed direct image links inside a zero-width space HTML tag to display images without cluttering your text link list:\n\n"
        "<code>&lt;a href=\"https://link-to-your-image.jpg\"&gt;&#8203;&lt;/a&gt;</code>\n\n"
        "<b>Spoiler Media:</b>\n"
        "Wrap text or links inside spoiler tags to keep media hidden until clicked."
    )
    await call.message.edit_text(text, reply_markup=get_back_to_guides_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "guide_channel")
async def cb_guide_channel(call: CallbackQuery):
    text = (
        "📢 <b>Channel Setup & Auto-Formatting</b>\n\n"
        "<b>How to setup:</b>\n"
        "1. Add @RichMDHelpBot as an <b>Administrator</b> to your channel.\n"
        "2. Grant permissions to <b>Post Messages</b> and <b>Edit Messages</b>.\n"
        "3. Any post published or updated in your channel will automatically be formatted using HTML or Markdown settings!"
    )
    await call.message.edit_text(text, reply_markup=get_back_to_guides_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "menu_channel")
async def cb_channel_menu(call: CallbackQuery):
    await cb_guide_channel(call)

@router.callback_query(F.data == "menu_settings")
async def cb_settings_menu(call: CallbackQuery):
    text = (
        "⚙️ <b>Bot Settings</b>\n\n"
        "• <b>Default Parse Mode:</b> HTML / MarkdownV2\n"
        "• <b>Link Preview:</b> Enabled\n"
        "• <b>Channel Auto-Format:</b> Active\n\n"
        "<i>All default parameters are optimized for maximum compatibility.</i>"
    )
    await call.message.edit_text(
        text, 
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="⬅️ Back to Main Menu", callback_query_data="menu_main")]]
        ), 
        parse_mode="HTML"
    )

# --- Echo & Live Preview Engine ---

@router.message(F.text & ~F.text.startswith("/"))
async def process_user_text(message: Message):
    raw_text = message.text

    # Attempt to render as HTML first, fallback to standard text if formatting tags are malformed
    try:
        await message.answer(
            f"✨ <b>Rich Message Preview:</b>\n\n{raw_text}",
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False
        )
    except TelegramBadRequest as e:
        await message.answer(
            f"⚠️ <b>Parsing Error:</b> Your text contains invalid markup tags.\n\n"
            f"<b>Details:</b> <code>{e.message}</code>\n\n"
            "<b>Original Text:</b>\n" + raw_text,
            parse_mode=ParseMode.HTML
        )
