@echo off
echo ========================================
echo    NETFLIX PERFORMANCE TEST SUITE
echo ========================================
echo.

REM Check if API is running
echo 🔍 Checking if API is available...
curl -s http://localhost:8000 >nul
if errorlevel 1 (
    echo ❌ ERROR: API not running at http://localhost:8000
    echo.
    echo Please start the API first:
    echo 1. Ask Team A to start their FastAPI server
    echo 2. Ensure it's running on port 8000
    echo 3. Try: curl http://localhost:8000
    pause
    exit /b
)
echo ✅ API is running!
echo.

echo Select test to run:
echo 1 - Baseline Test (50 users, 3 minutes)
echo 2 - With Cache Test (100 users, 5 minutes)
echo 3 - High Load Test (200 users, 5 minutes)
echo 4 - Run All Tests (15 minutes total)
echo 5 - Quick Test (10 users, 1 minute)
echo.

set /p choice="Enter choice (1-5): "

if "%choice%"=="1" goto baseline
if "%choice%"=="2" goto cache
if "%choice%"=="3" goto highload
if "%choice%"=="4" goto all
if "%choice%"=="5" goto quick
goto end

:baseline
echo.
echo 🚀 Running Baseline Test (50 users, 3 min)...
locust -f locustfile.py --host=http://localhost:8000 --headless -u 50 -r 10 --run-time 3m --csv=baseline --html=report_baseline.html
echo ✅ Baseline test complete!
goto show_results

:cache
echo.
echo 🚀 Running Cache Test (100 users, 5 min)...
locust -f locustfile.py --host=http://localhost:8000 --headless -u 100 -r 20 --run-time 5m --csv=cache --html=report_cache.html
echo ✅ Cache test complete!
goto show_results

:highload
echo.
echo 🚀 Running High Load Test (200 users, 5 min)...
locust -f locustfile.py --host=http://localhost:8000 --headless -u 200 -r 50 --run-time 5m --csv=highload --html=report_highload.html
echo ✅ High load test complete!
goto show_results

:quick
echo.
echo 🚀 Running Quick Test (10 users, 1 min)...
locust -f locustfile.py --host=http://localhost:8000 --headless -u 10 -r 5 --run-time 1m --csv=quick --html=report_quick.html
echo ✅ Quick test complete!
goto show_results

:all
echo.
echo 🚀 Running ALL Tests (this will take ~15 minutes)...
echo.
echo Test 1/4: Baseline (50 users, 3 min)...
locust -f locustfile.py --host=http://localhost:8000 --headless -u 50 -r 10 --run-time 3m --csv=baseline --html=report_baseline.html
echo.
echo Test 2/4: Cache Test (100 users, 5 min)...
locust -f locustfile.py --host=http://localhost:8000 --headless -u 100 -r 20 --run-time 5m --csv=cache --html=report_cache.html
echo.
echo Test 3/4: High Load (200 users, 5 min)...
locust -f locustfile.py --host=http://localhost:8000 --headless -u 200 -r 50 --run-time 5m --csv=highload --html=report_highload.html
echo.
echo ✅ All tests complete!
goto show_results

:show_results
echo.
echo ========================================
echo 📊 Test Results
echo ========================================
dir *.csv *.html

echo.
echo To generate charts, run:
echo python collect_metrics.py
echo.

:end
pause