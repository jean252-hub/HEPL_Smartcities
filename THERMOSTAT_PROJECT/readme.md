# Exercice 3 : Thermostat Intelligent avec Raspberry Pi Pico

## Matériel utilisé

Le programme s'utilise avec :

- un **Raspberry Pi Pico** (ou Pico 2 W) ;
- un capteur de température et d'humidité **DHT20** ;
- un écran **LCD 1602** (liaison I2C) ;
- un **potentiomètre** (capteur d'angle rotatif) ;
- une **LED** ;
- un **buzzer**.

## Bibliothèques requises

Pour fonctionner, ce code nécessite le téléversement de deux bibliothèques sur la mémoire du Raspberry Pi Pico :
- `dht20.py` : pour la communication et la lecture du capteur de température.
- `lcd1602.py` : pour la gestion de l'affichage sur l'écran LCD.

## Configuration des broches (Pins)

- **Potentiomètre** : Broche analogique `A0` (`ADC0`)
- **Écran LCD** : Bus `I2C1` — SCL sur `Pin 7`, SDA sur `Pin 6`
- **Capteur DHT20** : Bus `I2C0` — SCL sur `Pin 9`, SDA sur `Pin 8`
- **LED** : Broche numérique `Pin 16` (pilotée en PWM)
- **Buzzer** : Broche numérique `Pin 18` (piloté en PWM)

## Organisation du programme

Le script principal utilise une architecture multitâche (via des threads) pour gérer simultanément la surveillance de la consigne et la régulation de la température.

### 1. Gestion de la température de consigne (Thread dédié)

Un thread secondaire est démarré en tâche de fond pour lire en continu la valeur analogique du potentiomètre.

Selon la position du potentiomètre (valeur de 0 à 65535), un calcul est effectué pour mapper cette position sur une plage de température de **15.0°C à 35.0°C**. La valeur obtenue est arrondie au dixième (0.1°C).

Ce thread permet de modifier dynamiquement et en temps réel la température de consigne souhaitée, sans bloquer le reste du programme.

### 2. Régulation et états du thermostat (Boucle principale)

La boucle principale lit la température ambiante du capteur DHT20 toutes les scondes et adapte le comportement des périphériques selon 3 états :

#### État 1 : Température inférieure ou égale à la consigne (T ≤ Consigne)
- L'écran LCD affiche la consigne sur la première ligne et la température ambiante sur la seconde.
- La LED est **éteinte**.
- Le buzzer est **éteint**.

#### État 2 : Température légèrement supérieure à la consigne (Consigne < T < Consigne + 3°C)
- L'écran LCD affiche la consigne et la température ambiante.
- La LED simule un **dimmer** avec une variation progressive de l'intensité via un signal PWM sinusoïdal d'une période de 2 secondes.
- Le buzzer reste **éteint**.

#### État 3 : Mode Alarme (T ≥ Consigne + 3°C)
- L'écran LCD passe en mode Alarme : la première ligne fait **défiler le mot "ALARM"** et clignote, tandis que la deuxième ligne affiche les températures.
- La LED **clignote rapidement** (toutes les 100 ms).
- Le buzzer **émet un son continu** pour avertir d'une surchauffe critique.

## Fonctionnement général

Au démarrage, le programme initialise les connexions I2C et PWM, puis lance le thread de lecture du potentiomètre. 

La boucle principale mesure continuellement la température ambiante. Elle compare cette valeur à la consigne définie par l'utilisateur pour adapter instantanément l'affichage (normal ou défilement d'alerte), l'état visuel de la LED (éteinte, respiration, ou clignotement) et l'alerte sonore du buzzer.

## Détails sur les fonctions complexes du code

Le programme utilise `time.ticks_ms()` (le temps écoulé en millisecondes depuis le démarrage) pour animer la LED et l'écran LCD de manière fluide, **sans jamais bloquer l'exécution** du reste du code avec des pauses de type `sleep()`.

### 1. Gestion de la LED : `ledcontroller(state)`
Cette fonction contrôle l'intensité de la LED via un signal PWM (valeur de 0 à 30000) selon 3 modes :

*   **Mode Alarme (`state == 2`) : Clignotement rapide**  
    Le temps en millisecondes est divisé par 100, puis l'opérateur `% 2` détermine si le résultat est pair ou impair. Cela fait osciller instantanément la LED entre la luminosité maximale (30000) et l'extinction (0) toutes les **100 ms**.
*   **Mode Alerte (`state == 1`) : Effet "Respiration / Dimmer"**  
    Une fonction sinus (`math.sin`) est appliquée sur le temps écoulé (divisé par 2000). Le résultat mathématique oscille naturellement entre -1 et 1 toutes les **2 secondes**. Un traitement ramène cette valeur entre 0.0 et 1.0, permettant à l'intensité de la LED de croître et décroître de manière très fluide.
*   **Mode Normal (`else`) : Éteinte**  
    Le rapport cyclique PWM est forcé à 0 pour éteindre complètement la LED.

### 2. Gestion de l'affichage d'urgence : `lcdAlarm(tempA, tempC)`
Cette fonction gère l'écran LCD (16 colonnes, 2 lignes) en cas d'alarme critique. Elle combine deux animations sur la première ligne :

*   **Le défilement du mot "ALARM"**  
    Toutes les **150 ms**, la variable `position` augmente pour décaler le texte vers la droite. Le calcul `(position + i) % 16` insère le mot lettre par lettre et applique un défilement automatique : dès qu'une lettre dépasse le bord droit (colonne 15), elle réapparaît instantanément sur le bord gauche (colonne 0) pour un effet de roulement infini.
*   **Le clignotement global**  
    Toutes les **300 ms**, un test de parité temporelle (`% 2`) décide soit d'afficher le texte défilant, soit d'injecter une ligne de 16 espaces vides. Cela provoque le clignotement intermittent de l'animation.
*   **Affichage des données**  
    Pendant que la première ligne s'anime, la seconde ligne affiche en continu la température ambiante réelle et la température de consigne de manière fixe pour rester lisible.
