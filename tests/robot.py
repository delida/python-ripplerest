# -*- coding:utf-8 -*-
import sys 
sys.path.append("../")

from ripplerest.client import Client 

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

class Robot(object):
    def __init__(self, robot_id):
        self.clienthelper = Client(config.server_host + ":" + str(config.sercer_port), config.is_https) 

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
            _secret = _robot_info[1]

        self.address = _address
        self.secret = _secret
        self.money = {} #type: value


    def get_master_balances(self):
        return self.get_balances(config.issuer_account)

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

    def active_account(self, currency_type, currency_value, issuer_account, wallet_address, issuer_secret):
        _active_dict = {}
        try:
            _active_dict = self.clienthelper.active_account(currency_type, currency_value, issuer_account, 
                wallet_address, issuer_secret)
        except Exception, e:
            print "active_account error", e

        return _active_dict

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
            print "3333333", secret, _trustline
            return self.clienthelper.post_trustline(address, secret, _trustline)
        except Exception, e:
            print "grant_trustline error", e 
        
    def _get_one_robot(self, robot_id):
        return rdbhelper.get_one_robot_info(robot_id)

    def _set_one_robot(self, robot_id, address, secret):
        rdbhelper.set_one_robot_info(robot_id, address, secret)

####temp test

robot_obj = Robot(2)

if robot_obj.address is not None:
    print robot_obj.money
    print robot_obj.grant_trustline(robot_obj.address, robot_obj.secret, 5, "USD")
    print robot_obj.get_balances(robot_obj.address)