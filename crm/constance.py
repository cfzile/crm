MAIN_PAGE_NAME = 'Главная'
SITE_SIGN_UP_NAME = 'Регистрация'
SITE_SIGN_IN_NAME = 'Вход'
PROFILE_PAGE_NAME = 'Профиль'
NON_CORRECT_DATA = 'Введены некорректные данные'
EVENT_INFO = "Инфо."
EVENT_ERROR = "Ошибка"
SUCCESSFUL = "Операция прошла успешно."

TASKS_PAGE_NAME = 'Задачи'
TESTS_PAGE_NAME = 'Тесты'
TEMPLATES_PAGE_NAME = 'Шаблоны'
SUBORDINATES_PAGE_NAME = 'Подчиненные'

PAGES = [[PROFILE_PAGE_NAME, 'home'], [TASKS_PAGE_NAME, 'tasks'], [TESTS_PAGE_NAME, 'grade'],
         [TEMPLATES_PAGE_NAME, 'grade_templates'], [SUBORDINATES_PAGE_NAME, 'subordinates']]

GRADE_TEMPLATE_TYPES_LIST = [(0, 'авто'), (1, 'оценка сотрудником'), (1, 'оценка руководителем')]
GRADE_TEMPLATE_TYPES_DICT = {i[0]: i[1] for i in GRADE_TEMPLATE_TYPES_LIST}
GRADE_STATUS_DICT = {0: 'Назначен', 1: 'Пройден'}

ROLE_LIST = [(0, 'руководитель'), (1, 'сотрудник'), (2, 'клиент')]
ROLE_DICT = {i[0]: i[1] for i in ROLE_LIST}

PROTOTYPE_LIST = [(-1, '-'), (1, 'Кафе'), (2, 'Офис'), (3, 'Магазин')]
PROTOTYPE_DICT = {i[0]: i[1] for i in PROTOTYPE_LIST}
