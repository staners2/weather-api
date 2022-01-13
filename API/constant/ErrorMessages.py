

class ErrorMessages(object):
    NOT_FOUND_REQUIRED_PARAMS = "Не заполнены все поля для запроса"

    REGISTRATION_ERROR_400 = "Данный пользователь уже зарегистрирован"
    LOGIN_ERROR_401 = "Пользователя с такими данными не существует"

    COUNTRIES_NOT_FOUND = "Страны с такими параметрами не найдено"

    HISTORIES_NOT_FOUND = "У данного пользователя отсутствует история"
    HISTORY_NOT_FOUND = "Записи о данной истории больше не существует"

    GET_RANDOM_TYPES_NOT_FOUND = "Указанного типа не существует"