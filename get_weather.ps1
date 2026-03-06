[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
$client = New-Object System.Net.WebClient
$url = "https://wttr.in/Beijing?format=3&lang=zh"
$result = $client.DownloadString($url)
Write-Output $result
