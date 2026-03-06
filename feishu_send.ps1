param(
    [string]$message
)

$webhook = "https://open.feishu.cn/open-apis/bot/v2/hook/7fea2a65-4d06-4e5f-bbcf-99f89188568a"
$json = @{
    msg_type = "text"
    content = @{
        text = $message
    }
} | ConvertTo-Json -Depth 3

$body = [System.Text.Encoding]::UTF8.GetBytes($json)
$request = [System.Net.HttpWebRequest]::Create($webhook)
$request.Method = "POST"
$request.ContentType = "application/json; charset=utf-8"
$request.ContentLength = $body.Length
$stream = $request.GetRequestStream()
$stream.Write($body, 0, $body.Length)
$stream.Close()

$response = $request.GetResponse()
$reader = New-Object System.IO.StreamReader($response.GetResponseStream(), [System.Text.Encoding]::UTF8)
$result = $reader.ReadToEnd()
Write-Host $result
