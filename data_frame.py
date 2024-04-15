from sqlyghter import Sqloghter
import text as t

db = Sqloghter()


# метод получения словаря с 15 ключами и значениями к ним из таблицы capabilities
def get_data_frame(user_id):
    """Метод обрабатывает полученные данные из БД и вовращает словарь из 15 пар ключ-значение

    Args:
        user_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    data = db.get_value_capabilities(user_id)[0]
    data.pop('id')
    data.pop('user_id')
    data.pop('sum_general_bals')
    data.pop('sum_bals_compare_with_developer')
    data.pop('sum_bals_compare_with_tester')
    data.pop('sum_bals_compare_with_analist')
    data.pop('sum_bals_compare_with_prodact')
    data.pop('sum_bals_compare_with_project')

    return data

# метод получения суммы очков, которая считается из результатов прохождения теста
def get_sum_data(data):
    """метод получения суммы очков, которая считается из результатов прохождения теста

    Args:
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    res = 0
    for i in t.get_list_whis_title_on_english():
        res = res + data[i]
    return res

# метод получения списка с результатами теста
def get_data_frame_only_value(data):
    """метод получения списка с результатами теста

    Args:
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    list = []
    for i in t.get_list_whis_title_on_english():
        list.append(data[i])
    return list

