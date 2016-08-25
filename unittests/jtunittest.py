# -*- coding:utf-8 -*-
import sys 
sys.path.append("../")

import unittest
import time, datetime

from ripplerest.client import Client 
import config
import websocket
from websocket import create_connection
import json
import threading

def exeTime(func):  
    def _func(*args, **args2):  
        t0 = time.time()  
        back = func(*args, **args2)  
        print "@%.3fs taken for {%s}" % (time.time() - t0, func.__name__) 
        return back  
    return _func 

class WebSocketClient:
    def __init__(self, ws_address):
        self._shutdown = True
        self.ws = create_connection(ws_address)
        print self.ws.recv()#, self.ws.__dict__

    # def __del__(self):
    #     print "WebSocketClient __del__", self.close()

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
        print "close..."
        _data = {
            "command": "close",
        }
        self._shutdown = False
        return self.send(_data) 

    def receive(self):
        try:    
            msg = json.loads(self.ws.recv().decode('utf-8'))
            print 'websocket<<<<<<<< receiving % s', json.dumps(msg, indent=2)
        except Exception, e:
            print e
        
class JingtumTestCase(unittest.TestCase):
    def setUp(self):
        self.clienthelper = Client(config.server_host + ":" + str(config.sercer_port), config.is_https)  

    def tearDown(self):
        pass

    def _priGetInfoFromDB(self):
        fo = open("testdb.txt", "r")
        l = fo.readline()
        _address, _secret = l.split(":::")
        fo.close()
        return _address, _secret

    @exeTime
    def test_S001_GenerateWallet(self):
        ret_dict = None
        try:
            ret_dict = self.clienthelper.generate_wallet() 
        except Exception, e:
            print "generate_wallet error", e

        self.assertEqual(ret_dict.has_key("wallet"), True)

        fo = open("testdb.txt", "w+")
        datas = str(ret_dict["wallet"]["address"]) + ":::" + str(ret_dict["wallet"]["secret"])
        fo.write(datas)
        fo.close()

        print "[testGenerateWallet]", ret_dict
   
    @exeTime     
    def test_S011_ActiveAccount(self):
        ret_dict = None
        _address, _secret = self._priGetInfoFromDB()
        try:
            ret_dict = self.clienthelper.active_account("SWT", 100000000, config.issuer_account, 
                _address, config.issuer_secret, None)
        except Exception, e:
            print "active_account error", e

        self.assertEqual(ret_dict.has_key("success") and ret_dict["success"], True)

        print "[testActiveAccount]", ret_dict

    def test_S024_Sleep(self):
        time.sleep(10)
        self.assertEqual(True, True)

    @exeTime     
    def test_S034_ActiveAccount(self):
        ret_dict = None
        _address, _secret = self._priGetInfoFromDB()

        websocket_handler = WebSocketClient(config.web_socket_address)  
        websocket_handler.subscribe_message_by_account(_address, _secret) 
        t = threading.Thread(target=websocket_handler.receive, args=())
        t.setDaemon(False)
        t.start()

        try:
            ret_dict = self.clienthelper.active_account("USD", 5, config.currency_ulimit_account, 
                _address, config.currency_ulimit_secret, config.issuer)
        except Exception, e:
            print "active_account error", e

        self.assertEqual(ret_dict.has_key("success") and ret_dict["success"], True)

        print "[testActiveAccount_ws]", ret_dict
        

    def test_S043_Sleep(self):
        time.sleep(10)
        self.assertEqual(True, True)
    
    @exeTime    
    def test_S051_GetBalance(self):
        _ret = []

        _address, _secret = self._priGetInfoFromDB()
        try:
            _g = self.clienthelper.get_balances(_address)
        except Exception, e:
            print "get_balances error", e 
            
        while 1:
            try:
                _res = _g.next()
                _ret.append(_res)
            except StopIteration:
                break

        print "[testGetBalance]", _ret
        self.assertNotEqual(len(_ret), 0)

    @exeTime
    def test_S061_PlaceOrder(self):
        _ret_dict = {}

        _address, _secret = self._priGetInfoFromDB()
        try:
            _ret_dict = self.clienthelper.place_order(_address, _secret, "buy", "USD", 1, 
                "SWT", 2, config.issuer, None)
        except Exception, e:
            print "place_order error", e  

        self.assertEqual(_ret_dict.has_key("success") and _ret_dict["success"], True)

        fo = open("tmphash.txt", "w+")
        fo.write(_ret_dict["hash"])
        fo.close()
            
        print "[testPlaceOrder]", _ret_dict

    # @exeTime
    # def test_S065_RetrieveOrderTransaction(self):
    #     _ret_dict = {}
    #     _address, _secret = self._priGetInfoFromDB()
    #     fo = open("tmphash.txt", "r")
    #     hash_id = fo.readline()
    #     fo.close()
    #     try:
    #        _ret_dict = self.clienthelper.retrieve_order_transaction(_address, hash_id)
    #     except Exception, e:
    #         print "retrieve_order_transaction error", e  
        
    #     print "[testRetrieveOrderTransaction]", _ret_dict

    @exeTime
    def test_S071_GetOrders(self):
        _ret_dict = {}

        _address, _secret = self._priGetInfoFromDB()
        try:
            _ret_dict = self.clienthelper.get_account_orders(_address)
        except Exception, e:
            print "get_account_orders error", e 

        if _ret_dict.has_key("orders") and len(_ret_dict["orders"]) > 0:
            o = _ret_dict.pop()

            fo = open("tmpsequence.txt", "w+")
            fo.write(o["sequence"])
            fo.close()

        self.assertEqual(_ret_dict.has_key("orders"), True)

        print "[testGetOrders]", _ret_dict

    @exeTime
    def test_S081_CancelOrder(self):
        _ret_dict = {}

        _address, _secret = self._priGetInfoFromDB()

        fo = open("tmpsequence.txt", "r")
        order_sequence = fo.readline()
        fo.close()

        try:
            _ret_dict = self.clienthelper.cancel_order(_address, _secret, order_sequence)
        except Exception, e:
            print "cancel_order error", e  
        
        print "[testCancelOrder]", _ret_dict, order_sequence

    @exeTime
    def test_S091_GetOrderBook(self):
        _ret_dict = {}
        _address, _secret = self._priGetInfoFromDB()
        try:
           _ret_dict = self.clienthelper.get_order_book(_address, "SWT", "USD")
        except Exception, e:
            print "get_order_book error", e  
        
        print "[testGetOrderBook]", _ret_dict

    @exeTime
    def test_S101_OrderTransaction(self):
        _ret_dict = {}
        _address, _secret = self._priGetInfoFromDB()
        try:
           _ret_dict = self.clienthelper.order_transaction_history(_address)
        except Exception, e:
            print "order_transaction_history error", e  
        
        print "[testOrderTran]", _ret_dict

    @exeTime
    def test_S111_AddRelations(self):
        _ret_dict = {}
        _address, _secret = self._priGetInfoFromDB()
        try:
           _ret_dict = self.clienthelper.add_relations(config.issuer_account, config.issuer_secret, "authorize", _address, 
                "USD", config.issuer, 1)
        except Exception, e:
            print "add_relations error", e  
        
        print "[testAddRelations]", _ret_dict

    def test_S113_Sleep(self):
        time.sleep(5)
        self.assertEqual(True, True)

    @exeTime
    def test_S121_GetRelations(self):
        _ret_dict = {}
        _address, _secret = self._priGetInfoFromDB()
        try:
           _ret_dict = self.clienthelper.get_relations(config.issuer_account, "authorize", _address, "USD")
        except Exception, e:
            print "get_relations error", e  
        
        print "[testGetRelations]", _ret_dict

    @exeTime
    def test_S131_GetCounterRelations(self):
        _ret_dict = {}
        _address, _secret = self._priGetInfoFromDB()
        try:
           _ret_dict = self.clienthelper.get_counter_relations(_address, "authorize", config.issuer_account, "USD")
        except Exception, e:
            print "get_counter_relations error", e  
        
        print "[testGetCounterRelations]", _ret_dict

    @exeTime
    def test_S141_DeleteRelations(self):
        _ret_dict = {}
        _address, _secret = self._priGetInfoFromDB()
        try:
           _ret_dict = self.clienthelper.delete_relations(config.issuer_account, config.issuer_secret, "authorize", _address, 
                config.issuer, "USD")
        except Exception, e:
            print "delete_relations error", e  
        
        print "[testDeleteRelations]", _ret_dict

    @exeTime    
    def test_S151_PostSettings(self):
        _ret_dict = {}

        _address, _secret = self._priGetInfoFromDB()
        try:
            _settings = {"settings" : {"regular_key": config.currency_ulimit_account}}
            _ret_dict = self.clienthelper.post_account_settings(_address, _secret, **_settings)
        except Exception, e:
            print "post_account_settings error", e 
            
        print "[test_S151_PostSettings]", _ret_dict

    @exeTime    
    def test_S161_GetSettings(self):
        _ret_dict = {}

        _address, _secret = self._priGetInfoFromDB()
        try:
            _ret_dict = self.clienthelper.get_account_settings(_address)
        except Exception, e:
            print "get_account_settings error", e 
            

        print "[test_S161_GetSettings]", _ret_dict

    @exeTime    
    def test_S171_PostSettings2(self):
        _ret_dict = {}

        _address, _secret = self._priGetInfoFromDB()
        try:
            _signers = {"signers" : {"master_weight": 10, "quorum": 20, "signer_entries": 
                {"account" : config.currency_ulimit_account, "weight": 5}}}
            _ret_dict = self.clienthelper.post_account_settings(_address, _secret, **_signers)
        except Exception, e:
            print "post_account_settings2 error", e 
            
        print "[test_S171_PostSettings2]", _ret_dict

    @exeTime    
    def test_S181_GetSigners(self):
        _ret_dict = {}

        _address, _secret = self._priGetInfoFromDB()
        try:
            _ret_dict = self.clienthelper.get_account_signers(_address)
        except Exception, e:
            print "get_account_signers error", e 
            

        print "[test_S181_GetSigners]", _ret_dict

    @exeTime    
    def test_S900_PostOperations(self):
        _ret_dict = {}

        _address, _secret = self._priGetInfoFromDB()
        try:
            _signers = [{"secret": _secret}, {"secret": config.issuer_secret} ]
            _operations = [
                {
                    "account": _address,
                    "type": "SetRegularKey",
                    "settings": {
                        "regular_key": config.currency_ulimit_account
                    }
                },
                {
                    "account": _address,
                    "type": "sell",
                    "order": {
                        "type": "sell",
                        "taker_gets": {
                            "currency": "USD",
                            "counterparty": config.issuer,
                            "value": "1"
                        },
                        "taker_pays": {
                            "currency": "SWT",
                            "value": "20",
                        }
                    },
                },
                {
                    "account": _address,
                    "type": "TrustSet",
                    "trustline": {
                        "limit": "1",
                        "currency": "USD",
                        "counterparty": config.issuer,
                        "account_trustline_frozen": True
                    }
                },
                {
                    "type": "Payment",
                    "account": config.issuer_account,
                    "payment": {
                        "source_account": config.issuer_account,
                        "destination_amount": {
                            "currency": "SWT",
                            "issuer": "",
                            "value": "200"
                        },
                        "destination_account": _address,
                        "paths": "[]"
                    }
                }
       

            ]
            _ret_dict = self.clienthelper.post_operations(_address, _secret, _signers, _operations)
        except Exception, e:
            print "post_operations error", e 
            
        print "[test_S900_PostOperations]", _ret_dict


    # # @exeTime
    # # def test_S990_PlaceOrder(self):
    # #     _ret_dict = {}

    # #     _address, _secret = self._priGetInfoFromDB()
    # #     try:
    # #         _ret_dict = self.clienthelper.place_order(_address, _secret, "buy", "SWT", 2, 
    # #             "USD", 1, None, config.issuer)
    # #     except Exception, e:
    # #         print "place_order error", e  

    # #     self.assertEqual(_ret_dict.has_key("success") and _ret_dict["success"], True)

    # #     fo = open("tmphash.txt", "w+")
    # #     fo.write(_ret_dict["hash"])
    # #     fo.close()
            
    # #     print "[testPlaceOrder2]", _ret_dict

    # @exeTime    
    # def test_S951_GetBalance(self):
    #     _ret = []

    #     _address, _secret = self._priGetInfoFromDB()
    #     try:
    #         _g = self.clienthelper.get_balances(_address)
    #     except Exception, e:
    #         print "get_balances error", e 
            
    #     while 1:
    #         try:
    #             _res = _g.next()
    #             _ret.append(_res)
    #         except StopIteration:
    #             break

    #     print "[testGetBalance]", _ret
    #     self.assertNotEqual(len(_ret), 0)


    @exeTime    
    def test_S999_GetBalance(self):
        _ret = []

        _address, _secret = self._priGetInfoFromDB()
        try:
            _g = self.clienthelper.get_balances(config.issuer_account)
        except Exception, e:
            print "get_balances error", e 
            
        while 1:
            try:
                _res = _g.next()
                _ret.append(_res)
            except StopIteration:
                break

        print "[MasterBalance]", _ret
        self.assertNotEqual(len(_ret), 0) 

if __name__ == "__main__":
    print "current_time:::", str(datetime.datetime.fromtimestamp(int(time.time())))

    unittest.main()
    