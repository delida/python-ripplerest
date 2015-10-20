# -*- coding:utf-8 -*-
server_host = "kapi.jingtum.com"
sercer_port = 443
is_https = True

issuer_account = "jHb9CJAWyB4jr91VRWn96DkukG4bwdtyTh"
issuer_secret = "snoPBjXtMeMyMHUVTgbuqAfg1SUTb"
currency_value = 128
currency_type = "SWT"

ulimit_account = "jHb9CJAWyB4jr91VRWn96DkukG4bwdtyTh"
ulimit_secret = "snoPBjXtMeMyMHUVTgbuqAfg1SUTb"
issuer = "jBciDE8Q3uJjf111VeiUNM775AMKHEbBLS"


web_socket_address = "ws://kapi.jingtum.com:5002"

api_receive_keywords = ("connection", "subscription", "ledger", 
    "transaction main account", "transaction affected account", "close")

min_heart_interval = 10
max_process_interval = 30

policy_condition_lists = (
    ("SWT", ">", 120),
    ("SWT", "<", 120),
    ("SWT", "<", 1),
    ("USD", "<", 1),
    )

policy_result_lists = (
    ("SWT", 10, "USD", 1, None, issuer),
    ("USD", 1, "SWT", 10, issuer),
    ("SWT", 100),
    ("USD", 1),
    )

robot_policy_lists = (
    ("balance", ),
    ("order", 0, 1), # action_type, policy_condition, policy_result_lists
    ("order", 1, 0),
    ("payment", 2, 2), # action_type, policy_condition, policy_result_lists
    ("payment", 3, 3),
    )