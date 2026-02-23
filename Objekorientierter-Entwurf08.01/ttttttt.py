@startuml
actor Benutzer
 
participant GUI
participant Lagerverwaltung
participant Lagerplatz
participant Roboter
 
Benutzer -> GUI : Button „Einlagern“ drücken
GUI -> Lagerverwaltung : einlagern(pArtikelname, pStueckzahl)
 
activate Lagerverwaltung
 
Lagerverwaltung -> Lagerverwaltung : findeLagerplatz(pArtikelname)
 
loop Für alle Lagerplätze (Suche Artikel)
    Lagerverwaltung -> Lagerplatz : gibArtikelname()
    Lagerplatz --> Lagerverwaltung : name
end
 
alt Artikel bereits vorhanden
    Lagerverwaltung -> GUI : melden("Lagerplatz X gefunden")
else Artikel nicht gefunden
    loop Für alle Lagerplätze (Suche freien Platz)
        Lagerverwaltung -> Lagerplatz : istFrei()
        Lagerplatz --> Lagerverwaltung : bool
    end
 
    alt Freier Platz gefunden
        Lagerverwaltung -> GUI : melden("Ware wird eingelagert")
    else Kein Platz frei
        Lagerverwaltung -> GUI : melden("Lager voll, einlagern nicht möglich")
        deactivate Lagerverwaltung
        return
    end
end
 
Lagerverwaltung -> Roboter : einlagern(pLagerplatz)
Roboter --> Lagerverwaltung : bool
 
alt Einlagern erfolgreich
    Lagerverwaltung -> Lagerplatz : einlagern(pArtikelname, pStueckzahl)
    Lagerverwaltung -> GUI : updateGui()
else Fehler
    Lagerverwaltung -> GUI : melden("Fehler beim Einlagern")
end
 
deactivate Lagerverwaltung
@enduml