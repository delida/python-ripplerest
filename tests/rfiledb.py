# -*- coding:utf-8 -*-

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

    def get_one_robot_info(self, robot_id):
        if robot_id in self.idx:
            return (self.address[self.idx.index(robot_id)], self.secret[self.idx.index(robot_id)])
        else:
            return ()

    def set_one_robot_info(self, robot_id, address, secret):
        datas = str(address) + ":::" + str(secret)
        self.fo.write(str(robot_id)+":::" + datas)

        self.idx.append(robot_id)
        self.address.append(address)
        self.secret.append(secret)


rdbhelper = RobotDB()

# rid = 3
# a = rdbobj.get_one_robot_info(rid)

# if len(a) == 0:
#     rdbobj.set_one_robot_info(rid, "123" + str(rid) + "56\n")
# else:
#     print a




