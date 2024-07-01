import csv
from collections import defaultdict

# returns a list of dictionarys that contain deficit data for almost every day 
def loadDeficitData(path):
    data = []

    with open(path, encoding = 'utf-8') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter = ',')    
        
        for row in csv_reader:
            data.append(row)
    
    return data

def selectMonthlyData(data, month, year):
    monthlyData = []
    for row in data:
        #print(int(row['Calendar Quarter Number']))
        if (int(row['Calendar Year']) == year and int(row['Calendar Month Number']) == month):
            monthlyData.append(row)
    return monthlyData

#returns monthly public debt, Intragovernmental Holdings and total (public) debt
def calculateDeficits(data):
    last = data[len(data)-1]
    first = data[0]
    #print(first)
    #print(last)
    monthlyPublicDebt = float(first['Debt Held by the Public']) - float(last['Debt Held by the Public'])
    monthlyIntagovHoldings = float(first['Intragovernmental Holdings']) - float(last['Intragovernmental Holdings'])
    monthlyTotalDebt = float(first['Total Public Debt Outstanding']) - float(last['Total Public Debt Outstanding'])
    return monthlyPublicDebt, monthlyIntagovHoldings, monthlyTotalDebt


class EconEntity:
    def __init__(self, name, money):
        self.name = name
        self.money = money
    
    def pay(self, recipient, amount):
        self.money -= amount
        recipient.money += amount
        print(f"{self.name} gave {recipient.name} ${amount}.")

    def balance(self):
        print(f"{self.name} has ${self.money}.")


def startTreasury(treasury, fed, 
                  govSpending, socialSecurity, tsyInterestBanks, tsyInterestFed, tsyInterestHouse):
    # Treasury -> FED Transactions
    treasury.pay(fed, govSpending)
    treasury.pay(fed, socialSecurity)
    treasury.pay(fed, tsyInterestBanks)
    treasury.pay(fed, tsyInterestFed)
    treasury.pay(fed, tsyInterestHouse)

def startFED(fed, treasury, banks, 
             firmTax, bankTax, houseTax, openMarketOperations, houseBuysTsy, profitReturnsToTsy,   
             govSpending, socialSecurity, tsyInterestBanks, tsyInterestHouse):
    # FED -> Treasury Transactions
    fed.pay(treasury, firmTax)
    fed.pay(treasury, bankTax)
    fed.pay(treasury, houseTax)
    fed.pay(treasury, openMarketOperations)
    fed.pay(treasury, houseBuysTsy)
    fed.pay(treasury, profitReturnsToTsy)

    # FED -> Banks Transactions
    fed.pay(banks, govSpending)
    fed.pay(banks, socialSecurity)
    fed.pay(banks, tsyInterestBanks)
    fed.pay(banks, tsyInterestHouse)

def startBanks(banks, fed, firms, households, 
             firmTax, bankTax, houseTax, openMarketOperations, houseBuysTsy,  
             govSpending, issueLoanFirms, householdsConsume,
             socialSecurity, tsyInterestHouse, issueLoanHouse, paysHouseholds):
    # Banks -> FED Transactions
    banks.pay(fed, firmTax)
    banks.pay(fed, bankTax)
    banks.pay(fed, houseTax)
    banks.pay(fed, openMarketOperations)
    banks.pay(fed, houseBuysTsy)

    # Banks -> Firms Transactions
    banks.pay(firms, govSpending)
    banks.pay(firms, issueLoanFirms)
    banks.pay(firms, householdsConsume)

    # Banks -> Households Transactions
    banks.pay(households, socialSecurity)
    banks.pay(households, tsyInterestHouse)
    banks.pay(households, issueLoanHouse)
    banks.pay(households, paysHouseholds)

def startFirms(firms, banks, 
               firmTax, firmLoanPaymentWithInterest, paysHouseholds):
    # Firms -> Banks Transactions
    firms.pay(banks, firmTax)
    firms.pay(banks, firmLoanPaymentWithInterest)
    firms.pay(banks, paysHouseholds)

def startHouseholds(households, banks, 
               houseTax, houseBuysTsy, houseLoanPaymentWithInterest, householdsConsume):
    # Households -> Banks Transactions
    households.pay(banks, houseTax)
    households.pay(banks, houseBuysTsy)
    households.pay(banks, houseLoanPaymentWithInterest)
    households.pay(banks, householdsConsume)

    
def plusSign(number):
    if number > 0:
        return "+"
    
def showInBillions(number):
    number //= 10**2
    number /= 10**7
    return "$" + str(number) + " B"

def main():
    
    # initializing of economic entities for the SFC model
    fed = EconEntity("Federal Reserve (FED)", 0)
    treasury = EconEntity("US Treasury", 0)
    banks = EconEntity("Banking sector", 0)
    firms = EconEntity("Firm sector", 0)
    households = EconEntity("Household sector", 0)

    # initializing variables

    # Treasury variables
    factor = 10**9
    govSpending = factor * (10)  
    socialSecurity = factor * (8) 
    tsyInterestBanks = factor * (2)
    tsyInterestFed = factor * (2)
    tsyInterestHouse = factor * (1)
    openMarketOperations = factor * (3) 

    # FED variables
    profitReturnsToTsy = factor * (1)

    # Banks variables
    issueLoanFirms = factor * (2)
    issueLoanHouse = factor * (2)

    # Firms variables
    paysHouseholds = factor * (3)
    firmLoanPaymentWithInterest = factor * (5)

    # Households variables
    houseBuysTsy = factor * (1 + 1)
    householdsConsume = factor * (5)
    houseLoanPaymentWithInterest = factor * (4)

    # Taxes
    firmTax = factor * (1)
    bankTax = factor * (1)
    houseTax = factor * (2)

    publicDebt = - (firmTax + bankTax + houseTax + profitReturnsToTsy - govSpending - socialSecurity - tsyInterestBanks - tsyInterestFed - tsyInterestHouse)

    startTreasury(treasury, fed, 
                  govSpending, socialSecurity, tsyInterestBanks, tsyInterestFed, tsyInterestHouse)
    
    startFED(fed, treasury, banks, 
             firmTax, bankTax, houseTax, openMarketOperations, houseBuysTsy, profitReturnsToTsy,   
             govSpending, socialSecurity, tsyInterestBanks, tsyInterestHouse)
    
    startBanks(banks, fed, firms, households, 
             firmTax, bankTax, houseTax, openMarketOperations, houseBuysTsy,  
             govSpending, issueLoanFirms, householdsConsume,
             socialSecurity, tsyInterestHouse, issueLoanHouse, paysHouseholds)
    
    startFirms(firms, banks, 
               firmTax, firmLoanPaymentWithInterest, paysHouseholds)
    
    startHouseholds(households, banks, 
               houseTax, houseBuysTsy, houseLoanPaymentWithInterest, householdsConsume)
    
    print("\nBalance of each economic entity:")
    fed.balance()
    treasury.balance()
    banks.balance()
    firms.balance()
    households.balance()

    print("Public Debt for given model:", showInBillions(publicDebt))



    # Real world US deficits

    # data loading
    path = "Seminar 2/Deficit_data/DebtPenny.csv"
    data = loadDeficitData(path)
    #print(data)

    # select deficit data for specific month of a given year between 2019 and 2024
    month = 4
    year = 2021

    monthlyData = selectMonthlyData(data, month, year)
    #print(monthlyData)
    
    # calculate monthly increase or decrease in debt for given month
    monthlyPublicDebt, monthlyIntagovHoldings, monthlyTotalDebt = calculateDeficits(monthlyData)

    print(f"\nMonthly change of Public Debt for the {month}th month of {year}: {plusSign(monthlyPublicDebt)} {showInBillions(monthlyPublicDebt)}")
    print(f"Monthly change of Intragovernmental Holdings for the {month}th month of {year}: {plusSign(monthlyIntagovHoldings)} {showInBillions(monthlyIntagovHoldings)}")
    print(f"Monthly change of Total Debt for the {month}th month of {year}: {plusSign(monthlyTotalDebt)} {showInBillions(monthlyTotalDebt)}")
    

main()