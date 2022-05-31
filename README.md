# SPLOKS
Sploks est un programme de remplacement de Coliks, qui est utilisée depuis 17 ans dans le magasin Sports-Time d'Echallens pour gérer la location de matériel de sports d'hiver.

## Mettre en place l'environnement

### Applications à télecharger

- [PyCharm](https://www.jetbrains.com/pycharm/download/#section=windows) ou un IDE de votre choix.
- [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) ou un autre outil SQL de votre préference.
- [Python 3](https://www.python.org/downloads/) - La dernière version de Python 3.
- [QtDesigner](https://build-system.fman.io/qt-designer-download) si vous désirez ouvrir les fichiers _.ui_

### Guide d'installation
Après avoir installé les programmes au dessus:

1. Lancer le script SQL qui se trouve dans _docs/workbench_
2. Dans le dossier "sploks", dupliquez le fichier _const.py.example_ et effacez lui l'extension _.example_
3. Remplacez les "_..._" par vos propres configs SQL
4. Ensuite, ouvrir le CMD et entrez:

    ```
    pip install pyqt5
    pip install pyqt5-tools
    pip install mysql-connector-python-rf
    pip install reportlab
    ```

5. Vous pouvez maintenant fermer le CMD et ouvrir le dossier Sploks avec votre IDE (PyCharm, chez nous).
6. Dans le projet (alt+1 si pas visible), click droit sur _sploks.py_ et clickez sur l'option _run sploks_.
7. Votre projet devrait normalement ce lancer si tout est bien installé.

## Documentations
- **[Documentation de projet](/docs/Documentation%20de%20projet.pdf)**
- **[Journaux de travail](/logbook)** - Dossier contenant un journal de travail par SPRINT

