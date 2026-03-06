import subprocess
import time

# 方法1: 使用 mshta
print("测试 mshta 通知...")
subprocess.run(['mshta', 'vbscript:Execute("CreateObject(\'WScript.Shell\').Popup \'这是一个测试通知！\', 10, \'🧘 活动提醒\', 64:close")'], shell=True)

print("通知已发送")
