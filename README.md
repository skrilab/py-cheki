# py-cheki

## Apraksts
Šis ir improvizēts mēģinājums kaut kā automatizēt pirkumu čeku iesniegšanu https://cekuloterija.lv/ portālā.
Uz doto brīdi risinājums balstās uz 'Google Lens' aplikāciju un primitīviem Python skriptu salikumiem, kuri nolasa datora 'clipboard' saturu un tajā ar 'regex' meklēšanas šabloniem mēģina atpazīt nepieciešamos datus un automātiski aizpildīt čeku iesniegumu loterijas portālā.

Ņemot vērā, ka pirkumu čeku veidi ir dažādi un katra čeka atpazīšanai sākotnēji ir nepieciešams paliels manuāls darbs, tad uz doto brīdi risinājums spēj atrast nepieciešamos datus tikai zemāk uzrādīto uzņēmumu čekos:
 - Virši-A DUS
 - Mego veikals
 - Mēness aptieka
 - Apotheka aptieka

### Pilnvērtīga risinājuma lietošanai nepieciešams:
- Dators ar:
    - Uzstādītu 'Python 3.9.x' (vai jaunāku) un papildus moduļiem (skat. zemāk 'Python vides sagatavošana');
    - Lejupielādētu 'GeckoDriver' web aplikāciju testēšanas rīku/serveri (to var iegūt [šeit](https://github.com/mozilla/geckodriver/releases));
        - 'geckodriver.exe' izpildāmais fails jānovieto 'C:\webdriver\\' mapē (nekāda instalācija nav nepieciešama);
    - Mozilla Firefox interneta pārlūku un tajā pierakstītu (signed-in) Google kontu;
- Android telefons ar Google kontu un uzstādītu 'Google Lens' aplikāciju (to var iegūt [šeit](https://play.google.com/store/apps/details?id=com.google.ar.lens));
    - Apple iekārtas nav pārbaudītas.


### Python vides sagatavošana
Zemāk ir aprakstīta Python un konkrētā risinājuma sagatavošana;
- Izveido jaunu mapi: `mkdir "py-cheki" && cd "py-cheki"`    
- Izveido jaunu Python virtuālo vidi: `python3 -m venv`
- Noklonē Git repozitoriju: `git clone "https://github.com/skrilab/py-cheki.git"`
- Uzstāda nepieciešamos Python moduļus: `pip install -r requirements.txt`


### Lietošana
- Atver 'Mozilla Firefox' interneta pārlūku;
- No komandrindas palaiž 'main.py' Python skriptu: `py .\main.py`
- Izmantojot 'Google Lens' aplikāciju nofotografē izklātu pirkuma čeku;
- 'Google Lens' aplikācijā izvēlas sadaļu 'Text' un 'Select all';
- Kad viss fotografētā čeka teksts ir iezīmēts, izvēlas 'Copy to computer';
- Norāda aktīvo datoru izvēloties 'Select';
    - Ja viss ir veiksmīgi, tad datorā jāparādās paziņojumam (notification) no interneta pārlūka;
- Gaida Python skriptu izpildi un veiksmīga rezultāta gadījumā tiek automātiski aizpildīts čeka iesniegums https://cekuloterija.lv/ portālā;
    - Pirms čeka iesniegšanas ir iespēja salīdzināt datus un apstiprināt iesniegšanu vai atcelt to;
- Procesu var turpināt ar nākošo čeku vai apturēt skripta izpildi nospiežot 'ctrl + c' kombināciju.