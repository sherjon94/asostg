@echo off
chcp 65001 > nul
title Asosnoma Generator Telegram Bot
echo ======================================================
echo       Asosnoma Generator Telegram Bot
echo ======================================================
echo.

python bot.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Bot to'xtadi yoki xatolik yuz berdi.
    pause
)
