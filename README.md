# Pics2Morph

 Image Morphing Script with GUI and Video Creation

Description:
This Python script enables users to create smooth image morphing transitions between a series of images with an intuitive graphical user interface (GUI). It also generates a video from the processed images.

Features:

User-friendly GUI:

Select a folder containing images.
Specify the number of transition frames between images.
Set the video's frames per second (FPS) and quality.

Morphing Transition:
Creates seamless transitions between consecutive images using linear blending.
Video Generation:
Outputs a high-quality MP4 video containing all images and transitions.
Error Handling:
Ensures images have the same dimensions.
Provides clear error messages for incorrect inputs.

Batch Processing:
Automatically processes all images in the selected folder.
Saves results in a structured output folder.

Cross-platform Compatibility:
Supports Windows and other Python-compatible platforms.

Dependencies:

opencv-python-headless
numpy
tqdm

How to Run:

For windows: just click "RunMeFirst.bat"

For other OS:
Install Python and required libraries.
(open with a notepad RunMefirst.bat and install manually)
Run the script (Pics2Morph.py) to start the GUI.
Follow the prompts to generate transitions and the final video.

-----
#Résumé en Français.
#Script de Morphing d'Images avec Interface Graphique et Création de Vidéo

Description :

Ce script Python permet de créer des transitions fluides entre une série d'images via une interface graphique conviviale (GUI). Il génère également une vidéo à partir des images traitées.

Fonctionnalités :

Interface graphique intuitive :

Sélection d’un dossier contenant des images.
Configuration du nombre d’images de transition.
Définition des images par seconde (FPS) et de la qualité de la vidéo.

Transitions fluides :
Génère des transitions homogènes entre des images consécutives à l'aide d'un mélange linéaire.

Création de vidéo :
Produit une vidéo MP4 de haute qualité regroupant toutes les images et transitions.

Gestion des erreurs :
Vérifie que les dimensions des images sont identiques.
Affiche des messages clairs en cas d'erreur.

Traitement par lots :
Traite automatiquement toutes les images d’un dossier.
Sauvegarde les résultats dans un dossier de sortie organisé.

Compatibilité multiplateforme :
Fonctionne sous Windows et autres plateformes compatibles avec Python.

Dépendances :

opencv-python-headless
numpy
tqdm

Instructions d’exécution :

Mettez les deux fichiers (pics2morph.py et RunMeFirst.bat) dans un dossier prévu pour ça: exemple "Pics2Morph"

Pour windows: cliquez juste sur "RunMeFirst.bat"

Pour les autres OS (Linux, mac etc)

Installer Python et les bibliothèques nécessaires. (ouvrez l fichier RunMeFirst.bat avec un éditeur de texte, un blocnote ...)
Lancer le script (Pics2morph.py)  pour démarrer l’interface graphique.
Suivre les instructions pour générer les transitions et la vidéo finale.
