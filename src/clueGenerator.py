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

    driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
    Definitions=[] #List to store name of the product
    Ranks=[] #List to store price of the product
    driver.get("http://wordnetweb.princeton.edu/perl/webwn")
    ## Click on Frequency Counts to rank clues easy to hard. Hard or easy ones might be optional for the user.
    showfreq = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/form[2]/select/option[4]")))
    
    showfreq.click()
    def webster(word,nyClue):
    print("Searching in http://wordnetweb.princeton.edu/perl/webwn...")
    driver.get('http://wordnetweb.princeton.edu/perl/webwn')
    
    textBox = driver.find_element_by_id('s')
    textBox.send_keys(word)
    SearchWordNet_Button=WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/form[1]/input[2]")))
    SearchWordNet_Button.click()
    print('Keyword has been entered.\n')
    
    # False if word is not avaliable.
    generatedClue = -1
    elementValid = driver.FindElement(By.XPath(“.//*[text()='Your search did not return any results.'] ”))
    if len(elementValid) > 0:
        print('The word \'' + word + '\' ' + 
              RED + 'is not found' + END + ' in Worldnet.\n')
        generatedClue = -1
    else:
        # --------- Get the possible clues -------------------------------
        worddefCounter=1# For now taking only first definition of the word
        possibleClue = driver.find_element_by_xpath('/html/body/div[2]/ul[1]/li[' + num2str(worddefCounter) + ']/text()[3]'
        # -----------------------------------------------------
        
        
        # ---------- Check if the word is not changed by Merriam -------------
        plurality_condition = False
        element_word_input=driver.find_element_by_xpath('/html/body/div[2]/ul[1]/li[1]/b'
                                                    
        if element_word_input.lower() != word:
            print('The input \'' + word + '\' and dictionary word \'' + 
                  element_word_input + '\' ' + RED + 'do not match' + END + '.')
# ------------------------------------------ABOVE THIS LINE IS ADJUSTED-----------------------------------------------------------------------------------------
            index_found = word.find(element_word_input.split(' ')[0]) # Does the element_word_input contain the keyword.
            if index_found != -1: # if it contains the keyword then,
                if (element_word_input + 's') != word and (element_word_input + 'es') != word: # check if is not plural with 's', 'es' then,
                    # asyet -> yet
                    print('The words \'' + word + '\' and \'' + element_word_input + 
                          '\' are ' + RED + 'irrelevant' + END + '.\n')
                    generatedClue = -1
                    return generatedClue
                # apples -> apple
                print('Keyword \'' + word + '\' is the plural form of \'' + 
                      element_word_input + '\'.\n')
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
    

    return generatedClue
