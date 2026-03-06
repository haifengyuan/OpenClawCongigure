import os
import subprocess

# 使用 PowerShell 发送 Toast 通知
ps_script = '''
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] > $null

$template = @"
<toast>
    <visual>
        <binding template="ToastText02">
            <text id="1">🧘 活动提醒</text>
            <text id="2">这是一个测试通知！</text>
        </binding>
    </visual>
    <audio src="ms-winsoundevent:Notification.Default"/>
</toast>
"@

$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml($template)
$toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("活动提醒").Show($toast)
'''

subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
