[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null

function Send-Notification {
    param([string]$title, [string]$message)
    
    $template = "<toast><visual><binding template=`"ToastText02`"><text id=`"1`">$title</text><text id=`"2`">$message</text></binding></visual><audio src=`"ms-winsoundevent:Notification.Default`"/></toast>"
    
    $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
    $xml.LoadXml($template)
    $toast = New-Object Windows.UI.Notifications.ToastNotification $xml
    [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("OpenClaw").Show($toast)
}

$startTime = Get-Date -Hour 9 -Minute 0 -Second 0
$endTime = Get-Date -Hour 19 -Minute 0 -Second 0
$intervalMinutes = 45

# 计算今天的提醒时间点
$reminderTimes = @()
$current = $startTime
while ($current -le $endTime) {
    $reminderTimes += $current
    $current = $current.AddMinutes($intervalMinutes)
}

Write-Host "活动提醒已启动！"
Write-Host "提醒时间: 09:00 - 19:00，每45分钟一次"
Write-Host "按 Ctrl+C 停止"

$lastReminderFile = "$env:TEMP\openclaw_last_reminder.txt"

while ($true) {
    $now = Get-Date
    
    # 检查是否在时间范围内
    $todayStart = Get-Date -Hour 9 -Minute 0 -Second 0
    $todayEnd = Get-Date -Hour 19 -Minute 0 -Second 0
    
    if ($now -ge $todayStart -and $now -le $todayEnd) {
        # 读取上次提醒时间
        $lastReminder = [DateTime]::MinValue
        if (Test-Path $lastReminderFile) {
            $lastStr = Get-Content $lastReminderFile -ErrorAction SilentlyContinue
            [DateTime]::TryParse($lastStr, [ref]$lastReminder) | Out-Null
        }
        
        # 检查是否需要提醒（距上次超过45分钟）
        if ($now - $lastReminder -ge [TimeSpan]::FromMinutes($intervalMinutes)) {
            Send-Notification -title "🚶 该活动一下了！" -message "你已经坐了45分钟，起来走走吧~"
            Write-Host "[$(Get-Date -Format 'HH:mm')] 已发送提醒"
            $now.ToString() | Out-File $lastReminderFile -Force
        }
    }
    
    Start-Sleep -Seconds 60
}
