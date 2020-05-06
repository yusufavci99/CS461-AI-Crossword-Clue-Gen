# -*- coding: utf-8 -*-
"""
Created on Fri May  1 22:13:56 2020

@author: Asus
"""

import nltk
from nltk.corpus import wordnet
import wikipedia
from nltk import pos_tag
from nltk import RegexpParser
newClues=[]
entry_present_tense=0
entry_past_tense=0
entry_foreign_word=0
generate_noun_clue=0
entry="Garden"
tokenized_entry=nltk.word_tokenize(entry)
token=nltk.pos_tag(tokenized_entry)
for t in token:
    if t[1] == 'FW':# NYT RULE #4 CHECKING FOREIGN WORDS
        entry_foreign_word=1
        #return -1 check original clue
    if t[1] == 'VBD' or t[1] == 'VBN':# NYT RULE #1 TENSES MUST BE MATCHED, so we control the tense of the entry(word)
        entry_past_tense=1
        print('Entry tense is past tense')
    if t[1] == 'VBP' or t[1] == 'VBZ':# NYT RULE #1 TENSES MUST BE MATCHED, so we control the tense of the entry(word)
        entry_present_tense=1
        print('Entry tense is present tense')
    if t[1].find('NN') == 0 or t[1].find('NNS') == 0 or t[1].find('NNP') == 0:# given entry must corresponds to noun as well. Rule #2 NYT "PART OF SPEECH"
        generate_noun_clue=1
        print('generating a noun clue')
        
    #if t[1].find('')
    
        
p = wikipedia.search(entry)

if len(p) != 0:# Check if there is a page related to the entry
    searches=wikipedia.search(entry,results=1,suggestion=False)
    Sentence=wikipedia.summary(searches[0],sentences=1)
    page = wikipedia.page(searches[0])
# =============================================================================
#     indx_searches=-1
#     for possible_title in searches:
#         indx_searches+=1
#         if possible_title.lower() == entry.lower():
#             print(indx_searches)
#             print(searches[indx_searches])
#             Sentence=wikipedia.summary(searches[indx_searches],sentences=1)
#             page = wikipedia.page(searches[indx_searches])
# =============================================================================
            
    #content_page=page.content
    #content_page_summary=page.summary#page summary
    print("search is successful, moving on...")
else:# if not 
    searches=wikipedia.search(entry,results=1,suggestion=False)# Use suggest function to let wikipedia choose for the closest word
    Sentence=wikipedia.summary(searches[0],sentences=1)
    page = wikipedia.page(searches[0])
    
tokenized_possible_clue = nltk.word_tokenize(Sentence)
# =============================================================================
#     indx_searches=-1
#     for possible_title in searches:
#         indx_searches+=1
#         if possible_title.lower() == entry.lower():
#             Sentence=wikipedia.summary(searches[indx_searches],sentences=1)
#             page = wikipedia.page(searches[indx_searches])
# =============================================================================
    #content_page=page.content
    #content_page_summary=page.summary#page summary 
    

page_header_index=str(page).find("'")
page_header=str(page)[page_header_index+1:-2]
page_header=page_header.lower()

Plural=False# NYT RULE #3 CHECKING PLURALITY CONDITION
if entry.lower() == page_header + 's' or entry.lower() == page_header + 'es':
    Plural=True


tokens_tag = nltk.pos_tag(tokenized_possible_clue)
#indx_possibleClue=content_page_summary.find(".")
noun_phrase_element=[]
if generate_noun_clue == 1:#  NYT RULE #2 'PART OF SPEECH'starts here for noun clue generation
    
    #noun_phrase_grammar = "NP: {<DT>?<JJ_available>*<NN>}"#this case, we will define a simple grammar with a single regular-expression rule
    #npcp = nltk.RegexpParser(noun_phrase_grammar)# noun phrase chunk parser
    tokens_tag = nltk.pos_tag(tokenized_possible_clue)#token tags of the tokenized possible clue
    #result_tree = npcp.parse(tokens_tag)#Parsed as semantic tree, for noun phrase generation we need to parse the tokens_tag and get noun phrases
    JJ_available=0
    NN_available=0
    NNS_available=0
    IN_available=0
    NN_cnt=1
    for parse in tokens_tag:# We successfully implement a meaninggul noun phrase for noun entry
        
        print(parse)
        
        if parse[1] == 'NN' and IN_available == 1:
            noun_phrase_element.append(parse[0] + ',')
            print('NN')
            print(parse[1])
            
        if parse[1] == 'JJ':
            noun_phrase_element.append(parse[0] + ' ')
            JJ_available=1
            print(parse[1])
            print('JJ_available')
        if parse[1] == 'NN'and JJ_available == 1 and NN_cnt!=2:
            noun_phrase_element.append(parse[0] + ' ')
            NN_available=1
            NN_cnt+=1
            print('NN')
            print(parse[1])
        if parse[1] == 'NNS'and NN_available == 0 and JJ_available == 1 and NN_cnt!=2:
            noun_phrase_element.append(parse[0] + ' ')
            NNS_available=1
            NN_cnt+=1
            print('NNS')
            print(parse[1])
            
        if parse[1] == 'IN'  and (NNS_available == 1 or NN_available == 1):
            noun_phrase_element.append(parse[0] + ' ')
            IN_available=1
            print('IN')
            print(parse[1])
            
        if JJ_available == 1 and (NNS_available == 1 or NN_available == 1) and IN_available == 1:
            newClues.append(noun_phrase_element)
            JJ_available=0
            NN_available=0
            NNS_available=0
            
            
           

        # to find nth occurrence of substring 


possibleClue=" "
i=0
for word in tokenized_possible_clue:#omit similar wordings
    i+=1
    if word.lower() == entry.lower():
        tokenized_possible_clue[i-1]="..."
        
    if word.lower() == entry.lower() + "ing":
        tokenized_possible_clue[i-1]="..."
        
    if word.lower() == entry.lower() + "ed":
        tokenized_possible_clue[i-1]="..."

    if word.lower() == entry.lower() + "d":
        tokenized_possible_clue[i-1]="..."
        
    if word.lower() == entry.lower() + "ly":
        tokenized_possible_clue[i-1]="..."
        
    if word.lower() == entry.lower() + "lly":
        tokenized_possible_clue[i-1]="..."
        
    if word.lower() == entry.lower() + "ally":
        tokenized_possible_clue[i-1]="..."
        
    if word.lower() == entry.lower() + "able":
        tokenized_possible_clue[i-1]="..."
        
    if word.lower() == entry.lower() + "ble":
        tokenized_possible_clue[i-1]="..."
        
    if word.lower() == page_header.lower():
        tokenized_possible_clue[i-1]="..."
        
    if word.lower() == page_header.lower() + "ing":
        tokenized_possible_clue[i-1]="..."
        
    if word.lower() == page_header.lower() + "ed":
        tokenized_possible_clue[i-1]="..."
        
    if word.lower() == page_header.lower() + "d":
        tokenized_possible_clue[i-1]="..."
    
    if word.lower() == page_header.lower() + "ly":
        tokenized_possible_clue[i-1]="..."
        
    if word.lower() == page_header.lower() + "lly":
        tokenized_possible_clue[i-1]="..."
        
    if word.lower() == page_header.lower() + "ally":
        tokenized_possible_clue[i-1]="..."
        
    if word.lower() == page_header.lower() + "able":
        tokenized_possible_clue[i-1]="..."
        
    if word.lower() == page_header.lower() + "ble":
        tokenized_possible_clue[i-1]="..."
        
if page_header.find(entry.lower()) == -1 and entry_past_tense==0 and entry_present_tense==0:# if we can't find entry on the page title in wikipedia return -1
    print("Invalid output")
    #return -1


        
if entry_present_tense==1:
    possibleClue = possibleClue.join(tokenized_possible_clue)
    possibleCLue= possibleClue + "(Present)"
elif entry_past_tense==1:
    possibleClue = possibleClue.join(tokenized_possible_clue)
    possibleClue= possibleClue + "(Past)"
elif Plural:
    possibleClue = possibleClue.join(tokenized_possible_clue)
    possibleClue= possibleClue + "(Plural)"
    
    
                                     

#possibleClue = possibleClue.join(tokenized_possible_clue)

newClues.append(possibleClue)
print(newClues)
# =============================================================================
# x=0
# for n in range(1,3):#get only first 3 occurences
#     sub_str = "."
#     occurrence = n
# 	
# 
#   # Finding nth occurrence of substring to set seperate sentences from given summary page of Wikipedia
#     v = -1
#     for i in range(0, occurrence): 
#         v = content_page_summary.find(sub_str, v + 1) 
# 
#   # Printing nth occurrences 
#         print (str(occurrence) + "th" + " occurrence of .(dot) is at", v) 
#         
#        
#         possibleClue=content_page_summary[x:v+1]
#         line=possibleClue.split(" ") 
#         print(line)
#         i=0
#         x=v+1
#         for word in line:#omit similar wordings
#             i+=1
#             if word.lower() == entry:
#                 line[i-1]="...."
#             if word.lower() == page_header:
#                 line[i-1]="...."
#             if word.lower() == page_header + "ing":
#                 line[i-1]="...."
#             if word.lower() == page_header + "ed":
#                 line[i-1]="...."
#             if word.lower() == page_header + "d":
#                 line[i-1]="...."
#             if word.lower() == page_header + "ly":
#                 line[i-1]="...."
#             if word.lower() == page_header + "lly":
#                 line[i-1]="...."
#             if word.lower() == page_header + "ally":
#                 line[i-1]="...."
#             if word.lower() == page_header + "able":
#                 line[i-1]="...."
#             if word.lower() == page_header + "ble":
#                 line[i-1]="...."
# =============================================================================
                
        
# =============================================================================
#         possibleClue=" "
#         if Plural:
#             possibleClue = possibleClue.join(line)+ " (Plural)"
#             newClues.append(possibleClue)     
#         else:
#             possibleClue = possibleClue.join(line)
#             newClues.append(possibleClue)
# =============================================================================
            
print(newClues)
    
    


        
