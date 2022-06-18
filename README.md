# py-cheki

## Apraksts
Šis ir improvizēts mēģinājums kaut kā automatizēt pirkumu čeku iesniegšanu https://cekuloterija.lv/ portālā.
Uz doto brīdi risinājums balstās uz 'Google Lens' aplikāciju un primitīviem Python skriptu salikumiem, kuri nolasa datora 'clipboard' saturu un tajā ar 'regex' meklēšanas šabloniem mēģina atpazīt nepieciešamos datus un automātiski aizpildīt čeku iesniegumu loterijas portālā.

Ņemot vērā, ka pirkumu čeku veidi ir dažādi un katra čeka atpazīšanai sākotnēji ir nepieciešams paliels manuāls darbs, tad uz doto brīdi risinājums spēj atrast nepieciešamos datus tikai zemāk uzrādīto uzņēmumu čekos:
 - Virši-A DUS
 - Mego veikals
 - Mēness aptieka
 - Apotheka aptieka
 - RIMI
 - Pepco Latvia
 - Apranga
 - Sportland

### Pilnvērtīga risinājuma lietošanai nepieciešams:
- Dators ar:
    - Uzstādītu 'Python 3.9.x' (vai jaunāku) un papildus moduļiem (skat. zemāk 'Python vides sagatavošana');
    - Lejupielādētu 'GeckoDriver' web aplikāciju testēšanas rīku/serveri (to var iegūt [šeit](https://github.com/mozilla/geckodriver/releases));
        - 'geckodriver.exe' izpildāmais fails jānovieto 'C:\webdriver\\' mapē (nekāda instalācija nav nepieciešama);
    - Mozilla Firefox interneta pārlūku;
    - Google Chrome interneta pārlūku un tajā pierakstītu (signed-in) Google kontu;
- Android telefons ar Google kontu un uzstādītu 'Google Lens' aplikāciju (to var iegūt [šeit](https://play.google.com/store/apps/details?id=com.google.ar.lens));
    - Apple iekārtas nav pārbaudītas.


### Python vides sagatavošana
Zemāk ir aprakstīta Python un konkrētā risinājuma sagatavošana:
1. Izveido jaunu mapi: `mkdir "py-cheki" && cd "py-cheki"`    
2. Izveido jaunu Python virtuālo vidi: `python3 -m venv`
3. Noklonē Git repozitoriju: `git clone "https://github.com/skrilab/py-cheki.git"`
4. Uzstāda nepieciešamos Python moduļus: `pip install -r requirements.txt`


### Lietošana
1. Atver 'Google Chrome' interneta pārlūku ar pierakstītu (signed-in) Google kontu;
2. No komandrindas palaiž 'main.py' Python skriptu: `py .\main.py`
3. Izmantojot 'Google Lens' aplikāciju nofotografē izklātu pirkuma čeku;
4. 'Google Lens' aplikācijā izvēlas sadaļu 'Text' un 'Select all';
5. Kad viss fotografētā čeka teksts ir iezīmēts, izvēlas 'Copy to computer';
6. Norāda aktīvo datoru izvēloties 'Select';
    - Ja viss ir veiksmīgi, tad datorā jāparādās paziņojumam (notification) no Chrome interneta pārlūka;
7. Gaida Python skriptu izpildi un veiksmīga rezultāta gadījumā Firefox interneta pārlūkā tiek automātiski aizpildīts čeka iesniegums https://cekuloterija.lv/ portālā;
    - Pirms čeka iesniegšanas ir iespēja salīdzināt datus un apstiprināt iesniegšanu vai atcelt to;
8. Procesu var turpināt ar nākošo čeku vai apturēt skripta izpildi nospiežot 'ctrl + c' kombināciju.