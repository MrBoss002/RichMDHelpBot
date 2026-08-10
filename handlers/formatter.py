import re
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest

from database import set_channel_footer, get_channel_footer, delete_channel_footer

router = Router()

# --- Custom Markdown / Shorthand Transpiler ---

def parse_custom_markdown(text: str) -> str:
    # 1. Code block shortcut: /// code /// -> <pre><code>code</code></pre>
    text = re.sub(r"///\n?(.*?)\n?///", r"<pre><code>\1</code></pre>", text, flags=re.DOTALL)

    # 2. Collapsible block shortcut: ???Title??? Body -> <details><summary>Title</summary>Body</details>
    text = re.sub(r"\?\?\?(.*?)\?\?\?\s*(.*)", r"<details><summary>\1</summary>\2</details>", text)

    # 3. Pull-quote shortcut: """quote — author""" -> <aside>quote<cite>author</cite></aside>
    text = re.sub(r'"""(.*?)\s*—\s*(.*?)"""', r"<aside>\1<cite>\2</cite></aside>", text)

    # 4. Formulas shortcut: $ formula $ and $$ formula $$
    text = re.sub(r"\$\$(.*?)\$\$", r"<tg-math-block>\1</tg-math-block>", text, flags=re.DOTALL)
    text = re.sub(r"\$(.*?)\$", r"<tg-math>\1</tg-math>", text)

    # 5. Headings: #_ Heading -> Bold Header
    text = re.sub(r"^#+_\s*(.*?)$", r"<b>\1</b>", text, flags=re.MULTILINE)

    # 6. Checkboxes: - [ ] and - [x]
    text = re.sub(r"^- \[ \]\s*", r"☐ ", text, flags=re.MULTILINE)
    text = re.sub(r"^- \[x\]\s*", r"☑️ ", text, flags=re.MULTILINE)

    # 7. Horizontal rule: --- -> divider line
    text = re.sub(r"^---$", r"━━━━━━━━━━━━━━━━━━", text, flags=re.MULTILINE)

    # 8. Standard Markdown bold/italic fallback
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)", r"<i>\1</i>", text)

    return text

# --- Keyboards ---

def get_guides_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📖 Markdown Guide", callback_query_data="guide_md"),
                InlineKeyboardButton(text="🌐 HTML Guide", callback_query_data="guide_html")
            ],
            [
                InlineKeyboardButton(text="🖼 Media Guide", callback_query_data="guide_media"),
                InlineKeyboardButton(text="📢 Channel Guide", callback_query_data="guide_channel")
            ],
            [
                InlineKeyboardButton(text="🎨 Full Demo", callback_query_data="guide_demo"),
                InlineKeyboardButton(text="ℹ️ About", callback_query_data="menu_about")
            ]
        ]
    )

def get_back_to_guides_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Back to Menu", callback_query_data="menu_guides")]
        ]
    )

# --- Interactive Guide Handlers ---

@router.callback_query(F.data == "menu_guides")
async def cb_guides_menu(call: CallbackQuery):
    guide_text = (
        "📖 <b>Formatting Guides</b>\n\n"
        "Send Markdown or HTML formatted text directly to this bot. "
        "The bot will return a beautifully formatted preview that you can forward directly to your channel!"
    )
    await call.message.edit_text(guide_text, reply_markup=get_guides_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "guide_md")
async def cb_guide_md(call: CallbackQuery):
    text = (
        "📖 <b>Markdown Guide</b>\n\n"
        "<b>Text styles:</b>\n"
        "<code>**bold**</code> <code>*italic*</code> <code>~~strike~~</code> <code>`code`</code>\n\n"
        "<b>Headings:</b>\n"
        "<code>#_ Heading 1</code>\n"
        "<code>##_ Heading 2</code>\n\n"
        "<b>Lists & Tasks:</b>\n"
        "- milk\n"
        "- [ ] todo\n"
        "- [x] done\n\n"
        "<b>Code block shortcut:</b>\n"
        "<code>///\nprint('hello')\n///</code>"
    )
    await call.message.edit_text(text, reply_markup=get_back_to_guides_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "guide_html")
async def cb_guide_html(call: CallbackQuery):
    text = (
        "🌐 <b>HTML Guide</b>\n\n"
        "<b>Text styles:</b>\n"
        "<code>&lt;b&gt;bold&lt;/b&gt;</code> <code>&lt;i&gt;italic&lt;/i&gt;</code> <code>&lt;u&gt;underline&lt;/u&gt;</code> <code>&lt;tg-spoiler&gt;spoiler&lt;/tg-spoiler&gt;</code>\n\n"
        "<b>Expandable & quotes:</b>\n"
        "<code>&lt;details&gt;&lt;summary&gt;Title&lt;/summary&gt;Content&lt;/details&gt;</code>\n"
        "<code>&lt;blockquote&gt;Quote&lt;/blockquote&gt;</code>\n\n"
        "<b>Formulas:</b>\n"
        "<code>&lt;tg-math&gt;x^2 + y^2&lt;/tg-math&gt;</code>"
    )
    await call.message.edit_text(text, reply_markup=get_back_to_guides_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "guide_media")
async def cb_guide_media(call: CallbackQuery):
    text = (
        "🖼 <b>Media Guide</b>\n\n"
        "<b>Single Photo / Video:</b>\n"
        "<code>![caption](https://example.com/photo.jpg)</code>\n\n"
        "<b>Invisible Media Preview:</b>\n"
        "<code>&lt;a href=\"https://link-to-your-image.jpg\"&gt;&#8203;&lt;/a&gt;</code>"
    )
    await call.message.edit_text(text, reply_markup=get_back_to_guides_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "guide_channel")
async def cb_guide_channel(call: CallbackQuery):
    text = (
        "📢 <b>Channel Setup</b>\n\n"
        "1. Send your formatted raw text to this bot.\n"
        "2. The bot will instantly return the rendered message.\n"
        "3. Forward that message directly into your channel!\n\n"
        "<b>Footer Management:</b>\n"
        "• <code>/setfooter &lt;channel_id&gt; &lt;text&gt;</code>\n"
        "• <code>/delfooter &lt;channel_id&gt;</code>"
    )
    await call.message.edit_text(text, reply_markup=get_back_to_guides_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "guide_demo")
async def cb_guide_demo(call: CallbackQuery):
    text = (
        "🎨 <b>Full Demo</b>\n"
        "A sample showing every feature together:\n\n"
        "<b>1) Styles</b>\n"
        "<b>bold</b> · <i>italic</i> · <s>strike</s> · <code>code</code> · <u>underline</u> · <tg-spoiler>spoiler</tg-spoiler>\n\n"
        "<b>2) Lists & tasks</b>\n"
        "• first item\n"
        "• second item\n"
        "☑️ done\n"
        "☐ pending\n\n"
        "<b>3) Quote</b>\n"
        "<blockquote>Knowledge is power. Always.</blockquote>\n\n"
        "<b>4) Pull-quote</b>\n"
        "<aside>Simplicity is the ultimate sophistication.<cite>Da Vinci</cite></aside>\n\n"
        "<b>5) Formulas</b>\n"
        "Inline <tg-math>a^2 + b^2 = c^2</tg-math> and block:\n"
        "<tg-math-block>\\sum_{i=1}^n i = \\frac{n(n + 1)}{2}</tg-math-block>\n\n"
        "<b>6) Code block</b>\n"
        "<pre><code class=\"language-python\">def hi():\n    print(\"hello world\")</code></pre>\n\n"
        "<b>7) Table</b>\n"
        "<table>"
        "<tr><th>Name</th><th>Score</th></tr>"
        "<tr><td>Ali</td><td>95</td></tr>"
        "<tr><td>Reza</td><td>88</td></tr>"
        "</table>\n\n"
        "<b>8) Expandable</b>\n"
        "<details><summary>Tap to reveal</summary>Hidden content revealed!</details>\n\n"
        "<b>9) Live time & map</b>\n"
        "[time: 2026-07-01 20:00] [map: 35.6892, 51.3890]"
    )
    await call.message.edit_text(
        text, 
        reply_markup=get_back_to_guides_keyboard(), 
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )

@router.callback_query(F.data == "menu_about")
async def cb_menu_about(call: CallbackQuery):
    text = (
        "ℹ️ <b>About RichMDHelpBot</b>\n\n"
        "This bot helps channel admins format text, create code snippets, build tables, insert math formulas, "
        "and generate clean channel posts that can be forwarded directly."
    )
    await call.message.edit_text(text, reply_markup=get_back_to_guides_keyboard(), parse_mode="HTML")

# --- Footer Commands ---

@router.message(F.text.startswith("/setfooter"))
async def cmd_set_footer(message: Message):
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.answer("⚠️ <b>Usage:</b> <code>/setfooter &lt;channel_id&gt; &lt;footer_text&gt;</code>", parse_mode="HTML")
        return
    try:
        channel_id = int(args[1])
        await set_channel_footer(channel_id, args[2])
        await message.answer(f"✅ Footer saved for channel ID <code>{channel_id}</code>", parse_mode="HTML")
    except ValueError:
        await message.answer("❌ Invalid channel ID.", parse_mode="HTML")

@router.message(F.text.startswith("/delfooter"))
async def cmd_del_footer(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("⚠️ <b>Usage:</b> <code>/delfooter &lt;channel_id&gt;</code>", parse_mode="HTML")
        return
    try:
        channel_id = int(args[1])
        await delete_channel_footer(channel_id)
        await message.answer(f"🗑 Footer removed for channel ID <code>{channel_id}</code>", parse_mode="HTML")
    except ValueError:
        await message.answer("❌ Invalid channel ID.", parse_mode="HTML")

# --- Channel Auto-Post & User Renderer Handlers ---

@router.channel_post(F.text)
async def auto_format_channel_post(post: Message):
    footer = await get_channel_footer(post.chat.id)
    raw = parse_custom_markdown(post.text)
    final_text = f"{raw}\n\n{footer}" if footer else raw
    try:
        await post.edit_text(final_text, parse_mode=ParseMode.HTML, disable_web_page_preview=False)
    except TelegramBadRequest:
        pass

@router.message(F.text & ~F.text.startswith("/"))
async def process_user_text(message: Message):
    formatted = parse_custom_markdown(message.text)
    try:
        await message.answer(formatted, parse_mode=ParseMode.HTML, disable_web_page_preview=False)
    except TelegramBadRequest as e:
        await message.answer(f"⚠️ <b>Parsing Error:</b>\n<code>{e.message}</code>", parse_mode="HTML")
