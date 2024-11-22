from __base__.__BaseMsg import BaseMsg as Msg
from ..utils.BaseValue import AC_CTROL

class SpeciMsg(Msg):
    def __init__(self, msg: dict = None) -> None:
        self.__msg = msg
        
        try:
            self.__type = msg['type']
            if not isinstance(self.__type, AC_CTROL):
                raise "Type Format Error! Should be AC_CTROL!"
            self.__value = msg['value']
            self.__auth = msg['authority']
        except:
            raise "SpeciMsg's original msg format error!"
        
    def _get_authority(self):
        return self.__auth
        
    def _get_type(self):
        return self.__type
    
    def _get_value(self):
        return self.__value