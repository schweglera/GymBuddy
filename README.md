# Django Blog
## Schritt 1: Libraries installieren
```bash
python -m pip install -r requirements.txt
```

## Schritt 2: Datenbankmigrationen durchführen
```bash
$ cd myblog
$ python manage.py makemigrations blog
$ python manage.py migrate
```

## Schritt 3: Webapp starten
```bash
$ cd myblog
$ python manage.py runserver
```

## Testing
```bash
$ cd myblog
$ python manage.py test
```

### Testabdeckung mit `coverage.py`
```bash
$ cd myblog
$ coverage run manage.py test
$ coverage report
$ coverage html
```
