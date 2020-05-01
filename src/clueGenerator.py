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
    
    except:
         
        print("Entry couldn't found in the wordnet, now searching in Wikipedia...")
        newClues=-1

    return "error"
# =============================================================================
# print(clueGenerator(" ", "car"))
# =============================================================================
