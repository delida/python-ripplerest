# -*- coding:utf-8 -*-
server_host = "tapi.jingtum.com" #"kapi.jingtum.com"
sercer_port = 443
is_https = True

web_socket_address = "ws://tapi.jingtum.com:5002" #"ws://kapi.jingtum.com:5002"

issuer_account = "jHb9CJAWyB4jr91VRWn96DkukG4bwdtyTh"
issuer_secret = "snoPBjXtMeMyMHUVTgbuqAfg1SUTb"
currency_value = 128
currency_type = "SWT"

ulimit_account = "jHb9CJAWyB4jr91VRWn96DkukG4bwdtyTh"
ulimit_secret = "snoPBjXtMeMyMHUVTgbuqAfg1SUTb"
issuer = "jBciDE8Q3uJjf111VeiUNM775AMKHEbBLS" #"jBciDE8Q3uJjf111VeiUNM775AMKHEbBLS"

robot_main_account = "jUFZJJnTbwBzuZcSuWc2nMFNpaGeWtRCD6"
robot_main_secret = "ssKt7P86m5PBYmMAJoay6YZ1gNTvq"

currency_ulimit_account = "jJ8PzpT7er3tXEWaUsVTPy3kQUaHVHdxvp"
currency_ulimit_secret = "shYK7gZVBzw4m71FFqZh9TWGXLR6Q"

api_receive_keywords = ("connection", "subscription", "ledger", 
    "transaction main account", "transaction affected account", "close")

min_heart_interval = 10
max_process_interval = 15

start_robot_id = 3
end_robot_id = 4

policy_condition_lists = (
    ("SWT", ">", 100),
    ("USD", ">", 1),
    ("SWT", "<", 1),
    ("USD", "<", 1),
    )

policy_result_lists = (
    ("SWT", 10, "USD", 1, None, issuer),
    ("USD", 1, "SWT", 10, issuer),
    ("SWT", 100),
    ("USD", 2),
    )

robot_policy_lists = (
    ("balance", ),
    ("addrelations", "authorize") # action_type, relation_type
    ("order", 0, 1), # action_type, policy_condition, policy_result_lists
    ("order", 1, 0),
    ("paymentswt", 2, 2), # action_type, policy_condition, policy_result_lists
    ("paymentusd", 3, 3),
    ("orderlist",),
    ("cancelorder", 2) # action_type, order_cnt_max to cancel
    )