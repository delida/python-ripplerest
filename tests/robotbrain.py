# -*- coding:utf-8 -*-

from websocket import create_connection
import config
import json
from robot import Robot
import time, datetime
from rfiledb import rloghelper

class WebSocketClient:
    def __init__(self, ws_address):
        self.ws = create_connection(ws_address)
        print self.ws.recv()#, self.ws.__dict__

    def __del__(self):
        print "WebSocketClient __del__", self.close()

    def send(self, data):
        ret = None
        data = json.dumps(data).encode('utf-8')
        try:
            self.ws.send(data)
            ret = self.ws.recv()
        except Exception, e:
            print "websocket send error", e
        return ret

    def subscribe_message_by_account(self, address, secret):
        _data = {
            "command": "subscribe",
            "account": address,
            "secret": secret 
        }
        return self.send(_data)

    def close(self):
        _data = {
            "command": "close",
        }
        return self.send(_data) 


class RobotBrain(object): # only one
    def __init__(self, start_robot_id, end_robot_id):
        self.websocket_client_helper = WebSocketClient(config.web_socket_address)
        self.robot_objs = {}
        self.last_heart_beat = 0
        self.tmp_heart_cnt = 0

        self.init_robot(start_robot_id, end_robot_id)

    def __del__(self):
        print "robotbrain close"
        print "RobotBrain __del__", self.websocket_close()

    def init_robot(self, start_robot_id, end_robot_id):
        for i in range(start_robot_id, end_robot_id + 1):
            self.robot_objs[i] = Robot(i)
            self.subscribe_message_by_account(self.robot_objs[i].address, 
                self.robot_objs[i].secret)
            rloghelper.robot_write(i, "subscribe_message_by_account", self.robot_objs[i].address) 

        # self.robot_objs[start_robot_id] = Robot(start_robot_id)
        # #self.robot_objs[start_robot_id].get_balances(self.robot_objs[start_robot_id].address)
        # self.robot_objs[end_robot_id] = Robot(end_robot_id)
        # print self.subscribe_message_by_account(self.robot_objs[start_robot_id].address, 
        #     self.robot_objs[start_robot_id].secret)
        # print self.subscribe_message_by_account(self.robot_objs[end_robot_id].address, 
        #     self.robot_objs[end_robot_id].secret) 


    def receive_socket_data(self, data):
        if data.has_key("type"):
            if data["type"] in config.api_receive_keywords:
                _func = getattr(self, 'do_%s' % data["type"].replace(" ", "_").lower(), None)
                if _func:
                    _func(data)
                else:
                    rloghelper.write("robotbrain receive_socket_data error, unprocess func::"+data["type"])
                    print "robotbrain receive_socket_data error, unprocess func::", data["type"]
            else:
                rloghelper.write("robotbrain receive_socket_data error, unknown type::"+data["type"])
                print "robotbrain receive_socket_data error, unknown type::", data
        else:
            rloghelper.write("robotbrain receive_socket_data error, can not format")
            print "robotbrain receive_socket_data error, can not format::", data

    def subscribe_message_by_account(self, address, secret):
        try:
            return self.websocket_client_helper.subscribe_message_by_account(address, secret)
        except Exception, e:
            print "robotbrain subscribe_message_by_account error", e

    def websocket_close(self):
        try:
            return self.websocket_client_helper.close()
        except Exception, e:
            print "robotbrain websocket_close error", e

    def do_connection(self, data):
        #print "in do_connection", data
        rloghelper.write(str(data))

    def do_ledger(self, data):
        _time = int(time.time())
        if _time - self.last_heart_beat > config.min_heart_interval:
            if _time - self.last_heart_beat > config.max_process_interval:
                self.tmp_heart_cnt = 0
                self.last_heart_beat = _time
                print "in do_ledger", str(datetime.datetime.fromtimestamp(_time))
                self.do_policy()
            else:
                print "in do_ledger, wait ...", _time - self.last_heart_beat
        else:
            self.tmp_heart_cnt += 1
            #print "in do_ledger:: too many heart beat", str(datetime.datetime.fromtimestamp(_time)), self.tmp_heart_cnt

    def do_policy(self):
        for rid, robot in self.robot_objs.items():
            print "Begin:::Robot"+str(rid)
            for policy in config.robot_policy_lists:
                if policy[0] == "balance":
                    #if len(robot.money) == 0: 
                        robot.get_balances(robot.address)
                        print  "robot"+ str(rid), robot.money
                        rloghelper.robot_write(rid, policy[0], robot.money)

                elif policy[0] == "order":
                    print str(datetime.datetime.fromtimestamp(int(time.time()))), "robot"+ str(rid), "order", robot.money
                    _expr = """
if robot.money.has_key("{p1}"):
    if int(float(robot.money["{p1}"])) {p2} {p3}:
        robot.place_order(robot.address, robot.secret, "buy", *config.policy_result_lists[{p4}])
                    """
                    _expr = _expr.format(p1=config.policy_condition_lists[policy[1]][0],\
                        p2=config.policy_condition_lists[policy[1]][1],\
                        p3=config.policy_condition_lists[policy[1]][2],\
                        p4=policy[2])
                    #print "robot"+ str(rid), _expr
                    exec(_expr)
                    # if robot.money.has_key("SWT"):
                    #     if int(float(robot.money["SWT"])) > 50:
                    #         robot.place_order(robot.address, robot.secret, "buy", *config.policy_result_lists[1])
                    # else:
                    #     print "robot"+ str(rid), robot.money

                elif policy[0] == "payment":
                    _expr = """
if not robot.money.has_key("{p1}") or int(float(robot.money["{p1}"])) {p2} {p5}:
        robot.active_account("{p3}", {p4}, config.issuer_account, robot.address, config.issuer_secret)
                    """
                    _expr = _expr.format(p1=config.policy_condition_lists[policy[1]][0],\
                        p2=config.policy_condition_lists[policy[1]][1],\
                        p3=config.policy_result_lists[policy[2]][0],\
                        p4=config.policy_result_lists[policy[2]][1],\
                        p5=config.policy_condition_lists[policy[1]][2])
                    #print "robot"+ str(rid), _expr
                    exec(_expr)


    def do_transaction_main_account(self, data):
        print "do_transaction_main_account", data

    def do_transaction_affected_account(self, data):
        print "do_transaction_affected_account", data

robotbrain = RobotBrain(2, 4)