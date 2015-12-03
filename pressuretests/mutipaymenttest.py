# -*- coding:utf-8 -*-
import threading

import sys, os 
sys.path.append("../")

import time, datetime

from ripplerest.client import Client 
import config

testing_account_hapi =  [
                    "jadVkD6wqscmmb17BdSB6jetkfZkHYE56t",
                    "j3WYDYZ8bYmSKcVxXbb5oQ2Qc4UrqNbij3",
                    "j3J3BT6XrZ8JY1Nkg1FDcDVXY4vTyi7www",
                    "jhDnMW9CkJmiwWPgXjhTfLVa5AChPgrRwu",
                    "jEpKagEgPpTXKDApzBtv8cgW1RPBcy5ghr",
                    "ja7azKWL5ARfrru8gN1qyBzcJMuqGFYxAD",
                    "j9rqNtJUB1YJHtJ1AjHEfHUjU2jmJpxBNc",
                    "jfc1j4E5AUatLxQv6NqWu5BkWPfj2WAAcV",
                    "jLpaCgBPJ2wnELqPz38ZGkg2YDZC5oxsCu",
                    "jHck6FBPkvax97qjK83PoJRJoR5znPHHa7",
                    "jDd7Rm1MeNQmmbA4yY5cGaR5nausC1a4KF",
                    "jDW8TsD1JZygYeRGXEDLnAq2LLuwUmsFuT",
                    "jh8xMhjAZy4UbX7BMbcN3pabAADWB6XgLz",
                    "jpTSLAfkH9iD12VRGB1HR699PzLEXS6kuK",
                    "jUKmMLFJVLV4KQWmDQ4obDBsBwntfgxXA9",
                    "jJL3Gad875JwCjiWRGUbBnC7JxExiAwcQR",
                    "j4G2EiG8TjmdcLk5gZJc6kJZpySzkMvoUC",
                    "jnKJ8QDmEwKjj3cM5AaBQ69MShCcMW66qQ",
                    "j42yVs2f2g6vAtniFgZfmV8nwUvjGNbbmu",
                    "j41q1BLkhwJ7fe5DcmNStptSP676bXiXuG",
                    ]

testing_account = [
                    "jGbMaHpLmtHddFKvSoAkLSUcyYiZH27TSJ",
                    "jBGiEmySBTQnnwhmeDXYgH8FVXf7zm9UHP",
                    "jKBa2RErU6ioM3k21JVLSurrnWPnnR6V3K",
                    "jfMbB7tyaRgjcAV8L285cVumjqh93mhWvT",
                    "j9yxJ67Jegun2Zkb7xrMYer56RuZs14PKu",
                    "jNaZCf3VPUwXhKkmpDXFk3RM5FMyDuwygt",
                    "jLZWVQDWdjrhxLbQ485xjEsDuhVaEQ4nc9",
                    "jhNGghKy7MXNke4FXYuTE79tv1VSGTi2mC",
                    "jL3kPSgppNK62yMKNGjU7k5VTRk6HLA2C3",
                    "jDJqJabapTh59rNT3uUtAPenurpg5v4Zoh",
                    "js54wUjXdtZLF8ANh5evdnMUT19AGGdzkT",
                    "jQwvM5o9KSSFV9u9aLgeKoqEwEUQyZ9zLf",
                    "j35xEduCgGkPLvpY6JEGCNL8FzHzYtobqD",
                    "jKPKVLFetG7AKnJeGrnci2pKbEAkzHRr8y",
                    "jJ4eA3hSJEwNWXZZ3sDWLvq66szE7EVLi6",
                    "jGPiWXMtrxGEUanBaCXEjHFkJNN8CEYMpT",
                    "jKusvLxu3AZ1T2QhGa9dtUg9Yko68Zkt9P",
                    "jDkm978WfHmtKdWQYWmxZQNESP3gmEnQhM",
                    "jQnr1fQ4VEMM3JpXBKmuyfPsFYZJ5RL4tJ",
                    "jLCoQPzTmTvd2uNjvePpeENAF6xebmpgeN",
                    "jNmDE1ABirPWoqh9wBFyxqJBeDfWeUgbH",
                    "jM8yMe33DjudaxXSp2DXunMwRVntnVBkdn",
                    "jNSx925KmmBNtVU7nqFotLXGKD7ss5Jdtq",
                    "j3Y9V63SunATnn3z9x2Gpv9oXhLaH79UWN",
                    "jspfHo3xvEYv1GXQ5r6bd1tuqewVP33YF9",
                    "jJZzXQUw3YSkU6oATTk9nbokcMF7xCUVn4",
                    "jHHfQLYtngLaC84PuGRH4vcawByhcCn1fA",
                    "jGXPMTxeWuZwofS8qa6A9qzxq2w3uKeihM",
                    "j9H5WJ4Kkt4sK2C22fDgkww4ymaQowBn6h",
                    "j4Yrd5nnw11NtyfpZg3weET9PX4T5WRXoE",
                    "jKbKdPGBde6w7qt9UNeArPcuXb7K5D4qix",
                    "jMNAzTNHerBHAH5pZZ5peXrVzoqkqHKCYN",
                    "jwcpTGG5Le9Tof6DiGepADLAtyd1k1BdEn",
                    "jDaq17y6tcCvbH8Z7jbLiAioYStnobzvB7",
                    "jNQtkU47zG54ajf4GrAzZZQBQJYAghcMz5",
                    "jGhWpfuG7STR9y2jQ6W9eYxg75VboChTzw",
                    "jGxTSDRfkAirYaSjZnZXEMv3UTMS5HtWPY",
                    "jUFjcfxZymXWCQ8zN5qpokjWVtEGBvdgJM",
                    "jsc93oQaJuqzao5HFcj1cMZw8xK6J1ZNXr",
                    "jnuAhqTWc88yjHACvdycjWsuK3EXztPW6L",
# jP7NFiBVKCZkNiq5gpzxWdhKFpAiaN2MQi:::shMU9Xjy3MSYoteBqshiWHpsp3yFp
# jnk72hUgiFdPVrYA3Y61RoqP5Rez6ifiiH:::shVJtXyUMjeQihLDkM7t6PuNFGVX3
# jPCnY5PsJd9tUmh6PLfNBPCiBAP1JhUdeD:::spvpsZEpkKGVNtbmiG8yv2mqW6AZn
# jD6tQMFvTQEXV8wfqHZiQ1KpLvujCukKZs:::sawAdyc246oodxzxz8aFdAXnG7vBF
# jKk7pnpZKPxN6dGUVfbVu27NNRCeLahM6C:::sn3bFzhvkMSHhonpUVp7VTVAyWs4P
# jMys6g4FbcovxPAcBbByqjDtHjGfpsuTwq:::ssfH8cJdry1KuHXA4p2zkkHPdMemY
# jo3evcE8QT4EgeviVXTGMbWsoJ5j6s8yN:::shJ1NrhcP8Nafa9cXvcWYqL9fW2Y2
# j9VqgMo1Y4nQFLUNb4Qbnm1a6V3PVcE7xH:::ssfyf4yv4VRt7KXXY4XQvQjL7P7EM
# jJLAJnXP6T3ieovsGGQ81DttyQM4CmBLr6:::snazREEUHwVvHSYADXdF93K23835U
# jpHm7RGecu3NEe4WfBJEMJi8Hbw7Rdpnum:::shQtrXbrXdCK7MR7EXrC8Uup59xge
# jLESTYUUKfwoh6uGqDxw2anmwtTSX8oCcz:::ssYkyshhvkGXypAC7bAA5MjezFrZF
# jGWvsvA9BLmYKZphAUaF9EWTHtmV5Dx5Pe:::ssfcAcTpmTHCfj813zyv7ajdFaWdd
# jQKtZGGVv79kkoyYBbL61hGxUnRxU8WMY:::shffRTYbuY3LFRiYKWuzH1j6hAcru
# jpaqDJrnD6hrdQoxp7nt5MSdTArMXePUxX:::ssb5MFK9Mg8sehr3zG7diEJu6UefM
# j3aG8CDbrm1aFK9AAwNWswo3Z9TEv16avm:::sndEiiMjiamEcEHPxhG27PQkbWp7S
# jaqJBgVM1a9KNbbbhnVTP4cVjCG99HjGVk:::snQXcuzoMxmCo831dyDhPoFEuTW9r
# jsPXiKauXtmywzTGCWsVDgKwZ5HSoxiVeH:::ssbzd26sMYHeQ3W1SDq3K9bMWgXkE
# jGeGJ3QnmbPG65j57nnoWca7mooVgEudZQ:::sh1tjzkbpFiR5pq7eHwk1ybBFsdkd
# jJBFwdyLYdzxU4CLrpAxRtgtqcnQLzd3PR:::spqAxzUySrXKYHofhvg1whiwY7Kja
# jLEy91sPKopz3vdP7Xu8eaCQFL3QFJEXSb:::shEfBAD2Tpz8gKqmjpGwF34AWWFL1
# jN3s6rXV3Y3Ae6AfjAizDvr8ZyttB6B7p3:::shUgxnki2pJFudgKBSnnfg8uMfntM
# ja7U2J46spkuwp73ksQwGEs71akHZrfivi:::ssMVJaYs3Y3eL76Zqde8UaNmkuu9n
# jo3EfPK1xC3vJFWUnDMy31ztErQLyiS4P:::shECSgCSqsE2oYMWhLCx72r4FXRPY
# jHhArPbTMKywBGC8qGcpJxjTAzoQ9Zcu7D:::snxxTbTDquVLdaAy6SeZWB76z6ixE
# jh9mjtRU8jSgqpyfqTo4fgZYcDe1Ndv2rV:::shitBYPHq4EAPrHpFMfojddUJXWyi
# jMWSGQTMtc9MvaF3QGFQZkJY9PK73g8X88:::ssAoBYKq4Mb7jjCjZzkuVpiGzBxx2
# j3gb2TRLnNm56Xybg2CfgS2UouADX9ZZV5:::snmwhRNXPEL77Urn61YCQXaD7nM6P
# jQNCpr9ZXX48dktNSJ4XetDXQTjj3WdjD:::sp8Jh59gv1gYibcdm4HP4sELoVWSk
# j35UdKL9RSqgoeXkQktpaHu6s5J5vkJ35h:::ssEdh6SknDo5yLRduwSP5HJLpFAb8
# jKKpJb6cVQBdbGWh5yeZxv81dpYnFE8n3j:::ss2AWNewDNbRnXyUdJ1D2cYmsTi5z
]

def exeTime(func):  
    def _func(*args, **args2):  
        t0 = time.time()  
        back = func(*args, **args2)  
        print "@%.3fs taken for {%s}" % (time.time() - t0, func.__name__) 
        return back  
    return _func 

@exeTime  
def doPayment(y, num):
    global mutex, g_num, p_num
    clienthelper = Client(config.server_host + ":" + str(config.sercer_port), config.is_https)             
    #print threading.currentThread().getName()
  
    for x in xrange(0, int(num)):
        mutex.acquire()
        try:
            _address = testing_account[y]
            ret_dict = clienthelper.active_account("SWT", 1, config.issuer_account, 
                _address, config.issuer_secret, None)
            if ret_dict.has_key("success") and ret_dict["success"]:
                p_num += 1
            else:
                print "Error in payment:", ret_dict
        except Exception, e:
            fo1 = open("dopaymenterror.txt", "a")
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
def checkAccount():   
    global c_num, g_num

    g_num = 0

    for _address in testing_account:
        time.sleep(0.2)
        try:
            _ret = _priGetBalance(_address) #[{"currency":"SWT", "value":30}]           
            if len(_ret) > 0:
                for r in _ret:
                    if r["currency"] == "SWT" and r["value"] > 0:
                        c_num += 1
                        
                        _fg = 1
                        if os.path.exists("paymentaccount.txt"):
                            fo = open("paymentaccount.txt", "r")
                            
                            lines = fo.readlines()
                            for l in lines:
                                addr, val = l.split(":::")
                                if addr==_address:
                                    g_num += int(r["value"])-int(val)
                                    print "AFTER--_address:%s, value:%s, delta:%s "%(_address, r["value"], int(r["value"])-int(val))
                                    _fg = 0      
                            fo.close()

                        if _fg:
                            fo = open("paymentaccount.txt", "a")
                            datas = str(_address) + ":::" + r["value"] +  "\n"
                            print "BEFORE--_address:%s, value:%s"%(_address, r["value"])
                            fo.write(datas)
                            fo.close()
                        break
                    else:
                        print "Error in check(2)", _ret
            else:
                print "Error in check(1)", _ret           
        except Exception, e:
            #print "Error in check(0)", x, k, str(x*50+k), _address, _secret
            fo1 = open("getbalanceerror1.txt", "a")
            datas = str(_address) + ":::" + str(e) +  "\n"
            fo1.write(datas)
            fo1.close()
            continue

    print "g_num::", g_num 

def checkAccountThead(num, per):
    threads = []
    for x in xrange(0, num):
        threads.append(threading.Thread(target=checkAccount, args=(x, per,)))
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join() 

def main(num, per):
    global mutex, g_num, p_num, c_num
    g_num, p_num, c_num = 0, 0, 0
    
    mutex = threading.Lock()
     
    threads = []
    checkAccount()
    
    t0 = time.time()  
    
    for x in xrange(0, num):
        threads.append(threading.Thread(target=doPayment, args=(x, per,)))
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join() 

    print "Payment done,  all threads used %s seconds, wait %s to check ..." % (time.time() - t0, config.waitseconds)
    time.sleep(config.waitseconds)

    print "<%s>PAYMENT REPORT: <%s>\n Wanted Count <%s>\n PaymentOk Count <%s>\n CheckOk Count <%s>\n" %\
        (str(datetime.datetime.now()), config.server_host, num * per, p_num, c_num) 

    checkAccount()
    #checkAccountThead(config.threadnum, config.numpertherad)


    print _priGetBalance(config.issuer_account)
         
    
if __name__ == '__main__':
    global c_num
    is_payment = 0
    if is_payment:
        print str(datetime.datetime.now()), "payment ..."
        main(20, 1)
    else:
        c_num = 0
        print str(datetime.datetime.now()), "checking ..."
        checkAccount()
        #checkAccountThead(config.threadnum, config.numpertherad)
        print str(datetime.datetime.now()), c_num