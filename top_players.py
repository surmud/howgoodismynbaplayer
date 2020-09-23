from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import matplotlib.pyplot as plt



def displayStats(category, playerName, driver):
    if(category == "points"):
        driver.get("https://www.basketball-reference.com/leaders/pts_career.html")
        chart = driver.find_element_by_id("nba")

    elif(category == "assists"):
        driver.get("https://www.basketball-reference.com/leaders/ast_career.html")
        chart = driver.find_element_by_id("nba")
    elif(category == "rebounds"):
        driver.get("https://www.basketball-reference.com/leaders/trb_career.html")
        chart = driver.find_element_by_id("nba")
    
    elif category == "steals":
        driver.get("https://www.basketball-reference.com/leaders/stl_career.html")
        chart = driver.find_element_by_id("nba")
        
    elif category == "blocks":
        driver.get("https://www.basketball-reference.com/leaders/blk_career.html")
        chart = driver.find_element_by_id("nba")
        
    chartText = chart.text
    chartList = chartText.split("\n")
    playersList = []
    statsList = []
    file = open(category+".txt", "w")
  
    #iterate through the list and split each entry by it's whitespace
    #add each entry into it's own list
    for i in range(len(chartList)):
        chartList[i] = chartList[i].split(" ") 
        #print(chartList[i])
        playerIgnoreText = chartList[0][1]

        #add to the player list
        if(chartList[i][1] != playerIgnoreText and chartList[i][1] != ""):
            #add the first name concatenated with the last name
            nameToAdd = chartList[i][1] + " " + chartList[i][2]
            nameToAdd = nameToAdd.replace("*", "")
            playersList.append(nameToAdd)
            file.write(nameToAdd+" ")
            statsList.append(chartList[i][len(chartList[i]) - 1])
            file.write(str(chartList[i][len(chartList[i]) - 1])+"\n")
        #handle the case where some players don't have a number in the beginning
        elif chartList[i][0] == "":
            nameToAdd = chartList[i][3] + " " + chartList[i][4]
            nameToAdd = nameToAdd.replace("*", "") #remove the * from the names of players who are retired
            playersList.append(nameToAdd) #add the player to the list
            file.write(nameToAdd+ " ")
            statsList.append(chartList[i][len(chartList[i]) - 1])
            file.write(str(chartList[i][len(chartList[i]) - 1])+"\n")
        

    file = file.close()
    isFound = False
    for i in range(len(playersList)):
        if(playerName.upper() == playersList[i].upper()):
            print(playersList[i], "is number", i+1, "for the most", category, "all-time")
            isFound = True
            return statsList[i]
        #print(str(i + 1)+".", playersList[i])
    if isFound == False:
        #print(playerName, "wasn't found in the top 250 for", category)
        return False


def main():

    
    playerName = input("Enter in the name of the player: ")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    driver = webdriver.Chrome(options=options)

    #chrome_options = webdriver.ChromeOptions()
    #driver = webdriver.Chrome()

    #print("loading...\n")
    
    statsList = []
    
    ptsFoundOrNah = displayStats("points", playerName, driver)
    astsFoundOrNah = displayStats("assists", playerName, driver)
    rebsFoundOrNah = displayStats("rebounds", playerName, driver)
    stlsFoundOrNah = displayStats("steals", playerName, driver)
    blksFoundOrNah = displayStats("blocks", playerName, driver)
    driver.quit()
    
    if ptsFoundOrNah == False and astsFoundOrNah == False and\
        rebsFoundOrNah == False and stlsFoundOrNah == False and\
        blksFoundOrNah == False:

        print(playerName, "wasn't found in any category")
        print(playerName, "is either a terrible player or you spelled his name wrong.")
    else:
        statsList.append(int(ptsFoundOrNah))
        statsList.append(int(rebsFoundOrNah))
        statsList.append(int(astsFoundOrNah))
        statsList.append(int(blksFoundOrNah))
        statsList.append(int(stlsFoundOrNah))
     
        #playerStats = {"Player Name": playerName, "Points": ptsFoundOrNah}
   
        #print(playerStats)


        plt.bar(["points", "rebounds", "assists", "blocks", "steals"], statsList)
        #plt.plot(playerData)
        plt.title(playerName + "'s all-time stats")
        plt.ylabel("amount in category")
        plt.show() 
    
main()