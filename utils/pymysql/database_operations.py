import datetime
import json
from .connection import connection


def save_specifications(spe):
    cursor = connection.cursor()
    # sign_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    room_id = spe['room_id']
    id_card = spe['id_card']
    request_time = spe['request_time'].strftime("%Y-%m-%d %H:%M:%S")
    serve_time = spe['serve_time']
    serve_start = spe['serve_start'].strftime("%Y-%m-%d %H:%M:%S")
    serve_end = spe['serve_end'].strftime("%Y-%m-%d %H:%M:%S")
    wait_time = spe['wait_time']
    request_period = spe['request_period']
    wind_spd = spe['wind_spd']
    now_air_cost = spe['now_air_cost']
    now_cost_ratio = spe['now_cost_ratio']
    
    query = 'insert into specifs (room_id, id_card, request_time, serve_time, serve_start, serve_end, wait_time, request_period, wind_spd, now_air_cost, now_cost_ratio) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    values = (room_id, id_card, request_time, serve_time, serve_start, serve_end, wait_time, request_period, wind_spd, now_air_cost, now_cost_ratio)
    try:
        cursor.execute(query, values)
        connection.commit()
    except Exception as e:
        print(f"插入失败: {str(e)}")
    finally:
        cursor.close()
        

def get_specifications(room_id, id_card):
    cursor = connection.cursor()
    query = 'select * from specifs where id_card = %s and room_id = %s;'
    cursor.execute(query,(id_card, room_id))
    rows = cursor.fetchall()
    
    if rows:
        specifications = [
            {
            'room_id' : str(row[1]),
            'id_card' : str(row[2]),
            'request_time' : str(row[3]),
            'serve_start' : str(row[5]),
            'serve_end' : str(row[6]),
            'total_serve' : str(row[4]),
            'wind' : row[9] - 1,
            'now_cost' : str(row[10]),
            'cost_ratio' : str(row[11])
            }
            for row in rows
        ]
        
        cursor.close()
        
        return specifications
    
    cursor.close()
    
    return None


def load_guest():
    cursor = connection.cursor()
    query = 'select * from guest'
    cursor.execute(query)
    rows = cursor.fetchall()
    
    if rows:
        roomer_data = [
            {
                'id_card' : row[0],
                'room_id' : row[1],
                'phone_number' : row[2],
                'sign_time' : row[3],
                'power_usage' : row[5],
                'total_cost' : row[6],
                'air_cost' : row[7]
            }
            for row in rows
        ]
        
        cursor.close()
        return roomer_data
    
    return None
    
    
    

# 查询空房
def empty():
    """查询空房

    Args:
        room_id (_int_): _房间号_

    Returns:
        _字典_: _接口文档中data的格式_
    """
    cursor = connection.cursor()

    # 查询语句和参数
    # query = "SELECT room_id FROM room WHERE room_id LIKE %s AND status = %s"
    query = "SELECT room_id FROM room WHERE  status = %s"
    # values = (f'%{room_id}%', 0)  # 这里是模式和状态值
    values = (0)

    cursor.execute(query, values)
    rows = cursor.fetchall()  # 获取查询结果
    cursor.close()
    ava_room = [str(row[0]) for row in rows]
    if ava_room:
        result = 1
        error_detail = ""
    else:
        result = 0
        error_detail = "很抱歉，酒店已住满，暂无房间可用！"

    current_datetime = datetime.datetime.now()
    # 操作时间
    sign_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    # 返回值
    data = {
        "ava_room": ava_room,
        "result": result,
        "error_detail": error_detail,
        "sign_time": sign_time
    }
    return data, len(ava_room)

# print(empty(2))
# 办理入住
def data_check_in(id_card, room_id, phone_number):
    """_将顾客信息存入数据库中_

    Args:
        id_card (_int_): _身份证号_
        room_id (_string_): _房间号_
        phone_number (_string_): _手机号_

    Returns:
        _None_: _description_
    """
    cursor = connection.cursor()
    current_datetime = datetime.datetime.now()
    # 入住时间
    sign_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    query = 'insert into guest (id_card, room_id, phone_number, sign_time) values (%s, %s, %s, %s)'
    values = (id_card, room_id, phone_number, sign_time)
    try:
        cursor.execute(query, values)
        connection.commit()
    except Exception as e:
        print(f"插入失败: {str(e)}")
    finally:
        cursor.close()
    
    cursor = connection.cursor()
    query = 'update room set status = %s where room_id = ' + f'{room_id}'    
    cursor.execute(query, 1)
    connection.commit()
    cursor.close()
    
    return None

# 房客计费等信息更新
def guest_update(room_id, air_cost, power_usages, total_cost):
    cursor = connection.cursor()
    query = 'update guest set air_cost = %s, power_usage = %s, total_cost = %s where room_id = ' + f'{room_id}'
    value = (air_cost, power_usages, total_cost)
    cursor.execute(query, value)
    connection.commit()
    cursor.close
    

# 办理退房
def data_check_out(id_card):
    """办理退房

    Args:
        id_card (_string_): 身份证号，用于找到该顾客

    Returns:
        None
    """
    cursor = connection.cursor()
    current_datetime = datetime.datetime.now()
    # 退房时间
    check_out_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # 查询语句和参数
    bill = {}
    query = "select * from guest where id_card = %s"
    cursor.execute(query, id_card)
    rows = cursor.fetchall()  # 获取查询结果
    
    is_exist = True
    try:
        if rows:
            # 将顾客信息转存到历史顾客表中
            bill['in_time'] = str(rows[0][3])
            bill['out_time'] = str(datetime.datetime.now())
            bill['now_cost'] = str(rows[0][-1])
            query_2 = 'insert into guest_history (id_card, room_id, phone_number, check_in_time,open_id,power_usage,total_cost,air_cost, check_out_time) values (%s,%s, %s, %s, %s,%s, %s, %s,%s);'
            values = rows[0]+(check_out_time,)
            print(values)
            cursor.execute(query_2, values)
            # 将顾客信息从顾客表中删除
            query_3 = 'delete from guest where id_card = %s;'
            cursor.execute(query_3, id_card)
            connection.commit()
            
        else:
            print('未查询到此id: %s', id_card)
            is_exist = False
    except:
        pass
    cursor.close()
    return is_exist, bill


# 查询空调状态
def condition(id):
    """查询空调状态，传给信息面板

    Args:
        id (int): 空调的唯一表示，这里的id和room_id对应

    Returns:
        字典:包含空调的各种信息的键值对
    """
    cursor = connection.cursor()

    # 查询语句和参数
    query = "select * from air_conditioner where id = %s"
    values = (id)

    cursor.execute(query, values)
    rows = cursor.fetchall()  # 获取查询结果
    if rows:
        result = rows[0]
        data = {
            'status': result[1],
            'tem': result[2],
            'wind_spe': result[3],
            'wind_drc': result[4],
            'mode': result[5]
        }
        cursor.close()
        return data
    else:
        print("未查询到结果")
        cursor.close()
        return None


# 修改空调状态
def change_conditioner(id, id_card, **kwargs):
    """修改空调状态，这里使用了动态sql，在调空调温度、风速、检修等功能都可以调用这一个方法

    Args:
        id (int): 空调的唯一标识

    Returns:
        None
    """
    cursor = connection.cursor()
    # 初始化 SQL 查询
    sql_query = "update air_conditioner set "

    # 创建一个列表，用于存储要更新的字段和对应的值
    update_values = []

    # 遍历传递的参数并检查是否存在且不为空，然后将其添加到更新列表中
    if 'status' in kwargs and kwargs['status'] is not None:
        update_values.append(f"status = '{kwargs['status']}'")

    if 'tem' in kwargs and kwargs['tem'] is not None:
        update_values.append(f"tem = {kwargs['tem']}")

    if 'wind_spd' in kwargs and kwargs['wind_spd'] is not None:
        update_values.append(f"wind_spd = {kwargs['wind_spd']}")

    if 'wind_drc' in kwargs and kwargs['wind_drc'] is not None:
        update_values.append(f"wind_drc = '{kwargs['wind_drc']}'")

    if 'mode' in kwargs and kwargs['mode'] is not None:
        update_values.append(f"mode = '{kwargs['mode']}'")

    if 'error_detail' in kwargs and kwargs['error_detail'] is not None:
        update_values.append(f"error_detail = '{kwargs['error_detail']}'")

    # 将要更新的字段和值连接成字符串
    update_str = ', '.join(update_values)
    # 构建 SQL 查询
    if update_str:
        sql_query += f" {update_str} where id = {id};"
        cursor.execute(sql_query)
        connection.commit()
        cursor.close()
        # 记录这一次修改
        record(id, id_card)
    else:
        print("未查询到空调信息")
        cursor.close()
    return None


# 记录每一次修改（在每次修改空调状态后自动执行）
def record(id, id_card):
    """记录每一次修改，用于计算花费

    Args:
        id (int): 空调唯一标识

    Returns:
        None
    """
    cursor = connection.cursor()
    current_datetime = datetime.datetime.now()
    # 入住时间
    change_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    data = json.dumps(condition(id))
    query = "insert into air_conditioner_logs (air_conditioner_id,change_time,info,id_card) values(%s,%s,%s,%s)"
    values = (id, change_time, data, id_card)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    return None


# 查询修改记录
def inquiry(room_id):
    """查询修改记录，用来计算花费

    Args:
        room_id (int): 空调/房间唯一标识

    Returns:
        data 字典: 包含修改后的空调状态和修改时间
    """
    cursor = connection.cursor()
    query = "select change_time,info from air_conditioner_logs where air_conditioner_id = %s"
    cursor.execute(query, room_id)
    rows = cursor.fetchall()  # 获取查询结果
    cursor.close()
    data = []
    for row in rows:
        change_time = row[0]  # 假设第一个元素是时间戳
        info = row[1]  # 假设第二个元素是信息
        info = json.loads(info)
        change_time = change_time.strftime("%Y-%m-%d %H:%M:%S")
        info["change_time"] = change_time
        data.append(info)
    return data


# 写入账单
def save_bill(room_id, run_time, power_usage, power_cost):
    """将账单存入数据库中,用于备案

    Args:
        room_id (_type_): _description_
        run_time (_type_): _description_
        power_usage (_type_): _description_
        power_cost (_type_): _description_

    Returns:
        _type_: _description_
    """
    cursor = connection.cursor()
    current_datetime = datetime.datetime.now()
    create_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")  # 写入时间
    
    query = "select * from bill where room_id = %s"
    cursor.execute(query, room_id)
    rows = cursor.fetchall()  # 获取查询结果
    
    if len(rows) > 0:   # 已存在先前账单
        query = "update bill set  runtime = %s, power_usage = %s, power_cost = %s,create_time = %s where room_id = "+f'{room_id}'
        values = (run_time, power_usage, power_cost, create_time)
        try:
            cursor.execute(query, values)
            connection.commit()
        except Exception as e:
            print(f"插入失败: {str(e)}")
        finally:
            cursor.close()
            
    else:       # 不存在之前的账单
        query = 'insert into bill (room_id, runtime, power_usage,power_cost,create_time) values (%s, %s, %s, %s,%s)'
        values = (room_id, run_time, power_usage, power_cost, create_time)
        try:
            cursor.execute(query, values)
            connection.commit()
        except Exception as e:
            print(f"插入失败: {str(e)}")
        finally:
            cursor.close()
    return None


# 出示账单 --想了想，感觉没必要，因为基本上要出示订单的时候才进行订单计算
""" def get_bill(room_id):
    ""出示详单，在退房时使用

    Args:
        room_id (id): 房间号，房间的唯一标识

    Returns:
        列表 bill: 按顺序 订单id 房间号 运行时间 用电量 花费
    ""
    cursor = connection.cursor()
    # sql语句
    query = "Select * from bill where room_id = %s"
    cursor.execute(query, room_id)
    rows = cursor.fetchall()  # 获取查询结果
    cursor.close()
    if rows:
        bill = list(rows[0])
    else:
        bill = None
    return bill """
