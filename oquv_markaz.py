from aiogram import Bot, Dispatcher, types,F
from aiogram.filters import CommandStart
from aiogram.types import Message
import asyncio
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from database import *

bot = Bot(token="7983230662:AAG2N4tMpLvPKzuD43GtgyPQ8CgVQuANMME")


class RegisterForm(StatesGroup):
    course_name = State()
    course_price = State()
    complete_information = State()
    teacher = State()


dp = Dispatcher()

def reply_buttons():
    btns = [
             [types.KeyboardButton(text='Oquv kurslar'),
              types.KeyboardButton(text='Bizning afzalliklarimiz'),
              types.KeyboardButton(text='Kurs qoshish')]
              ]
    buttons = types.ReplyKeyboardMarkup(keyboard=btns,resize_keyboard=True)
    return buttons
    
def inline_buttons():
    builder = InlineKeyboardBuilder()
    courses = get_all_course_data()
    for i in courses:
        builder.row(
            InlineKeyboardButton(text=f'{i[0]}',callback_data=f'course_{i[1]}'),
        )

    return builder.as_markup()
    
        

@dp.message(CommandStart())
async def start(message:Message,state:FSMContext):
    await message.reply(text='Botimiszga hush kelibsiz',reply_markup=reply_buttons())


@dp.message(F.text =='Oquv kurslar')
async def set_oquv_kurslar(message:Message):
    if len(get_all_course_data())!=0:
        await message.answer(text='Mavjud kurslar',reply_markup=inline_buttons())
    else:
        await message.answer(text='Afsuski xozir kurslar mavjud emas')

@dp.callback_query(lambda c: c.data and c.data.startswith('course_'))
async def callback_ansert(callback_query: types.CallbackQuery, state: FSMContext):
    data = get_count_course()
    course_name_element = int(callback_query.data.split('_')[1])
    course_name_index = course_name_element-1
    if course_name_index < len(get_count_course()):
        course_name = data[course_name_index]
        text = (f'Kurs nomi: {course_name[1]}\nKurs narhi: {course_name[2]}\nKurs xaqida: {course_name[3]}\nO`qituvchi: {course_name[4]}')
        await callback_query.message.answer(text=text)
    else:
        await callback_query.message.answer(text='Kurs topilmadi')

@dp.message(F.text =='Bizning afzalliklarimiz')
async def set_bizning_afzalliklarimiz(message:Message,):
    await message.answer(text='Biz haqimizda toliq malumot olish uchun admin bilan boglaning')
    


@dp.message(lambda message:message.text =='Kurs qoshish')
async def set_kurs_qoshish(message:Message,state:FSMContext):
    if message.from_user.id == 5425737535:  
        create_table_course_data()
        await message.answer(text='Kurs nomini kiriting')
        await state.set_state(RegisterForm.course_name)
    else:
        await message.answer(text='Afsuski! Kurs qoshish bolimidan faqatgina admin profilida foydalanish mumkin')

    @dp.message(RegisterForm.course_name)
    async def set_course_name(message: Message, state: FSMContext):
        await state.update_data(course_name=message.text)
        await message.answer(text='Kurs narhini kiriting')
        await state.set_state(RegisterForm.course_price)

    @dp.message(RegisterForm.course_price) 
    async def set_course_price(message:Message,state:FSMContext):
        await state.update_data(course_price=message.text)
        await message.answer(text='Toliq malumot kiriting')
        await state.set_state(RegisterForm.complete_information)

    @dp.message(RegisterForm.complete_information)
    async def set_complete_information(message:Message,state:FSMContext):
        await state.update_data(complete_information=message.text)
        await message.answer(text='Kurs oqituvchisi xaqida malumot kiriting')
        await state.set_state(RegisterForm.teacher)

    @dp.message(RegisterForm.teacher)
    async def set_teacher(message:Message,state:FSMContext):
        await state.update_data(teacher=message.text) 
        data = await state.get_data()
        inset_row_course_data(data['course_name'],data['course_price'],data['complete_information'],data['teacher'])
        await message.answer(text='Kurs muvaffaqqiyatli qoshildi')
        
   




async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
