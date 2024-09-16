#Webscraping app. Used for extracting data from ATG website
from selenium import webdriver  #Selenium driver is an automated testing framework used for the validation of websites (and web applications)
                                #The selenium package is used to automate web browser interaction from Python.
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup   #Beautiful Soup is a Python library for pulling data out of HTML and XML files.
                                #Web Scraping with Beautiful Soup.
import time
import csv
import pandas as pd
from pathlib import Path
import os

# DataFrame(explanation in swedish):
#racenum = Loppets unika idnummer ,startnum = hästens startnummer,horsename = hästens namn,driver = kuskens namn,trainer = tränarens namn,
#playpercent = hur mycket hästen är spelad i %,moneywin = intjänade pengar för hästen,resrace1 =resultat i senaste loppet ,pricesumrace1 = prissumma i senaste loppet,
#resrace2 = resultat i nästsenaste loppet,pricesumrace2 = prissumma i nästsenaste loppet ,resrace3,pricesumrace3,resrace4,pricesumrace4,resrace5 = resultat i femtesenaste loppet,pricesumrace5= prissumma i femtesenaste loppet ,
#winnernum = nummer på vinnaren i loppet ,driver_id = kusk id,trainer_id 0 tränar id, winner = anger om aktuell häst vann loppet, 1 för vinst och annars 0

header= "racenum;startnum;horsename;driver;trainer;playpercent;moneywin;resrace1;pricesumrace1;resrace2;pricesumrace2;resrace3;pricesumrace3;resrace4;pricesumrace4;resrace5;pricesumrace5;winnernum\n"
avdelningar = ["avd/1","avd/2","avd/3","avd/4","avd/5","avd/6","avd/7","avd/8"]
newData = False

def ScrapeAtgData(url):
    print(f"Nu börjar skrapningen av {url} \nAvvakta, det tar ca 15 sekunder....")
    options = webdriver.ChromeOptions()
    #options.add_argument('--user-data-dir=C:/Users/Ari/AppData/Local/Google/Chrome/User Data/Default')
    #options.add_argument('--profile-directory=Default')
    #options.add_argument('--profile-directory=C:/Users/Ari/AppData/Local/Google/Chrome/User Data/Default')
    #options.add_argument('--disk-cache-dir=C:\Users\Ari\AppData\Local\Google\Chrome\User Data\Default\Cache\Cache_Data') 
    #options.add_argument('--headless')         #Headless, Scraping without opening the webbrowser
    driver = webdriver.Chrome(options=options)
    #driver = webdriver.Edge()    #Try this if you only have edge installed on your computer
    #driver = webdriver.Firefox() #Try this if you only have firefox installed on your computer
    driver.get(url)
    time.sleep(0.3)


    try:
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='MuiButtonBase-root MuiButton-root MuiButton-contained MuiButton-containedSuccess MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButton-fullWidth MuiButton-root MuiButton-contained MuiButton-containedSuccess MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButton-fullWidth frame-132aezr']"))).click()
    except:
        print('oops 1. klick misslyckades')
        
        
        #TEST
    #try:
    #    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='MuiButtonBase-root MuiButton-root MuiButton-outlined MuiButton-outlinedPrimary MuiButton-sizeMedium MuiButton-outlinedSizeMedium MuiButton-root MuiButton-outlined MuiButton-outlinedPrimary MuiButton-sizeMedium MuiButton-outlinedSizeMedium horse-1erm2vz-RaceSettings-styles--changeStartlistButton']"))).click()
    #except:
    #    print('oops. klick misslyckades')
        
    #try:
    #    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='MuiButtonBase-root MuiListItemButton-root MuiListItemButton-gutters MuiListItemButton-root MuiListItemButton-gutters horse-1qw7nxx-StartlistCustomizationDrawer-styles--startlistItem']"))).click()
    #    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='MuiTouchRipple-root horse-w0pj6f']"))).click()
   #     WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='MuiButtonBase-root MuiRadio-root MuiRadio-colorPrimary PrivateSwitchBase-root MuiRadio-root MuiRadio-colorPrimary Mui-checked MuiRadio-root MuiRadio-colorPrimary horse-1ewp53a']"))).click()
        #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='MuiButtonBase-root MuiListItemButton-root MuiListItemButton-gutters MuiListItemButton-root MuiListItemButton-gutters horse-qmct39-StartlistCustomizationDrawer-styles--startlistItem']"))).click()
   # except:
   #     print('oops. klick misslyckades')    
    
    #END TEST    
        
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='MuiButtonBase-root MuiButton-root MuiButton-outlined MuiButton-outlinedPrimary MuiButton-sizeMedium MuiButton-outlinedSizeMedium MuiButton-root MuiButton-outlined MuiButton-outlinedPrimary MuiButton-sizeMedium MuiButton-outlinedSizeMedium horse-ce1mpu-RaceSettings-styles--expandAllButton']"))).click()
    except:
        print('oops 2. klick misslyckades')
        
    x = 0 ; i = 0
    while i < 15:     #Scroll down to bottom of webpage to be able to scrape all data
        time.sleep(0.3)
        driver.execute_script(f"window.scrollTo(0, {x})")
        i +=1
        x +=500   
    
    htmlRaw = BeautifulSoup(driver.page_source,'html.parser')            #Load whole webpage to htmlRaw
    path = Path(__file__).parent / "data/temp.csv"
    with path.open("w", newline='',encoding="utf8") as D2: #Save all data to a file
        out = csv.writer(D2)
        out.writerow(htmlRaw)
    driver.quit()
    
    print(f"Skrapningen av {url} är nu slutförd")   


def ScrapeSorting(raceNumber):
    row=0
    dontSave = False
    list = [] #Holds all relevant data, unsorted.

    path = Path(__file__).parent / "data/temp.csv"
    with path.open('r',encoding="utf8") as file:   
        for line in file:
            row += 1
            #if line[17:64] == "horse-1vmhsvw-ToggleHarryBoyButton-styles--harr":   #Row 464
            if line[32:64] == "MuiTouchRipple-root horse-w0pj6f" or line[16:48] == "<link data-react-helmet=\"\"true\"\"" or line[35:65] == "MuiTableCell-root MuiTableCell":
                try:
                    #line.split("horse-1hcp75k-HorseCell-styles--driverName")[1][3:].split("</p><p class=")[0]  
                    line.split("horse-1hnlc0r-HorseCell-styles--driverName")[1][3:].split("</p><p class=")[0]
                    print("Split - Skrapningen lyckades")
                except:
                    try:
                        line.split("horse-1hcp75k-HorseCell-styles--driverName")[1][3:].split("</p><p class=")[0]
                        print("Split - Skrapningen misslyckades")
                    except:
                        pass
                list.append(line)              
    rowNum = 0
    if not dontSave:
        for post in list: #Sorting out useful data from scraped raw-data
            broken = False
            rowNum += 1
            name = post.split("horse-l2uirb-HorseCell-styles--horseName")
            
            if len(name) == 1:  #broken horse(struken häst)
                name = post.split("horse-sripkt-HorseCell-styles--horseName")
                broken = True
                
            if rowNum == 1:
                if broken:  #broken horse(struken häst)
                    driver = "Stuken" + post.split("horse-13mtk98-HorseCell-styles--driverName")[1][3:].split("</p><p class=")[0] + "Stuken"
                else:
                    try:
                        driver = post.split("horse-1hnlc0r-HorseCell-styles--driverName")[1][3:].split("</p><p class=")[0]
                    except:
                        #Bytt kusk:
                        #driver = post.split("horse-1i7hnt6-HorseCell-styles--driverName")[1][3:].split("</p><p class=")[0]
                        driver = post.split("horse-1hcp75k-HorseCell-styles--driverName")[1][3:].split("</p><p class=")[0]
                        print(driver)   
                    #driver = post.split("horse-1hnlc0r-HorseCell-styles--driverName")[1][3:].split("</p><p class=")[0]                
                tracknumber = rowNum
                if tracknumber > 9:
                    horsename = name[1][4:].split("<span ")[0]
                else:
                    horsename = name[1][4:].split("<span ")[0]
            else:
                if rowNum < len(list):
                    
                    if broken:  #broken horse(struken häst)
                        try:
                            driver = "Stuken" + post.split("horse-13mtk98-HorseCell-styles--driverName")[1][3:].split("</p><p class=")[0] + "Stuken"
                        except:
                            driver = "Struken"
                    else:
                        try:
                            driver = post.split("horse-1hnlc0r-HorseCell-styles--driverName")[1][3:].split("</p><p class=")[0]
                        except:
                            driver = post.split("horse-1hcp75k-HorseCell-styles--driverName")[1][3:].split("</p><p class=")[0]
                      
                    
                    horseDataRow1 = f";{tracknumber};{horsename};{driver}" 
                    tracknumber = rowNum
                    if tracknumber > 9:
                        horsename = name[1][4:].split("<span ")[0]
                    else:
                        horsename = name[1][4:].split("<span ")[0]
                    
                    #if broken:  #broken horse(struken häst)
                    #    driver = "Stuken" + post.split("horse-13mtk98-HorseCell-styles--driverName")[1][3:].split("</p><p class=")[0] + "Stuken"
                    #else:
                    #    try:
                    #        driver = post.split("horse-1hnlc0r-HorseCell-styles--driverName")[1][3:].split("</p><p class=")[0]
                    #    except:
                    #        driver = post.split("horse-1hcp75k-HorseCell-styles--driverName")[1][3:].split("</p><p class=")[0]
                            
                    percent = post.split("startlist-cell-betdistribution")[1][3:].split("<span style=")[0]
                    #trainer = post.split("startlist-cell-trainer")[1][3:].split("</span></")[0]
                    trainer = post.split("startlist-cell-trainer\"\" style=\"\"white-space: break-spaces;")[1][3:].split("</span></")[0]
                    try:
                        moneyEarned1 = post.split("startlist-cell-earnings")[1][3:].split("</span></td><td class=")[0]
                        moneyEarned ="".join(c for c in moneyEarned1 if  c.isdecimal())
                    except:
                        moneyEarned = "0"
                    
                    try:
                        placementRace1 = post.split("tableCellBody\"\"><span style=\"\"font-weight: 600;\"\">")[1].split("</span></td><td class=\"\"MuiTableCell-root")[0]
                        #pricesumRace1 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg-ExtendedStartTable-styles--tableCellBody\"\">")[8].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg")[0][:-1] 
                        pricesumRace1 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9-PreviousStartsTable-styles--tableCellBody\"\">")[8].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9")[0][:-1]    
                    except:
                        placementRace1 =""
                        pricesumRace1 =""
                    try:
                        placementRace2 = post.split("tableCellBody\"\"><span style=\"\"font-weight: 600;\"\">")[2].split("</span></td><td class=\"\"MuiTableCell-root")[0]
                        #pricesumRace2 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg-ExtendedStartTable-styles--tableCellBody\"\">")[19].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg")[0][:-1]    
                        pricesumRace2 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9-PreviousStartsTable-styles--tableCellBody\"\">")[19].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9")[0][:-1]    
                    except:
                        placementRace2 =""
                        pricesumRace2 =""
                    try:
                        placementRace3 = post.split("tableCellBody\"\"><span style=\"\"font-weight: 600;\"\">")[3].split("</span></td><td class=\"\"MuiTableCell-root")[0]
                        #pricesumRace3 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg-ExtendedStartTable-styles--tableCellBody\"\">")[30].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg")[0][:-1]    
                        pricesumRace3 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9-PreviousStartsTable-styles--tableCellBody\"\">")[30].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9")[0][:-1]    
                    except:
                        placementRace3 =""
                        pricesumRace3 =""
                    try:
                        placementRace4 = post.split("tableCellBody\"\"><span style=\"\"font-weight: 600;\"\">")[4].split("</span></td><td class=\"\"MuiTableCell-root")[0]
                        #pricesumRace4 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg-ExtendedStartTable-styles--tableCellBody\"\">")[41].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg")[0][:-1]
                        pricesumRace4 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9-PreviousStartsTable-styles--tableCellBody\"\">")[41].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9")[0][:-1]    
                    except:
                        placementRace4 =""
                        pricesumRace4 =""
                    try:
                        placementRace5 = post.split("tableCellBody\"\"><span style=\"\"font-weight: 600;\"\">")[5].split("</span></td><td class=\"\"MuiTableCell-root")[0]
                        #pricesumRace5 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg-ExtendedStartTable-styles--tableCellBody\"\">")[52].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg")[0][:-1]
                        pricesumRace5 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9-PreviousStartsTable-styles--tableCellBody\"\">")[52].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9")[0][:-1]    
                    except:
                        placementRace5 =""
                        pricesumRace5 =""
                    horseDataRow2 = f";{trainer};{percent};{moneyEarned};{placementRace1};{pricesumRace1};{placementRace2};{pricesumRace2};{placementRace3};{pricesumRace3};{placementRace4};{pricesumRace4};{placementRace5};{pricesumRace5};99"
                    horseDataRow3 = str(raceNumber) + horseDataRow1 + horseDataRow2
                   
                    if horseDataRow1[-6:] != "Stuken":
                        path = Path(__file__).parent / "data/races.csv"
                        with path.open('a', newline='') as csvfile:   
                            csv_writer = csv.writer(csvfile)    # creating a csv dict writer object
                            csv_writer.writerow([horseDataRow3]) # Write strings to the file
                    
                if rowNum == len(list):
                    #trainer = post.split("startlist-cell-trainer")[1][3:].split("</span></")[0]
                    trainer = post.split("startlist-cell-trainer\"\" style=\"\"white-space: break-spaces;")[1][3:].split("</span></")[0]
                    percent = post.split("startlist-cell-betdistribution")[1][3:].split("<span style=")[0]
                    try:
                        moneyEarned1 = post.split("startlist-cell-earnings")[1][3:].split("</span></td><td class=")[0]
                        moneyEarned ="".join(c for c in moneyEarned1 if  c.isdecimal())
                    except:
                        moneyEarned = "0"
                    try:
                        placementRace1 = post.split("tableCellBody\"\"><span style=\"\"font-weight: 600;\"\">")[1].split("</span></td><td class=\"\"MuiTableCell-root")[0]
                        #pricesumRace1 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg-ExtendedStartTable-styles--tableCellBody\"\">")[8].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg")[0][:-1]
                        pricesumRace1 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9-PreviousStartsTable-styles--tableCellBody\"\">")[8].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9")[0][:-1]
                    except:
                        placementRace1 =""
                        pricesumRace1 =""
                    try:
                        placementRace2 = post.split("tableCellBody\"\"><span style=\"\"font-weight: 600;\"\">")[2].split("</span></td><td class=\"\"MuiTableCell-root")[0]
                        #pricesumRace2 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg-ExtendedStartTable-styles--tableCellBody\"\">")[19].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg")[0][:-1]
                        pricesumRace2 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9-PreviousStartsTable-styles--tableCellBody\"\">")[19].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9")[0][:-1]
                    except:
                        placementRace2 =""
                        pricesumRace2 =""
                    try:    
                        placementRace3 = post.split("tableCellBody\"\"><span style=\"\"font-weight: 600;\"\">")[3].split("</span></td><td class=\"\"MuiTableCell-root")[0]
                        #pricesumRace3 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg-ExtendedStartTable-styles--tableCellBody\"\">")[30].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg")[0][:-1]
                        pricesumRace3 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9-PreviousStartsTable-styles--tableCellBody\"\">")[30].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9")[0][:-1]
                    except:
                        placementRace3 =""
                        pricesumRace3 =""
                    try:
                        placementRace4 = post.split("tableCellBody\"\"><span style=\"\"font-weight: 600;\"\">")[4].split("</span></td><td class=\"\"MuiTableCell-root")[0]
                        #pricesumRace4 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg-ExtendedStartTable-styles--tableCellBody\"\">")[41].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg")[0][:-1]
                        pricesumRace4 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9-PreviousStartsTable-styles--tableCellBody\"\">")[41].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9")[0][:-1]
                    except:
                        placementRace4 =""
                        pricesumRace4 =""
                    try:
                        placementRace5 = post.split("tableCellBody\"\"><span style=\"\"font-weight: 600;\"\">")[5].split("</span></td><td class=\"\"MuiTableCell-root")[0]
                        #pricesumRace5 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg-ExtendedStartTable-styles--tableCellBody\"\">")[52].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-138wacg")[0][:-1]
                        pricesumRace5 = post.split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9-PreviousStartsTable-styles--tableCellBody\"\">")[52].split("</td><td class=\"\"MuiTableCell-root MuiTableCell-body MuiTableCell-sizeMedium horse-1sok8q9")[0][:-1]
                    except:
                        placementRace5 =""
                        pricesumRace5 =""
        #rows in csv file: racenum;startnum;horsename;driver;trainer;playpercent;moneywin;resrace1;pricesumrace1;resrace2;pricesumrace2;resrace3;pricesumrace3;resrace4;pricesumrace4;resrace5;pricesumrace5;winnernum
        horseData = str(raceNumber) + f";{tracknumber};{horsename};{driver};{trainer};{percent};{moneyEarned};{placementRace1};{pricesumRace1};{placementRace2};{pricesumRace2};{placementRace3};{pricesumRace3};{placementRace4};{pricesumRace4};{placementRace5};{pricesumRace5};99" #99-Dummy winner, the race arn´t run so the winner is unknown
        
        # writing to csv file
        if driver[-6:] != "Stuken":
            path = Path(__file__).parent / "data/races.csv"
            with path.open('a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile) # creating a csv dict writer object
                csv_writer.writerow([horseData]) # Write strings to the file        
    print("Sorteringen är nu genomförd\n")


def ScrapeAtg():  
         ##If new driver or new trainer use 999, if not found in driver_id_map and trainer_id_map
    def replace_noll(numbernoll):
        if isinstance(numbernoll, str):
            numbernoll = numbernoll.replace(None, 999).replace("0", 999)
        elif pd.isnull(numbernoll):  # Check for empty strings
            return 999
        return numbernoll   
    
    path = Path(__file__).parent / "data/nextRace.txt"
    with path.open('r+') as fil:
        nextRace = fil.readline().strip()         # read one line
    numberOfRaces = int(nextRace[12])    
    
    if len(nextRace) == 0:
        print("Inget lopp att skrapa, lägg till travlopp i \"nextRace.txt\" om du vill skrapa.") 
    else:
        path = Path(__file__).parent / "data/races.csv"
        #with path.open('r+') as fil:
        with path.open('w+') as fil: #create new file if not exist
            fil.write(header)
            fil.readline()           # read one line
            fil.truncate(fil.tell()) # terminate the file here
        
        i = 0
        while i < numberOfRaces: 
        #while i < 1: #test kör bara en gång  
            url ="https://www.atg.se/spel/" + nextRace + avdelningar[i]
            ScrapeAtgData(url) 
            num = str(i+1)      
            ScrapeSorting(num)
            i += 1
            
    global newData
    newData = True
    path = Path(__file__).parent / "./data/nextRaceData.csv"
    #path = Path(__file__).parent / "./data/nextRaceDatatemp.csv"
    Sorting(path)
    
    # Read the CSV file into a DataFrame
    #path = Path(__file__).parent / "./data/nextRaceDatatemp.csv"
    df = pd.read_csv(path, sep = ',')     
    path = Path(__file__).parent / "./data/trainingData.csv"
    dp = pd.read_csv(path,sep = ',')
    # Create a dictionary to map each unique driver and trainer to a unique ID
    driver_id_map = {driverm: idx for idx, driverm in enumerate(dp['driver'].unique())}
    trainer_id_map = {trainerm: idx for idx, trainerm in enumerate(dp['trainer'].unique())}
 
    # Create a new column 'driver_id', 'trainer_id' and map the driver and trainer names to their corresponding IDs
    df['driver_id'] = df['driver'].map(driver_id_map)
    df['trainer_id'] = df['trainer'].map(trainer_id_map)

    df['driver_id'] = df['driver_id'].apply(replace_noll)
    df['trainer_id'] = df['trainer_id'].apply(replace_noll)
    
     # Create a new columns 'rp1'-'rp5'
     # 'rp1'-'rp5' are used later by script result.py in the machine learning algoritm.
    df['rp1'] = df['resrace1'] / df['pricesumrace1']
    df['rp2'] = df['resrace2'] / df['pricesumrace2']
    df['rp3'] = df['resrace3'] / df['pricesumrace3']
    df['rp4'] = df['resrace4'] / df['pricesumrace4']
    df['rp5'] = df['resrace5'] / df['pricesumrace5']
    
    # Write the modified DataFrame back to a CSV file
    path = Path(__file__).parent / "./data/nextRaceData.csv"
    df.to_csv(path,index=False)
    
def Sorting(fileName):
    
    global newData
    if newData:
            
       #Om horse disqualified,qualifyning race(kvallopp) or place missing set place to 9
        def replace_chars(shortening):
            if isinstance(shortening, str):
                shortening = shortening.replace("0", "9").replace("k", "9").replace("d", "9").replace(" ", "9")
            elif pd.isnull(shortening):  # Check for empty strings
                return "9"
            return shortening     

        #Om prissumma missing set prissumme to 30
        def replace_null(numbernull):
            if isinstance(numbernull, str):
                numbernull = numbernull.replace(None, "30").replace("0", "30")
            elif pd.isnull(numbernull):  # Check for empty strings
                return "30"
            return numbernull     
        
        # Read the CSV file into a DataFrame
        path = Path(__file__).parent / "data/races.csv"
        df = pd.read_csv(path,sep = ';')     
        
        # Create a dictionary to map each unique driver and trainer to a unique ID
        driver_id_map = {driverm: idx for idx, driverm in enumerate(df['driver'].unique())}
        trainer_id_map = {trainerm: idx for idx, trainerm in enumerate(df['trainer'].unique())}

        # Create a new column 'driver_id', 'trainer_id' and map the driver and trainer names to their corresponding IDs
        df['driver_id'] = df['driver'].map(driver_id_map)
        df['trainer_id'] = df['trainer'].map(trainer_id_map)
        df['resrace5'] = df['resrace5'].apply(replace_chars)
        df['resrace4'] = df['resrace4'].apply(replace_chars)
        df['resrace3'] = df['resrace3'].apply(replace_chars)
        df['resrace2'] = df['resrace2'].apply(replace_chars)
        df['resrace1'] = df['resrace1'].apply(replace_chars)
        df['pricesumrace5'] = df['pricesumrace5'].apply(replace_null)
        df['pricesumrace4'] = df['pricesumrace4'].apply(replace_null)
        df['pricesumrace3'] = df['pricesumrace3'].apply(replace_null)
        df['pricesumrace2'] = df['pricesumrace2'].apply(replace_null)
        df['pricesumrace1'] = df['pricesumrace1'].apply(replace_null)
        # Write the modified DataFrame back to a CSV file
        df.to_csv(fileName, index=False)
        newData = False

    else:
        print("Ingen ny data, metoden körs inte. Ändra \"newData\" till True om du vill använda funktionen")


def RemoveTempFiles():
    path = Path(__file__).parent / "data/temp.csv"
    if os.path.exists(path):
        os.remove(path)
    else:
        print(f"Filen {path} finns inte, borttagningen misslyckades")
    path = Path(__file__).parent / "data/races.csv"
    if os.path.exists(path):
        os.remove(path)
    else:
        print(f"Filen {path} finns inte, borttagningen misslyckades")
        

ScrapeAtg()
RemoveTempFiles()
