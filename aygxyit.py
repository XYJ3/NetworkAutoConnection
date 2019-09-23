import requests
import time
import subprocess

'''

# 校园网自动登录

'''

# 检测网络状态

def checkNetwork():
    a = subprocess.Popen('ping -n 2 8.8.8.8', shell=True,
                         stdout=subprocess.PIPE)
    if(a.wait()):  # 返回值为1表示网络连接中断
        return(False)
    else:
        return(True)


# 注销登录

def netLogout():
    logoutUrl = 'http://172.168.254.6:801/eportal/?c=ACSetting&a=Logout&wlanuserip=172.19.150.185&wlanacip=172.168.254.100&wlanacname=&port=&hostname=172.168.254.6&iTermType=1&session=null'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    response = requests.get(logoutUrl, headers=headers)
    if response.status_code==200:
        log('注销登录成功')
    else:
        log('注销失败')


# 登录

def netLogin():
    loginUrl = 'http://172.168.254.6:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=172.168.254.6&iTermType=1&wlanuserip=172.19.150.185&wlanacip=172.168.254.100&mac=000000000000&ip=172.19.150.185&enAdvert=0&loginMethod=1'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    data = {
        'DDDDD': ',0,17031210228@unicom',
        'upass': '888888',
        'R1': '0',
        'R2': '0',
        'R6': '0',
        'para': '00',
        '0MKKey': '123456',
        'buttonClicked': '',
        'redirect_url': '',
        'err_flag': '',
        'username': '',
        'password': '',
        'user': '',
        'cmd': '',
        'Login': '',
    }
    resp = requests.post(loginUrl, headers=headers, data=data)
    if resp.status_code == 200:
        log('登陆成功')
        log('检测网络状态......')
        if checkNetwork():
            log('网络正常\n')
    else:
        log('登录失败')


# 日志记录

def log(logs):
    print(logs)
    file = open(r"D:\net_connection_logs.txt", "a",encoding='UTF-8')
    file.write(time.asctime(time.localtime(time.time())) +
               ": "+logs+"\n")
    file.close()


if __name__ == "__main__":
    # 检测网络状态
    print('已启动')
    global count
    count=0
    while (1):
        if checkNetwork(): # 网络正常
            count=0
        else:              # 网络中断
            log('网络中断')
            netLogout()    # 注销
            netLogin()     # 登录
            count += 1
        if count==5:      # 如果多次登录失败，需要手动修复网络
            log('等待手动修复')
            while(1):
                if checkNetwork():
                    log('网络已修复')
                    break
                time.sleep(5)
        time.sleep(5)
