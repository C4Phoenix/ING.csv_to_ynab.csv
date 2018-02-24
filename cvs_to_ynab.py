#code to convert ING banking csv to format ynab can understand
import os
import csv #to edit csv files
import sys #to get the launch arguments

openPath = "[filename]"#will need convertion if taken from program launch param

def mutate_moneyFormat(money_str, mod):
    money = float(money_str.replace(',','.'))
    if(mod == "Af"):
        return money * -1
    else:
        return money

# Datum,Naam / Omschrijving,Rekening,Tegenrekening,Code,Af Bij,Bedrag (EUR),MutatieSoort,Mededelingen
def mutate_row(str_Array):
    return [
        str_Array[0],#date
        str_Array[1],#Payee
        str_Array[8],#memo
        mutate_moneyFormat(str_Array[6], str_Array[5])#amount
    ]

current_dir = os.getcwd() + "\\"
newFileName = "tempFileName.csv"

with open(openPath) as csvFile:
    reader = csv.reader(csvFile)

    with open(current_dir+ newFileName, mode='w') as write_csv_file:
        writer = csv.writer(write_csv_file, dialect='unix')
        for row in reader:
            if(reader.line_num == 1):#first row needs the tags
                new_row = ["Date","Payee","Memo","Amount"]#format for ynab
            else:
                new_row = mutate_row(row)
            writer.writerow(new_row)
            #print(new_row)    
print(current_dir)
