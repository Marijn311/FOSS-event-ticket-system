# EventTiks
Deze file bevat een toelichting bij het ticketsysteem uit deze map. 

Dit mapje "EventTiks" bevat alles wat je nodig hebt om alle deelnemers van een activiteit automatisch een mail te sturen met een unieke toegangscode. Ook is er een script wat de codes kan verifiëren aan de deur. Verder is er een ondersteunende pyhton file die makkelijk via python sql commandos naar de database kan sturen om zo de database "handmatig" aan te passen als dat nodig zou zijn.
Ook hebt ik in de scipts super veel comments gezet zodat het hopelijk goed te volgen is voor mensen die minder van programmeren afweten dan ik.

Dit systeem zorgt ervoor dat het niet meer nodig is om (visite)kaartjes te kopen. Dit is duurzamer en bespaart meer dan 100 euro per jaar voor de feestcommissie. Verder kan dit systeem ook gebruikt worden voor andere Prot activiteiten. Dan hoeft er niet meer aangekloot te worden met afgedrukte inschrijflijsten.

Dit systeem is bedacht en gecodeerd door mij (Marijn Borghouts) met dank aan TechNIEK voor het helpen opzetten en begrijpen van de database infrastructuur. Dit systeem is begonnen als een simpel idee maar uiteindelijk uitgegroeid tot een best serieus hobby project. Als er dingen niet duidelijk zijn of je hebt na dit bestand nog steeds vragen dan kun je me altijd mailen op m.m.borghouts@student.tue.nl 

Zorg er voor dat je dit systeem een keer goed opzet en test voordat iedereen dronken op een feest staat want anders wordt het echt een drama. In het begin lijkt dit systeem misschien te technisch maar als je de setup één keer hebt gedaan, en er een keer mee hebt gewerkt is alles super simpel. Iedereen met een minimale basis kennis van python zou dit systeem moeten kunnen gebruiken en begrijpen.


Tickets genereren:
1.	Het eerste wat je moet doen is een Gmailadres vinden of aanmaken waarmee je de mails wilt verzenden. Om te zorgen dat dit python script in je Gmail kan inloggen en mails kan sturen moet je wat aanpassen in de instellingen van het Gmail account. Je moet “toegang door minder goed beveiligde apps” toestaan. (Helaas gaat Google dit op 30 mei 2022 veranderen, dus dan moet er voortaan een extra beveiligingsstap met een 16 cijferige code gebeuren. Maar dat zie ik tegen die tijd wel.) 
2.	Als je "verzender-Gmail" gereed is moet je vervolgens de inschrijvingslijst van een activiteit van de site downloaden als Excel bestand. Dit bestand moet je in het mapje “EventTiks” zetten en je moet hem hernoemen naar "participants". De eerste rij van elke kolom moet aangeven wat er in de kolom staat (vgm is dit standaard al zo bij Prot.)
3.	Vervolgens open je het "sending_tickets" script op je laptop met een editor zoals Spyder of VSCode. Je moet een aantal dingen in dit script aanpassen als je mails wilt zenden.
	-Op line X vul je de locatie (de folder op je latop) in waar de deelnemerslijst staat opgeslagen.
	-Op line Y vul je in wat de sender-email is, dit is het Gmailadres wat de tickets gaat verzenden. 
	-Op line Z vul je de et onderwerp en de inhoud van de mail in.
4.	Zorg dat de database online is en dat je goed verbonden bent, als je kiest om een nieuwe database te maken.
5.	Als je het script nu runt kan het zijn dat je nog wat packages moet instaleren als je die in je conda environment mist. (Een nieuwe environment aanmaken is geen slecht idee)
6.	Als het script runt zonder errors dan vraagt hij om een wachtwoord. Dit is het wachtwoord wat bij het Gmail account hoort van de sender-Gmail. Zodra je een goed wachtwoord intypt worden alle mails meteen verzonden! 




Tickets Checken:
Voor het verifiëren van de tickets kun je het "run_website_for_checking_tickets" script runnen op je laptop of nog beter op een kleine computer die altijd aan kan staan zoals een Raspberry Pi aan de stroom ergens in een kastje met slot. Als je het script runt, dan host de computer die dat doet de website. Op deze website kunnen mensen aan de deur inloggen met een door mij bepaalde gebruikersnaam en wachtwoord. Eenmaal ingelogt kunnen ze de ticket codes invullen om te verifiëren of ze geldig zijn.  

1. Het script runt al het goed is meteen. Je hoeft alleen te zprgen dat de database verbinding goed gaat door te checken of die gegevens nog kloppen.
2. Het script output een IP-adress waarop de website runt. Echter willen we graag dat de webserver (de Raspberry Pi) bereikbaar is vanaf een andere locatie (de deur van InVivo of van de Villa). Daarom hebben we het externe IP adress nodig van de Pi en het bijbehoorende port-nummer. IP-adressen kun je bekijken door "ipconfig in je terminal te typen". Om deze statisch te maken (wat je wil) of om de port-nummer aan te passen heb je toegang tot de modem nodig. Dit is niet mogelijk op de uni, tenzij de Intern van het bestuur dat weet te fixen. Maar ik vrees dat de Pi dus bij iemand thuis zal moeten staan.

Voor het beheren van de raspberry-Pi (gelieve niet aan te komen tenzij je weet wat je doet):
Dit werkt sws alleen vanaf mijn wifi in Woensel.
1. inloggen met "  ssh pi@192.168.2.120  " en het wachtwoord is: raspberry
2. cd EventTiks/
3. python run_website_for_checking_tickets.py
4. ctrl+z
5. bg
6. disown

met sudo reboot kan je heel de boel afsluiten en daarna dus weer opnieuw opstarten zoals hierboven.

