
from sklearn.model_selection import train_test_split
from sklearn.metrics import balanced_accuracy_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn import tree
from pathlib import Path
import pandas as pd

print("Nu körs python maskininlärning(modellen tränas), vänligen avvakta")

# Läs in historisk data:
path = Path(__file__).parent / "./data/trainingData.csv"
data = pd.read_csv(path)
# Läs in prediktion data:
path = Path(__file__).parent / "./data/nextRaceData.csv"
preddata = pd.read_csv(path)

# Förbered attribut. ta bort(drop) "moneywin", "playpercent", om du vill använda modellen utan att ta hänsyn till hur mycket en häst är spelad.
#Tar bort variabler som inte bedöms relevanta för att erhålla bästa möjliga resultat.
Xpred = preddata.drop(columns=["moneywin","playpercent","racenum","winnernum","horsename","driver","trainer","resrace1","pricesumrace1",
                               "resrace2","pricesumrace2","resrace3","pricesumrace3","resrace4","pricesumrace4","resrace5","pricesumrace5","rp4","rp5"])  


                    # Förbered attribut som ska vara med i maskininlärningen
X = data.drop(columns=["moneywin","playpercent","winner","racenum","winnernum","horsename","driver","trainer","resrace1","pricesumrace1",
                       "resrace2","pricesumrace2","resrace3","pricesumrace3","resrace4","pricesumrace4","resrace5","pricesumrace5","rp4","rp5"]) 
y = data["winner"]  # Målvariabel: Har värde 1 eller 0, 1 om hästen vann annars 0.

# Dela upp data i tränings- och testuppsättningar
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01, random_state=42)

                                                                                           
# Tränar flera modeller och använder summan av alla prediktioner i slutresultet.          # Jag har provat flera algoritmer(modeller) från
models = {                                                                                # scikit men fått bäst resultat med dessa 3:
  "Random Forest": RandomForestClassifier(max_depth=6,n_estimators=150, random_state=42),
  "Gradient Boosting": GradientBoostingClassifier(max_depth=6,n_estimators=200, random_state=42),
  "Decision Tree": tree.DecisionTreeClassifier(max_depth=6,random_state=42)
}


sumDict = {}    # addera sannolikhet för att häst vinner i sumDict
modelNumber = 0
for model_name, model in models.items():
    
    calibrated_model = CalibratedClassifierCV(model, method='sigmoid')
    calibrated_model.fit(X_train, y_train)

    # Gör prediktioner på testuppsättningen för att få träffsäkerheten på modellen.
    y_pred_proba = calibrated_model.predict_proba(X_test)
    # Gör prediktioner på min prediktion data
    yy_pred_proba = calibrated_model.predict_proba(Xpred)
 
    trotrace = {}
    horsenum = 1
    racenum = 1
    for i, (prob, startnum) in enumerate(zip(yy_pred_proba, Xpred['startnum'])):
        
        if startnum < horsenum: #new racenum
            racenum += 1
        trotrace[int(f"{racenum}{startnum}")] = round(prob[1]*100,1)
        if modelNumber == 0:
          sumDict[int(f"{racenum}{startnum}")] = round(prob[1]*100,2)
        else:
          tempPercent = sumDict[int(f"{racenum}{startnum}")]
          sumDict[int(f"{racenum}{startnum}")] = round(round(prob[1]*100,2) + tempPercent,1)
        horsenum = startnum
    modelNumber += 1              

    print(f"Modell: {model_name}")
    # Utvärdera modellen med "balanced_accuracy_score"
    accuracy = balanced_accuracy_score(y_test, y_pred_proba.argmax(axis=1))
    print(f"Träffsäkerhet: {accuracy:.2f}\n")

trotrace = dict(sumDict)
sorted_dict = dict(sorted(trotrace.items(), key=lambda item: (int(str(item[0])[0]), -item[1])))

if racenum == 8: #För v86, 8 lopp
  printList = ["Lopp 1:		Lopp 2:		Lopp 3:		Lopp 4:		Lopp 5:		Lopp 6:		Lopp 7:		Lopp 8:    ","","","","","","","","","","","","","","",""]
elif racenum == 6: #För v64, 6 lopp:
  printList = ["Lopp 1:		Lopp 2:		Lopp 3:		Lopp 4:		Lopp 5:		Lopp 6:                            ","","","","","","","","","","","","","","",""]
else:
  printList = ["Lopp 1:		Lopp 2:		Lopp 3:		Lopp 4:		Lopp 5:		Lopp 6:		Lopp 7:                ","","","","","","","","","","","","","","",""]

racenum = "1"
Listindex = 0
print("________________________________________________________________________________________________________________________________\n")
print("Första siffran i respektive lopp anger hästnummer och" +
      " andra siffran anger vinstchansen(ju större siffa ju större vinstchans).\n" +
      "\n                                           ***Lycka till!!!***")
print("________________________________________________________________________________________________________________________________")
for horseNum, percent in sorted_dict.items():     
  if racenum != str(horseNum)[0]:
    # print(f"Lopp {str(horseNum)[0]}:")
    while Listindex < 15:
        #printList[Listindex + 1] = printList[Listindex + 1] + "                "
        printList[Listindex + 1] = printList[Listindex + 1] + "		"
        Listindex += 1

    Listindex = 1
  
  else:
      Listindex += 1  
  printList[Listindex] = printList[Listindex] + ("{} \t{}\t".format(str(horseNum)[1:], percent))
  racenum = str(horseNum)[0]

#Printar ut resultatet
i = 0
while i < 16:  
  print(printList[i])
  i += 1  
print("________________________________________________________________________________________________________________________________")

#Sparar undan resultatet i en fil
path = Path(__file__).parent / "data/resultData.txt"
with path.open('w+') as file:
    for item in printList:
        file.write(item+"\n")