import pymysql
import text as t
import configparser 

config = configparser.ConfigParser() 
config.read("your path to/configs.ini") 

class Sqloghter:
    def __init__(self):
        self.connection = pymysql.connect(
            user=config["MySql"]["userr"],
            host=config["MySql"]["hostt"],
            port=3306,
            password=config["MySql"]["passwordd"],
            database=config["MySql"]["db_namee"],
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.connection.cursor()
    
    def check_exists_user(self, user_id):
        """проверяет наличие пользователя в БД

        Args:
            user_id (_type_): ID пользователя

        Returns:
            _type_: вернёт 1 если существует и 0 если нет
        """
        self.cursor.execute("CALL check_exists_user ('{0}');".format(user_id))
        list = self.cursor.fetchall()
        item = list[0]['item']
        return item
    
    def add_user_in_users(self, user_id):
        """Добавляет пользователя в БД, но только в том случае, если его там ещё нет

        Args:
            user_id (_type_): ID пользователя

        Returns:
            _type_: _description_
        """
        return self.cursor.execute("CALL AddUser ('{0}');".format(user_id))
    
    def add_user_in_cat(self, user_id):
        """Добавляет пользователя в таблицу capabilities, но только если пользователь есть в таблице users

        Args:
            user_id (_type_): ID пользователя

        Returns:
            _type_: _description_
        """
        return self.cursor.execute("CALL AddUserincat ('{0}');".format(user_id))
    
    def check_passed_the_test(self, user_id):
        """Вернёт индикатор тестирования

        Args:
            user_id (_type_): ID пользователя

        Returns:
            _type_: _description_
        """
        self.cursor.execute("CALL check_passed_the_test ('{0}')".format(user_id))
        list = self.cursor.fetchall()
        item = list[0]['indicate']
        return item
    
    def get_value_capabilities(self, user_id):
        """ возвращет строку из таблицы capabilities по id пользователя

        Args:
            user_id (_type_): ID пользователя

        Returns:
            _type_: возвращает список в котором лежит словарь
        """
        self.cursor.execute("CALL get_value_capabilities ('{0}')".format(user_id))
        list = self.cursor.fetchall()
        return list
    
    def update_indicate_user(self, user_id, indicate):
        """изменяет поле indicate у пользователя

        Args:
            user_id (_type_): ID пользователя
            indicate (_type_): Индикатор

        Returns:
            _type_: _description_
        """
        return self.cursor.execute("CALL update_indicate_user ('{0}', {1})".format(user_id, indicate))
    
    def update_degry_whis_dinamic_reqest(self, user_id, column_name, degry):
        """Обновляет ответы пользователя при прохождении теста

        Args:
            user_id (_type_): ID пользователя
            column_name (_type_): Название столбца в БД
            degry (_type_): Значение

        Returns:
            _type_: _description_
        """
        return self.cursor.execute("CALL update_degry ('{0}', '{1}', '{2}')".format(column_name, user_id, degry))
    
    def giv_volue_compare(self,column_names, user_id):
        """Получает значение из конкретного поля для определённого пользователя 

        Args:
            column_names (_type_): Название столбца
            user_id (_type_): ID пользователя 

        Returns:
            _type_: _description_
        """
        self.cursor.execute("CALL giv_volues_compare ('{0}', '{1}')".format(column_names, user_id))
        list = self.cursor.fetchall() 
        item = list[0][column_names] 
        return item
    
    def update_link_finish_img(self, user_id):
        """Обновляет в БД ссылку по которой лежит итоговый результат тестирования

        Args:
            user_id (_type_): ID пользователя 

        Returns:
            _type_: _description_
        """ 
        return self.cursor.execute("CALL update_link_finish_img ('{0}', '{1}')".format(user_id, t.get_way_of_finish_img(user_id)))
    
    def update_time_content_test(self, user_id):
        """Обновляет время прохождения теста

        Args:
            user_id (_type_): ID пользователя 

        Returns:
            _type_: _description_
        """
        return self.cursor.execute("CALL update_time_content_test ('{0}')".format(user_id))
    
    def update_link_data_test(self, user_id):
        """Обновляет в БД ссылку, по которой лежит портрет пользователя

        Args:
            user_id (_type_): ID пользователя 

        Returns:
            _type_: _description_
        """
        return self.cursor.execute("CALL update_link_data_test ('{0}', '{1}')".format(user_id, t.get_way_of_img(user_id)))
    
    def update_link_copmare(self, user_id, name_specific):
        """Обновляет в БД ссылку, по которой лежит один из портретов сравнения со специалистами

        Args:
            user_id (_type_): ID пользователя 
            name_specific (_type_): специализация

        Returns:
            _type_: _description_
        """
        procedure_name = 'update_link_data_compare_' + name_specific
        return self.cursor.execute("CALL {0} ('{1}', '{2}');".format(procedure_name, user_id, t.get_way_of_img_compare(user_id, name_specific)))
    


    


    def commit(self):
        """Вносим изменение в табл"""
        self.connection.commit()