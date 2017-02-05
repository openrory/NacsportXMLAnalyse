-- ALGEMEEN --
auteur: Rory Sie
datum: 18 juli 2016
versie: 0.1

-- INLEIDING --
Deze applicatie maakt een automatische analyse van het XML-bestand zoals dat door Nacsport wordt gegenereerd.

-- REQUIREMENTS --
Om deze applicatie te starten dient u aan de volgende requirements te voldoen:

- Python 3.5
- xmltodict >= 0.10.2
- matplotlib == 1.5.3
- bokeh == 0.12.4
- pandas >= 0.19.2



-- STARTEN --
U roept het bestand aan op de volgende manier: python3 xml_analyse.py "<pad+bestandsnaam>" "-<type bestand>"}
Bij <type bestand> kunt u -t aangeven voor "team" en -i voor "individueel"
