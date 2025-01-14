@echo off
SET SCRIPT_NAME=image_morphing_gui.py

:: Vérifier si Python est installé
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python n'est pas installé. Veuillez l'installer depuis https://www.python.org/downloads/.
    pause
    exit /b
)

:: Vérifier et installer les bibliothèques nécessaires
echo Vérification et installation des bibliothèques nécessaires...
pip install opencv-python-headless numpy tqdm >nul 2>&1
IF ERRORLEVEL 1 (
    echo Une erreur est survenue lors de l'installation des bibliothèques.
    pause
    exit /b
)

:: Lancer le script Python
echo Lancement du script Python...
python Pics2Morph.py

pause
