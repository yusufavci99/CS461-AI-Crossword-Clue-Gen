def createNewClue(originalClue, entry):
    
    from nltk.corpus import wordnet
    
    
    
    try:
        newClues=[]
        syns = wordnet.synsets(entry)
        plurality_check=syns[0].lemmas()[0].name()
        Plural=False
        if entry == plurality_check+"s" or entry == plurality_check+"es":
            Plural=True
            
        possibleClue=syns[0].definition()
        print(possibleClue)
        if len(possibleClue) != 0: 
            if Plural:
                possibleClue = possibleClue + " (Plural)"
                newClues.append(possibleClue)
            else:
                newClues.append(possibleClue)
            return newClues[0]
        else:
            print("no definition clues available")
            newClues=-1
            
        
        print("Your clues so far:" + str(newClues))
        
        
        
        possibleClue=syns[0].examples()
        if len(possibleClue) != 0: 
            line=possibleClue[0].split(" ") 
            print(line)
            i=0
            for word in line:
                i+=1
                if word == entry:
                    line[i-1]="...."
                if word == plurality_check:
                    line[i-1]="...."
                    
            possibleClue=" "
            if Plural:
                possibleClue = possibleClue.join(line)+ " (Plural)"
                newClues.append(possibleClue)
        
            else:
                possibleClue = possibleClue.join(line)
                newClues.append(possibleClue)
                
            return newClues[0]
            
        else:
            print("no example clues available")
            newClues=-1
            #return newClues
            
        
        print(newClues)
    
    except:# If we could not find in the wordnet
         
        print("Entry couldn't found in the wordnet, now searching in Wikipedia...")
        
        import nltk
        from nltk.corpus import wordnet
        import wikipedia
        from nltk import pos_tag
        from nltk import RegexpParser
        newClues=[]
        Plural = 0
        entry_present_tense=0
        entry_past_tense=0
        entry_foreign_word=0
        generate_noun_clue=0
        #entry="Basketballs"
        tokenized_entry=nltk.word_tokenize(entry)
        token=nltk.pos_tag(tokenized_entry)
        for t in token:
            if t[1] == 'FW':# NYT RULE #4 CHECKING FOREIGN WORDS
                entry_foreign_word=1
                # check original clue
            if t[1] == 'NNS'or t[1] == 'NNPS': #NYT RULE #3 CHECKING PLURALITY CONDITION
                Plural = 1
            
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
        
        # NYT RULE #3 CHECKING PLURALITY CONDITION
        if entry.lower() == page_header + 's' or entry.lower() == page_header + 'es':
            Plural = 1
        
        
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
                          
                if parse[1] == 'JJ':
                    noun_phrase_element.append(parse[0] + ' ')
                    JJ_available=1
                    print(parse[1])
                    print('Starting with adding JJ to the noun phrase...')
                if parse[1] == 'NN'and JJ_available == 1:
                    noun_phrase_element.append(parse[0] + ' ')
                    NN_available=1
                    NN_cnt+=1
                    print('Continuing with adding NN into the noun phrase if JJ is available...')
                    print(parse[1])
                if parse[1] == 'NNS'and NN_available == 0 and JJ_available == 1 and NN_cnt!=2:
                    noun_phrase_element.append(parse[0] + ' ')
                    NNS_available=1
                    print('Continuing with adding NNS into the noun phrase if JJ is available but NN is not available...')
                    print(parse[1])
                    
                if parse[1] == 'IN'  and (NNS_available == 1 or NN_available == 1):
                    noun_phrase_element.append(parse[0] + ' ')
                    IN_available=1
                    print('Continuing with adding IN into the noun phrase if NN or NNS is available...')
                    print(parse[1])
                    
                if JJ_available == 1 and (NNS_available == 1 or NN_available == 1) and IN_available == 1 and NN_cnt==3:
                    #newClues.append(noun_phrase_element)
                    JJ_available=0
                    NN_available=0
                    NNS_available=0
                    print(NN_cnt)
                    break
            
            possibleClue=""
            print('NOUN PHRASE ELEMENT')
            print(noun_phrase_element)
            
            i=0
            for word in noun_phrase_element:#omit similar wordings
                i+=1
                if word.lower() == entry.lower():
                    noun_phrase_element[i-1]="..."
                    
                if word[:-1].lower() == entry[:-1].lower():#Omitting when entry is plural but content of the sentence has singular form of the entry
                    noun_phrase_element[i-1]="..."
                        
                if word[:-2].lower() == entry[:-2].lower():#Omitting when entry is plural but content of the sentence has singular form of the entry
                    noun_phrase_element[i-1]="..."
                    
                if word.lower() == entry.lower() + "ing":
                    noun_phrase_element[i-1]="..."
                    
                if word.lower() == entry.lower() + "ed":
                    noun_phrase_element[i-1]="..."
            
                if word.lower() == entry.lower() + "d":
                    noun_phrase_element[i-1]="..."
                    
                if word.lower() == entry.lower() + "ly":
                    noun_phrase_element[i-1]="..."
                    
                if word.lower() == entry.lower() + "lly":
                    noun_phrase_element[i-1]="..."
                    
                if word.lower() == entry.lower() + "ally":
                    noun_phrase_element[i-1]="..."
                    
                if word.lower() == entry.lower() + "able":
                    noun_phrase_element[i-1]="..."
                    
                if word.lower() == entry.lower() + "ble":
                    noun_phrase_element[i-1]="..."
                    
                if word.lower() == page_header.lower():
                    noun_phrase_element[i-1]="..."
                    
                if word.lower() == page_header.lower() + "ing":
                    noun_phrase_element[i-1]="..."
                    
                if word.lower() == page_header.lower() + "ed":
                    noun_phrase_element[i-1]="..."
                    
                if word.lower() == page_header.lower() + "d":
                    noun_phrase_element[i-1]="..."
                
                if word.lower() == page_header.lower() + "ly":
                    noun_phrase_element[i-1]="..."
                    
                if word.lower() == page_header.lower() + "lly":
                    noun_phrase_element[i-1]="..."
                    
                if word.lower() == page_header.lower() + "ally":
                    noun_phrase_element[i-1]="..."
                    
                if word.lower() == page_header.lower() + "able":
                    noun_phrase_element[i-1]="..."
                    
                if word.lower() == page_header.lower() + "ble":
                    noun_phrase_element[i-1]="..."
             
            
            possibleClue = possibleClue.join(noun_phrase_element)
            print(noun_phrase_element)
            newClues=possibleClue
            print('Possible Clue is: ' + possibleClue)
            #newClues.append(possibleClue)
            print(newClues)
            if len(newClues) > 1:# if we can't find that means no JJ in the possible clue
                if Plural:
                    newClues = possibleClue + '(Plural)'
                    return newClues
                return newClues
                print('New clue found!')
                
            else:# JJ is not in the sentence then, start with NN or NNS to build noun phrase
                print('Starting the search without JJ element...')
                NN_available=0
                NNS_available=0
                IN_available=0
                NN_cnt=1
                for parse in tokens_tag:# We successfully implement a meaninggul noun phrase for noun entry
                    
                    print(parse)# parsing each tokens
            
                    if parse[1] == 'NN' and NN_cnt!=2:
                        noun_phrase_element.append(parse[0] + ' ')
                        NN_available=1
                        NN_cnt+=1
                        print('Continuing with adding NN into the noun phrase if JJ is available...')
                        print(parse[1])
                    if parse[1] == 'NNS'and NN_available == 0 and NN_cnt!=2:
                        noun_phrase_element.append(parse[0] + ' ')
                        NNS_available=1
                        NN_cnt+=1
                        print('Continuing with adding NNS into the noun phrase if JJ is available but NN is not available...')
                        print(parse[1])
                        
                    if parse[1] == 'IN'  and (NNS_available == 1 or NN_available == 1):
                        noun_phrase_element.append(parse[0] + ' ')
                        IN_available=1
                        print('Continuing with adding IN into the noun phrase if NN or NNS is available...')
                        print(parse[1])
                        
                    if parse[1] == 'NNP' and IN_available == 1:
                        noun_phrase_element.append(parse[0] + ' ')
                        print('Found IN, finding NN word...')
                        print(parse[1])
                        IN_available=0
                        
                    if (NNS_available == 1 or NN_available == 1) and IN_available == 1:
                        #newClues.append(noun_phrase_element)
                        NN_available=0
                        NNS_available=0
                        #IN_available=1
                newClues=[]
                possibleClue=""
                print('NOUN PHRASE ELEMENT')
                print(noun_phrase_element)
                i=0
                for word in noun_phrase_element:#omit similar wordings
                    i+=1
                    if word.lower() == entry.lower():
                        noun_phrase_element[i-1]="..."
                        
                    if word[:-1].lower() == entry[:-1].lower():#Omitting when entry is plural but content of the sentence has singular form of the entry
                        noun_phrase_element[i-1]="..."
                        
                    if word[:-2].lower() == entry[:-2].lower():#Omitting when entry is plural but content of the sentence has singular form of the entry
                        noun_phrase_element[i-1]="..."
               
                    if word.lower() == entry.lower() + "ing":
                        noun_phrase_element[i-1]="..."
                        
                    if word.lower() == entry.lower() + "ed":
                        noun_phrase_element[i-1]="..."
                
                    if word.lower() == entry.lower() + "d":
                        noun_phrase_element[i-1]="..."
                        
                    if word.lower() == entry.lower() + "ly":
                        noun_phrase_element[i-1]="..."
                        
                    if word.lower() == entry.lower() + "lly":
                        noun_phrase_element[i-1]="..."
                        
                    if word.lower() == entry.lower() + "ally":
                        noun_phrase_element[i-1]="..."
                        
                    if word.lower() == entry.lower() + "able":
                        noun_phrase_element[i-1]="..."
                        
                    if word.lower() == entry.lower() + "ble":
                        noun_phrase_element[i-1]="..."
                        
                    if word.lower() == page_header.lower():
                        noun_phrase_element[i-1]="..."
                        
                    if word.lower() == page_header.lower() + "ing":
                        noun_phrase_element[i-1]="..."
                        
                    if word.lower() == page_header.lower() + "ed":
                        noun_phrase_element[i-1]="..."
                        
                    if word.lower() == page_header.lower() + "d":
                        noun_phrase_element[i-1]="..."
                    
                    if word.lower() == page_header.lower() + "ly":
                        noun_phrase_element[i-1]="..."
                        
                    if word.lower() == page_header.lower() + "lly":
                        noun_phrase_element[i-1]="..."
                        
                    if word.lower() == page_header.lower() + "ally":
                        noun_phrase_element[i-1]="..."
                        
                    if word.lower() == page_header.lower() + "able":
                        noun_phrase_element[i-1]="..."
                        
                    if word.lower() == page_header.lower() + "ble":
                        noun_phrase_element[i-1]="..."
                    
                possibleClue = possibleClue.join(noun_phrase_element)
                
                if Plural:
                    newClues = possibleClue + ' (Plural)'
                    return newClues
                newClues=possibleClue
                print('New Clue is: ' + newClues)
                return newClues
                
         
        elif generate_noun_clue == 0:
              
            possibleClue=" "
            i=0
            for word in tokenized_possible_clue:#omit similar wordings
                i+=1
                if word.lower() == entry.lower():
                    tokenized_possible_clue[i-1]="..."
                    
                if word.lower() == entry[:-1].lower():#Omitting when entry is plural but content of the sentence has singular form of the entry
                    tokenized_possible_clue[i-1]="..."
                        
                if word.lower() == entry[:-2].lower():#Omitting when entry is plural but content of the sentence has singular form of the entry
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
                    
            # =============================================================================
            # if page_header.find(entry.lower()) == -1 and entry_past_tense==0 and entry_present_tense==0:# if we can't find entry on the page title in wikipedia return -1
            #     print("Invalid output")
            #     #return -1
            # =============================================================================
            
            
                    
            if entry_present_tense==1:
                possibleClue = possibleClue.join(tokenized_possible_clue)
                possibleCLue= possibleClue + "(Present)"
                newClues=possibleClue
                return newClues
            elif entry_past_tense==1:
                possibleClue = possibleClue.join(tokenized_possible_clue)
                possibleClue= possibleClue + "(Past)"
                newClues=possibleClue
                return newClues
            elif Plural:
                possibleClue = possibleClue.join(tokenized_possible_clue)
                possibleClue= possibleClue + "(Plural)"
                newClues=possibleClue
                return newClues
                
              
            possibleClue = possibleClue.join(tokenized_possible_clue)
            
            newClues=possibleClue
            
            return newClues
                
                
                
        

        
        

    return "error"
# =============================================================================
# print(clueGenerator(" ", "car"))
# =============================================================================
