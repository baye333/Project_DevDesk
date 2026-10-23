# DevDesk

Espace de travail personnel pour développeurs et étudiants en informatique.
Centralise les projets, tâches, notes techniques, apprentissages, documents et le calendrier.

## Prérequis

- Python 3.12 ou compatible (testé avec Python 3.13)
- Windows PowerShell

## Installation (Windows)

```powershell
cd D:\MonEspace\Documents\project_django
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Ouvrez [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Tests

```powershell
python manage.py test
```

## Compte administrateur

```powershell
python manage.py createsuperuser
```

L'interface d'administration Django est disponible sur `/admin/`.
