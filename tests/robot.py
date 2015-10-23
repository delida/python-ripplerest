# -*- coding:utf-8 -*-
import sys 
sys.path.append("../")

from ripplerest.client import Client 
import thread
import time
import config

# client = Client(config.server_host + ":" + str(config.sercer_port), config.is_https)

# #print client.get_server_info()

# #b = client.get_balances(config.issuer_account)

# #print b.next()
# #print b.next()
# #print b.next()

# #while 1:
# #    try:
# #        print b.next()
# #    except StopIteration:
# #        break

# wallet_dict = client.generate_wallet()   
# print wallet_dict
# res = client.active_account(config.currency_type, config.currency_value, config.issuer_account, 
#     wallet_dict["wallet"]["address"], config.issuer_secret)

# print "res", res

# b = client.get_balances(wallet_dict["wallet"]["address"])
# print b.next()

# print "end" 

from rfiledb import rdbhelper
from rfiledb import rloghelper

def exeTime(func):  
    def _func(*args, **args2):  
        t0 = time.time()  
        #print "@%s, {%s} start" % (time.strftime("%X", time.localtime()), func.__name__)  
        back = func(*args, **args2)  
        #print "@%s, {%s} end" % (time.strftime("%X", time.localtime()), func.__name__)  
        print "@%.3fs taken for {%s}" % (time.time() - t0, func.__name__) 
        rloghelper.write("@%.3fs taken for {%s}" % (time.time() - t0, func.__name__) ) 
        return back  
    return _func  

class Robot(object):
    def __init__(self, robot_id):
        self.clienthelper = Client(config.server_host + ":" + str(config.sercer_port), config.is_https) 
        self.robot_id = robot_id
        
        _address, _secret = None, None

        _robot_info = self._get_one_robot(robot_id) 
        if len(_robot_info) == 0:
            _address, _secret = self.generate_wallet()

            if _address is not None:
                _res = self.active_account(config.currency_type, config.currency_value, config.issuer_account, 
                    _address, config.issuer_secret)
                if _res.has_key("success") and _res["success"]:
                    self._set_one_robot(robot_id, _address, _secret)
        else:
            _address = _robot_info[0]
            _secret = _robot_info[1][:-1]

        self.address = _address
        self.secret = _secret
        self.money = {} #type: value

    def get_master_balances(self):
        return self.get_balances(config.issuer_account)

    @exeTime
    def generate_wallet(self):
        try:
            _wallet_dict = self.clienthelper.generate_wallet() 
        except Exception, e:
            print "generate_wallet error", e

        if _wallet_dict.has_key("wallet"):
            _dict = _wallet_dict["wallet"]
            if _dict.has_key("address") and _dict.has_key("secret"):
                return _dict["address"], _dict["secret"]
            else:
                return None, None

    @exeTime
    def active_account(self, currency_type, currency_value, issuer_account, wallet_address, issuer_secret, issuer=None):
        #print self.robot_id, "active_account", currency_type, currency_value, issuer_account, wallet_address, issuer_secret
        rloghelper.robot_write(self.robot_id, "active_account", (currency_type, currency_value, issuer_account, wallet_address))
        #return
        _active_dict = {}
        try:
            _active_dict = self.clienthelper.active_account(currency_type, currency_value, issuer_account, 
                wallet_address, issuer_secret, issuer)
        except Exception, e:
            print "active_account error", e

        return _active_dict

    @exeTime
    def get_balances(self, address):
        _ret = []
        try:
            _g = self.clienthelper.get_balances(address)
        except Exception, e:
            print "get_balances error", e 

        while 1:
            try:
                _res = _g.next()
                if _res.has_key("currency") and _res.has_key("value"):
                    self.money[_res["currency"]] = _res["value"]
                _ret.append(_res)
            except StopIteration:
                break

        return _ret

    def grant_trustline(self, address, secret, limit, currency_type, counterparty=""):
        _trustline = {"limit": str(limit), "currency": currency_type, "counterparty": counterparty}
        try:
            return self.clienthelper.post_trustline(address, secret, _trustline)
        except Exception, e:
            print "grant_trustline error", e 

    @exeTime
    def place_order(self, address, secret, order_type, get_type, get_value, pay_type, pay_value, 
        get_counterparty=None, pay_counterparty=None):
        print self.robot_id, "place_order tmp return", address, secret, order_type, get_type, get_value, pay_type, pay_value
        rloghelper.robot_write(self.robot_id, "place_order", (address, secret, order_type, get_type, get_value, pay_type, pay_value))
        _ret_dict = {}
        try:
            _ret_dict = self.clienthelper.place_order(address, secret, order_type, pay_type, pay_value, 
                get_type, get_value, pay_counterparty, get_counterparty)
        except Exception, e:
            print "place_order error", e  
        return _ret_dict

    @exeTime
    def get_account_orders(self, address):
        _ret_dict = {}
        try:
           _ret_dict = self.clienthelper.get_account_orders(address)
        except Exception, e:
            print "get_account_orders error", e  
        return _ret_dict

    @exeTime
    def cancel_order(self, address, secret, order_sequence):
        _ret_dict = {}
        try:
           _ret_dict = self.clienthelper.cancel_order(address, secret, order_sequence)
        except Exception, e:
            print "cancel_order error", e  
        return _ret_dict

    def get_order_book(self, address, base, counter):
        _ret_dict = {}
        try:
           _ret_dict = self.clienthelper.get_order_book(address, base, counter)
        except Exception, e:
            print "get_order_book error", e  
        return _ret_dict

    def retrieve_order_transaction(self, address, hash_id):
        _ret_dict = {}
        try:
           _ret_dict = self.clienthelper.retrieve_order_transaction(address, hash_id)
        except Exception, e:
            print "retrieve_order_transaction error", e  
        return _ret_dict

    def order_transaction_history(self, address):
        _ret_dict = {}
        try:
           _ret_dict = self.clienthelper.order_transaction_history(address)
        except Exception, e:
            print "order_transaction_history error", e  
        return _ret_dict
        
    def _get_one_robot(self, robot_id):
        return rdbhelper.get_one_robot_info(robot_id)

    def _set_one_robot(self, robot_id, address, secret):
        rdbhelper.set_one_robot_info(robot_id, address, secret)

####temp test

is_robot2 = False

robot_obj = Robot(2)

if robot_obj.address is not None and is_robot2:
    print "robot2 start------------------"
    print robot_obj.get_balances(robot_obj.address)
    #print robot_obj.money
    #print robot_obj.grant_trustline(robot_obj.address, robot_obj.secret, 5, "USD", "jJ8PzpT7er3tXEWaUsVTPy3kQUaHVHdxvp")
    #robot_obj.active_account("USD", "10", config.ulimit_account, robot_obj.address, config.ulimit_secret, config.issuer)
    #print robot_obj.place_order(robot_obj.address, robot_obj.secret, "buy", "SWT", 10, "USD", 1, None, config.issuer)
    print robot_obj.get_account_orders(robot_obj.address)
    #print robot_obj.cancel_order(robot_obj.address, robot_obj.secret, 2)
    #print robot_obj.get_account_orders(robot_obj.address)
    #print robot_obj.get_order_book(robot_obj.address, "USD", "SWT") 

    #print robot_obj.get_balances(robot_obj.address)

#robot_obj.get_balances(config.ulimit_account)


# robot_obj3 = Robot(3)
# if robot_obj3.address is not None and False:
#     print "robot3 start------------------"
#     #robot_obj3.active_account("USD", "1", config.ulimit_account, robot_obj3.address, config.ulimit_secret, config.issuer)
#     print robot_obj3.get_balances(robot_obj3.address)
#     #print robot_obj3.money
#     #print robot_obj3.grant_trustline(robot_obj3.address, robot_obj3.secret, 1, "USD", config.issuer)
#     #print robot_obj3.place_order(robot_obj3.address, robot_obj3.secret, "sell", "SWT", 10, "USD", 1, None, config.issuer)
#     robot_obj3.get_account_orders(robot_obj3.address)
#     print robot_obj3.retrieve_order_transaction(robot_obj3.address, 
#         "2382E8A0B5826C691A994E4EAFB8D43AD86C44922B18B6FD22CECED391CD6D61")

robot_obj4 = Robot(4)
if robot_obj4.address is not None and  is_robot2:
    print "robot4 start------------------"
    #robot_obj4.active_account("USD", "1", config.ulimit_account, robot_obj4.address, config.ulimit_secret, config.issuer)
    print robot_obj4.get_balances(robot_obj4.address)
    #print robot_obj4.money
    #print robot_obj4.place_order(robot_obj4.address, robot_obj4.secret, "sell", "USD", 1, "SWT", 10, config.issuer, None)
    #print robot_obj4.place_order(robot_obj4.address, robot_obj4.secret, "buy", "USD", 1, "SWT", 10, config.issuer, None)
    robot_obj4.get_account_orders(robot_obj4.address)
    # print robot_obj4.retrieve_order_transaction(robot_obj4.address, 
    #     "2382E8A0B5826C691A994E4EAFB8D43AD86C44922B18B6FD22CECED391CD6D61")
    #robot_obj4.order_transaction_history(robot_obj4.address)
    