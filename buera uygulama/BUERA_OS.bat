@echo off
title BUERA OS Baslatici
color 0A
echo ==========================================
echo      BUERA OS BASLATILIYOR...
echo ==========================================
echo.

:: 1. Adım: Dosyanın olduğu klasöre git (Çok önemli)
cd /d "%~dp0"
echo Calisma Klasoru: %CD%
echo.

:: 2. Adım: Önce standart 'python' komutuyla deniyoruz
echo [DENEME 1] python komutu ile aciliyor...
python -m streamlit run app.py

:: Eğer yukarıdaki hata verirse (%errorlevel% 0 değilse), buraya girer
if %errorlevel% NEQ 0 (
    echo.
    echo [HATA] 'python' komutu calismadi. 
    echo [DENEME 2] 'py' komutu ile deneniyor...
    echo.
    py -m streamlit run app.py
)

:: Eğer hala hata varsa kapanmasın, biz okuyalım
if %errorlevel% NEQ 0 (
    echo.
    echo ==========================================
    echo [KRITIK HATA] UYGULAMA ACILAMADI!
    echo Muhtemel Sebepler:
    echo 1. Python yuklu degil veya Path'e eklenmemis.
    echo 2. 'streamlit' kutuphanesi yuklu degil (pip install streamlit yapilmali).
    echo 3. Dosya adi 'app.py' degil.
    echo ==========================================
    echo.
)

echo.
echo Pencereyi kapatmak icin bir tusa basin...
pause