def createNewClue(generatedClues, entry):
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
    
    driver.get("http://wordnetweb.princeton.edu/perl/webwn")
    ## Click on Frequency Counts to rank clues easy to hard. Hard or easy ones might be optional for the user.
    showfreq = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/form[2]/select/option[4]")))
    showfreq.click()
    
    
    print("Searching in http://wordnetweb.princeton.edu/perl/webwn...")
    driver.get('http://wordnetweb.princeton.edu/perl/webwn')
    
    textBox = driver.find_element_by_id('s')
    textBox.send_keys(entry)
    SearchWordNet_Button=WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/form[1]/input[2]")))
    SearchWordNet_Button.click()
    print('Keyword has been entered.\n')
    
    # False if entry is not avaliable.
    generatedClues = -1
    elementValid = driver.find_element_by_xpath('/html/body/h3').text()
    if len(elementValid) > 0:
        print('The entry \'' + entry + '\' ' + 
              RED + 'is not found' + END + ' in Worldnet.\n')
        generatedClues = -1
    else:
        # --------- Get the output of Wordnet to check it afterwards ------------------------------
        element_entry_output = driver.find_element_by_xpath('/html/body/div[2]/ul[1]/li[1]/b')
       
        
        # ---------- Check if the entry is not changed by Wordnet, for example cars ---> car ----------------------------------
        plurality_condition = False                                              
        if element_entry_output.lower() != entry:
            print('The input \'' + entry + '\' and dictionary entry \'' + 
                  element_entry_output + '\' ' + RED + 'do not match' + END + '.')
# ------------------------------------------ABOVE THIS LINE IS ADJUSTED-----------------------------------------------------------------------------------------
            index_found = entry.find(element_entry_output.split(' ')[0]) # Does the element_entry_output contain the keyword.
            if index_found != -1: # if it contains the keyword then,
                if (element_entry_output + 's') != entry or (element_entry_output + 'es') != entry: # check if is not plural with 's', 'es' then,
                    # cars--->apple
                    print('The words \'' + entry + '\' and \'' + element_entry_output + 
                          '\' are ' + RED + 'irrelevant' + END + '.\n')
                    generatedClues = -1
                    return generatedClues
                 elseif (element_entry_output +'s') == entry or (element_entry_output + 'es') == entry):
                # apples -> apple
                print('Keyword \'' + entry + '\' is the plural form of \'' + 
                      element_entry_output + '\'.\n')
                plural_condition = True
            else:
                #Webstie Output, aka element_entry_output, of Wordnet does not contain searched entry
                generatedClues = -1
                return generatedClues
       
    
        # ---------- Get possible clues -----------------------
        generatedClues=[]
        possibleClue = driver.find_element_by_xpath('/html/body/div[2]/ul[1]/li[1]').text()# first definition
        if plural_condition:
                generatedClues.append(line + '(Plural)')
             else:
                generatedClues.append(line)
 
        #possibleClue = driver.find_element_by_xpath('/html/body/div[2]/ul/li['+ num2str(indx) + ']').text()
            
            #For example sentences
            possibleClue = driver.find_element_by_xpath('/html/body/div[2]/ul[2]/li[2]/i').text()
            #filter example sentence
            line=possibleClue.split(' ')
            i=0;
            for x in line:
            i+=1
            if entry == x:
                possibleClue=possibleClue.strip(line[i-1])
                line[i-1]="...."
                
             if plural_condition:
                generatedClues.append(line + '(Plural)')
             else:
                generatedClues.append(line)
         
    

    

    return generatedClues
