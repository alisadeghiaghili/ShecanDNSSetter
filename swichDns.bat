@echo off
setlocal

REM Specify the DNS addresses
set "dns1=178.22.122.100"
set "dns2=185.51.200.2"

REM Check the current DNS configuration
netsh interface ipv4 show dnsservers "Ethernet" | findstr /c:"DHCP" > nul
if %errorlevel% equ 0 (
    REM Current DNS is automatic, so set custom DNS
    netsh interface ipv4 set dns "Ethernet" static %dns1% primary
    netsh interface ipv4 add dns "Ethernet" %dns2% index=2
    echo DNS set to custom addresses: %dns1% and %dns2%
) else (
    REM Current DNS is custom, so set to automatic
    netsh interface ipv4 set dns "Ethernet" dhcp
    echo DNS set to automatic configuration
)

endlocal
