@echo off
chcp 65001 >nul

echo ================================
echo Uploading files...
echo ================================

:: 把 scp 命令写在同一行，避免 ^ 带来的空格问题
scp -i "%USERPROFILE%\.ssh\sshpd" "%~dp0config.yaml" "%~dp0sync_clash_proxy_groups.py" root@10.0.0.30:/root

if errorlevel 1 (
    echo SCP upload failed
    pause
    exit /b
)

echo ================================
echo Running remote commands...
echo ================================

ssh -i "%USERPROFILE%\.ssh\sshpd" root@10.0.0.30 "/root/update_clash_nginx.sh"

if errorlevel 1 (
    echo Remote execution failed
    pause
    exit /b
)

echo ================================
echo Done
echo ================================

pause