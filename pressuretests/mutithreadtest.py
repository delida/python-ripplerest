# -*- coding:utf-8 -*-
import threading

import sys 
sys.path.append("../")

import time, datetime

from ripplerest.client import Client 
import config

def exeTime(func):  
    def _func(*args, **args2):  
        t0 = time.time()  
        back = func(*args, **args2)  
        print "@%.3fs taken for {%s}" % (time.time() - t0, func.__name__) 
        return back  
    return _func 

@exeTime  
def createAccount(num):
    global mutex, g_num, p_num
    clienthelper = Client(config.server_host + ":" + str(config.sercer_port), config.is_https)             
    #print threading.currentThread().getName()
  
    for x in xrange(0, int(num)):
        mutex.acquire()
        try:
            ret_dict = clienthelper.generate_wallet() 
            if ret_dict.has_key("wallet"):
                g_num += 1
                _address, _secret = ret_dict["wallet"]["address"], ret_dict["wallet"]["secret"]
                fo = open("accountdb.txt", "a")
                datas = str(_address) + ":::" + str(_secret) + "\n"
                fo.write(datas)
                fo.close()
                ret_dict = clienthelper.active_account("SWT", 28, config.issuer_account, 
                    _address, config.issuer_secret, None)
                if ret_dict.has_key("success") and ret_dict["success"]:
                    p_num += 1
                else:
                    print "Error in payment:", ret_dict
            else:
                print "Error in wallet", ret_dict
        except Exception, e:
            fo1 = open("createaccounterror.txt", "a")
            fo1.write(str(e))
            fo1.close()
            
        mutex.release()

def _priGetBalance(address):
    _ret = []
    clienthelper = Client(config.server_host + ":" + str(config.sercer_port), config.is_https)      
    _g = clienthelper.get_balances(address)
    while 1:
        try:
            _res = _g.next()
            _ret.append(_res)
        except StopIteration:
            break

    return _ret

@exeTime
def checkAccount(x, i):   
    global c_num
    fo = open("accountdb.txt", "r")
    lines = fo.readlines()

    for k, l in enumerate(lines[x*i:x*i+i]):
        _address, _secret = l.split(":::")
        time.sleep(0.2)
        try:
            _ret = _priGetBalance(_address) #[{"currency":"SWT", "value":30}]

            # fo1 = open("tmpresult.txt", "a")
            # datas = str(x*50+k) + ":::" + str(x) + "," + str(k) + ":::" + str(_ret) + "\n"
            # fo1.write(datas)
            # fo1.close()

            if len(_ret) > 0:
                for r in _ret:
                    if r["currency"] == "SWT" and r["value"] > 0:
                        c_num += 1
                        break
                    else:
                        print "Error in check(2)", x, k, _ret
            else:
                print "Error in check(1)", x, k, _ret
        except Exception, e:
            #print "Error in check(0)", x, k, str(x*50+k), _address, _secret
            fo1 = open("getbalanceerror.txt", "a")
            datas = str(x*i+k) + ":::" + str(x) + "," + str(k) + ":::" + str(_address) + ":::" + str(_secret) + "\n"
            fo1.write(datas)
            fo1.close()
            continue

    fo.close()

def checkAccountThead(num, per):
    threads = []
    for x in xrange(0, num):
        threads.append(threading.Thread(target=checkAccount, args=(x, per,)))
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join() 

def main(num):
    t0 = time.time()  
    global mutex, g_num, p_num, c_num
    g_num, p_num, c_num = 0, 0, 0
    
    mutex = threading.Lock()
     
    threads = []
    
    for x in xrange(0, num):
        threads.append(threading.Thread(target=createAccount, args=(config.numpertherad,)))
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join() 

    print "Create done,  all threads used %s seconds, wait %s to check ..." % (time.time() - t0, config.waitseconds)
    time.sleep(config.waitseconds)
    #checkAccount()
    checkAccountThead(config.threadnum, config.numpertherad)

    print "<%s>CREATE ACCOUNT REPORT: <%s>\n Wanted Count <%s>\n WalletOk Count <%s>\n PaymentOk Count <%s>\n CheckOk Count <%s>\n" %\
        (str(datetime.datetime.now()), config.server_host, config.threadnum * config.numpertherad, g_num, p_num, c_num) 

    print _priGetBalance(config.issuer_account)
         
    
if __name__ == '__main__':
    global c_num
    if config.is_create:
        print str(datetime.datetime.now()), "creating ..."
        main(config.threadnum)
    else:
        c_num = 0
        print str(datetime.datetime.now()), "checking ..."
        #checkAccount()
        checkAccountThead(config.threadnum, config.numpertherad)
        print str(datetime.datetime.now()), c_num