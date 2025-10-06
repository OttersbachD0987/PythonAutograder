@echo off

if exist ".\venv" (
    echo venv exists.
) else (
    echo venv does not exist, creating now.
    py -m venv venv
)

./venv/Scripts/activate.bat