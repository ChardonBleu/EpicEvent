# EpicEvent

![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/ChardonBleu/EpicEvent?color=green)
![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/ChardonBleu/EpicEvent/django)
![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/ChardonBleu/EpicEvent/djangorestframework)
![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/ChardonBleu/EpicEvent/sentry-sdk?color=yellow)  
![GitHub repo size](https://img.shields.io/github/repo-size/ChardonBleu/EpicEvent?color=informational)
![GitHub last commit](https://img.shields.io/github/last-commit/ChardonBleu/EpicEvent)



![Epicevent logo](https://user.oc-static.com/upload/2020/09/22/16007804386673_P10.png "Epicevent logo")



Projet 12 de la formation DA python d'Openclassrooms.

API de gestion et de suivi de clientèle. L'application doit permettre aux utilisateurs de créer des clients, d'ajouter des contrats et des évènements  pour ces clients.  
L'authentification des utilisateurs se fait par token JWT.  
Une équipe de gestion peut administrer les utilisateurs en passant par la console d'administration de Django.  l'équipe de gestion attribut les vendeurs aux clients et attribue les organisateurs aux évènements. Seuls les membres de l'équipe de gestion peuvent supprimer des clients, contrats ou évènements.  
Une équipe de vente peut ajouter de nouveaux clients au fur et à mesure de leur démarchage. Ils peuvent créer des contrats pour ces clients, puis créer des évènements. Ils peuvent mettre à jour les clients et contrats qu'ils ont en charge.
Une équipe de support (organisation) gère les évènements. Ils peuvent mettre à jour les évènements et contrats qu'ils ont en charge.

Installation
---
Télécharger les dossiers et fichiers et les copier dans un dossier de votre choix.  
Dans la console aller dans le dossier choisi.

Environnement virtuel
---
https://packaging.python.org/tutorials/managing-dependencies/


Installer pipenv de manière isolée grâce à pipx:
```bash
pip install pipx
```
puis

```bash
pipx install pipenv
```

Créer un environnement virtuel:
```bash
pipenv install
```

Activer cet environnement virtuel:

```bash 
pipenv shell 
```


Packages:
---

Les modules sont contenus dans le fichier Pipfile.


Base de donnée:
---

Créer une base de donnée dans Postgresql avec un useradmin et remplacer dans settitngs.py la configuration avec votre propre base de donnée.  
```bash 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<non-de_votre-bdd>',
        'USER': '<nom_du_user_admin_de_votre_bdd',
        'PASSWORD': '<mot_de_passe_de_votre_user_admin>',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Exécution
---
Se mettre dans le répertoire racine.

Créer un superuser pour pouvoir accéder à la console admin:
```bash 
python manage.py createsuperuser
```

Faire les migrations pour l'initialisation de la base de donnée:

```bash 
python manage.py makemigrations
```
puis:

```bash 
python manage.py migrate
```

Puis lancer le serveur:

```bash 
python manage.py runserver
```
Le serveur de développement se lance et son adresse s'affiche dans la console:

`Django version 3.2.9, using settings 'EpicEvent.settings'`  
`Starting development server at http://127.0.0.1:8000/`  
`Quit the server with CTRL-BREAK.`


Aller sur l'adresse http `http://127.0.0.1:8000/admin` pour utiliser la console admin en tant que superuser.
Vous pouvez alors commencer à créer des utilisateurs des groupes de vente et de support.

Consulter la documentation de l'API pour une utilisation sur Postman en tant qu'utilisateur des groupes vente ou support:  

    https://documenter.getpostman.com/view/17354834/UVC2Hpaj

Vous pouvez aussi tester l'API en utilisant le module swagger: `http://127.0.0.1:8000/swagger/`



Lancer les tests
---

Documentation pytest et coverage:

    https://docs.pytest.org/en/6.2.x/

    https://coverage.readthedocs.io/en/coverage-5.5/

Le fichier pytest.ini a été configuré pour exécuter coverage en même temps que pytest.  
Depuis le répertoire racine lancer pytest
```bash 
pytest
```

Après excécution des tests aller consulter le résulat du coverage dans le dossier nouvellement créé htmlcov en ouvrant le fichier index.html dans un navigateur.


Ressources utilisées
---

Ressources web:

Les environnements virtuels:

    https://www.youtube.com/watch?v=YVa-97TJAR4&t=4582s


Le cours Openclassrrom "Modélisez et implémentez une base de données relationnelle avec UML":

    https://openclassrooms.com/fr/courses/4055451-modelisez-et-implementez-une-base-de-donnees-relationnelle-avec-uml


La documentation officielle de Django:

    https://docs.djangoproject.com/en/3.0/


La documentation officielle de DjangoRestFramework:

    https://www.django-rest-framework.org/


Le tutoriel de Docstring pour l'installation d'une base de donnée Postgresql pour Django:

    https://www.docstring.fr/formations/configurer-postgresql-avec-django/introduction-a-la-formation-1404/


La documentation Postman:

    https://learning.postman.com/docs/publishing-your-api/documenting-your-api/

Le markdown guide:

    https://www.markdownguide.org/basic-syntax/

La documentation swagger:

    https://drf-yasg.readthedocs.io/en/stable/

Remerciements:
---

Un très grand merci à ma mentor Sandrine Suire pour la transmission de son savoir, son accompagnement de qualité et sa patience à tout (ré)expliquer dans les moments de perdition.

Et merci à tous les membres du Discord DA python: 
http://discord.pythonclassmates.org/
