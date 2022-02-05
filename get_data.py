import clipboard
#import linecache
import re
from lib2to3.pgen2 import driver
from xml.dom.minidom import Element
from selenium import webdriver
import time
import os.path

PATH = "C:\chromedriver_win32\chromedriver.exe"


# Izveidot jaunu failu (parrasktit esosu) un ierakstit clipboard saturu;
#f = open("outfile-temp.txt", "w", encoding="utf-8")
#f.write(data)
#f.close()


# Definejam zinamo veikalu PVN reg. NR. (pec siem tiek noteikts ceka paraugs);
virsiDus = "40003242733"       #Degviela Virši-A DUS
megoVeikals = "40003642393"           #Rimi veikals

# Funkcija lai izgutu nepieciesamos datus no clipboard satura;
def get_data():
    #clipboard.copy("abc")  # now the clipboard content will be string "abc"
    data = clipboard.paste()  # text will have the content of clipboard
    
    global veikals_PVN
    global veikals_KASE
    global veikals_CEKS
    global veikals_SUMMA
    global veikals_DATUMS
    global veikals_Orig_DATUMS

    # Clipboad datos samekle PVN numuru;
    #veikals_PVN = re.findall(r"kods LV(\d+)", data)[0]
    veikals_PVN = re.findall(r"(4000\d\d\d\d\d\d\d)", data)[0]
    print(veikals_PVN)


    # Nosaka ceka paraugu un izgust vajadzigos datus;
    if veikals_PVN == virsiDus:
        print("Found Virši-A DUS!")
    
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


    elif veikals_PVN == megoVeikals:
        print("Found Mego veikals!")

        megoVeikals_kase = re.findall(r"Nr.(\d.R\d+)", data)[0]
        print(megoVeikals_kase)
        veikals_KASE = megoVeikals_kase
    
        megoVeikals_ceks = re.findall(r"eks.(\d./\d+)", data)[0]
        print(megoVeikals_ceks)
        veikals_CEKS = megoVeikals_ceks

        megoVeikals_summa = re.findall(r"(\d+,\d+).EUR", data)[0]
        print(megoVeikals_summa)    
        veikals_SUMMA = megoVeikals_summa

        megoVeikals_datums = re.findall(r"(\d\d.\d\d.\d\d\d\d).\d.:\d.:\d.", data)[0]
        #print(virsiDus_datums)
        veikals_Orig_DATUMS = megoVeikals_datums
        if megoVeikals_datums[0] == "0":
            megoVeikals_datums = megoVeikals_datums.replace('0', '')[0]
            print(megoVeikals_datums)
        veikals_DATUMS = megoVeikals_datums
    
    else:
        print("Not found!")


# Fukncija lai izveidotu jaunu failu un ierakstitu izguto datu (caur regex) saturu;
def write_file():
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


# Funkcija lai automatiski aizpilditu formu ar iegutajiem datiem;
def fill_form():
    driver = webdriver.Chrome(PATH)
    driver.get('https://cekuloterija.lv/')
    #print(driver.title)
    time.sleep(0.5)

    # akceptejam Cookies;
    btn_cookie = driver.find_element_by_xpath('//*[@id="app"]/div/div[5]/button')
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
    input_TEL.send_keys("29991579")
    time.sleep(5)

    # iesniedzam formu;
    #btn_FIN = driver.find_element_by_xpath('//*[@id="modal"]/div/div/div[2]/div[1]/button')
    #btn_FIN.click()
    #time.sleep(1)

    #driver.quit()


