def createNewClue(generatedClue, entry):
    # We will search the word not clue! Easiest way.
    # Either We can directly get data of google, wikipedia or something else with simulated annealing algorithm.
    # Or implement a embeded algorithm that generate clues, which is very hard thing to do.
    # Rather use the following methods, 
    
    #Meriam-Webster website,Oxford's dictionary, wordnet can be used.
    
    # Couple things to be careful about.
    #Misspelled Word Scenario (In NYT puzzle, words are not always real ones. Return failure when this is the case)
    #Altered Entry Scenario( In webster dictionary, entries might be corrected or altered. Return failure when this is the case)
    #Plural/Singular Form Scenario (Plural entries are corrected by webster dictionary, indicate plurality to the originalClue when this is the case)
    #Abbreviation Scenario
    #Foreign Word Scenario
    #Proper Scenario: If all these conditions are successfully met, we announce success.
    
    def webster(word,nyClue):

    driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
    
    driver.get("http://wordnetweb.princeton.edu/perl/webwn")
    ## Click on Frequency Counts to rank clues easy to hard. Hard or easy ones might be optional for the user.
    showfreq = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/form[2]/select/option[4]")))
    showfreq.click()
    
    
    print("Searching in http://wordnetweb.princeton.edu/perl/webwn...")
    driver.get('http://wordnetweb.princeton.edu/perl/webwn')
    
    textBox = driver.find_element_by_id('s')
    textBox.send_keys(word)
    SearchWordNet_Button=WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/form[1]/input[2]")))
    SearchWordNet_Button.click()
    print('Keyword has been entered.\n')
    
    # False if word is not avaliable.
    generatedClue = -1
    elementValid = driver.find_element_by_xpath('/html/body/h3').text()
    if len(elementValid) > 0:
        print('The word \'' + word + '\' ' + 
              RED + 'is not found' + END + ' in Worldnet.\n')
        generatedClue = -1
    else:
        # --------- Get the output of Wordnet to check it afterwards ------------------------------
        element_word_output = driver.find_element_by_xpath('/html/body/div[2]/ul[1]/li[1]/b').text()
       
        
        # ---------- Check if the word is not changed by Wordnet, for example cars ---> car ----------------------------------
        plurality_condition = False                                              
        if element_word_output.lower() != word:
            print('The input \'' + word + '\' and dictionary word \'' + 
                  element_word_output + '\' ' + RED + 'do not match' + END + '.')
# ------------------------------------------ABOVE THIS LINE IS ADJUSTED-----------------------------------------------------------------------------------------
            index_found = word.find(element_word_output.split(' ')[0]) # Does the element_word_output contain the keyword.
            if index_found != -1: # if it contains the keyword then,
                if (element_word_output + 's') != word or (element_word_output + 'es') != word: # check if is not plural with 's', 'es' then,
                    # cars--->apple
                    print('The words \'' + word + '\' and \'' + element_word_output + 
                          '\' are ' + RED + 'irrelevant' + END + '.\n')
                    generatedClue = -1
                    return generatedClue
                 elseif (element_word_output +'s') == word or (element_word_output + 'es') == word):
                # apples -> apple
                print('Keyword \'' + word + '\' is the plural form of \'' + 
                      element_word_output + '\'.\n')
                plural_condition = True
            else:
                #Webstie Output, aka element_word_output, of Wordnet does not contain searched word
                clue = -1
                return clue
        # ---------------------------------------------------------------------
# ------------------------------------------ABOVE THIS LINE IS ADJUSTED-----------------------------------------------------------------------------------------
    
    
        # ---------- Get possible clues -----------------------
        possibleClue_xpath_index = driver.find_element_by_xpath('/html/body/div[2]/ul[1]/li[1]/text()[3]')
        possibleClue = possibleClue_xpath_index.text
        
        print('Possible clues are listed below:')
        possibleClue = []
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
    

    return generatedClue
