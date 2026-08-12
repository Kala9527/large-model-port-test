@echo off
setlocal EnableExtensions

set "PROJECT_DIR=%~dp0"
set "CONDA_ROOT=D:\Miniconda3"
set "ENV_NAME=LargeModelPortTest_env"
set "ENV_PATH=%CONDA_ROOT%\envs\%ENV_NAME%"
set "PYTHON_EXE=%ENV_PATH%\python.exe"
set "APP_HOST=0.0.0.0"
set "APP_PORT=5181"
set "CONDA_TEMP_DIR=%PROJECT_DIR%.tmp"

if not exist "%CONDA_TEMP_DIR%" mkdir "%CONDA_TEMP_DIR%" >nul 2>nul
set "TEMP=%CONDA_TEMP_DIR%"
set "TMP=%CONDA_TEMP_DIR%"

cd /d "%PROJECT_DIR%"

echo.
echo ============================================================
echo  LargeModelPortTest startup
echo ============================================================
echo  Project dir : %PROJECT_DIR%
echo  Conda root  : %CONDA_ROOT%
echo  Env path    : %ENV_PATH%
echo  Python exe  : %PYTHON_EXE%
echo  Temp dir    : %CONDA_TEMP_DIR%
echo  Local URL   : http://127.0.0.1:%APP_PORT%
echo ============================================================
echo.

if not exist "%CONDA_ROOT%\Scripts\conda.exe" (
    echo [ERROR] Conda was not found at "%CONDA_ROOT%\Scripts\conda.exe".
    echo Please install Miniconda there, or edit CONDA_ROOT in start.bat.
    pause
    exit /b 1
)

if not exist "%PYTHON_EXE%" (
    echo [INFO] Conda environment was not found. Creating Python 3.11 env...
    call "%CONDA_ROOT%\Scripts\conda.exe" create -y -p "%ENV_PATH%" python=3.11
    if errorlevel 1 (
        echo [ERROR] Failed to create conda environment.
        pause
        exit /b 1
    )
)

echo [1/5] Activating conda environment...
call "%CONDA_ROOT%\Scripts\activate.bat" "%ENV_PATH%" >nul 2>nul
if errorlevel 1 (
    echo [WARN] conda activate failed. Continuing with "%PYTHON_EXE%" directly.
) else (
    echo [OK] Conda environment activated.
)

if not exist "%PROJECT_DIR%requirements.txt" (
    echo [ERROR] requirements.txt was not found.
    pause
    exit /b 1
)

echo [2/5] Checking Python dependencies...
"%PYTHON_EXE%" -c "import fastapi, uvicorn, jinja2, httpx, multipart" >nul 2>nul
if errorlevel 1 (
    echo [INFO] Missing dependencies detected. Installing requirements...
    "%PYTHON_EXE%" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install Python dependencies.
        pause
        exit /b 1
    )
) else (
    echo [OK] Dependencies are available.
)

echo [3/5] Checking project import...
"%PYTHON_EXE%" -c "from main import app; assert app.title" >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Project import failed. Please check main.py and installed packages.
    pause
    exit /b 1
)
echo [OK] Project import passed.

if /i "%~1"=="--check-only" (
    echo [OK] Check-only mode completed.
    exit /b 0
)

echo [4/5] Checking whether port %APP_PORT% is already serving this app...
powershell -NoProfile -ExecutionPolicy Bypass -Command "try { $r = Invoke-WebRequest -Uri 'http://127.0.0.1:%APP_PORT%/health' -UseBasicParsing -TimeoutSec 2; if ($r.StatusCode -eq 200 -and $r.Content -like '*ok*') { exit 10 } else { exit 11 } } catch { exit 0 }"
if "%ERRORLEVEL%"=="10" (
    echo [OK] Service is already running at http://127.0.0.1:%APP_PORT%
    pause
    exit /b 0
)

powershell -NoProfile -ExecutionPolicy Bypass -Command "$c = Get-NetTCPConnection -LocalPort %APP_PORT% -ErrorAction SilentlyContinue; if ($c) { exit 12 } else { exit 0 }"
if "%ERRORLEVEL%"=="12" (
    echo [ERROR] Port %APP_PORT% is already in use, but /health did not match this app.
    echo Please stop the process using this port, or edit APP_PORT in start.bat.
    pause
    exit /b 1
)

echo [5/5] Starting FastAPI server...
echo.
echo Open this URL in your browser:
echo   http://127.0.0.1:%APP_PORT%
echo.
echo Press Ctrl+C to stop the server.
echo.
"%PYTHON_EXE%" -m uvicorn main:app --host %APP_HOST% --port %APP_PORT%

endlocal
