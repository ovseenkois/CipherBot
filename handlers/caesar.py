from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove

from handlers import constants
from project_cipher.caesar import Encode, Decode, DecodeWithoutShift


def make_keyboard(values: list[str]):
    kb = [[types.KeyboardButton(text=i)] for i in values]
    return types.ReplyKeyboardMarkup(keyboard=kb,
                                     resize_keyboard=True,
                                     input_field_placeholder="Выберите тип операции")


available_operations = ['Зашифровать', 'Дешифровать', 'Взломать']
available_language = ['Русский', 'Английский']


class CaesarOrderOperation(StatesGroup):
    choosing_language = State()
    choosing_operation = State()
    choosing_shift = State()
    choosing_string = State()


router = Router()


@router.message(Command('start'))
async def command_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text=constants.welcome_message,
                         parse_mode=ParseMode.MARKDOWN_V2,
                         reply_markup=ReplyKeyboardRemove())


@router.message(Command('help'))
async def command_help(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text=constants.welcome_message,
                         parse_mode=ParseMode.MARKDOWN_V2,
                         reply_markup=ReplyKeyboardRemove())


@router.message(StateFilter(None), Command('caesar'))
async def command_caesar(message: types.Message, state: FSMContext):
    await message.answer(text='Выберите язык',
                         reply_markup=make_keyboard(available_language))
    await state.set_state(CaesarOrderOperation.choosing_language)


@router.message(CaesarOrderOperation.choosing_language, F.text.in_(available_language))
async def language_chosen(message: types.Message, state: FSMContext):
    await state.update_data(chosen_language=message.text.lower())
    await message.answer(text='Введите тип операции',
                         reply_markup=make_keyboard(available_operations))
    await state.set_state(CaesarOrderOperation.choosing_operation)


@router.message(CaesarOrderOperation.choosing_language)
async def language_chosen_wrong(message: types.Message):
    await message.answer(text='Я не знаю такого языка\nВыберите один из предложенных',
                         reply_markup=make_keyboard(available_language))


@router.message(CaesarOrderOperation.choosing_operation, F.text.in_(available_operations[:2]))
async def operation_chosen(message: types.Message, state: FSMContext):
    await state.update_data(chosen_operation=message.text.lower())
    await message.answer(text='Теперь введите ключ(целое число)',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(CaesarOrderOperation.choosing_shift)


@router.message(CaesarOrderOperation.choosing_operation, F.text == available_operations[2])
async def operation_chosen(message: types.Message, state: FSMContext):
    await state.update_data(chosen_operation=message.text.lower())
    await state.update_data(chosen_shift='взлом')
    await message.answer(text='Введите текст',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(CaesarOrderOperation.choosing_string)


@router.message(CaesarOrderOperation.choosing_operation)
async def operation_chosen_wrong(message: types.Message):
    await message.answer(text="Я не знаю такой операции.\nВведите одну из предложенных операций",
                         reply_markup=make_keyboard(available_operations))


@router.message(CaesarOrderOperation.choosing_shift, F.text.isdigit())
async def shift_chosen(message: types.Message, state: FSMContext):
    await state.update_data(chosen_shift=int(message.text))
    await message.answer(text='Введите текст')
    await state.set_state(CaesarOrderOperation.choosing_string)


@router.message(CaesarOrderOperation.choosing_shift)
async def shift_chosen_wrong(message: types.Message):
    await message.answer(text='Такой ключ не подходит\nВведите еще раз(ключ должен быть целым числом)')


@router.message(CaesarOrderOperation.choosing_string, F.text)
async def string_chosen(message: types.Message, state: FSMContext):
    print(message.text)
    await state.update_data(chosen_string=message.text)
    user_data = await state.get_data()
    string = user_data['chosen_string']
    shift = user_data['chosen_shift']
    if user_data['chosen_language'] == 'русский':
        language = 'rus'
    else:
        language = 'eng'
    shift = user_data['chosen_shift']
    if shift == 'взлом':
        new_string = DecodeWithoutShift(string, language)
    else:
        if user_data['chosen_operation'] == 'зашифровать':
            new_string = Encode(string, shift, language)
        else:
            new_string = Decode(string, shift, language)
    await message.answer(text=f'Результат операции: \n{new_string}')
    await state.clear()


@router.message(CaesarOrderOperation.choosing_string)
async def string_chosen_wrong(message: types.Message, state: FSMContext):
    await message.answer(text='Некорректный ввод\nПопробуйте снова')
