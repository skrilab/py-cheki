# py-cheki

## Apraksts
Šis ir improvizēts mēģinājums kaut kā automatizēt pirkumu čeku iesniegšanu https://cekuloterija.lv/ portālā.
Uz doto brīdi risinājums balstās uz 'Google Lens' aplikāciju un primitīviem Python skriptu salikumiem, kuri nolasa datora 'clipboard' saturu un tajā ar 'regex' meklēšanas šabloniem mēģina atpazīt nepieciešamos datus un automātiski aizpildīt čeku iesniegumu loterijas portālā.


### Pilnvērtīga risinājuma lietošanai nepieciešams:
- Dators ar:
    - Uzstādītu Python 3.9.x un papildus moduļiem (skat. zemāk 'Python vides sagatavošana');
    - Google Chrome interneta pārlūku un tajā pierakstītu (signed-in) Google kontu;
- Android telefons ar Google kontu un uzstādītu 'Google Lens' aplikāciju (to var iegūt [šeit](https://play.google.com/store/apps/details?id=com.google.ar.lens));
    - Apple iekārtas nav pārbaudītas.


### Python vides sagatavošana
Aprakstīta Python un konkrētā risinājuma (ar requirements.txt) sagatavošana;
- papildus izmantotie Python moduļi;
- chromedriver
- u.c.


### Lietošana
- Palaiž 'main.py' Python skriptu (py .\main.py);
- Izmantojot Google Lens aplikāciju nofotografē izklātu pirkuma čeku;
- Google Lens aplikācijā izvēlas sadaļu 'Text' un 'Select all';
- Kad viss fotografētā čeka teksts ir iezīmēts, izvēlas 'Copy to computer';
- Norāda aktīvo datoru izvēloties 'Select';
    - Ja viss ir veiksmīgi, tad datorā jāparādās paziņojumam (notification) no Google Chrome pārlūka;
- Gaida Python skriptu izpildi un veiksmīga rezultāta gadījumā tiek automātiski aizpildīts čeka iesniegums https://cekuloterija.lv/ portālā;
    - Pirms čeka iesniegšanas ir iespēja salīdzināt datus un apstiprināt iesniegšanu vai atcelt to;
- Procesu var turpināt ar nākošo čeku vai izbeigt skripta izpildi nospiežot 'ctrl + c' kombināciju.