
# Keskustelusovellus

### Projektin kuvaus: 
Sovelluksessa on keskusteluja eri aiheittain, yksi keskustelu muodostuu yhdestä tai useammasta viestistä. 
Käyttäjät kirjautuvat omilla käyttäjätunnuksillaan sovellukseen sisään. Sovelluksessa on ylläpitäjä sekä yksi tai useampia peruskäyttäjiä. Sovelluksen etusivulla on listattu aiheet sisältäen ketjujen sekä viestien määrän per aihe ja viimeisen viestin lähetysajankohta. 

Sovellus on testattavissa [Herokussa](https://tsoha-discussionapp.herokuapp.com/). Testitunnukset:
- normikäyttäjä - tunnus: testaaja, salasana: testi123
- ylläpitäjä - tunnus: administrator, salasana: salasana123
    
    
### Toiminnot:
  - Keskustelut:
    - Aiheet ovat valmiina sovelluksessa ja lisäksi ylläpitäjä voi luoda uusia aiheita. 
    - Uusi keskustelu (liittyen tiettyyn aiheeseen) avataan luomalla sille otsikko ja kirjoittamalla aloitusviesti, vain sisäänkirjautunut käyttäjä voi luoda keskustelun. 
    - Keskusteluun osallistutaan vastaamalla ketjuun (pitää olla sisäänkirjautunut).
    - Käyttäjä, joka on luonut aiheketjun voi muokata sen otsikkoa tai lähettämänsä viestin sisältöä.
    - Lisäksi käyttäjä voi poistaa luomansa ketjun tai viestin. 
  - Haku: 
    - Viestejä voidaan hakea jollakin tietyllä hakusanalla.
  - Ylläpitäjällä on oikeus lisätä/poistaa keskusteluja sekä muokata/poistaa viestejä. 
  - Ylläpitäjällä on oikeus poistaa aiheita - aiheet piilotetaan peruskäyttäjiltä ja jäävät vain ylläpitäjän nähtäviksi.  
  - Lisäksi ylläpitäjä voi luoda salaisia keskustelualueita, joihin vain ylläpitäjän määrittelemillä käyttäjillä on pääsy. Ylläpitäjä voi lisätä käyttäjiä salaisille alueille käyttäjätunnuksen perusteella.

