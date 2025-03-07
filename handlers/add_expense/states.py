from aiogram.fsm.state import State, StatesGroup


class AddExpenseStatesGroup(StatesGroup):
    entering_amount = State()
    entering_name = State()
    choosing_category = State()
