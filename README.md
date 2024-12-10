**Ohjelmistotekniikka**, _harjoitustyö_

Budget-buddy

Sovellus tulojen ja menojen kirjaamiseen.
Sovelluksessa on graafinen käyttöliittymä, josta voit lisätä kuluja. Valitsemalla rivin voit myös muokata tai poistaa erän. Tietokantaan voi alustaa dataa napilla populate database, ja sovellus näyttää tulojen ja menojen yhteenlasketun tilanteen. Tietokannan voi myös tyhjentää napilla Reset database. Voit myös ladata kulut CSV tiedostoon, tai ladata CSV tiedostosta kulut sovellukseen.

[Määrittely dokumentti](https://github.com/Lindrax/Ohte/tree/main/dokumentaatio/vaatimusmaarittely.md).

[tuntikirjanpito](https://github.com/Lindrax/Ohte/tree/main/dokumentaatio/tuntikirjanpito.md).

[changelog](https://github.com/Lindrax/Ohte/tree/main/dokumentaatio/changelog.md).

[arkkitehtuuri](https://github.com/Lindrax/Ohte/tree/main/dokumentaatio/arkkitehtuuri.md).

[Release](https://github.com/Lindrax/Ohte/releases/tag/viikko6).

[Käyttöohje](https://github.com/Lindrax/Ohte/blob/main/dokumentaatio/kayttoohje.md)


Sovelluksen käyttö:

1. Siirry hakemistoon budget-buddy ja asenna riippuvuudet komennolla poetry install.

2. alusta tietokanta komennolla poetry run invoke build

3. käynnistä komennolla poetry run invoke start

Muuta:

- Testikattavuuden voi selvittää komennolla poetry run invoke coverage-report
- testit voi suorittaa komennolla poetry run invoke test
- kirjoitusasun voi tarkistaa poetry run invoke lint
- automaattiset korjaukset voi tehdä poetry run invoke format
