#code to convert ING banking csv to format ynab can understand
#place ONLY ing csv files here as this program will try to convert every .csv it can find exept for *_ynab.csv
#writen by Jacco Steegman
import csv #to edit csv files
import os , fnmatch# to find csv's

#important if not in dutch make write the string that indicates a negative value...
modForNegetiveValue = 'Af' #<- ...here

#convert only value to a negative value with correct decimal 
def mutate_moneyFormat(money_str, mod):
    money = float(money_str.replace(',','.'))#convert the , notation to . so python and understands 
    if mod == modForNegetiveValue : #if the mod says it is negative
        return money * -1 #make it negative
    else:
        return money #dont make it negative

# convert :[Datum,Naam / Omschrijving,Rekening,Tegenrekening,Code,Af Bij,Bedrag (EUR),MutatieSoort,Mededelingen]
# to [date, payee, memo, amount]
def mutate_row(str_Array):
    return [
        str_Array[0],#date
        str_Array[1],#Payee
        str_Array[8],#memo
        mutate_moneyFormat(str_Array[6], str_Array[5])#amount
    ]

def find(path):#finds csv files to convert
    result = []#declare array to be returned
    for root, dirs, files in os.walk(path): #get all the files in the path
        for name in files:#for every file in files 
            if fnmatch.fnmatch(name, "*.csv"):#check if it has the  csv patern
                if "_ynab.csv" not in name:#exclude ones that are already converted
                    print(name)
                    result.append(os.path.join(root, name))#add it to the list with full path
    return result


working_dir = os.getcwd()#get working dir for finding every csv file to convert
for openPath in find(working_dir):#for every found path 
    with open(openPath) as csvFile: #open it
        reader = csv.reader(csvFile) #desicnate a reader for it
        
        #make filename
        filelocName = csvFile.name[:-4]#remove the .csv
        filelocName = filelocName + "_ynab.csv" #add _ynab.csv
        print(filelocName)#print new file name

        #make Write file
        with open(filelocName, mode='w') as write_csv_file:
            writer = csv.writer(write_csv_file, dialect='unix')#create handle

            #fill write file
            for row in reader:#for every row in the csv file
                if reader.line_num == 1 :#if it is the first row
                    new_row = ["Date","Payee","Memo","Amount"]#add the ynab tags
                else:#not first row?
                    new_row = mutate_row(row)#mutate it like it says above
                writer.writerow(new_row) #really write it now!

