import pymysql
import configparser


def connect_to_database(host, user, password, database):
    try:
        connection = pymysql.connect(
            host=host, user=user, password=password, db=database)
        return connection
    except Exception as e:
        print(f"连接数据库失败: {str(e)}")
        return None


# 创建配置文件解析器
config = configparser.ConfigParser()
config.read('config.ini')  # 你的配置文件的路径
print(config)

# # 从配置文件中获取数据库连接参数
# database_section = config['database']
# host = database_section['host']
# user = database_section['user']
# password = database_section['password']
# database = database_section['database']
host = 'localhost'
user = 'root'
password = 'xiaguoyang123'
database = 'bupt_hotel'
connection = connect_to_database(host, user, password, database)
