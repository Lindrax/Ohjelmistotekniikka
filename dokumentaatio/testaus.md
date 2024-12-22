# Testausdokumentti

Ohjelmaa on testattu manuaalisesti sekä yksikkö testeillä

## Yksikkö- ja integraatiotestaus

### Sovelluslogiikka

Sovelluslogiikasta vastaavaa `BudgetManager`-luokkaa testataan `TestBudgetManager`-testiluokalla. `BudgetManager`-olio alustetaan hyödyntämällä SQLite-tietokantaa, joka toimii testien aikana muistissa (`:memory:`). Tietokannan alustus tapahtuu `DatabaseManager`-luokan avulla.

Testiluokka käyttää riippuvuuksina `BudgetRepository`-ja `DatabaseManager`-luokkia. Näin testataan sovelluslogiikan ja tietokantatoimintojen välistä yhteistyötä.

Testattuja toiminnallisuuksia ovat mm.:

- Merkintöjen lisääminen, muokkaaminen, poistaminen ja hakeminen.
- Kokonaismäärän laskeminen.
- CSV-tiedostojen tuonti ja vienti.

### Repositorio-luokat

`BudgetRepository`-luokan toiminnallisuuksia testataan osana `BudgetManager`-luokan testejä.

### Testauskattavuus

Sovelluksen haaraumakattavuus on 91%.

Testit kattavat:

- Sovelluslogiikan perustoiminnallisuudet.
- Tietokannan ja CSV-tiedostojen väliset toiminnot.

## Järjestelmätestaus

Sovelluksen järjestelmätestaus on suoritettu manuaalisesti.

### Asennus ja konfigurointi

Sovellus on asennettu ja testattu kehitysympäristössä sekä muistissa toimivalla SQLite-tietokannalla. Testeissä on tarkistettu, että tietokanta alustuu oikein ja että ohjelma toimii ilman ulkoisia tiedostoja.

Lisäksi CSV-toiminnot on testattu luomalla ja tuomalla esimerkkitiedostoja. Vastaavasti virheellisiä tiedostomuotoja on käsitelty odotetusti.

### Toiminnallisuudet

Kaikki sovelluksen toiminnallisuudet on pyritty testaamaan

- Merkintöjen käsittely (lisäys, poisto, muokkaus).
- CSV-tiedostojen tuonti ja vienti.
- Kokonaismäärän laskeminen.

Virheellisiä syötteitä, kuten tyhjiä arvoja tai virheellisiä datatyyppejä on kokeiltu.

## Sovellukseen jääneet laatuongelmat

Sovellus ei tällä hetkellä anna selkeitä virheilmoituksia seuraavissa tilanteissa:

- Tietokantayhteyttä ei voida muodostaa (esim. tiedosto-oikeudet puuttuvat).
- CSV-tiedostojen käsittelyssä esiintyy tuntemattomia virheitä.
