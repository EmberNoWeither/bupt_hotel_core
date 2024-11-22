import datetime


class BaseTimer(object):
    def __init__(self) -> None:
        self.__records = {
            'first_record' : datetime.datetime.now()
        }
    def __call__(self, *args, **kwds):
        return datetime.datetime.now()
    
        
    def record_now(self, now_key : str):
        self.__records[now_key] = datetime.datetime.now()
        
    def calculate_delta(self, key1, key2):
        return (self.__records[key2] - self.__records[key1])