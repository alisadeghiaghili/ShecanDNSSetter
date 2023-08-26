@echo off
setlocal

REM Elevate the script to run with administrator privileges
REM >nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system" && (
    REM goto :continue
REM ) || (
    REM echo Requesting administrative privileges...
    REM "%SYSTEMROOT%\System32\runas.exe" /noprofile /user:%USERDOMAIN%\%USERNAME% "%~dp0%0"
    REM exit /b
REM )

REM :continue

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

REM Get the current DNS configuration after changes
echo Current DNS configuration after changes:
netsh interface ipv4 show dnsservers "Ethernet"

pause
endlocal
