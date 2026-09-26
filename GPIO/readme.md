Jean Gazon

Le code présent s’utilise à l’aide d’un bouton et d’une LED.

La LED a trois modes de fonctionnement :

* Mode 1 : clignotement à 0,5 Hz.
* Mode 2 : clignotement à 0,25 Hz.
* Mode 3 : LED éteinte.

Le code utilise un thread pour avoir une lecture continue du bouton, appelant la fonction `read_button`.

La fonction `read_button` change la valeur du compteur et passe la valeur de `buttonEffectActive` à `true` pour activer l’effet lors du changement de fonctionnement (à chaque appui).

La fonction `ledPower` regarde dans quel cycle on se trouve et allume la LED en fonction du fonctionnement choisi.

`buttonEffect` allume la LED pendant deux secondes à chaque appui sur le bouton.

La boucle principale regarde si `buttonEffectActive` est à `true`. Si oui, elle crée l’effet ; sinon, elle appelle le fonctionnement global (`ledPower`).

Les variables `timeLed1` et `timeLed2` permettent de changer la fréquence de clignotement.

Les variables `buttonStep` permettent de changer le nombre de clics nécessaires pour chaque fonctionnement.
