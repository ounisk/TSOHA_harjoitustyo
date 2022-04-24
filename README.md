## Välipalautus 3, 24.4.2022:
- Sovellus on testattavissa [Herokussa](https://tsoha-discussionapp.herokuapp.com/). Testitunnukset:
    - normikäyttäjä - tunnus: testaaja, salasana: testi123
    - ylläpitäjä - tunnus: administrator, salasana: salasana123
- Toiminnallisuudet ovat pitkälti ne, jotka projektikuvauksessa (alla) on kerrottu, huomioi:
    - ylläpitäjä lisää käyttäjän salaiselle alueelle käyttäjätunnuksen perusteella
    - ylläpitäjä oikeus poistaa aiheita on toteutettu, niin että aiheet jäävät tietokantaan (ks. kurssimateriaali, osa 2), mutta näiden piilotettujen (ts.poistettujen) aiheiden näkyvyys on rajoitettu vain adminille. Puntaroin myös vaihtoehtoa deletoida poistettu aihe kokonaan tietokannasta, mutta totesin, että voi olla halutumpaa säilyttää kuitenkin historia - tämä jättää mahdollisuuden lisätoiminnoille, esim. jos aihe haluttaisiin palauttaa näkyville joskus myöhemmin.
- Alkuviikkoina minulla oli hankaluuksia ja kömpelyyttä testauksen ja tuotantoon ajon kanssa, koska en ollut tietoinen flaskin dev-ympäristöstä. Vinkit flaskin dev-ympäristöön sain pajasta - ja se helpotti huomattavasti työn tekemistä.
- TODO:
    - ulkoasun viimeistely
    - koodin putsaus ylimääräisistä sotkuista ja kommenteista         



## Välipalautus 2, 3.4.2022:
- Sovellus on vasta aluillaan ja pahasti kesken - testausta ei juurikaan pysty tekemään. 
- Ensimmäisen 2 viikon aikana olen käynyt materiaalin läpi, käyttänyt aikaa PostgreSQL:n ja Herokun asentamiseen ja suunnitellut sovelluksen toteutusta. Viikolla 3 olen päässyt toteutuksen ja ohjelmoinnin pariin.
- Sovelluksen taulut, pohja ja toiminnallisuuksia on luotu - kaikki on Gitissä.
- Sovellus on [Herokussa](https://tsoha-discussionapp.herokuapp.com/). Testausta varten on luotu käyttäjä - käyttäjätunnus: testaaja, salasana: testi123, mutta sisäänkirjautuminen EI toimi (tulee "Bad request" virheilmoitus).
- Herokun tietokantaan olen INSERT-komennoilla luonut muutamia aiheita, jotta varmistun, että etusivu näyttää jokseenkin halutunlaiselta.
- TODO: 
    - toiminnallisuuksien kehittäminen edelleen mm.
        - sisäänkirjautuminen toimivaksi 
        - viestien kirjoitus ja toteutus niin, että ohjaantuvat oikeaan ketjuun ja aiheeseen
    - tietoturva seikkojen huomioiminen ja toteutus
    - ulkoasun hiominen



# Keskustelusovellus

### Projektin kuvaus: 
Sovelluksessa on keskusteluja eri aiheittain, yksi keskustelu muodostuu yhdestä tai useammasta viestistä. 
Käyttäjät kirjautuvat omilla käyttäjätunnuksillaan sovellukseen sisään. Sovelluksessa on ylläpitäjä sekä yksi tai useampia peruskäyttäjiä. Sovelluksen etusivulla on listattu aiheet sisältäen ketjujen, viestien määrän per aihe ja viimeisen viestin lähetysajankohta. 

**Toiminnot:**
  - Keskustelut:
    - Uusi keskustelu avataan luomalla sille otsikko ja kirjoittamalla aloitusviesti. 
    - Keskusteluun osallistutaan vastaamalla ketjuun. 
    - Käyttäjä, joka on luonut aiheketjun voi muokata sen otsikkoa tai lähettämänsä viestin sisältöä.
    - Lisäksi käyttäjä voi poistaa ketjun tai viestin. 
  - Haku: 
    - Viestejä voidaan hakea jollakin tietyllä hakusanalla.
  - Ylläpitäjällä on oikeus lisätä/poistaa keskusteluja.  
  - Lisäksi ylläpitäjä voi luoda salaisia keskustelualueita, joihin vain ylläpitäjän määrittelemillä käyttäjillä on pääsy.
