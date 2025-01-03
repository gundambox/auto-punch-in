# 程式描述

* auto-punch-in 使用指令
```
python auto_punch_in.py --mode punch_in
python auto_punch_in.py --mode check_out
```

* `skip_dates.txt` 中可輸入不要打卡的時間(請假、出差...)
* 運作後，程式會產生 `log.txt` 可用來檢察程式是否正確運作。
```
2025-01-02 18:04:05,303 - INFO - ------------auto punch-in start------------
2025-01-02 18:04:05,304 - INFO - Today is not a skip day
2025-01-02 18:04:09,447 - INFO - enter account: Hua
2025-01-02 18:04:09,474 - INFO - enter passward: Testing
2025-01-02 18:04:09,480 - INFO - check out submit
2025-01-02 18:04:14,632 - INFO - end mission
2025-01-03 08:52:39,563 - INFO - ------------auto punch-in start------------
2025-01-03 08:52:39,570 - INFO - Today is not a skip day
2025-01-03 08:52:43,881 - INFO - enter account: Hua
2025-01-03 08:52:43,911 - INFO - enter passward: Testing
2025-01-03 08:52:43,917 - INFO - punch in submit
2025-01-03 08:52:49,075 - INFO - end mission
```


# 安裝

`pip install selenium`

`scheduler_file` 要透過 `windows 工作排程器`匯入，並調整：
* `一般`中的使用者帳戶
* `觸發程序`中的時間
* `動作`中啟動程式的相對路徑


