def ABB(word,nyClue):
    print("*******  Searching: ",word," ********")
    print("Searching in https://www.abbreviations.com/...")
    driver.get('https://www.abbreviations.com/')
    print("Puzzle URL is opened.\n")
    
    textBox3 = driver.find_element_by_id('search')
    textBox3.send_keys(word)
    textBox3.send_keys(Keys.RETURN)      # Press enter
    
    element5=driver.find_elements_by_class_name("desc")
    if(len(element5)==0):
        element5=driver.find_elements_by_css_selector(".defs-int.rc5")
        if(len(element5)!=0):    
            clue=(element5[0]).text.split("\n")[1]
            print('Possible clues are listed below:\n',"1) " ,clue,'\n')
            print("\n Our new clue is: \n",clue,"\n")
            return clue
        else:
            element5=driver.find_elements_by_css_selector(".no-items.rc5.row")
            element5=(element5[0]).text.split(".")[0]
            print('The word \''+ word + '\'' + RED + ' is not found' + END +' in Abbreviation Dictionary.\n')
            return -1    
    else:
        abrv_array=[]
        abrv_array.append(element5[1].text)
        print('Possible clues are listed below:')
        for x in range(len(abrv_array)):
            abrv_array[x]=(abrv_array[x]+ ' (abbreviation)')
            print(str(x) + ') ' + abrv_array[x])
        print('')
        return clueFilter(word, nyClue, abrv_array)
