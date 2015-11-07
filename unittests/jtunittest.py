# -*- coding:utf-8 -*-
import sys 
sys.path.append("../")

import unittest
import time

from ripplerest.client import Client 
import config

def exeTime(func):  
    def _func(*args, **args2):  
        t0 = time.time()  
        back = func(*args, **args2)  
        print "@%.3fs taken for {%s}" % (time.time() - t0, func.__name__) 
        return back  
    return _func 

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
            ret_dict = self.clienthelper.active_account("SWT", 28, config.issuer_account, 
                _address, config.issuer_secret, None)
        except Exception, e:
            print "active_account error", e

        self.assertEqual(ret_dict.has_key("success") and ret_dict["success"], True)

        print "[testActiveAccount]", ret_dict

    def test_S024_Sleep(self):
        time.sleep(5)
        self.assertEqual(True, True)

    @exeTime     
    def test_S034_ActiveAccount(self):
        ret_dict = None
        _address, _secret = self._priGetInfoFromDB()
        try:
            ret_dict = self.clienthelper.active_account("USD", 1, config.issuer_account, 
                _address, config.issuer_secret, config.issuer)
        except Exception, e:
            print "active_account error", e

        self.assertEqual(ret_dict.has_key("success") and ret_dict["success"], True)

        print "[testActiveAccount]", ret_dict

    def test_S043_Sleep(self):
        time.sleep(5)
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

    @exeTime
    def test_S065_RetrieveOrderTransaction(self):
        _ret_dict = {}
        _address, _secret = self._priGetInfoFromDB()
        fo = open("tmphash.txt", "r")
        hash_id = fo.readline()
        fo.close()
        try:
           _ret_dict = self.clienthelper.retrieve_order_transaction(_address, hash_id)
        except Exception, e:
            print "retrieve_order_transaction error", e  
        
        print "[testRetrieveOrderTransaction]", _ret_dict

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

    # @exeTime
    # def test_S990_PlaceOrder(self):
    #     _ret_dict = {}

    #     _address, _secret = self._priGetInfoFromDB()
    #     try:
    #         _ret_dict = self.clienthelper.place_order(_address, _secret, "buy", "SWT", 2, 
    #             "USD", 1, None, config.issuer)
    #     except Exception, e:
    #         print "place_order error", e  

    #     self.assertEqual(_ret_dict.has_key("success") and _ret_dict["success"], True)

    #     fo = open("tmphash.txt", "w+")
    #     fo.write(_ret_dict["hash"])
    #     fo.close()
            
    #     print "[testPlaceOrder2]", _ret_dict


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
    unittest.main()