from .__BaseMsg import BaseMsg as Msg

class BaseTransfer(object):
    def __init__(self) -> None:
        self.__msg_pipe = []
        self.__froms = []
        self.__keys = []
        
    
    def __call__(self, From:str, key:str):
        return self.take_msg(From, key)
        
        
    def transfer_msg(self, msg:Msg, From:str, key:str):
        self.__msg_pipe.append(msg)
        self.__froms.append(From)
        self.__keys.append(key)
        
        
    def take_msg(self, From:str, key:str):
        msg = None
        id = None
        for idx, writer in enumerate(self.__froms):
            if writer == From:
                if key == self.__keys[idx]:
                    msg = self.__msg_pipe[idx]
                    id = idx
        
        self.__keys.pop(id)
        self.__froms.pop(id)
        self.__msg_pipe.pop(id)
        
        return msg
    
    
condition_transfer = BaseTransfer()