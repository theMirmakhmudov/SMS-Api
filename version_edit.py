import asyncio
import logging
import this

from aiogram import Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import buttons
from config import TOKEN, API_KEY
from aiogram import Bot
import requests


class Form(StatesGroup):
    phone_number = State()
    sms_text = State()
    finish = State()


dp = Dispatcher()

count = 0


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"<b>Assalomu Aleykum, Xurmatli {message.from_user.mention_html()}</b>",
                         reply_markup=buttons.keyboard1)

    @dp.message(F.text == "SMS Yuborish ✉️")
    async def send_sms(message: types.Message, state: FSMContext):
        await state.set_state(Form.phone_number)
        edit_mes = await message.answer(
            "<b>SMS yuborish uchun telefon raqamingizni yuboring\nExample: +998913483370</b>")

        @dp.message(Form.phone_number)
        async def upload_contact(message: types.Message, state: FSMContext, bot: Bot):
            if len(message.text) == 13:
                await state.update_data(phone_number=message.text)
                await state.set_state(Form.sms_text)
                await message.delete()
                await bot.edit_message_text(chat_id=message.chat.id, message_id=edit_mes.message_id,
                                            text="<b>SMS yuborish uchun sms matnini yuboring</b>")
            else:
                await message.answer("<b>Siz noto'g'ri raqam yubordingiz qayta yuboring\nExample: +998913483370</b>")

        @dp.message(Form.sms_text)
        async def upload_text(message: types.Message, state: FSMContext, bot: Bot):
            await state.update_data(sms_text=message.text)
            await message.delete()
            await state.set_state(Form.finish)
            await bot.edit_message_text(chat_id=message.chat.id, text="<b>Ma'lumotlaringiz qabul qilindi ✅</b>",
                                        message_id=edit_mes.message_id)

            data = await state.get_data()
            await state.clear()
            phone_number = data.get("phone_number", "Unknown")
            sms_text = data.get("sms_text", "Unknown")
            import requests

            url = "https://whatsms.p.rapidapi.com/send_sms"

            querystring = {"phone_number": f"{phone_number}", "message": f"{sms_text}"}

            payload = {}
            headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key": API_KEY,
                "X-RapidAPI-Host": "whatsms.p.rapidapi.com"
            }

            response = requests.post(url, json=payload, headers=headers, params=querystring)

            print(response.json())

            await message.answer("SMS muvaffaqiyatli yuborildi")
            await bot.delete_message(chat_id=message.chat.id, message_id=edit_mes.message_id)


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot, polling_timeout=1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
