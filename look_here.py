from unstructured.partition.pdf import partition_pdf
#we are using a dictionary to store the data
from unstructured.chunking.title import chunk_by_title
#import json to store
import json
#import panda
import pandas as pd

elements = partition_pdf(filename="practise.pdf", chunking_strategy="by_title", include_orig_elements=True)

#write a function to read the data which returns a dictionary to then turn into a json file (stuff above  in a function) read_json pass in the pdf filenmae
devscode-remote://codespaces%2Brefactored-orbit-r4g9g7pgp4653445/workspaces/rollsroyce/practise%20files/master_service.pdff read_file(filename):
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
text_list = []
category_list = []
index_list = []
index_to_add = 0

for i in range((len(element_dict)-1)):
  text_list.append(element_dict[i]["text"])
  category_list.append(element_dict[i]["type"])
  if (element_dict[i]["type"]!="Title"):
     index_to_add+=1   
  index_list.append(index_to_add)

data = [{'text': text, 'category': category} for text, category in zip(text_list, category_list)]
df = pd.DataFrame(data)
df.insert(0, "index", index_list , True)
print(df)
