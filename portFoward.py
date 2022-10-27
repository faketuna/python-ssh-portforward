from sshtunnel import SSHTunnelForwarder
import time
import os
import math


userDir = os.environ['USERPROFILE']
sshKeyFile = f'{userDir}\\.ssh\\id_rsa'
# SSHキーのパスワード
sshKeyPassword = ""

# リモートのSSHアドレス/ポート
SSHRemoteAddr = ''
SSHRemotePort = 18660

# 接続するユーザー名
userName = ''

# リモートのポート
RemoteForwardAddress = 8000
# 自分のPCのポート
LocalForwardAddress = 8000



def main():
    server = SSHTunnelForwarder(
        (SSHRemoteAddr, SSHRemotePort), 
        ssh_username=userName,
        ssh_pkey=sshKeyFile, 
        ssh_private_key_password=sshKeyPassword,
        remote_bind_address=("127.0.0.1", RemoteForwardAddress),
        local_bind_address=("localhost", LocalForwardAddress),
        set_keepalive=60.0
    )
    startTime = time.time()
    sessionTime = time.time()
    runAllowed = True
    isAlreadyDisconnected = False
    lastDisconnectedTime = 0
    while runAllowed:
        if(not server.is_active):
            printState(startTime=startTime, variableTime=lastDisconnectedTime, isRunning=False)
            if (not isAlreadyDisconnected):
                lastDisconnectedTime = time.time()
                isAlreadyDisconnected = True
            server.start()
            if (server.is_active):
                sessionTime = time.time()
                isAlreadyDisconnected = False
        else:
            printState(startTime=startTime, variableTime=sessionTime, isRunning=True)

def printState(startTime, variableTime, isRunning):
    
    if (isRunning):
        print(
            'ポートフォワードは実行中' + '\n' + 
            '総実行時間: ', math.floor(time.time() - startTime), "秒            " + "\n" + 
            '現在のセッション: ', math.floor(time.time() - variableTime), "秒            " + "\n" + 
            '終了はCTRL + C' + "\n" +
            '\033[4A',
            end=""
        )
    else:
        print(
            'ポートフォワードは停止中' + '\n' + 
            '総実行時間: ', math.floor(time.time() - startTime), "秒            " + "\n" + 
            '切断から: ', math.floor(time.time() - variableTime), "秒            " + "\n" +
            '終了はCTRL + C' + "\n" +
            '\033[4A',
            end=""
        )


if __name__ == '__main__':
    main()