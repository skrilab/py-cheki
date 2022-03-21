import clipboard
import re
from lib2to3.pgen2 import driver
from xml.dom.minidom import Element
from selenium import webdriver
import time
import os.path
import ctypes
import mani_dati

class MbConstants:
    MB_OKCANCEL = 1
    IDCANCEL = 2
    IDOK = 1

PATH = "C:\chromedriver_win32\chromedriver.exe"


# Definejam zinamo veikalu PVN reg. NR. (pec siem tiek noteikts ceka paraugs);
paraugs_2 = ["40003642393","40003723815"]   # 2. paraugs | Mego veikals, Apotheka aptieka
paraugs_3 = ["40003242733","40003520643"]   # 3. paraugs | Virši-A DUS, Maxima veikals
paraugs_8 = ["55403012521"]   # 8. paraugs | Meness aptieka

#virsiDus = "40003242733"        # 3. paraugs | Virši-A DUS
#megoVeikals = "40003642393"     # 2. paraugs | Mego veikals
menessAptieka = "55403012521"   # 8. paraugs | Meness aptieka
maximaVeikals = "40003520643"   # 3. paraugs | Maxima veikals
#apotheka_aptieka = "40003723815" # 2. paraugs | Apotheka aptieka


# Fukncija lai izveidotu jaunu pagaidu clipboard datu uzglabasanas failu talakai datu apstradei;
def write_tempfile():
    dati = clipboard.paste()
    cwd = os.getcwd()
    timestr = time.strftime("%d%m%Y-%H%M%S")
    global targetFile
    targetFile = os.path.join(cwd, timestr + ".txt")
    temp_file = open(targetFile, "w", encoding="utf-8")
    
#    temp_line = dati.replace("\r", "!")
    temp_line = dati.replace("\n", " ")
#    temp_line = temp_line.replace("  ", " ")
    temp_file.write(temp_line)
    temp_file.close()
  
#    no_lbreaks = ""
#    for line in temp_line:
#        strip_line = line.rstrip("\r\n")
#        no_lbreaks += strip_line
#    temp_file.write(no_lbreaks.replace("!!", " "))
#    temp_file.close()


# Funkcija pagaidu datu faila dzesanai
def del_tempfile():
    os.remove(targetFile)


# Funkcija lai izgutu nepieciesamos datus no clipboard satura;
def get_data():
    #Definejam clipboard saturu;    
#    data = clipboard.paste()
    data = open(targetFile, "r", encoding="utf-8")
    data = str(data.read())
    
    global veikals_PVN
    global veikals_KASE
    global veikals_CEKS
    global veikals_SUMMA
    global veikals_DATUMS
    global veikals_Orig_DATUMS

    # Clipboad datos samekle PVN numuru. Pagaidam caur error handling funkciju;
    try:
        veikals_PVN = re.findall(r"(4000\d\d\d\d\d\d\d)", data)[0] # Visi ar LV4000 kodiem
    except:
        veikals_PVN = re.findall(r"LV(55\d\d\d\d\d\d\d\d\d)", data)[0] # ar LV55xxx kodiem, piem. Meness aptieka
    print(veikals_PVN)


    # Nosaka ceka paraugu un izgust vajadzigos datus;
### paraugs_3
    # Virsi...
#    if veikals_PVN == virsiDus:
#        print("Found Virši-A DUS!")
    if veikals_PVN in paraugs_3:
        print("Noteikts 2. parauga čeks")

        virsiDus_kase = re.findall(r"Nr.(\d.R\d+)", data)[0]
        print(virsiDus_kase)
        veikals_KASE = virsiDus_kase
    
        virsiDus_ceks = re.findall(r"eks.(\d./\d+)", data)[0]
        print(virsiDus_ceks)
        veikals_CEKS = virsiDus_ceks

        virsiDus_summa = re.findall(r"(\d+,\d+).EUR", data)[0]
        print(virsiDus_summa)    
        veikals_SUMMA = virsiDus_summa

        virsiDus_datums = re.findall(r"(\d\d.\d\d.\d\d\d\d).\d.:\d.:\d.", data)[0]
        #print(virsiDus_datums)
        veikals_Orig_DATUMS = virsiDus_datums
        if virsiDus_datums[0] == "0":
            virsiDus_datums = virsiDus_datums.replace('0', '')[0]
            print(virsiDus_datums)
        veikals_DATUMS = virsiDus_datums

### paraugs_2
    elif veikals_PVN in paraugs_2:
        print("Noteikts 2. parauga čeks")
        
        kases_nr = re.search(r"(?<=numurs: )SP-LV\d+|(?<=numurs: )AI\d+|Al\d+", data)[0]
        print(kases_nr)
#        megoVeikals_kase = re.findall(r"numurs: (SP-LV\d+)", data)[0]
        if kases_nr.startswith("Al") == True:
            kases_nr = kases_nr.replace("Al", "AI")
#            print(kases_nr)
        veikals_KASE = kases_nr

        ceka_nr = re.findall(r"Dok. Nr.: (\d+/\d+)", data)[0] 
        print(ceka_nr)
        veikals_CEKS = ceka_nr

        ceka_summa = re.findall(r"Samaksai EUR  (\d+,\d+)", data)[0]
        print(ceka_summa)    
        veikals_SUMMA = ceka_summa

        ceka_datums = re.findall(r"(\d+-\d+-\d+).\d.:\d.:\d.", data)[0]
        # veikals_Orig_DATUMS ir log vajadzibam
        veikals_Orig_DATUMS = ceka_datums
        if ceka_datums[8] == "0":
            ceka_datums = ceka_datums.replace('0', '')[6]
            print(ceka_datums)
            veikals_DATUMS = ceka_datums
        else:
            ceka_datums = ceka_datums[8:]
            print(ceka_datums)
            veikals_DATUMS = ceka_datums


    # Maxima...
    elif veikals_PVN == maximaVeikals:
        print("Found Maxima veikals!")
    
        maximaVeikals_kase = re.findall(r"Nr.(\d.R\d+)", data)[0]
        print(maximaVeikals_kase)
        veikals_KASE = maximaVeikals_kase
    
        maximaVeikals_ceks = re.findall(r"eks.(\d./\d+)", data)[0]
        print(maximaVeikals_ceks)
        veikals_CEKS = maximaVeikals_ceks

        maximaVeikals_summa = re.findall(r"(\d+,\d+).EUR", data)[0]
        print(maximaVeikals_summa)    
        veikals_SUMMA = maximaVeikals_summa

        maximaVeikals_datums = re.findall(r"(\d+-\d+-\d+).\d.:\d.:\d.", data)[0]
        veikals_Orig_DATUMS = maximaVeikals_datums
        if maximaVeikals_datums[8] == "0":
            maximaVeikals_datums = maximaVeikals_datums.replace('0', '')[6]
            print(maximaVeikals_datums)
            veikals_DATUMS = maximaVeikals_datums
        else:
            maximaVeikals_datums = maximaVeikals_datums[8:]
            print(maximaVeikals_datums)
            veikals_DATUMS = maximaVeikals_datums

    # Meness aptieka...
    if veikals_PVN == menessAptieka:
        print("Found Mēness aptieka!")
    
        menessAptieka_kase = re.findall(r"[SAS. NR:\n+](75000\d\d\d)", data)[0]
        print(menessAptieka_kase)
        veikals_KASE = menessAptieka_kase
    
        menessAptieka_ceks = re.findall(r"DOK.+NR: (\d+)", data)[0]
        print(menessAptieka_ceks)
        veikals_CEKS = menessAptieka_ceks

        menessAptieka_summa = re.findall(r"[KOPA\n+](\d+,\d+).EUR", data)[0]
        print(menessAptieka_summa)    
        veikals_SUMMA = menessAptieka_summa

        menessAptieka_datums = re.findall(r"(\d+-\d+-\d+).\d.:\d.", data)[0]
        veikals_Orig_DATUMS = menessAptieka_datums
        if menessAptieka_datums[8] == "0":
            menessAptieka_datums = menessAptieka_datums.replace('0', '')[6]
            print(menessAptieka_datums)
            veikals_DATUMS = menessAptieka_datums
        else:
            menessAptieka_datums = menessAptieka_datums[8:]
            print(menessAptieka_datums)
            veikals_DATUMS = menessAptieka_datums


# Fukncija lai izveidotu jaunu log failu un ierakstitu izguto datu (caur regex) saturu;
def write_logfile():
    cwd = os.getcwd()
    timestr = time.strftime("%d%m%Y-%H%M%S")
    targetPath = os.path.join(cwd + '\logs')
    targetFile = os.path.join(targetPath, timestr + ".txt")
    f = open(targetFile, "w", encoding="utf-8")
    f.write(veikals_PVN + '\n')
    f.write(veikals_KASE + '\n')
    f.write(veikals_CEKS + '\n')
    f.write(veikals_SUMMA + '\n')
    f.write(veikals_DATUMS + '\n')
    f.write(veikals_Orig_DATUMS + '\n')
    f.close()


# Funkcija lai uzraditu pop-up logu datu salidzinasanai un iesniegsanai vai atsauksanai;
def message_window(message, title):
    return ctypes.windll.user32.MessageBoxW(0,message, title, MbConstants.MB_OKCANCEL)


# Funkcija lai automatiski aizpilditu formu ar iegutajiem datiem;
def fill_form():
    driver = webdriver.Chrome(PATH)
    driver.get('https://cekuloterija.lv/')
    #print(driver.title)
    time.sleep(0.5)

    # akceptejam Cookies;
    #btn_cookie = driver.find_element_by_xpath('//*[@id="app"]/div/div[5]/button')
    #btn_cookie = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[5]/button')
    btn_cookie = driver.find_element_by_css_selector('button.sc-hgRTRy.kHOOdZ')
    btn_cookie.click()
    time.sleep(0.5)

    # izvelamies iesniegt ceku;
    btn_inCeks = driver.find_element_by_css_selector('button.sc-bdVaJa')
    btn_inCeks.click()
    time.sleep(1)

    # ievadam PVN nr.;
    input_PVN = driver.find_element_by_name('taxpayer_number')
    input_PVN.send_keys(veikals_PVN)
    time.sleep(0.8)

    # ievadam kases aparata nr.;
    input_KASE = driver.find_element_by_name('cash_register_number')
    input_KASE.send_keys(veikals_KASE)
    time.sleep(0.8)

    # ievadam ceka nr.;
    input_CEKS = driver.find_element_by_name('number')
    input_CEKS.send_keys(veikals_CEKS)
    time.sleep(0.8)

    # ievadam ceka summu;
    input_SUM = driver.find_element_by_name('amount')
    input_SUM.send_keys(veikals_SUMMA)
    time.sleep(0.8)

    # izvelamies kalendaru un ievadam ceka datumu;
    btn_CAL = driver.find_element_by_xpath('//*[@id="modal"]/div/div/div[2]/div[1]/div[7]/div')
    btn_CAL.click()
    time.sleep(0.5)

    for elem in driver.find_elements_by_xpath("//span[@class = 'MuiIconButton-label']"):
        print(elem.text)
        #if elem.text == '1':
        if elem.text == veikals_DATUMS:
            elem.click()
            break
    time.sleep(1)

    # ievadam tel. nr.;
    input_TEL = driver.find_element_by_name('phone')
    input_TEL.send_keys(mani_dati.telefons)
    user_input = message_window(veikals_KASE + '\n' + veikals_CEKS + '\n' + veikals_SUMMA + '\n' + veikals_Orig_DATUMS + '\n',"Datu salīdzināšana")
    if  user_input == MbConstants.IDOK:
        print("ok pressed")
# iesniedzam formu;
        btn_FIN = driver.find_element_by_xpath('//*[@id="modal"]/div/div/div[2]/div[1]/button')
        btn_FIN.click()
        time.sleep(1)    
# izvelamies e-pasta apstiprinajumu par dalibu;
        btn_MAIL = driver.find_element_by_xpath('//*[@id="modal"]/div/div/div[4]/div[2]/button[2]')
        btn_MAIL.click()
        time.sleep(0.5)
# aizpildam e-pasta formu;
        input_MAIL = driver.find_element_by_name('email')
        input_MAIL.send_keys(mani_dati.epasts)
        time.sleep(1)
        btn_SENDMAIL = driver.find_element_by_xpath('//*[@id="modal"]/div/div/div[4]/div[2]/div/div/button')
        btn_SENDMAIL.click()
        time.sleep(5)    
        driver.quit()
    elif user_input == MbConstants.IDCANCEL:
        print("cancel presssed")
        driver.quit()