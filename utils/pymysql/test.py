from connection import connection
import datetime
from database_operations import empty, check_in, check_out, condition, change_conditioner, record, inquiry, save_bill
# data = empty('10')
# print(data)
# bill = get_bill(84)
# print(bill)
# check_in(1, 1, 1)
# check_out(1)
# data = condition(1)
# print(data)
# change_conditioner(1, status=1, tem=20)
# record(1)
# data = inquiry(1)
# print(data)


# 都手动测试过了，暂时先不写这么规范了
# 测试存储写入订单功能
def test_save_bill():
    room_id = 84
    run_time = 123
    power_usage = 23
    power_cost = 68
    save_bill(room_id, run_time, power_usage, power_cost)
    return None

