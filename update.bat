@echo off
setlocal enabledelayedexpansion

REM ========== CONFIG ==========
set REPO_DIR=C:\Your\Path\To\Project
set BRANCH=main
set PYTHON=.venv\Scripts\python
set PIP=.venv\Scripts\pip

REM ========= Helper to show original error ========
:ShowError
echo.
echo [ERROR] %1
echo ----------------------------------------------
echo ORIGINAL SYSTEM ERROR:
echo %ERROR_OUTPUT%
echo ----------------------------------------------
goto END


REM ========== START ==========
echo ============================================
echo       IPCO CMMS - Update and Run
echo ============================================
echo.

REM 0) Go to repo
echo [0] Changing directory to: %REPO_DIR%
cd /d "%REPO_DIR%" 2>temp_error.txt
if errorlevel 1 (
    set /p ERROR_OUTPUT=<temp_error.txt
    call :ShowError "Could not change to REPO_DIR. Check the path."
)

REM 1) Fetch
echo.
echo [1] Fetching origin/%BRANCH% ...
set ERROR_OUTPUT=
for /f "delims=" %%i in ('git fetch origin %BRANCH% 2^>temp_error.txt') do set ERROR_OUTPUT=
if errorlevel 1 (
    set /p ERROR_OUTPUT=<temp_error.txt
    call :ShowError "git fetch failed"
)

REM 2) Determine ahead/behind
for /f "tokens=1 2" %%i in ('git rev-list --left-right --count origin/%BRANCH%...HEAD 2^>temp_error.txt') do (
  set BEHIND=%%i
  set AHEAD=%%j
)
if errorlevel 1 (
    set /p ERROR_OUTPUT=<temp_error.txt
    call :ShowError "Could not compare commits (rev-list failed)"
)

echo.
echo [2] Commits behind: %BEHIND%
echo [2] Commits ahead : %AHEAD%

REM CASE: pull
if "%BEHIND%" NEQ "0" if "%AHEAD%"=="0" (
    echo.
    echo [3] Pulling latest changes...
    git pull origin %BRANCH% 2>temp_error.txt
    if errorlevel 1 (
        set /p ERROR_OUTPUT=<temp_error.txt
        call :ShowError "git pull failed"
    )
)

REM CASE: push
if "%AHEAD%" NEQ "0" if "%BEHIND%"=="0" (
    echo.
    echo [3] Pushing client updates...
    git add -A

    git commit -m "client updates" 2>temp_error.txt
    REM commit might fail if no changes → ignore this one

    git push origin %BRANCH% 2>temp_error.txt
    if errorlevel 1 (
        set /p ERROR_OUTPUT=<temp_error.txt
        call :ShowError "git push failed"
    )
)

REM CASE: diverged
if "%AHEAD%" NEQ "0" if "%BEHIND%" NEQ "0" (
    echo.
    echo [ERROR] Both ahead and behind (diverged). Manual merge required.
    goto END
)

echo.
echo [3] Repo synchronized.

REM 4) Install requirements
echo.
echo [4] Installing requirements...
%PIP% install -r requirements.txt 2>temp_error.txt
if errorlevel 1 (
    set /p ERROR_OUTPUT=<temp_error.txt
    call :ShowError "pip install failed"
)

REM 5) Migrations
echo.
echo [5] Running migrations...
%PYTHON% manage.py migrate 2>temp_error.txt
if errorlevel 1 (
    set /p ERROR_OUTPUT=<temp_error.txt
    call :ShowError "migrate failed"
)

REM 6) Run server
echo.
echo [6] Starting Django server...
echo.
%PYTHON% manage.py runserver 0.0.0.0:8000 2>temp_error.txt
if errorlevel 1 (
    set /p ERROR_OUTPUT=<temp_error.txt
    call :ShowError "runserver failed"
)

goto END

REM ========== END ==========
:END
echo.
echo ============================================
echo Script finished. Press any key to exit.
echo ============================================
pause
endlocal
