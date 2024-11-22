from utils.BaseValue import AC_STATUS, AC_CTROL, PA, AC_MODE, WIND_SPEED, is_simu
import time
import datetime
from EnviromenSim.__HotelSimulator import HotelSimulator as Hotel
import requests
from flask_cors import CORS
defaultencoding = 'utf-8'
from flask import Flask,render_template,request,json
import threading
from Runner.__base__.BaseRunner import Runner
import pandas as pd
import xlsxwriter


app = Flask(__name__)
cors = CORS(app, supports_credentials=True)

runner = Runner()
# print(type(AC_STATUS.Running))
# runner.Hotel_SimulatingCircule()
# print(type(datetime.datetime.now()))

def start_Simu():
    working_thread = threading.Thread(target=runner.Hotel_SimulatingCircule)
    working_thread.start()

# hotel = Hotel()

runner.hotel.Check_In(1,5443,546165564)
runner.hotel.Check_In(2,112,54616543564)
runner.hotel.Check_In(3,111,54616245564)
runner.hotel.Check_In(4,115,54616125564)
runner.hotel.Check_In(5,153,546161235564)

runner.hotel.Check_Out(1,5443,546165564)
runner.hotel.Check_Out(2,112,54616543564)
runner.hotel.Check_Out(3,111,54616245564)
runner.hotel.Check_Out(4,115,54616125564)
runner.hotel.Check_Out(5,153,546161235564)
@app.route('/', methods = ['POST'])
def main():
    return json.dumps({'status':'OK'})


@app.route('/open_control', methods = ['GET'])
def open_control():
    runner.hotel.is_simu = True
    
    return json.dumps({'status':'OK'})
    

@app.route('/check_in', methods = ['POST'])
def check_in():
    content = request.get_json()

    room_id = content["room_id"]
    room_id = int(room_id)
    user_name = content["user_name"]
    id_card = content["id_card"]
    
    checkIn = threading.Thread(target=runner.Hotel_CheckIn, args=(room_id, user_name, id_card))
    checkIn.start()
    return json.dumps({'status':'OK'})


@app.route('/control_ac', methods = ['POST'])
def control_ac():
    content = request.get_json()
    print(content)
    
    room_id = content["room_id"]
    room_id = int(room_id)
    is_on = content["is_on"]
    mode = content["mode"]
    tar_temp = content["tar_temp"]
    wind = content["wind"]
    
    control = threading.Thread(target=runner.Air_Controll, args=(room_id, is_on, mode, tar_temp, wind))
    control.start()

    return json.dumps({'status':'OK'})


@app.route('/make_bill', methods = ['POST'])
def make_bill():
    content = request.get_json()
    print(content)
    room_id = content["room_id"]
    room_id = int(room_id)
    user_name = content["user_name"]
    id_card = content["id_card"]
    
    bill = runner.Hotel_CheckOut(room_id, user_name, id_card)
    print(bill)
    excel_bill = {'room_id':room_id,
                    'user_name':user_name}
    excel_bill.update(bill)
    df = pd.DataFrame(
        bill, index=[0]
    )
    with pd.ExcelWriter(
        str(room_id)+'_'+user_name+'_bill.xlsx'
    ) as writer:
        df.to_excel(writer, sheet_name='bill')
        worksheet = writer.sheets['bill']
        worksheet.set_column('A:J', 20)
    
    return json.dumps(bill)


@app.route('/set_ratio', methods = ['POST'])
def set_cost_ratio():
    content = request.get_json()
    cost_rate = content['cost_rate']
    
    runner.Hotel_SetCostRule(cost_rate)
    return json.dumps({'status':'OK'})


@app.route('/update_status', methods = ['POST'])
def update_status():
    content = request.get_json()

    room_id = content["room_id"]
    room_id = int(room_id)
    status_info = runner.Hotel_RoomStatusGet(room_id)

    return json.dumps(status_info)


@app.route('/make_specifi', methods = ['POST'])
def get_specifications():
    
    content = request.get_json()
    print(content)
    
    room_id = content["room_id"]
    room_id = int(room_id)
    user_name = content["user_name"]
    id_card = content["id_card"]
    
    specifications = runner.Hotel_SpecificationMake(room_id, user_name, id_card)
    
    room_ids = []
    id_cards = []
    request_times = []
    serve_starts = []
    serve_ends = []
    total_serves = []
    winds = []
    now_costs = []
    cost_ratios = []
    
    for spec in specifications:
        room_ids.append(spec['room_id'])
        id_cards.append(spec['id_card'])
        request_times.append(spec['request_time'])
        serve_starts.append(spec['serve_start'])
        serve_ends.append(spec['serve_end'])
        total_serves.append(spec['total_serve'])
        wind = 'middle'
        if spec['wind']-1 == 1:
            wind = 'slow'
        elif spec['wind']-1 == 2:
            wind = 'middle'
        elif spec['wind']-1 == 3:
            wind = 'high'
        winds.append(wind)
        now_costs.append(spec['now_cost'])
        cost_ratios.append(spec['cost_ratio'])
        
    df = pd.DataFrame(
        {
            '房间号':room_ids,
            '身份证号':id_cards,
            '请求时间':request_times,
            '服务开始时间':serve_starts,
            '服务结束时间':serve_ends,
            '服务时长':total_serves,
            '风速':winds,
            '当前费用':now_costs,
            '当前费率':cost_ratios
        }
    )
    
    with pd.ExcelWriter(
        str(room_id)+'_'+user_name+'_spec.xlsx'
    ) as writer:
        df.to_excel(writer, sheet_name='spec')
        worksheet = writer.sheets['spec']
        worksheet.set_column('A:J', 20)

    return json.dumps(
        {'specs_list':specifications}
    )
    
    
    
if __name__ == '__main__':
    start_Simu()
    app.run(host='0.0.0.0',debug=False,threaded=True)

