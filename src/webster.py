def webster(word,nyClue):
    print("*******  Searching: ",word," ********")
    print("Searching in https://www.merriam-webster.com...")
    driver.get('https://www.merriam-webster.com/')
    print("Puzzle URL is opened.")
    
    textBox = driver.find_element_by_id('s-term')
    textBox.send_keys(word)
    textBox.send_keys(Keys.RETURN)      # Press enter
    print('Keyword has been entered.\n')
    
    # False if word is not avaliable.
    clue = -1
    elementValid = driver.find_elements_by_class_name("mispelled-word")
    if len(elementValid) > 0:
        print('The word \'' + word + '\' ' + 
              RED + 'is not found' + END + ' in Merriam-Webster.\n')
        clue = -1
    else:
        # --------- Get header -------------------------------
        # Contains header + parts of speech
        element2 = driver.find_elements_by_class_name("col-lg-12")
        
        # Get header only
        element3 = element2[0].find_element_by_class_name("hword")
        header = element3.text
        
        # Get parts of speech only
#        element4 = element2[0].find_elements_by_class_name("fl")
#        print('Elements are filtered by class \'fl\': ' + element4[0].text+'\n')
        # -----------------------------------------------------
        
        
        # ---------- Check if the word is not changed by Merriam -------------
        plural = False
        if header.lower() != word:
            print('The input \'' + word + '\' and dictionary word \'' + 
                  header + '\' ' + RED + 'do not match' + END + '.')

            idx = word.find(header.split(' ')[0]) # Does the element contain the keyword.
            if idx != -1: # if it contains the keyword then,
                if (header + 's') != word and (header + 'es') != word: # check if is not plural with 's', 'es' then,
                    # asyet -> yet
                    print('The words \'' + word + '\' and \'' + header + 
                          '\' are ' + RED + 'irrelevant' + END + '.\n')
                    clue = -1
                    return clue
                # apples -> apple
                print('Keyword \'' + word + '\' is the plural form of \'' + 
                      header + '\'.\n')
                plural = True
            else:
                clue = -1
                return clue
        # ---------------------------------------------------------------------
   
    
    
        # ---------- Get possible clues -----------------------
        element0 = driver.find_element_by_class_name("vg")
        
        element1 = element0.find_elements_by_class_name("dtText")
        print('Possible clues are listed below:')
        clue = []
        if len(element1)==0:
            element1 = element0.find_elements_by_class_name("unText")
            for x in element1:
                if x.text.find('—') != -1:
                    # Filter example sentences which include keyword.
                    line = x.text.split("\n")[0]
                    
                    # Filter ':' from definition.
                    line = line[2:len(line)]
                    if plural:    
                        clue.append(line + ' (plural)')
                    else:
                        clue.append(line)
                else:
                    if len(element0.find_elements_by_class_name("num")) == 0:
                        # List abbrev
                        clue.append(x.text + ' (abbreviation)')
                    else:
                        clue.append(x.text)
        else:
            for x in element1:
                if x.text.find(':') != -1:
                    # Filter example sentences which include keyword.
                    line = x.text.split("\n")[0]
                    
                    # Filter ':' from definition.
                    line = line[2:len(line)]
                    if plural:    
                        clue.append(line + ' (plural)')
                    else:
                        clue.append(line)
                else:
                    if len(element0.find_elements_by_class_name("num")) == 0:
                        # List abbrev
                        clue.append(x.text + ' (abbreviation)')
                    else:
                        if(x.text[0]=='—'):
                            continue
                        else:
                            clue.append(x.text)
            
        #Check clue language
        element_lang = driver.find_element_by_class_name("fl")
        element_def= element_lang.text.split(' ')[0]
        if (element_def != "noun" and element_def != "verb" and element_def != "adverb" and element_def != "adjective" and element_def != "noun," and element_def != "verb," and element_def != "adverb," and element_def != "adjective," and element_def != "abbreviation"):
            for x in range(len(clue)):
                clue[x]= clue[x]+ " in "+ element_def
        
        for i in range(len(clue)):
            print(str(i) + ') ' + clue[i])
        print("")
        clue = clueFilter(header, nyClue, clue)
        print("")
        
    return clue
