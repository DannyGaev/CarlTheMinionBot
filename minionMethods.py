from locale import currency
from operator import truediv
import random
import os
from minion import *
import datetime
import math
from typing import Optional

def makeTheMinion(name,forWhoSave):
    currentCwd = os.getcwd()
    keys_list = list(minions)
    index = random.randint(0, len(minions))
    index2 = random.randint(0, len(minions))
    minionName = keys_list[index-1]
    key2 = keys_list[index2-1]
    link = minions[key2]
    tokens = 30
    os.chdir(r"minionFiles")
    try:
        with open(f'{name}minion.txt', 'r') as minionFile:
            tokens = minionFile.readline().rstrip()
    except:
        pass
    with open(f'{name}minion.txt', 'w') as minionFile:
        minionFile.write(f"{tokens}\n{idGen()}\n{link}\n{minionName}\n0\n100\n20\n20")
    os.chdir(currentCwd)
    os.chdir("itemFiles")
    try:
        with open(f'{name}items.txt','r') as itemFile:
            print("file existed")
    except:
        with open(f'{name}items.txt','w') as itemFile:
            itemFile.write("0\n0\n0\n0")
            print("making file")
    os.chdir(currentCwd)
    with open("whohasMinion.txt", "r") as whoHasFile:
        allNames = whoHasFile.read().splitlines()
    with open("whoHasMinion.txt", "a") as whohasFile:
        if forWhoSave not in allNames:
            whohasFile.write(f"\n{forWhoSave}")
    return "Your Minion has been created! Use the '!get' command to view it!"

def getTheMinion(name):
    currentCwd = os.getcwd()
    os.chdir(r"minionFiles")
    with open(f'{name}minion.txt', 'r+') as minionFile:
        items = minionFile.readlines()
        theId = items[1]
        imageLink = items[2]
        name = items[3]
        minionLevel = items[4]
        minionHealth = items[5]
        minionDefense = items[6]
        minionAttack = items[7]
        os.chdir(currentCwd)
        return theId, imageLink, name, minionLevel, minionHealth, minionDefense, minionAttack
    
def amountTokens(name):
    currentCwd = os.getcwd()
    os.chdir(r"minionFiles")
    with open(f'{name}minion.txt', 'r+') as minionFile:
        items = minionFile.readlines()
        availableTokens = items[0]
        os.chdir(currentCwd)
        return availableTokens

def dailyTokens(name):
    generalDate = datetime.datetime.now()
    currentDate = generalDate.strftime("%x")
    currentCwd = os.getcwd()
    os.chdir(r"redeemFiles")
    try:
        with open(f'{name}redeem.txt', 'r+') as redeemFile:
            previousDate = redeemFile.readline().rstrip()
    except:
        with open(f'{name}redeem.txt', 'w') as redeemFile:
            date = datetime.datetime.now()
            redeemFile.write(date.strftime("%x"))
            previousDate = "0/0/0"
    os.chdir(currentCwd)
    if previousDate != currentDate:
        os.chdir(r"minionFiles")
        with open(f'{name}minion.txt', 'r+') as minionFile:
            items = minionFile.readlines()
            availableTokens = int(float(items[0]))
            with open(f'{name}minion.txt', 'w') as minionFile:
                availableTokens += 50
                minionFile.write(str(availableTokens)+"\n"+''.join(items[1:]))
                os.chdir(currentCwd)
                return "You've claimed your daily tokens!"
    else:
        os.chdir(currentCwd)
        return "Sorry, you've already claimed your daily tokens!"


def checkIfCanBuy(wantToSpend, name):
    currentCwd = os.getcwd()
    os.chdir(r"minionFiles")
    print(f"Cost during checking: {wantToSpend}")
    with open(f'{name}minion.txt', 'r+') as minionFile:
        items = minionFile.readlines()
        tokens = int(float(items[0]))
        print(f"Have: {tokens}, Want to Spend: {wantToSpend}")
    if int(wantToSpend) > tokens:
        os.chdir(currentCwd)
        return False
    else:
        os.chdir(currentCwd)
        return True
    
def checkIfUserHasMinion(targetToAttack):
    currentCwd = os.getcwd()
    os.chdir(r"minionFiles")
    ifFileExists = os.path.exists(f"{targetToAttack}minion.txt")
    os.chdir(currentCwd)
    return ifFileExists

def buyItem(cost,amount,name,itemName):
    currentCwd = os.getcwd()
    leveledUp = False
    os.chdir(r"minionFiles")
    with open(f'{name}minion.txt', 'r+') as minionFile:
        items = minionFile.readlines()
        availableTokens = int(float(items[0]))
        with open(f'{name}minion.txt', 'w') as minionFile:
            availableTokens -= cost
            minionFile.write(str(availableTokens)+"\n"+''.join(items[1:]))
            os.chdir(currentCwd)
        os.chdir("itemFiles")
        try:
            with open(f'{name}items.txt','r') as itemFile:
                print("file existed")
        except:
            with open(f'{name}items.txt','w') as itemFile:
                itemFile.write("0\n0\n0\n0")
                print("making file")
        with open(f'{name}items.txt', 'r') as itemFile:
            allThings = itemFile.readlines()
            bananaNum = int(allThings[0])
            fartGunNum = int(allThings[1])
            petRockNum = int(allThings[2])
            gruJellyNum = int(allThings[3])
        with open(f'{name}items.txt', 'w') as itemFile:
            if itemName == "banana":
                newBananaNum = bananaNum + amount
                highBananaNum = bananaNum + (newBananaNum - bananaNum)
                isHigherThanFive = bananaNum + (newBananaNum - bananaNum) >= 5
                bananaNum += amount
                if(bananaNum % 5 == 0 and bananaNum != 0) or isHigherThanFive:
                    os.chdir(currentCwd) 
                    theValue = (highBananaNum-5)/5
                    # if theValue < 0:
                    #     changingBy = (5*math.ceil(((highBananaNum-5)/5)))
                    # else:
                    changingBy = (5*math.floor(((highBananaNum-5)/5)))
                    bananaNum -= changingBy
                    os.chdir(r"minionFiles")
                    with open(f'{name}minion.txt', 'r') as minionFile:
                        thingsFromFile = minionFile.readlines()
                        print("getting minion level")
                        minionLevel = int(thingsFromFile[4])
                        print("got minion level")
                    with open(f'{name}minion.txt', 'w') as minionFile: #+(int(changingBy/5))
                        print("adding levels")
                        minionFile.write(''.join(thingsFromFile[0:4])+f"{str(minionLevel)}\n"+''.join(thingsFromFile[5:]))
                        leveledUp = True
                        os.chdir(currentCwd)
                        os.chdir(r"itemFiles")
                os.chdir(r"itemFiles")
            elif itemName == "fart gun":
                fartGunNum+=amount
            elif itemName == "pet rock":
                petRockNum+=amount
            elif itemName == "gru jelly":
                gruJellyNum+=amount
            itemFile.write(f"{str(bananaNum)}\n{str(fartGunNum)}\n{str(petRockNum)}\n{str(gruJellyNum)}")
            os.chdir(currentCwd)
            return "Successfully purchased", leveledUp

def checkInventory(name):
    currentCwd = os.getcwd()
    os.chdir(r"itemFiles")
    try:
        with open(f'{name}items.txt', 'r') as itemFile:
            allThings = itemFile.readlines()
            bananaNum = int(allThings[0])
            fartGunNum = int(allThings[1])
            petRockNum = int(allThings[2])
            gruJellyNum = int(allThings[3])
            os.chdir(currentCwd)
            return bananaNum, fartGunNum, petRockNum, gruJellyNum
    except:
        with open(f'{name}items.txt','w') as itemFile:
            itemFile.write("0\n0\n0\n0")
            return 0, 0, 0, 0
    
def haveEnough(quantity,name):
    currentCwd = os.getcwd()
    os.chdir(r"itemFiles")
    with open(f'{name}items.txt', 'r+') as itemFile:
        allItems = itemFile.readlines()
        fartGuns = int(allItems[1])
    os.chdir(currentCwd)
    if fartGuns >= quantity:
        return True
    else:
        return False

def isAlive(name):
    currentCwd = os.getcwd()
    os.chdir(r'minionFiles')
    with open(f'{name}minion.txt', 'r+') as minionFile:
        items = minionFile.readlines()
        health = int(items[5])
        if health <= 0:
            os.chdir(currentCwd)
            return False
        os.chdir(currentCwd)
        return True

def attackUser(targetName,name,fartGunNum:Optional[int]=0):
    currentCwd = os.getcwd()
    os.chdir(r"minionFiles")
    with open(f'{targetName}minion.txt', 'r+') as minionFile:
        items = minionFile.readlines()
        enemyMinionHealth = int(items[5])
        enemyMinionDefense = int(items[6])
        enemyMinionAttack = int(items[7])
    with open(f'{name}minion.txt', 'r+') as minionFile:
        items = minionFile.readlines()
        userMinionAttack = int(items[7])
    os.chdir(currentCwd)
    os.chdir(r"itemFiles")
    with open(f'{targetName}items.txt', 'r') as itemFile:
        allThings = itemFile.readlines()
        enemyPetRockNum = int(allThings[2])
    os.chdir(currentCwd)
    enemyMinionDefense += enemyPetRockNum*20
    userMinionAttack += fartGunNum*20
    startingDefense = enemyMinionDefense
    petRockToRemove = 0
    if enemyMinionDefense > 0:
        enemyMinionDefense -= userMinionAttack
        difference = startingDefense-enemyMinionDefense
        if difference >= 20:
            while difference > 0:
                difference -= 20
                petRockToRemove+=1
        if enemyMinionDefense <= 0:
            enemyMinionHealth += enemyMinionDefense
            enemyMinionDefense = 0
    else:
        enemyMinionHealth -= userMinionAttack
    os.chdir(r"minionFiles")
    with open(f'{targetName}minion.txt', 'r') as minionFile:
        items = minionFile.readlines()
    with open(f'{targetName}minion.txt', 'w') as minionFile:
        minionFile.write(''.join(items[0:5])+f"{enemyMinionHealth}\n{enemyMinionDefense}\n{enemyMinionAttack}")

    os.chdir(currentCwd)
    if enemyMinionHealth <= 0:
        os.chdir(r"minionFiles")
        with open(f'{targetName}minion.txt', 'r+') as minionFile:
            enemyItems = minionFile.readlines()
            enemyTokens = int(float(enemyItems[0]))

        toRecieve = enemyTokens * .3

        with open(f'{name}minion.txt', 'r+') as minionFile:
            items = minionFile.readlines()
            availableTokens = int(float(items[0]))
            availableTokens += toRecieve

        enemyTokens -= toRecieve

        with open(f'{targetName}minion.txt', 'w') as minionFile:
            minionFile.write(str(enemyTokens)+"\n"+''.join(enemyItems[1:]))

        with open(f'{name}minion.txt', 'w') as minionFile:
            minionFile.write(str(availableTokens-5)+"\n"+''.join(items[1:]))

        os.chdir(currentCwd)
        subtractFartGuns(fartGunNum,name)
        subtractPetRocks(petRockToRemove,targetName)
        return f"Defeated {targetName}'s Minion! You recieved {toRecieve} tokens", f"You did {userMinionAttack} damage!"
    else:
        os.chdir(currentCwd)
        subtractFartGuns(fartGunNum,name)
        subtractPetRocks(petRockToRemove,targetName)
        return f"{targetName}'s Minion has {enemyMinionDefense} defense points left, and {enemyMinionHealth} health points left!",f"You did {userMinionAttack} damage!"
        

def subtractPetRocks(amount,name):
    currentCwd = os.getcwd()
    os.chdir(r'itemFiles')
    with open(f'{name}items.txt', 'r') as itemsFile:
        allThings = itemsFile.readlines()
        fartGuns = int(allThings[2])
    with open(f'{name}items.txt', 'w') as itemsFile:
        print("sutracting fart guns")
        if (fartGuns - amount) < 0:
            amount = fartGuns
        itemsFile.write(''.join(allThings[0:2])+f"{fartGuns-amount}\n"+''.join(allThings[3:]))
    os.chdir(currentCwd)

def subtractFartGuns(amount,name):
    currentCwd = os.getcwd()
    os.chdir(r'itemFiles')
    with open(f'{name}items.txt', 'r') as itemsFile:
        allThings = itemsFile.readlines()
        fartGuns = int(allThings[1])
    with open(f'{name}items.txt', 'w') as itemsFile:
        print("sutracting fart guns")
        itemsFile.write(''.join(allThings[0:1])+f"{fartGuns-amount}\n"+''.join(allThings[2:]))
    os.chdir(currentCwd)

def sellTheItem(name,amount,itemName):
    currentCwd = os.getcwd()
    os.chdir(r"minionFiles")
    with open(f"{name}minion.txt", "r") as minionFile:
        items = minionFile.readlines()
        tokens = int(float(items[0]))
        os.chdir(currentCwd)
    os.chdir(r"itemFiles")
    with open(f"{name}items.txt", "r") as itemFile:
        inv = itemFile.readlines()
        bananaNum = int(inv[0])
        fartGunNum = int(inv[1])
        petRockNum = int(inv[2])
        gruJellyNum = int(inv[3])
        os.chdir(currentCwd)
    if itemName == "banana":
        if bananaNum >= int(amount):
            bananaNum -= int(amount)
            tokens += (int(amount)*10)
            decreaseQuantity(name,bananaNum,fartGunNum,petRockNum,gruJellyNum)
            addTokens(name,tokens)
            return f"Sold {amount} bananas!"
        else:
            return "You don't have enough Bananas to sell that many!"
    elif itemName == "fart gun":
        if fartGunNum >= int(amount):
            fartGunNum -= int(amount)
            tokens += (int(amount)*30)
            decreaseQuantity(name,bananaNum,fartGunNum,petRockNum,gruJellyNum)
            addTokens(name,tokens)
            return f"Sold {amount} fart guns!"
        else: 
            return "You don't have enough Fart Guns to sell that many!"
    elif itemName == "pet rock":
        if petRockNum >= int(amount):
            petRockNum -= int(amount)
            tokens += (int(amount)*30)
            decreaseQuantity(name,bananaNum,fartGunNum,petRockNum,gruJellyNum)
            addTokens(name,tokens)
            return f"Sold {amount} pet rocks!"
        else:
            return "You don't have enough Pet Rocks to sell that many!"
    elif itemName == "gru jelly":
        if gruJellyNum >= int(amount):
            gruJellyNum -= int(amount)
            tokens += (int(amount)*10)
            decreaseQuantity(name,bananaNum,fartGunNum,petRockNum,gruJellyNum)
            addTokens(name,tokens)
            return f"Sold {amount} Gru's Jellies!"
        else:
            return "You don't have enough Gru's Jellies to sell that many!"

def decreaseQuantity(name,item1,item2,item3,item4):
    currentCwd = os.getcwd()
    os.chdir(r"itemFiles")
    with open(f"{name}items.txt", "w") as itemFile:
        itemFile.write(f"{item1}\n{item2}\n{item3}\n{item4}")
        os.chdir(currentCwd)

def addTokens(name,quantity):
    currentCwd = os.getcwd()
    os.chdir(r"minionFiles")
    with open(f"{name}minion.txt", "r") as minionFile:
        allItems = minionFile.readlines()
    with open(f"{name}minion.txt", "w") as minionFile:
        minionFile.write(f"{int(float(allItems[0]))+int(quantity)}\n"+''.join(allItems[1:]))
        os.chdir(currentCwd)

def subtractTokens(name,quantity):
    currentCwd = os.getcwd()
    os.chdir(r"minionFiles")
    with open(f"{name}minion.txt", "r") as minionFile:
        allItems = minionFile.readlines()
    with open(f"{name}minion.txt", "w") as minionFile:
        minionFile.write(f"{int(float(allItems[0]))-int(quantity)}\n"+''.join(allItems[1:]))
        os.chdir(currentCwd)

def donateTokens(amount,donateTo,donateFrom):
    currentCwd = os.getcwd()
    addTokens(donateTo,amount)
    subtractTokens(donateFrom,amount)
    os.chdir(currentCwd)
    return f"{donateTo} recieved {amount} tokens from {donateFrom}!"
    

def playRockPaperScissors(choice):
    options = ["rock","paper","scissors"]
    compChoice = random.choice(options)
    if choice.lower() == "rock" and compChoice == "scissors":
        return f"I chose {compChoice}... you win!", True, False
    elif choice.lower()=="scissors" and compChoice == "paper":
        return f"I chose {compChoice}... you win!", True, False
    elif choice.lower()=="paper" and compChoice == "rock":
       return f"I chose {compChoice}... you win!", True, False
    elif choice.lower() == compChoice:
        return f"I chose {compChoice}... it's a tie!", False, True
    else:
        return f"I chose {compChoice}... you lose!", False, False

def playSlots():
    options = ["Evil","Kevin","Stuart"]
    rolls = []
    for x in range(0,3):
        rolls.append(random.choice(options))
    threeOfAKind = False
    threeOfAKind = rolls.count(rolls[0]) == len(rolls)
    return threeOfAKind, rolls[0], rolls[1], rolls[2]

def playCoinFlip():
    value =random.randint(0,1)
    return value

def subtractAmount(amount,name):
    currentCwd = os.getcwd()
    os.chdir(r"minionFiles")
    with open(f"{name}minion.txt", "r") as minionFile:
        items = minionFile.readlines()
        tokenAmount = int(float(items[0]))
    newAmount = int(amount)
    finalAmount = tokenAmount - newAmount
    with open(f"{name}minion.txt", "w") as minionFile:
        minionFile.write(f"{str(finalAmount)}\n"+''.join(items[1:]))
    os.chdir(currentCwd)

def addAmount(amount,name):
    currentCwd = os.getcwd()
    os.chdir(r"minionFiles")
    with open(f"{name}minion.txt", "r") as minionFile:
        items = minionFile.readlines()
        tokenAmount = int(float(items[0]))
    newAmount = float(amount)*1.5
    finalAmount = tokenAmount + newAmount
    with open(f"{name}minion.txt", "w") as minionFile:
        minionFile.write(f"{str(finalAmount)}\n"+''.join(items[1:]))
    os.chdir(currentCwd)

def idGen():
    id = ""
    for x in range(6):
        num = random.randint(0,1)
        if(num==0):
            id += randLetter()
        else:
            id += randNum()
    return id
    

def randLetter():
    letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    return random.choice(letters)

def randNum():
    numbers = ["0","1","2","3","4","5","6","7","8","9"]
    return random.choice(numbers)
