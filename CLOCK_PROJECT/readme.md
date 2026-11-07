# Jean Gazon

## Projet Horloge

## Matériel utilisé

Le programme s'utilise avec :

- un **Raspberry Pi Pico 2 W** ;
- un **servo-moteur** ;
- un **bouton poussoir**.

## Organisation du programme

Le projet se décompose en 4 fichiers :

- `main.py` : contient toute la logique du code nécessaire au fonctionnement de l'horloge ;
- `servo.py` : contient la fonction permettant de contrôler le servo-moteur ;
- `wifi_setup.py` : contient le mot de passe et le SSID du Wi-Fi ;
- `main_energy.py` : contient le même code que `main.py`, mais intègre le code permettant l'étude de la consommation énergétique du Raspberry Pi Pico.

## Explication du code

### Fichier `main.py`

Le code contient la fonction `connect_wifi`, qui tente de se connecter au réseau Wi-Fi à l'aide de l'identifiant et du mot de passe du fichier `wifi_setup`.

La fonction `sync_time` permet de récupérer l'heure UTC et de synchroniser l'horloge interne.

La fonction `local_time` permet d'ajouter les heures nécessaires pour avoir la bonne heure quand on change de fuseau horaire.

La fonction `update_clock` permet de calculer l'angle nécessaire au servo-moteur et de le transmettre à la fonction `servo.turn`, pour que le moteur se place à l'angle voulu. On peut choisir entre le mode 12 heures, où l'on utilise l'heure modulo 12, et le mode 24 heures, où l'on utilise l'heure modulo 24, selon le mode de fonctionnement sélectionné.

Un simple clic sur le bouton change le fuseau horaire, et un double clic change le mode d'affichage (12 h ou 24 h).

### Fichier `servo.py`

Un servo-moteur ne se commande pas avec un angle, mais avec la durée des impulsions qu'il reçoit. À 100 Hz, une impulsion se répète toutes les 10 ms, et c'est sa durée qui détermine la position du servo : plus l'impulsion est longue, plus l'angle est grand.

Sur le Raspberry Pi Pico, le rapport cyclique est donné par un nombre entre 0 et 65535 (duty_u16) : 0 correspond à un signal toujours à 0 et 65535 à un signal toujours à 1. Le calcul est une simple droite :

duty = angle / 180 × 13000 + 4000

angle / 180 donne une proportion entre 0 (0°) et 1 (180°) ;
× 13000 étale cette proportion sur une plage de 13000 unités ;
+ 4000 décale le résultat, car le servo ne réagit qu'à partir d'une impulsion minimale.

### Fichier `main_energy.py`

Ce fichier reprend le code de `main.py` et ajoute la fonction `power_cycle`, appelée toutes les 10 secondes à la place de la simple mise à jour de l'horloge. Elle fait passer le microcontrôleur par quatre états, dont on mesure la consommation avec le PPK2 :

1. **État 1** : microcontrôleur actif avec le Wi-Fi allumé (récupération de l'heure) ;
2. **État 2** : microcontrôleur actif sans Wi-Fi ;
3. **État 3** : microcontrôleur en light sleep (`lightsleep`) ;
4. **État 4** : microcontrôleur en deep sleep (`deepsleep`).

À la sortie du deep sleep, le Raspberry Pi Pico redémarre : le programme repart donc du début.


### Analyse de la consommation électrique (Raspberry Pi Pico 2 W)(alimentation 5v par le power profiler)

| État (60 s) | Mesure réelle | Théorie | Observation |
| :--- | :---: | :---: | :--- |
| **1. Actif + Wi-Fi** | **50 mA** *(pics 140–200 mA)* | 50 – 80 mA | Conforme (pics liés aux émissions RF). |
| **2. Actif sans Wi-Fi** | **36 mA** | 15 – 38 mA | Conforme (CPU actif, radio coupée). |
| **3. Light Sleep** | **28,6 mA** | 1,8 – 6 mA | Surconsommation (périphériques/USB actifs). |
| **4. Deep Sleep** | **28,6 mA** | 0,25 – 1,8 mA | **Écart majeur** (absence de vraie mise en veille profonde). |

**Explication de l'écart en veille (`Light Sleep` / `Deep Sleep`) :**
* **Défaut du régulateur embarqué (RT6154) :** Ce convertisseur est dimensionné pour de fortes charges (jusqu'à 3 A). À très faible courant, son rendement chute fortement et il continue de consommer un courant de repos et de commutation permanent.
* **Limitation matérielle/logicielle :** **28,6 mA** entre les états 3 et 4 indique également que le microcontrôleur (RP2350) et la puce sans-fil (CYW43439) ne coupent pas totalement leurs horloges internes (notamment si l'interface USB reste active ou si la broche d'alimentation Wi-Fi n'est pas isolée avant le sommeil).
