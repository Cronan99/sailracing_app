How to setup Sailracing app

python run.py to initialize the app and set up the db.

once initialized register a user to later set as admin and then shut down the server.

to set the users admin privileges, do the following:

type in terminal

flask shell
user = User.query.filter_by(username="your_admin_username").first()
user.admin = True
db.session.commit()
exit()


Now you can start the app again and use the created admin with its features.


Programmmet körs via webbläsaren.

Idéen var att skapa en app för att på en enkelt sätt spara och framta kappseglingsresultat.

Appen innehåller en inloggningsfunktion, för att kunna skapa båtobjekt krävs
att en användare är inloggad, för att skapa tävlingsobjekt krävs att en användare
med "admin" är inloggad.

Se ER-Diagram för databasstruktur.

Förtydligande båttermer:
SRS - är ett handikapptal för att omräkna tävlingstider
och det finns fler beroende på båt och utrustning

Segelnummer - är som ett regnummer för att kunna identifiera båtar på avstånd

För att bäst använda appen så skapar man först ett konto som man sätter till admin.
därefter skapar man minst två till konton som båda får skapa varsin båt.

till sist loggar man in som admin och skapar ett race. när väl racet är klart kan man
se resultat från startsidan.


Moment:

A. Säker programmering.
Jag använder mig av ett inloggsystem för att varje användare ska kunna
skapa och ta bort sina egna båtobject samt för speciell inlogg för admin som
i sin tur skapar och tar bort tävlingsobjekt. Varje konto sparas i databasen och deras
lösenord sparas i form av ett hash för ökad säkerhet.

C. API-integrationer.
Jag använder mig utav Requests för att både hämta data från nätet samt för att
kommunicera med den egna hemsidan och hämta hem användar input osv

D. Webbutveckling.
Hela appen drivs i grunden utav Flask där jag satt upp både själva appen men även databasen
kopplat med hjälp av SQLAlchemy. Jag har följt samma upplägg som vi lärt oss med en
mapp för templates där jag skrivit html, models för db, routes för att välja sida och
utils för specifika funktioner.

E. Automatisering.
Jag har skapat en modul som heter srs_scrape.py som automatiskt hämtar hem data
från nätet och sparar den till databasen för att sedan användas i appen.

F. Enhetstestning.
Alla testningsfiler slutar med _test.py för att enkelt kunna skriva pytest eller
pytest -v i terminalen för att alla tester ska köras. srs_scrape_test ligger vid srs_scrape
filen medans restrerande ligger i tets mappen i app mappen.

H. SQL med Python.
Alla objekt och all data som sparas i appen sparas och hämtas från en SQL-lite database
som ligger under instance/sailracing.db.