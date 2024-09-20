#import the partition library for pdf
from unstructured.partition.pdf import partition_pdf
#we are using a dictionary to store the data
from unstructured.chunking.title import chunk_by_title
#import json to store
import json
#import panda
import pandas as pd
#import Counter from collections library
from collections import Counter
#specify PDF file and call the partition_function
#this returns a list[Element]
#import tabulate to allow use to create tables
from tabulate import tabulate
from array import *
#json2table
from json2table import convert
import numpy

#write a function to read the data which returns a dictionary to then turn into a json file (stuff above  in a function) read_json pass in the pdf filenmae
def read_file(filename):
    #specify PDF file and call the partition_function
    #this returns a list[Element]
    #elements = partition_pdf(filename=filename, chunking_strategy="by_title", include_orig_elements=True)
    elements = partition_pdf(filename)
    #then to get the number of elements we can do len(elements)
    number_of_elements = len(elements)
    print("number of elements: ", number_of_elements)
    #print(Counter(type(element) for element in elements))
    #now create a dictionary 
    element_dict = [element.to_dict() for element in elements]
    return element_dict

element_dict = read_file("practise.pdf")

#element_To_Add is a list that will hold elements of sentences that are of the type NarrativeText, Text and Title
elements_to_add = []
title_counter = 0
title_position = []

for i in range((len(element_dict)-1)):
    #print(element_dict[i]["type"])
    if element_dict[i]["type"] == "Title":
        elements_to_add.append(element_dict[i]["text"])
        title_counter = title_counter + 1
        title_position.append(i)
    elif(element_dict[i]["type"] == "NarrativeText" or element_dict[i]["type"] == "Text"):
        elements_to_add.append(element_dict[i]["text"])


title_counter = 0
title_position = []

for i in range((len(element_dict)-1)):
   #print(element_dict[i]["type"])
   if element_dict[i]["type"] == "Title":
       elements_to_add.append(element_dict[i]["text"])
       title_counter = title_counter + 1
       title_position.append(i)
   elif(element_dict[i]["type"] == "NarrativeText" or element_dict[i]["type"] == "Text"):
       elements_to_add.append(element_dict[i]["text"])

#row_counter keeps track of the row of the table that the data needs to be stored on
row_counter = 0

max_table_size = 2 * len(elements_to_add)

#creates a numpty 2d array
table_data = numpy.array(range(max_table_size), dtype='a500').reshape(len(elements_to_add),2)

title_found = True

tempTitleHolder = "-"
tempClauseHolder = "-"

for i in range(0, len(elements_to_add) - 1):
  #this code below is necessary because it prevents a UnicodeEncodeError
    elements_to_add[i]=elements_to_add[i].encode('ascii', 'ignore').decode('ascii')
    if i in title_position:
        if title_found == True:
            #this above clause is try if the instance is encountered where the previous and current element are both of type "Title"
            tempClauseHolder = "-"

            table_data[(row_counter)] = tempTitleHolder
            table_data[(row_counter)][1] = tempClauseHolder

            row_counter = row_counter + 1
            tempTitleHolder = elements_to_add[i]

        else:
            #this above clause is try if the instance is encountered where the current element is of the type "Title" but the prevoius element isn't of type "Title"
            tempTitleHolder = elements_to_add[i]
            title_found = True

    else:
        if title_found == True:
            #this above clause is try if the instance is encountered where the current element isn't of the type "Title" but the prevoius element isn't of type "Title"
            tempClauseHolder = elements_to_add[i]

            table_data[(row_counter)] = tempTitleHolder
            table_data[(row_counter)][1] = tempClauseHolder

            row_counter = row_counter + 1
            tempTitleHolder = "-"
            tempClauseHolder = "-"

        else:
            #this above clause is try if the instance is encountered where the previous and current element are both not of type "Title"
            tempTitleHolder = "-"
            tempClauseHolder = elements_to_add[i]

            table_data[(row_counter)] = tempTitleHolder
            table_data[(row_counter)][1] = tempClauseHolder
            row_counter = row_counter + 1

        title_found = False




column_names = ["Title", "Clause info"]
#using tabulate a HTML table is stored in table
table = tabulate(table_data, headers=column_names, tablefmt="html")

#opens the HTML file and writes the HTML table (stored in table) to the file
html_file = open("table.html","w")
html_file.write(table)
html_file.close()


elements_to_add.insert(0, f"The number of headings is {title_counter}")

def write_to_json(filename):
    with open(filename, "w") as json_file:
        json.dump(elements_to_add, json_file, indent=4)

write_to_json("sample.json")


#write another one to save that files dictionary to a csv, two inputs, file to write it, call that function
def csv_creator(pdf_dict, file_location, new_elements):
    new = pd.DataFrame.from_dict(pdf_dict)
    file = open(file_location, 'w')
    for element in new_elements:
        file.write(str(element) + '\n')
    file.writelines(new)
    file.close()


    

#create a new function that converts the csv file to a table
#save file into variable
file_to_convert = pd.read_csv("sample.csv", on_bad_lines='skip')

#covert to html file 
file_to_convert.to_html("Table.html")
html_file = file_to_convert.to_html()

csv_creator(element_dict, "sample.csv", elements_to_add)

#main interest is unstructured and outputs from unstructured 
#lots of libraries do this and for RR it is trying to understand which are most useful... 
#look into staging a bit more
#pandas is relevant
#if we have time to trial image

#can we detect a title on an image using code rather than physically processing it?
