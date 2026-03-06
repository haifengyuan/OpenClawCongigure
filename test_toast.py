import ctypes
from ctypes import wintypes

# 使用 Windows API 显示一个简单的消息框
MessageBox = ctypes.windll.user32.MessageBoxW
MessageBox(None, "这是一个测试通知！", "🧘 活动提醒", 0x40 | 0x1000)  # MB_ICONINFORMATION | MB_SYSTEMMODAL
