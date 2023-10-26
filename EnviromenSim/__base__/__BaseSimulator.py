

class BaseSimulator(object):
    def __init__(self) -> None:
        self.__property = {}
        self.change_mode = True
    
    def __call__(self, *args: any, **kwds: any) -> any:
        
        if 'attr' not in list(kwds.keys()):
            try:
                kwds['show'] = True
                print(self.__property)
            except:
                pass
            return self.__property
        else:
            if kwds['attr'] not in list(self.__property.keys()):
                raise 'Didn\'t have this type of __property!, Call Error!'
            else:
                K = kwds['attr']
                return self.__property[K]
        
        
    def change(self):
        self.change_mode = True
        
    
    def fixed(self):
        self.change_mode = False
        
    
    def add_property(self, attr='', initial_value=None):
        if self.type_erro_detect(attr, initial_value):
            return "having basic error!"
        
        self.__property[attr] = initial_value
        return 1
    
    
    def delete_property(self, attr=''):
        if self.type_erro_detect(attr, 1):
            return "having basic error!"
        
        del self.__property[attr]
        
        return 1
    
    def type_erro_detect(self, attr='', value=None):
        if not isinstance(attr, str):
            raise "Key Value Should be string!"
        
        if value==None or self.change_mode!=True:
            print('Nothing Change! You may have none value or change_mode is False')
            return True
        
        if attr not in list(self.__property.keys()):
            print('Didn\'t have this type of __property!')
            return True
        
    
    def set_property(self, attr='', value:any=None):
        if self.type_erro_detect(attr, value):
            return "having basic error!"
        
        if isinstance(self.__property[attr], dict) or isinstance(self.__property[attr], list):
            raise "This type __property should have a operator for changing its value"
        
        self.__property[attr] = value
        
        return 1
        
        
    def set_property(self, attr='', value:any=None, operator:function=None, *args, **kwds):
        if self.type_erro_detect(attr, value):
                    return "having basic error!"
                
        if not isinstance(operator, function):
            raise "operator is not a function"
        
        result = operator(self.__property, attr, value, *args, **kwds)
        if len(result) != 1:
            raise "operator should just have one return value"
        
        self.__property[attr] = result
        return 1
        
    
    