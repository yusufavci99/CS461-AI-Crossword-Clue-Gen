def clueGenerator(originalClue, entry):
    
          # -*- coding: utf-8 -*-
    """
    Created on Thu Apr 30 19:18:31 2020

    @author: Mert Alagözlü v1.0
    """

    from nltk.corpus import wordnet



    try:
        originalClue=[]
        entry="carssqqq"
        syns = wordnet.synsets(entry)
        plurality_check=syns[0].lemmas()[0].name()
        Plural=False
        if entry == plurality_check+"s" or entry == plurality_check+"es":
            Plural=True

        possibleClue=syns[0].definition()
        if len(possibleClue) != 0: 
            if Plural:
                possibleClue = possibleClue + " (Plural)"
                originalClue.append(possibleClue)
            else:
                originalClue.append(possibleClue)

        else:
            print("no definition clues available")
            originalClue=-1


        print("Your clues so far:" + str(originalClue))



        possibleClue=syns[0].examples()
        if len(possibleClue) != 0: 
            line=possibleClue[0].split(" ") 
            print(line)
            for word in line:
                if word == entry:
                    print(len(word))
                    line[len(word)]="...."
                if word == plurality_check:
                    print(len(word))
                    line[len(word)]="...."

            possibleClue=" "
            if Plural:
                possibleClue = possibleClue.join(line)+ " (Plural)"
                originalClue.append(possibleClue)
            else:
                possibleClue = possibleClue.join(line)
                originalClue.append(possibleClue)

        else:
            print("no example clues available")
            originalClue=-1
            #return originalClue


        print(originalClue)
    
except:
    print("Entry couldn't found in the wordnet")
    originalClue=-1



    
# =============================================================================
# print(possibleClue)
# print("Your clues so far:" + str(originalClue))
# =============================================================================



    return originalClue
