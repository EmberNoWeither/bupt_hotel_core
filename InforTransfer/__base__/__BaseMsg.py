
class BaseMsg(object):
    def __init__(self, msg:dict=None) -> None:
        self.__msg = msg
    
    def _get_msg(self):
        return self.__msg
    
    def _change_msg(self, msg):
        return self.__msg