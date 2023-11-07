import pymysql
import text as t
import configparser 

config = configparser.ConfigParser() 
config.read("D:/Учёба в GB/Диплом/configs.ini") 

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
        self.cursor.execute("CALL check_exists_user ('{0}');".format(user_id))
        list = self.cursor.fetchall()
        item = list[0]['item']
        return item
    
    def add_user_in_users(self, user_id):
        return self.cursor.execute("CALL AddUser ('{0}');".format(user_id))
    
    def add_user_in_cat(self, user_id):
        return self.cursor.execute("CALL AddUserincat ('{0}');".format(user_id))
    
    def check_passed_the_test(self, user_id):
        self.cursor.execute("CALL check_passed_the_test ('{0}')".format(user_id))
        list = self.cursor.fetchall()
        item = list[0]['indicate']
        return item
    
    def get_value_capabilities(self, user_id):
        '''получаем данные из таблицы  capabilities по user_id'''
        self.cursor.execute("CALL get_value_capabilities ('{0}')".format(user_id))
        list = self.cursor.fetchall() #это команда возвращает список в котором лежит словарь
        return list
    
    def update_indicate_user(self, user_id, indicate):
        # изменяет поле indicate у пользователя
        return self.cursor.execute("CALL update_indicate_user ('{0}', {1})".format(user_id, indicate))
    
    def update_degry_whis_dinamic_reqest(self, user_id, column_name, degry):
        #применение одной процедуры с использованием динамического запроса
        return self.cursor.execute("CALL update_degry ('{0}', '{1}', '{2}')".format(column_name, user_id, degry))
    
    def giv_volue_compare(self,column_names, user_id):
        # процедура принимает имя столбца и id, возвращет значение из таблице capabilities по id пользователя, но возвращает из определённого столбца
        self.cursor.execute("CALL giv_volues_compare ('{0}', '{1}')".format(column_names, user_id))
        list = self.cursor.fetchall() 
        item = list[0][column_names] 
        return item
    
    def update_link_finish_img(self, user_id):
    #записываем ссылку финишной с результатми сравнения картинки в базу 
        return self.cursor.execute("CALL update_link_finish_img ('{0}', '{1}')".format(user_id, t.get_way_of_finish_img(user_id)))
    
    
    
    
    


    def commit(self):
        """Вносим изменение в табл"""
        self.connection.commit()