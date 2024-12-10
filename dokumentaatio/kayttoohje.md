# Käyttöohje

Lataa projektin viimeisin lähdekoodi [täältä](https://github.com/Lindrax/Ohte/releases).

## Ohjelman käynnistäminen

1. Asenna riippuvuudet:

```bash
poetry install
```

2. Alusta tietokanta:

```bash
poetry run invoke build
```

3. käynnistä:

```
poetry run invoke start
```

## Käyttö

Voit tyhjentää, tai täyttää tietokannan komennoilla Reset Database ja Populate Database.

Täyttämällä kentät ja painamalla Add Entry voit lisätä kuluja

Valitsemalla kulun, voit muokata sitä muokkaamalla kenttiä ja painamalla Modify Entry. Tai poistaa sen painamalla Delete Entry.

Voit ladata tallennetut kulut CSV tiedostoon napista Export to CSV.

Voit ladata valmiista CSV tiedostosta kulut tietokantaan valitsemalla Import from CSV

Klikkaamalla Exit poistut sovelluksesta
