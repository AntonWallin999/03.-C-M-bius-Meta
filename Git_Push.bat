REM ================================
REM RP9 Git Push – Updated Path
REM ================================

setlocal ENABLEDELAYEDEXPANSION

REM --- Byt till rätt repo ---
cd /d "C:\Users\Documents\RP9"
REM --------------------------

git status
REM --------------------------

git add .
REM --------------------------

git commit -m "html export"
REM --------------------------

git push
REM --------------------------

pause
