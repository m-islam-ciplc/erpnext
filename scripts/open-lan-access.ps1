# Run this script as Administrator (right-click PowerShell -> Run as administrator)
# Opens ERPNext dev server to other PCs on your LAN.

$ErrorActionPreference = "Stop"

Write-Host "Configuring LAN access for ERPNext on ports 8000 and 9000..."

# Remove old rules if re-running
netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=8000 2>$null | Out-Null
netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=9000 2>$null | Out-Null
netsh advfirewall firewall delete rule name="ERPNext Dev 8000" 2>$null | Out-Null
netsh advfirewall firewall delete rule name="ERPNext Dev 9000" 2>$null | Out-Null

# Forward LAN traffic on Windows -> WSL via localhost
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=8000 connectaddress=127.0.0.1 connectport=8000
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=9000 connectaddress=127.0.0.1 connectport=9000

# Allow inbound through Windows Firewall
netsh advfirewall firewall add rule name="ERPNext Dev 8000" dir=in action=allow protocol=TCP localport=8000
netsh advfirewall firewall add rule name="ERPNext Dev 9000" dir=in action=allow protocol=TCP localport=9000

Write-Host ""
Write-Host "Port forwarding:"
netsh interface portproxy show all

$ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {
	$_.IPAddress -notlike '127.*' -and
	$_.InterfaceAlias -eq 'Wi-Fi'
}).IPAddress

Write-Host ""
Write-Host "Share this URL with other users on the same network:"
Write-Host "  http://${ip}:8000"
Write-Host ""
Write-Host "On this PC you can also use: http://127.0.0.1:8000"
