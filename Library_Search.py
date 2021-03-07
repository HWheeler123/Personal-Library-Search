"""
Notes

To Do
     Make this an app for my phone.

     Add a section that extracts author/title from physical book
         Add to excel sheet
    
     Add a server for file updates via raspberry pi
         checks whether file is up to date
             newest date or whether the entries are the same?
                 if local is better
                     upload newest file
                 if server is better
                     download newest file
"""

import csv
import pandas as pd  #Used for the acronyms
import string

import cv2 #Used for image extraction
import pytesseract as pyt #Used for image extraction

#%% Global Variables

#Globabl variables corresponding to the appropriate column
author = 0
title = 1
series = 2
genres = 7


#Initial Load
pyt.pytesseract.tesseract_cmd = 'C:\\Users\\MyPC\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'

#%% CSV Loader
def CSV_Load():
    global csv_f
    csv_f = csv.reader(open('Library.csv'))
    return csv_f


#%% Server Interface
#Future home of server updates    


#%% Addition to Excel Sheet


#%% Image Extraction

#Code gotten from https://www.geeksforgeeks.org/text-detection-and-extraction-using-opencv-and-ocr/
def extractor():

    #Read image and convert to grayscale
    img = cv2.imread("sample.jpg")
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #Threshold setup
    ret, thresh1 = cv2.threshold(gray_img, 0, 255, cv2.THRESH_OTSU| cv2.THRESH_BINARY_INV)
    
    #Changing (18,18) to smaller values detects smaller targets, ie (10, 10) detects words
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
    
    #Finds contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    #Copies image
    img2 = img.copy()
    
    
    #Create a text file
    file = open("Detected_Txt.txt", "w+") #Opens in flush mode
    file.write("")
    file.close()
    
    #Loops through contours and passes to pytesseract to extract and write to the file.
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        rect = cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #Crops text for OCR
        cropped = img2[y:y+h, x:x+w]
        #file = open("Detected_Txt.txt", "a") #Opens in append mode
        
        #Applies OCR
        text = pyt.image_to_string(cropped)
        text.replace('\f', '')
        
        file = open("Detected_Txt.txt", "a") #Opens in append mode
        file.write(text + "\n")
        
        file.close()

#%% First User input
    
#Takes the user input, cleans it, and searches for tagged information
def user_input_First():
    
    print('Type Author(A), Title(T), Series(S), Partial Search(P), Other(O)): ')
    raw_input = input()
    
    #Sanitize the inputs
    clean_ui = raw_input.lower()
    
    #For Other Menu
    if clean_ui == "o":
        print('Type Genre(G), Total(Total), Acronyms(AC): ')
        raw_input = input()
        clean_ui = raw_input.lower()
    return clean_ui


#%% Second User Input
    
# Takes First input and asks for the appropriate section.
def user_input_Second(clean_ui, search):
    
    #For grammatical purposes
    if clean_ui == "ac":
        search_phrase = ""
    elif clean_ui == "a":
        print("Enter an", search, "here: ")
        search_phrase = input()
    elif clean_ui == "total":
        search_phrase = ""
    else:
        print("Enter a", search, "here: ")
        search_phrase = input()
    
    clean_search = search_phrase.lower()
    
    return clean_search


#%% Main Search Function
    
# Main Search Function.  Houses search_sub and search_all.
def Search(clean_ui, search_phrase):
    if clean_ui == "a":
        search_sub(author, search_phrase)
    elif clean_ui == "t":
        search_sub(title, search_phrase)
    elif clean_ui == "s":
        search_sub(series, search_phrase)
    elif clean_ui == "p":
        search_all(search_phrase)
    elif clean_ui == "g":
        search_sub(genres, search_phrase)
    elif clean_ui == "total":  #Total Number of books
        i = 0
        for row in csv_f:
            i = i + 1
        print("There are", i-1, "books.")
    elif clean_ui == "ac":
        AC_Table()
    else:
        print("Search Invalid.")


#%% Tag Menu

#Looks for correpsonding tag and gives more information.  Sets error flag to false if it has a tag.  Search feeds into Second user input.
def Tag_Menu(clean_ui):
    global author
    global title 
    global series
    global genres
    search = ""
    if clean_ui == "a" :
        search = "Author" #Feeds into Second User Input
        error = False
    elif clean_ui == "t" :
        search = "Title"
        error = False
    elif clean_ui == "s" :
        search = "Series"
        error = False
    elif clean_ui == "p":
        search = "Partial Phrase"
        error = False
    elif clean_ui == "g":
        search = "Genre"
        error = False
    elif clean_ui == "ac":
        search = "Acronym"
        error = False
    elif clean_ui == "total":
        search = "Total"
        error = False
    else:
        error = True
    return error, search
  
    
#%% Acryonym Table

#Pandas Dataframe for Acronyms

def AC_Table():
    data = pd.read_csv('Acronyms.csv')
    df = pd.DataFrame(data)
    #table = df.to_string(index = False)
    print(df)


#%% Actual search function.  

#Searches the columns for the search phrase provided by Search       
def search_sub(col, search_phrase):
    for row in csv_f:
        section = row[col]
        lower_case = section.lower()   
        clean_row = lower_case.translate(str.maketrans('','', string.punctuation))     
        if search_phrase == clean_row:
            print(row[0], "||", row[1], "||", row[2], "||", row[4])
        else:
            splitr = clean_row.split()
            for i in splitr:
                if search_phrase == i:
                    print(row[0], "||", row[1], "||", row[2], "||", row[4])


#%% Searches the entire document
                    
#Searches the entire document for a phrase or partial phrase           
def search_all(search_phrase):
    for row in csv_f:
        # Tests for complete phrases. Couldn't think of a better way than a while loop.
        for i in range(len(row)):
            section = row[i]
            lower_case = section.lower()   
            clean_row = lower_case.translate(str.maketrans('','', string.punctuation))
            if search_phrase == clean_row:
                print(row[0], "||", row[1], "||", row[2], "||", row[4])
            else:
                splitr = clean_row.split()
                for j in splitr:
                    if search_phrase == j:
                        print(row[0], "||", row[1], "||", row[2], "||", row[4]) 
        
                
#%% Main Loop

def main():
    while 1:
        CSV_Load()
        clean_ui = user_input_First()
        error, search = Tag_Menu(clean_ui)
        if error == True:
            print("Incorrect Option, Please Try Again.")
            while error == True:
                clean_ui = user_input_First()
                error, search = Tag_Menu(clean_ui)
                if error == False:
                    break
                print("Incorrect Option, Please Try Again.")
        search_phrase = user_input_Second(clean_ui, search)
        Search(clean_ui, search_phrase)
        print("Another Search Y/N?")
        breaks = input()
        breaks_clean = breaks.lower()
        if breaks_clean == "n":
            break

#extractor()
main()