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