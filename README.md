# 程式描述

* auto-punch-in 使用指令
```
python auto_punch_in.py --mode punch_in
python auto_punch_in.py --mode check_out
```

* `skip_dates.txt` 中可輸入不要打卡的時間(請假、出差...)

# 安裝

`pip install selenium`

`scheduler_file` 要透過 `windows 工作排程器`匯入，並調整：
* `一般`中的使用者帳戶
* `觸發程序`中的時間
* `動作`中啟動程式的相對路徑


