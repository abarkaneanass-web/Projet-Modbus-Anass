# Projet-Modbus-Anass


## User Story

En tant qu’opérateur de ligne,
je veux que la machine automatisée mesure la tension de la batterie, et à partir d'un certain seuil, mettre le convoyeur en marche pour permettre de trier les batterie, et assurer la rapidité.

## Fonctionnement

Capteur 1 : Capteur de mesure de tension : mesure la tension de la batterie.

Actionneur 1 : Moteur du convoyeur → A partir de 36V mettre le convoyeur en marche.

## Critères d’acceptation

Quand le capteur 1 mesure la tension de la batterie, un afficheur affiche la partie entière.

Si la tension est superieur à 36V alors le convoyeur se met en marche pour mener la batterie au stand d'éxpédition, autrement, le convoyeur reste éteint.

Une fois bloquée, la visseuse (actionneur 2) démarre automatiquement.

À la fin du vissage, le vérin se rétracte et le convoyeur redémarre.

En cas de non-détection du capteur 2, la machine reste en attente et signale une erreur à l’opérateur.


### Illustration
![Schéma de la machine](image2.png)
