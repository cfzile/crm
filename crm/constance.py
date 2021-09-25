MAIN_PAGE_NAME = 'Главная'
SITE_SIGN_UP_NAME = 'Регистрация'
SITE_SIGN_IN_NAME = 'Вход'
SHOW_PORTFOLIO_PAGE_NAME = 'Портфель: %s'
CREATE_PORTFOLIO_PAGE_NAME = 'Создать портфель'
COMPARE_PORTFOLIOS_PAGE_NAME = 'Сравнить портфели'
NON_CORRECT_DATA = 'Введены некорректные данные'
EVENT_INFO = "Инфо."
EVENT_ERROR = "Ошибка"
SUCCESSFUL = "Операция прошла успешно."
PAGES = [['Профиль', 'home'], ['Задачи', 'tasks'], ['Тесты', 'grade'],
         # ['События', 'events'],
         ['Шаблоны', 'grade_templates']]

GRADE_TEMPLATE_TYPES_LIST = [(0, 'авто'), (1, 'оценка сотрудником'), (1, 'самооценка')]
GRADE_TEMPLATE_TYPES_DICT = {i[0]: i[1] for i in GRADE_TEMPLATE_TYPES_LIST}
GRADE_STATUS_DICT = {0: 'Назначен', 1: 'Пройден'}