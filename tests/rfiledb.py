# -*- coding:utf-8 -*-
import time, datetime

class RobotDB:
    def __init__(self):
        self.fo = open("robotdb.txt", "a+")
        self.idx = []
        self.address = []
        self.secret = []
        lines = self.fo.readlines()
        for l in lines:
            v = l.split(":::")
            self.idx.append(int(v[0]))
            self.address.append(v[1])
            self.secret.append(v[2])

        print self.idx, self.address, self.secret

    def __del__(self):
        self.fo.close()

    def get_one_robot_info(self, robot_id):
        if robot_id in self.idx:
            return (self.address[self.idx.index(robot_id)], self.secret[self.idx.index(robot_id)])
        else:
            return ()

    def set_one_robot_info(self, robot_id, address, secret):
        datas = str(address) + ":::" + str(secret)
        self.fo.write(str(robot_id)+":::" + datas+"\n")

        self.idx.append(robot_id)
        self.address.append(address)
        self.secret.append(secret)

class RobotLogger:
    def __init__(self):
        self.fo = open("robotlogs.log", "a+")
        self.fo2 = open("syslogs.log", "a+")

    def __del__(self):
        self.fo.close()
        self.fo2.close()

    def write(self, data):
        _time = int(time.time())
        _data ="{time};;;;{data}\r\n"
        _data = _data.format(time=str(datetime.datetime.fromtimestamp(_time)), data=data)
        self.fo2.write(_data)

    def robot_write(self, robot_id, action, data):
        _time = int(time.time())
        _data ="{time};;;;{robotid};;;;{action};;;;{data}\r\n"
        _data = _data.format(time=str(datetime.datetime.fromtimestamp(_time)), robotid=robot_id, 
            action=action, data=data)
        self.fo.write(_data)



rdbhelper = RobotDB()
rloghelper = RobotLogger()

# rid = 3
# a = rdbobj.get_one_robot_info(rid)

# if len(a) == 0:
#     rdbobj.set_one_robot_info(rid, "123" + str(rid) + "56\n")
# else:
#     print a




