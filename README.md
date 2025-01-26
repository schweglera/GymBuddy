# Gym Buddy App
## Schritt 1: Python version prüfen
Kompatibel mit Version ab 3.12.1
```bash
python --version
```


## Schritt 2: Libraries installieren
```bash
python -m pip install -r requirements.txt
```

## Schritt 3: Welche Feaures implementiert wurden
```
Folgende Features wurden in dieser Web-App implementiert:

F1: Eigene Trainingspläne erstellen
    Die App bietet eine Möglichkeit eigene Trainingspläne zu erstellen
F2: Eigene Ernährungspläne erstellen
    Die App bietet eine Möglichkeit eigene Ernährungspläne zu erstellen
F3: Workouttracker
    Nutzer könnne ihre Workouts tracken, indem sie die Übungen, Datum und Länge erfassen
F4: Community
    Nutzer können sich in einem Forum mit anderen Nutzern austauschen
F5: Trainerprofil
    Das Feature ermöglich es Nutzern, in der App Personal Trainer zu kontaktieren. Dabei können sie aus einer Liste von Trainern auswählen und ihre persönlcihen Infomrationen/Erfahrungen vergleichen
```

## Schritt 4: Webapp starten
Da die Applikation keinen Hauptordner hat, kann man mit dem unteren Befehl die Webapp direkt starten:
```bash
$ python manage.py runserver
```

## Schritt 5: Manuelle E2E-Feature-Tests
```
Testing normaler User:
Schritt 1: Web App starten -> Registrieren
Schritt 2: Login

Schritt 3: Features testen
    3.1: Trainingspläne (Startpunkt: http://127.0.0.1:8000/)
        3.1.1: Auf Dashboard klicken
        3.1.2: Trainingsplan erstellen klicken
        3.1.3: Bezeichnung, Kategorie und mind. 2 Übungen eingeben
        3.1.4: Plan speichern
        3.1.5: Nach auto. Routing zurück zum Dashboard 
               -> Trainingsplan aufrufbar durch anwählen
               
    3.2: Ernährungspläne (Startpunkt: http://127.0.0.1:8000/)
        3.2.1: Auf Dashboard klicken
        3.2.2: Ernährungsplan erstellen klicken
        3.2.3: Mind. Bezeichnung, Mittagessen, Abendessen und Kalorien eingeben
        3.2.4: Plan speichern
        3.2.5: Nach auto. Routing zum Dashboard
               -> Ernährungsplan aufrufbar durch anwählen
               
    3.3: Workouttracker (Startpunkt: http://127.0.0.1:8000/)
        3.3.1: Auf Workout aufzeichnen klicken
        3.3.2: Datum eingeben (zeigt automatisch heutiges an), Kategorie eingeben, Dauer (hh:mm:ss)
               Erste Übung mit Übungsnamen, Anzahl Sätzen, Anzahl Wiederholungen, Gewicht eingeben
               Falls gewünscht weitere Übung mit dem +Übung hinzufügen Button anfügen und erneut ausfüllen
        3.3.3: Workout speichern
        3.3.4: Nach auto. Routing zurück zum Dashboard
               -> Auf Alle Workouts anzeigen klicken
                  Für Details auf das Workout klicken
                  
    3.4: Community (Startpunkt: http://127.0.0.1:8000/)
        3.4.1: auf Zu allen Beiträgen klicken
        3.4.2: auf Neuen Community-Beitrag erstellen klicken
        3.4.3: Titel und Inhalt eingeben
        3.4.4: Aritkel speichern
        3.4.5: Nach auto. Routing zum erstellten Artikel
               -> Kommentar hinzufügen
                  Autor und Text ausfüllen
                  Kommentar absenden klicken

Testing Admin-User:
Schritt 1: Web App starten -> Auf http://127.0.0.1:8000/adminregister/ (ist eine "secret URL")
Schritt 2: Username, Password, Password confirmation und Access Code "HWZ" eingeben
Schritt 3: Admin erstellen

Schritt 4: Login mit den erstellten Admin-Credentials
Schritt 5: Coach hinzufügen testen (Startpunkt http://127.0.0.1:8000/)
   5.1: auf Coach hinzufügen klicken
   5.2: Name, Trainingskategorie, Bio, Erfahrung in Jahren, Preis pro Stunde und E-Mail eingeben
   5.3: Coach erstellen klicken
   5.4: Nach auto. Routing zurück auf die Homepage
        -> Auf Hol dir einen Coach! klicken
           Der hinzugefügte Coach sollte zuunterst auftauchen und aufrufbar sein 
               
```

## Schritt 6: automatische Tests
```bash
$ python manage.py test
```
