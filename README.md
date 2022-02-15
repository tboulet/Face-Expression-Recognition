## Projet de détection d'expression faciales

### Description :

Le projet a pour but de construire un programme pour détecter les visages et leurs émotions associées depuis une image ou une vidéo prise en temps réelle. Les visages sont détectés et classifiés parmi 7 émotions : Angry, Disgust, Fear, Happy, Sad, Surprise et Neutral.

### Fichiers python à lancer :

videoCapture.py : prend une vidéo en entrée, traite chaque frame avec imageProcess.py et renvoie la vidéo traitée ainsi. Les visages sont détectés et classifiés.

game.py : lance une capture de la vidéo et des smileys à imiter le plus rapidement possible.
Paramètres de game(): 
    - playTime : durée du jeu   
    - dt_required : délai durant lequel l'émotion doit être reconnue en continu pour être validée
    - n_photos : nombre de photos souvenirs que le modèle prendra pendant le jeu, affichées à la fin
