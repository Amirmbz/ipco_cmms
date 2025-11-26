@echo off
setlocal enabledelayedexpansion

REM ===== CONFIG =====
REM Full path to your repo (folder that contains manage.py)
set REPO_DIR=C:\ipco\ipco_cmms
REM Your main branch name (change to master if needed)
set BRANCH=master

echo ============================================
echo      IPCO CMMS - Update and Run
echo ============================================
echo.

REM Go to repo directory
cd /d "%REPO_DIR%" || (
  echo [ERROR] Repository directory not found:
  echo         %REPO_DIR%
  pause
  exit /b 1
)

REM 1) Fetch latest changes
echo [1] Fetching latest changes from origin/%BRANCH% ...
git fetch origin %BRANCH%
if errorlevel 1 (
  echo [ERROR] git fetch failed. Check network or git remote.
  pause
  exit /b 1
)

REM 2) Compare local and remote heads (ahead/behind)
for /f "tokens=1 2" %%i in ('git rev-list --left-right --count origin/%BRANCH%...HEAD') do (
  set BEHIND=%%i
  set AHEAD=%%j
)

echo     Local commits AHEAD of origin/%BRANCH%: %AHEAD%
echo     Local commits BEHIND origin/%BRANCH%: %BEHIND%
echo.

REM CASE 1: Local is behind remote (pull)
if "%BEHIND%" NEQ "0" if "%AHEAD%"=="0" (
  echo [2] Local repo is BEHIND remote. Pulling latest changes...
  git pull origin %BRANCH%
  if errorlevel 1 (
    echo [ERROR] git pull failed (maybe conflicts?). Please contact your developer.
    pause
    exit /b 1
  )
  goto after_sync
)

REM CASE 2: Local is ahead remote (push)
if "%AHEAD%" NEQ "0" if "%BEHIND%"=="0" (
  echo [2] Local repo is AHEAD of remote. Committing and pushing client updates...
  git add -A
  git commit -m "client updates" >nul 2>&1
  if errorlevel 1 (
    echo     No new local changes to commit (this is OK).
  ) else (
    echo     Changes committed as "client updates".
  )

  git push origin %BRANCH%
  if errorlevel 1 (
    echo [ERROR] git push failed. Check network or remote permissions.
    pause
    exit /b 1
  )
  goto after_sync
)

REM CASE 3: Up to date
if "%AHEAD%"=="0" if "%BEHIND%"=="0" (
  echo [2] Local and remote are already in sync. No code changes.
  goto after_sync
)

REM CASE 4: Diverged (both ahead and behind)
echo [2] WARNING: Local and remote have diverged (both ahead and behind).
echo     This needs manual resolution on the dev machine.
pause
exit /b 1


:after_sync
echo.
echo [3] Checking and installing Python requirements (if requirements.txt exists)...
if exist requirements.txt (
  .\.venv\Scripts\pip install -r requirements.txt
  if errorlevel 1 (
    echo [ERROR] pip install failed. Check Python/virtualenv.
    pause
    exit /b 1
  )
) else (
  echo     requirements.txt not found, skipping dependency install.
)

echo.
echo [4] Running database migrations...
.\.venv\Scripts\python manage.py migrate
if errorlevel 1 (
  echo [ERROR] migrate failed. Check database connectivity or migrations.
  pause
  exit /b 1
)

echo.
echo [5] Starting Django development server...
echo     The server will stop when you close this window.
echo     Open http://127.0.0.1:8000/ in your browser.
echo.

.\.venv\Scripts\python manage.py runserver 0.0.0.0:8000

echo.
echo Django server stopped. Press any key to close this window.
pause
endlocal