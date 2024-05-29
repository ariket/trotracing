#Webscraping app. Used for extracting data from ATG website, I have fetced round 500 races 
from selenium import webdriver  #Selenium driver is an automated testing framework used for the validation of websites (and web applications)
                                #The selenium package is used to automate web browser interaction from Python.
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup   #Beautiful Soup is a Python library for pulling data out of HTML and XML files.
                                #Web Scraping with Beautiful Soup.
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import pandas as pd

# DataFrame:
#racenum = Loppets unika idnummer ,startnum = hästens startnummer,horsename = hästens snamn,driver = kuskens namn,trainer = tränarens namn,
#playpercent = hur mycket hästen är spelad i %,moneywin = intjänade pengar för hästen,resrace1 =resultat i senaste loppet ,pricesumrace1 = prissumma i senaste loppet,
#resrace2 = resultat i nästsenaste loppet,pricesumrace2 = prissumma i nästsenaste loppet ,resrace3,pricesumrace3,resrace4,pricesumrace4,resrace5 = resultat i femtesenaste loppet,pricesumrace5= prissumma i femtesenaste loppet ,
#winnernum = nummer på vinnaren i loppet ,driver_id = kusk id,trainer_id 0 tränar id, winner = anger om aktuell häst vann loppet, 1 för vinst och annars 0

#Följade v75 datum har skrapats:
# "2023-04-01/V75/aby/", "2023-04-06/V75/gavle/", "2023-04-07/V75/farjestad/", "2023-04-08/V75/klosterskogen/", "2023-04-09/V75/solvalla/", "2023-04-15/V75/axevalla/", "2023-04-22/V75/jagersro/", "2023-04-29/V75/orebro/",
# "2023-05-06/V75/aby/", "2023-05-13/V75/umaker/", "2023-05-20/V75/gavle/", "2023-05-27/V75/solvalla/","2023-06-03/V75/eskilstuna/","2023-06-10/V75/ostersund/", "2023-06-17/V75/boden/", "2023-06-25/V75/kalmar/",
# "2023-07-01/V75/bergsaker/", "2023-07-06/V75/halmstad/", "2023-07-08/V75/halmstad/", "2023-07-15/V75/arjang/", "2023-07-22/V75/axevalla/","2023-07-25/V75/jagersro/","2023-07-29/V75/hagmyren/","2023-08-05/V75/rattvik/","2023-08-12/V75/aby/", "2023-08-16/V75/solvalla/", "2023-08-19/V75/romme/",
# "2023-08-22/V75/jagersro/", "2023-08-26/V75/bergsaker/", "2023-09-02/V75/jagersro/", "2023-09-03/V75/jagersro/", "2023-09-16/V75/eskilstuna/", "2023-09-23/V75/farjestad/", "2023-09-30/V75/aby/",
# "2023-10-07/V75/boden/", "2023-10-14/V75/solvalla/", "2023-10-21/V75/orebro/", "2023-10-28/V75/jagersro/","2023-11-05/V75/solvalla/", "2023-11-11/V75/bergsaker/", "2023-11-18/V75/eskilstuna/", "2023-11-25/V75/jagersro/","2023-12-02/V75/solvalla/",
# "2023-12-09/V75/aby/","2023-12-16/V75/bollnas/","2023-12-23/V75/mantorp/", "2023-12-25/V75/umaker/","2023-12-26/V75/solvalla/", "2023-12-30/V75/gavle/", "2023-12-31/V75/axevalla/","2024-01-06/V75/romme/",
# "2024-01-13/V75/kalmar/", "2024-01-20/V75/bollnas/", "2024-01-27/V75/axevalla/","2024-02-03/V75/solvalla/","2024-02-10/V75/aby/"
loppV75 = [] #Fyll datum som du vill skrapa

#Följade v86 datum har skrapats:
# "2024-01-31/V86/bergsaker-solvalla/", "2024-01-24/V86/jagersro-solvalla/", "spel/2024-01-17/V86/aby-solvalla/", "2024-01-10/V86/bergsaker-solvalla/", "2024-01-03/V86/aby-solvalla/", "2023-12-20/V86/aby-solvalla/", "2023-12-13/V86/jagersro-solvalla/","2023-12-06/V86/bergsaker-solvalla/","2023-11-29/V86/aby-solvalla/", 
# "2023-11-15/V86/aby-solvalla/","2023-11-08/V86/jagersro-solvalla/""2023-04-05/V86/jagersro-solvalla/", "2023-04-12/V86/aby-solvalla/", "2023-04-26/V86/aby-solvalla/", "2023-05-03/V86/bergsaker-solvalla/", "2023-05-10/V86/jagersro-solvalla/", "2023-05-17/V86/aby-solvalla/", "2023-06-07/V86/amal/", "2023-06-21/V86/solvalla/", "2023-07-12/V86/solanget/","2023-07-19/V86/eskilstuna/"
# "2023-08-02/V86/visby/", "2023-08-09/V86/mantorp/","2023-08-02/V86/visby/", "2023-08-09/V86/mantorp/","2023-08-30/V86/aby-solvalla/""2023-09-06/V86/aby-solvalla/", "2023-09-13/V86/jagersro-solvalla/","2023-09-27/V86/aby-solvalla/", "2023-10-04/V86/jagersro-solvalla/"


avdelningar = ["avd/1","avd/2","avd/3","avd/4","avd/5","avd/6","avd/7"] #Lägg till "avd8" när skrapning sker på v86
newData = False

def ScrapeAtgData(url):
    print(f"Nu börjar skrapningen av {url} \nAvvakta, det tar ca 15 sekunder....")
    driver = webdriver.Chrome()  #NYI user may not have Chrome installed 
    #driver = webdriver.Edge() #Try this if you only have edge installed on your computer
    #driver = webdriver.Firefox() #Try this if you only have firefox installed on your computer
    driver.get(url)
    time.sleep(0.5)

    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='MuiButtonBase-root MuiButton-root MuiButton-contained MuiButton-containedSuccess MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButton-fullWidth MuiButton-root MuiButton-contained MuiButton-containedSuccess MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButton-fullWidth frame-132aezr']"))).click()
        #buttons.click()
    except:
        print('oops. click failed')
        
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='MuiButtonBase-root MuiButton-root MuiButton-outlined MuiButton-outlinedPrimary MuiButton-sizeMedium MuiButton-outlinedSizeMedium MuiButton-root MuiButton-outlined MuiButton-outlinedPrimary MuiButton-sizeMedium MuiButton-outlinedSizeMedium horse-ce1mpu-RaceSettings-styles--expandAllButton']"))).click()
        #buttons.click()
    except:
        print('oops. click failed')
        
    x = 0 ; i = 0
    while i < 15:     #Scroll down to bottom of webpage to be able to scrape all data
        time.sleep(0.3)
        driver.execute_script(f"window.scrollTo(0, {x})")
        i +=1
        x +=500   
    
    htmlRaw = BeautifulSoup(driver.page_source,'html.parser')            #Load whole webpage to htmlRaw
    with open('./data/temp.csv' ,"w", newline='',encoding="utf8") as D2: #Save all data to a file
        out = csv.writer(D2)
        out.writerow(htmlRaw) 
    driver.quit()
    
    print(f"Skrapningen av {url} är nu slutförd\n")   


def ScrapeSorting(WinnerHorse, raceNumberU):
    row=0 ;
    dontSave = False
    list = [] #Holds all relevant data, unsorted.

    with open('./data/temp.csv','r',encoding="utf8") as file:    
        for line in file:
            changedDriver = True
            row += 1
            #if line[17:64] == "horse-1vmhsvw-ToggleHarryBoyButton-styles--harr":   
            if line[32:64] == "MuiTouchRipple-root horse-w0pj6f" or line[16:48] == "<link data-react-helmet=\"\"true\"\"" or line[35:65] == "MuiTableCell-root MuiTableCell":
                try:
                    line.split("horse-1hcp75k-HorseCell-styles--driverName")[1][3:].split("</p><p class=")[0]                  
                        
                except:
                    changedDriver = False
                list.append(line)
     
    rowNum = 0
    if not dontSave:
        for post in list: #Sorting out useful data from scraped raw-data
            struken = False
            rowNum += 1
            name = post.split("horse-l2uirb-HorseCell-styles--horseName")
            
            if len(name) == 1:  #struken häst
                name = post.split("horse-sripkt-HorseCell-styles--horseName")
                struken = True
                
            if rowNum == 1:
                if struken:  #struken häst
                    driver = "Stuken" + post.split("horse-13mtk98-HorseCell-styles--driverName")[1][3:].split("</p><p class=")[0] + "Stuken"
                else:
                    driver = post.split("horse-1hnlc0r-HorseCell-styles--driverName")[1][3:].split("</p><p class=")[0]
                
                spår = rowNum
                if spår > 9:
                    horsename = name[1][4:].split("<span ")[0]
                else:
                    horsename = name[1][4:].split("<span ")[0]

            else:
                if rowNum < len(list):
                    hästdataRad1 = f";{spår};{horsename};{driver}"
             
                    spår = rowNum
                    if spår > 9:
                        horsename = name[1][4:].split("<span ")[0]
                    else:
                        horsename = name[1][4:].split("<span ")[0]
                    
                    if struken:  #struken häst
                        driver = "Stuken" + post.split("horse-13mtk98-HorseCell-styles--driverName")[1][3:].split("</p><p class=")[0] + "Stuken"
                    else:
                        try:
                            driver = post.split("horse-1hnlc0r-HorseCell-styles--driverName")[1][3:].split("</p><p class=")[0]
                        except:
                            driver = post.split("horse-1hcp75k-HorseCell-styles--driverName")[1][3:].split("</p><p class=")[0]
                            
                    percent = post.split("startlist-cell-betdistribution")[1][3:].split("<span style=")[0]
                    trainer = post.split("startlist-cell-trainer")[1][3:].split("</span></")[0]
                    insprungnapengar1 = post.split("startlist-cell-earnings")[1][3:].split("</span></td><td class=")[0]
                    insprungnapengar ="".join(c for c in insprungnapengar1 if  c.isdecimal())
                    try:
                        placeringLopp1 = post.split("tableCellBody\"\"><span style=\"\"font-weight: 600;\"\">")[1].split("</span></td><td class=\"\"MuiTableCell-root")[0]
                        #prissummaLopp1 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg-ExtendedStartTable-styles--tableCellBody\"\">")[8].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg")[0][:-1] 
                        prissummaLopp1 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9-PreviousStartsTable-styles--tableCellBody\"\">")[8].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9")[0][:-1]    
                    except:
                        placeringLopp1 =""
                        prissummaLopp1 =""
                    try:
                        placeringLopp2 = post.split("tableCellBody\"\"><span style=\"\"font-weight: 600;\"\">")[2].split("</span></td><td class=\"\"MuiTableCell-root")[0]
                        #prissummaLopp2 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg-ExtendedStartTable-styles--tableCellBody\"\">")[19].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg")[0][:-1]    
                        prissummaLopp2 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9-PreviousStartsTable-styles--tableCellBody\"\">")[19].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9")[0][:-1]    
                    except:
                        placeringLopp2 =""
                        prissummaLopp2 =""
                    try:
                        placeringLopp3 = post.split("tableCellBody\"\"><span style=\"\"font-weight: 600;\"\">")[3].split("</span></td><td class=\"\"MuiTableCell-root")[0]
                        #prissummaLopp3 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg-ExtendedStartTable-styles--tableCellBody\"\">")[30].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg")[0][:-1]    
                        prissummaLopp3 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9-PreviousStartsTable-styles--tableCellBody\"\">")[30].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9")[0][:-1]    
                    except:
                        placeringLopp3 =""
                        prissummaLopp3 =""
                    try:
                        placeringLopp4 = post.split("tableCellBody\"\"><span style=\"\"font-weight: 600;\"\">")[4].split("</span></td><td class=\"\"MuiTableCell-root")[0]
                        #prissummaLopp4 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg-ExtendedStartTable-styles--tableCellBody\"\">")[41].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg")[0][:-1]
                        prissummaLopp4 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9-PreviousStartsTable-styles--tableCellBody\"\">")[41].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9")[0][:-1]    
                    except:
                        placeringLopp4 =""
                        prissummaLopp4 =""
                    try:
                        placeringLopp5 = post.split("tableCellBody\"\"><span style=\"\"font-weight: 600;\"\">")[5].split("</span></td><td class=\"\"MuiTableCell-root")[0]
                        #prissummaLopp5 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg-ExtendedStartTable-styles--tableCellBody\"\">")[52].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg")[0][:-1]
                        prissummaLopp5 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9-PreviousStartsTable-styles--tableCellBody\"\">")[52].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9")[0][:-1]    
                    except:
                        placeringLopp5 =""
                        prissummaLopp5 =""
                    hästdataRad2 = f";{trainer};{percent};{insprungnapengar};{placeringLopp1};{prissummaLopp1};{placeringLopp2};{prissummaLopp2};{placeringLopp3};{prissummaLopp3};{placeringLopp4};{prissummaLopp4};{placeringLopp5};{prissummaLopp5};{WinnerHorse}"
                    hästdataRad3 = str(raceNumberU) + hästdataRad1 + hästdataRad2
                   
                    if hästdataRad1[-6:] != "Stuken":
                        with open("./data/races.csv", 'a', newline='') as csvfile:
                    # creating a csv dict writer object
                            csv_writer = csv.writer(csvfile)
                    # Write strings to the file
                            csv_writer.writerow([hästdataRad3])
                    
                if rowNum == len(list):
                    trainer = post.split("startlist-cell-trainer")[1][3:].split("</span></")[0]
                    percent = post.split("startlist-cell-betdistribution")[1][3:].split("<span style=")[0]
                    insprungnapengar1 = post.split("startlist-cell-earnings")[1][3:].split("</span></td><td class=")[0]
                    insprungnapengar ="".join(c for c in insprungnapengar1 if  c.isdecimal())
                    try:
                        placeringLopp1 = post.split("tableCellBody\"\"><span style=\"\"font-weight: 600;\"\">")[1].split("</span></td><td class=\"\"MuiTableCell-root")[0]
                        #prissummaLopp1 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg-ExtendedStartTable-styles--tableCellBody\"\">")[8].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg")[0][:-1]
                        prissummaLopp1 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9-PreviousStartsTable-styles--tableCellBody\"\">")[8].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9")[0][:-1]
                    except:
                        placeringLopp1 =""
                        prissummaLopp1 =""
                    try:
                        placeringLopp2 = post.split("tableCellBody\"\"><span style=\"\"font-weight: 600;\"\">")[2].split("</span></td><td class=\"\"MuiTableCell-root")[0]
                        #prissummaLopp2 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg-ExtendedStartTable-styles--tableCellBody\"\">")[19].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg")[0][:-1]
                        prissummaLopp2 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9-PreviousStartsTable-styles--tableCellBody\"\">")[19].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9")[0][:-1]
                    except:
                        placeringLopp2 =""
                        prissummaLopp2 =""
                    try:    
                        placeringLopp3 = post.split("tableCellBody\"\"><span style=\"\"font-weight: 600;\"\">")[3].split("</span></td><td class=\"\"MuiTableCell-root")[0]
                        #prissummaLopp3 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg-ExtendedStartTable-styles--tableCellBody\"\">")[30].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg")[0][:-1]
                        prissummaLopp3 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9-PreviousStartsTable-styles--tableCellBody\"\">")[30].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9")[0][:-1]
                    except:
                        placeringLopp3 =""
                        prissummaLopp3 =""
                    try:
                        placeringLopp4 = post.split("tableCellBody\"\"><span style=\"\"font-weight: 600;\"\">")[4].split("</span></td><td class=\"\"MuiTableCell-root")[0]
                        #prissummaLopp4 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg-ExtendedStartTable-styles--tableCellBody\"\">")[41].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg")[0][:-1]
                        prissummaLopp4 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9-PreviousStartsTable-styles--tableCellBody\"\">")[41].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9")[0][:-1]
                    except:
                        placeringLopp4 =""
                        prissummaLopp4 =""
                    try:
                        placeringLopp5 = post.split("tableCellBody\"\"><span style=\"\"font-weight: 600;\"\">")[5].split("</span></td><td class=\"\"MuiTableCell-root")[0]
                        #prissummaLopp5 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg-ExtendedStartTable-styles--tableCellBody\"\">")[52].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg")[0][:-1]
                        prissummaLopp5 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9-PreviousStartsTable-styles--tableCellBody\"\">")[52].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9")[0][:-1]
                    except:
                        placeringLopp5 =""
                        prissummaLopp5 =""
        
        #rows in csv file: racenum;startnum;horsename;driver;trainer;playpercent;moneywin;resrace1;pricesumrace1;resrace2;pricesumrace2;resrace3;pricesumrace3;resrace4;pricesumrace4;resrace5;pricesumrace5;winnernum
        hästdata = str(raceNumberU) + f";{spår};{horsename};{driver};{trainer};{percent};{insprungnapengar};{placeringLopp1};{prissummaLopp1};{placeringLopp2};{prissummaLopp2};{placeringLopp3};{prissummaLopp3};{placeringLopp4};{prissummaLopp4};{placeringLopp5};{prissummaLopp5};{WinnerHorse}"
        
        # writing to csv file
        if driver[-6:] != "Stuken":
            with open("./data/races.csv", 'a', newline='') as csvfile:
            # creating a csv dict writer object
                csv_writer = csv.writer(csvfile)

        # Write strings to the file
                csv_writer.writerow([hästdata])
           
    print("\nSorteringen är nu genomförd\n")


def ScrapeAtgResultat(url): 
    V75Winners = []
    driver = webdriver.Chrome()  #NYI user may not have Chrome installed 
    #driver = webdriver.Edge() #Try this if you only have edge installed on your computer
    #driver = webdriver.Firefox() #Try this if you only have firefox installed on your computer

    driver.get(url)
    time.sleep(0.3)    
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id='onetrust-accept-btn-handler']"))).click()
        #buttons.click()
    except:
        print('oops. misslyckades')
        
    time.sleep(0.4)
    x = 0 ; i = 0
    while i < 3:     #Scroll down to bottom of webpage to be able to scrape all data
        time.sleep(0.7)
        driver.execute_script(f"window.scrollTo(0, {x})")
        i +=1
        x +=500
    time.sleep(0.4)
    htmlRaw = BeautifulSoup(driver.page_source,'html.parser') #Load whole webpage to htmlRaw
    time.sleep(0.4)
    
    with open('./data/temp.csv' ,"w", newline='',encoding="utf8") as D2: #Save all data to a file
        out = csv.writer(D2)
        out.writerow(htmlRaw)     

    driver.quit()
    
    list = [] #Holds all relevant data, unsorted,
    time.sleep(0.2)
    with open('./data/temp.csv','r',encoding="utf8") as file:
        for line in file:
            if line[32:64] == "MuiTouchRipple-root horse-w0pj6f" or line[16:48] == "<link data-react-helmet=\"\"true\"\"":
                list.append(line)
                break
    
    for post in list: #Sorting out useful data from scraped raw-data
        v75result = post.split("horse-jf55t5-ResultsTable-styles--horseNumber")
        racenumber = 0
        for postresult in v75result:
            winnernum = postresult[3:].split("</span><span class=\"\"horse-1fp1sgb")
            if racenumber > 0:
                V75Winners.append(winnernum[0])
            racenumber += 1
            
    print(f"Skrapningen av {url} är nu slutförd\n") 
    return V75Winners

def ScrapeAtg():
    j = 0
    k = 85
    
    if len(loppV75) == 0:
        print("Inga lopp att skrapa, lägg till travlopp i \"loppV75\" om du vill skrapa.")
    
    else:
        while j < len(loppV75):
            i = 0
            url = "https://www.atg.se/spel/" + loppV75[j] + "avd/1/resultat"
            print(f"url : {url}") 
            V75Winners = ScrapeAtgResultat(url)
            print(V75Winners)
              
            while i < 7:  #Ändra till 8 när v86
                url ="https://www.atg.se/spel/" + loppV75[j] + avdelningar[i]
                ScrapeAtgData(url) 
                num = str(k)+ str(i+1)      
                ScrapeSorting(V75Winners[i],num)
                i += 1
            j += 1
            k += 1      

def Vikt():

    df = pd.read_csv('./data/modified_data.csv', sep = ',')

    #testt = df[(df["resrace1"] == '1') & (df['winnernum'] == df['startnum'])]
    #testt = df[df["resrace1"] == "1"]
    #print(testt)
    
    # Räkna hur ofta man vinner aktuellt lopp från resp startnummer.
    counts = len(df[(df["startnum"] == 1) & (df['winnernum'] == df['startnum'])])
    print("Antal vinster för häst från startbana 1:", counts)
    #Antal vinster för häst från startbana 1-15: 46, 47, 48, 66, 63, 58, 42, 27, 29, 29, 25, 20, 9, 5, 5
    
    # Räkna hur ofta man vinner aktuellt lopp om hästen tjänat över/under 500000kr.
    counts = len(df[(df["moneywin"] > 500000) & (df['winnernum'] == df['startnum'])])
    print("Antal vinster hästen vunnit om intjänat över 500k:", counts)
    #Antal vinster hästen vunnit om intjänat över 500k: 296
    #Antal vinster hästen vunnit om intjänat under 500k: 223
    
    # Räkna hur ofta man vinner aktuellt lopp om hästen också vunnit ett tidigare lopp.
    count = len(df[(df["resrace1"] == 1) & (df['winnernum'] == df['startnum'])])
    print("Antal vinster när man vunnit i senaste loppet man körde:", count)
    
    #Antal vinster när man vunnit i senaste loppet man körde: 170
    #Antal vinster när man vunnit i nästsenaste loppet man körde: 171
    #Antal vinster när man vunnit i tredjesenaste loppet man körde: 159 
    #Antal vinster när man vunnit i fjärdesenaste loppet man körde: 165 
    #Antal vinster när man vunnit i femtesenaste loppet man körde: 146
    #Antal vinster när man var tvåa i senaste loppet man körde: 97
    #Antal vinster när man var tvåa i nästsenaste loppet man körde: 91
    #Antal vinster när man var tvåa i 3-5 senasteloppet man körde: snittvärde 82
    #Antal vinster när man var trea i senaste loppet man körde: 58
    #Antal vinster när man var trea i nästsenaste loppet man körde: 59
    #Antal vinster när man var trea i 3-5 senasteloppet man körde: snittvärde 55
    #Antal vinster när man var fyra i senaste loppet man körde: 36
    #Antal vinster när man var femma i senaste loppet man körde: 23
    #Antal vinster när man var sexa i senaste loppet man körde: 32
    #Antal vinster när man var sjua/åtta i senaste loppet man körde: 10
    #Antal vinster när man var diskad i senaste loppet man körde: 23
    
    
def AddColumn():  
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv("./data/mod.csv", sep = ',') 
   
    # Create a new column 'winner' based on the condition
    df['winner'] = df.apply(lambda row: 1 if row['winnernum'] == row['startnum'] else 0, axis=1)

    # Convert the 'winner' column to int64 format
    df['winner'] = df['winner'].astype('int64')
    # Write the modified DataFrame back to a CSV file
    df.to_csv("./data/modXX.csv", index=False)

def AddColumn2():  
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv("./data/trainingData.csv", sep = ',')
   
    # Create a new column 'rp1'-'rp5' based on the condition
    df['rp1'] = df['resrace1'] / df['pricesumrace1']
    df['rp2'] = df['resrace2'] / df['pricesumrace2']
    df['rp3'] = df['resrace3'] / df['pricesumrace3']
    df['rp4'] = df['resrace4'] / df['pricesumrace4']
    df['rp5'] = df['resrace5'] / df['pricesumrace5']
    # Convert the 'winner' column to int64 format
    #df['winner'] = df['winner'].astype('int64')
    # Write the modified DataFrame back to a CSV file
    df.to_csv("./data/nextRaceData.csv", index=False)    

ScrapeAtg()
