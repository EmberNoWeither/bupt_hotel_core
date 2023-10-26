import enum


AC_STATUS = enum.Enum('AC_STATUS', ('Running', 'Stop', 'Error'))    # Air-Conditioning Status

ROOM_STATUS = enum.Enum('ROOM_STATUS', ('ava', 'using'))

PA = enum.Enum('People_Authority', ('roomer', 'administ', 'superAdminist'))

AC_MODE = enum.Enum('AC_MODE', ('Cold','Hot','Wind','Dry'))

AC_Control = enum.Enum('AC_Control', ('Open', 'Close', 'SetTemp', 'SetWindSpd', 'SetWindDirect',
                                      'ReportError', 'SetMode', 'ShowBill', 
                                      'EmergencyStop', 'FixError', 'ShowSpecifications', 'SetSweepMode'))

WIND_SPEED = enum.Enum('WIND_SPEED',('auto', 'slow', 'middle', 'high', 'super'))

WIND_DRC = enum.Enum('WIND_DRC', ('left', 'middle', 'right'))

SWEEP_MODE = enum.Enum('SWEEP_MODE', ('sweeping', 'stay'))
