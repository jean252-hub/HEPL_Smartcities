# Lecteur de musique avec Raspberry Pi Pico 2 W

## Matériel utilisé

Le programme s'utilise avec :

- un **Raspberry Pi Pico 2 W** ;
- un **buzzer passif** ;
- un **potentiomètre** ;
- un **bouton poussoir** ;
- une **LED**.

## Organisation du programme

Le programme est composé de deux fichiers Python :

### `setup_musique.py`

Ce fichier contient les différents paramètres nécessaires à la lecture des musiques :

- les paramètres rythmiques, notamment la durée des différentes notes ;
- les différentes mélodies disponibles ;
- les partitions associées à chaque mélodie ;
- les fréquences correspondant aux différentes notes.

### `buzzer.py`

Ce fichier contient toute la logique du programme.

Le fonctionnement est divisé en plusieurs parties :

#### 1. Lecture des partitions

Une fonction permet de lire une partition à partir des données présentes dans `setup_musique.py`.

Pour chaque note de la partition, le programme récupère sa fréquence et sa durée, puis la joue à l'aide du buzzer.

Une fonction dédiée permet de définir la fréquence du buzzer afin de produire la note correspondante.

Le programme contrôle également une LED : celle-ci s'allume lorsqu'une note est jouée et s'éteint pendant les silences.

#### 2. Gestion du volume

Un thread est utilisé pour lire en continu la valeur du potentiomètre.

Selon la position du potentiomètre, le programme définit plusieurs niveaux de volume. La valeur correspondante est ensuite appliquée au buzzer grâce au signal PWM.

Le thread permet ainsi de modifier le volume pendant qu'une musique est en cours de lecture, sans interrompre la mélodie.

Le programme vérifie également si une note est actuellement en cours de lecture afin d'éviter que le buzzer produise un son pendant les silences.

#### 3. Changement de musique avec une interruption

Une interruption est configurée sur le bouton poussoir.

À chaque appui sur le bouton, une fonction d'interruption est appelée et incrémente un compteur.

Le compteur permet de sélectionner la musique à jouer :

- `1` → **Blinding Lights**
- `2` → **Get Lucky**
- `3` → **Star Wars**
- `4` → **Bad Guy**

Lorsque le compteur atteint `5`, il revient à `1`. Cela permet de parcourir les différentes musiques disponibles en appuyant successivement sur le bouton.

#### 4. Sélection de la musique

La fonction `musicChoice()` utilise la valeur du compteur pour déterminer quelle partition doit être jouée.

Elle appelle ensuite la fonction de lecture de partition avec le nom de la mélodie correspondante.

Une fois la musique terminée, le programme attend quelques secondes avant de recommencer la lecture de la musique sélectionnée.

## Fonctionnement général

Le programme démarre un thread chargé de surveiller le potentiomètre afin d'adapter le volume du buzzer.

En parallèle, la boucle principale joue la musique sélectionnée.

Le bouton poussoir peut être utilisé à tout moment pour changer de musique grâce à l'interruption.

Le fonctionnement général peut donc être résumé ainsi :
