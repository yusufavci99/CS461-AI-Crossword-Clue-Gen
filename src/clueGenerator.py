from nltk.corpus import wordnet
import nltk
import wikipedia
from nltk import pos_tag
from nltk import RegexpParser
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
import requests 
from bs4 import BeautifulSoup

def merriamSynonym(word):
    r = requests.get("https://www.merriam-webster.com/dictionary/{}".format(word))
    soup = BeautifulSoup(r.content, "html.parser")
    sth = soup.find("ul",attrs={"class":"mw-list"})
    sth = str(sth)
    new = ''
    start = 0
    for i in range(len(sth)):
        if sth[i] == '>':
            start += 1
        elif start == 3 and sth[i] == '<':
            break
        elif start == 3:
            new += sth[i]
    return new

def merriamDefinition(word):
    r = requests.get("https://www.merriam-webster.com/dictionary/{}".format(word))
    soup = BeautifulSoup(r.content, "html.parser")
    mean = soup.find("span",attrs={"class":"dtText"}).text
    mean = mean[2:]
    mean = removeParantheses(mean)
    return mean

def replaceWithSynonyms(sentence):
    tokenized = nltk.word_tokenize(sentence)
    pos = nltk.pos_tag(tokenized)

    result = []
    for token in tokenized:
        nt = merriamSynonym(token)
        if nt != '' and (' ' not in nt):
            result.append(nt)
        else:
            result.append(token)
    #print(result)
    #print(pos)
    pos2 = nltk.pos_tag(result)
    #print(pos2)
    newSentence = ''
    for i in range(len(pos)):
        if pos[i][1] == 'IN':
        
            if pos[i][1] == pos2[i][1]:
                newSentence += pos2[i][0] + ' '
            else:
                newSentence += pos[i][0] + ' '
        else:
            newSentence += pos2[i][0] + ' '
            
    newSentence[:-1]
    return newSentence


def removeParantheses(word):
    print('Removing parantheses and improper signs from: ', word)
    paranthesesDepth = 0
    newWord = ''
    for i in range(len(word)):
        if word[i] == '(':
            paranthesesDepth += 1
        elif word[i] == ')':
            paranthesesDepth -= 1
        elif word[i] == ':' or word[i] == ';':
            break
        elif paranthesesDepth == 0:
            newWord += word[i]
    print('Result: ', newWord)
    return newWord

def trimSentence(sentence):
    print('Trimming the fetched sentence: ', sentence)
    foundIndex = None
    amisare = ('am', 'is', 'are')
    words = nltk.word_tokenize(sentence)
    pos = nltk.pos_tag(words)
    for i in range(len(pos)):
        if pos[i][0] in amisare:
            foundIndex = i
            break
        
    if foundIndex==None:
        return sentence
    result = ''
    for i in range(foundIndex + 1, len(words)):
        result += words[i] + ' '
        result[:-1]
        
    print('Result: ', result)
    return result

def createNewClue(originalClue, entry):
    
    porter = PorterStemmer()
    Plural = 0
    entry_present_tense=0
    entry_past_tense=0
    entry_foreign_word=0
    generate_noun_clue=0
    
    token=nltk.pos_tag([entry])
    for t in token:
        if t[1] == 'FW':# NYT RULE #4 CHECKING FOREIGN WORDS
            entry_foreign_word=1
            # check original clue
        if t[1] == 'NNS'or t[1] == 'NNPS': #NYT RULE #3 CHECKING PLURALITY CONDITION
            Plural = 1 
        if t[1] == 'VBD' or t[1] == 'VBN':# NYT RULE #1 TENSES MUST BE MATCHED, so we control the tense of the entry(word)
            entry_past_tense=1
            #print('Entry tense is past tense')
        if t[1] == 'VBP' or t[1] == 'VBZ':# NYT RULE #1 TENSES MUST BE MATCHED, so we control the tense of the entry(word)
            entry_present_tense=1
            #print('Entry tense is present tense')
        if t[1].find('NN') == 0 or t[1].find('NNS') == 0 or t[1].find('NNP') == 0:# given entry must corresponds to noun as well. Rule #2 NYT "PART OF SPEECH"
            generate_noun_clue=1
            #print('generating a noun clue')  
    
    
    possibleClues=[]
    print('Starting the search in wordnet for ' + entry + '...')
    try:
        syns = wordnet.synsets(entry)
    #plurality_check=syns[0].lemmas()[0].name()
        try:
            possibleClues.append(removeParantheses(syns[0].definition()))
        except:
            print('Definition not found in wordnet')
        try:
            #possibleClues.append(syns[0].examples())
            
            for example in syns[0].examples():
                
                possibleClues.append(removeParantheses(example))
                
            
        except:
            
            print('example is not found in wordnet')
        #print(possibleClues)
        
    except:
        print('Wordnet could not find anything.')
    print('Continue searching with merriam-webster dictionary...')
    try:
        possibleClues.append(removeParantheses(merriamDefinition(entry)))
        
    except:
        print('Webster could not find, right now!')
    try:      
        p = wikipedia.search(entry,results=1,suggestion=False)
        
        if len(p) != 0:# Check if there is a page related to the entry
            #searches=wikipedia.search(entry,results=1,suggestion=False)
            #Sentence=wikipedia.summary(p[0],sentences=1)
            possibleClues.append(removeParantheses(wikipedia.summary(p[0],sentences=1)))
            #page = wikipedia.page(p[0])
        
            print("search is successful, moving on...")
            
        
    except:
        print("search is unsuccessful, moving on...")
        
    print('found these clues: ')
    print(possibleClues)
    def artificialnlp(Sentence):

        tokenized_possible_clue = nltk.word_tokenize(Sentence)
        
        tokens_tag = nltk.pos_tag(tokenized_possible_clue)
        
        noun_phrase_element=[]
        if generate_noun_clue == 1:#  NYT RULE #2 'PART OF SPEECH'starts here for noun clue generation
            print('Generating artificial noun phrases...')
            #print('check point')
            #print(Sentence)
            tokenized_possible_clue = nltk.word_tokenize(trimSentence(Sentence))
            #print(tokenized_possible_clue)
            #print('check point 2')
            tokens_tag = nltk.pos_tag(tokenized_possible_clue)#token tags of the tokenized possible clue
            
    
            if porter.stem(entry.strip().lower()) in [porter.stem(w.lower()) for w in tokenized_possible_clue]:
                    
                a=0
                possibleClue = " "
                for word in tokenized_possible_clue:#omit similar wordings
                    a+=1
                    #print(word)
                    #print('hello')
                    #print(porter.stem(word.strip().lower()))
                    #print(porter.stem(entry.strip().lower()))
                    if porter.stem(word.strip().lower()) == porter.stem(entry.strip().lower()):
                        tokenized_possible_clue[a-1]="..."
                        
                possibleClue = possibleClue.join(tokenized_possible_clue)
                return possibleClue
            
            if len(tokenized_possible_clue) <= 5:
                return trimSentence(Sentence)
                            
            JJ_available=1
            NN_available=0
            NNS_available=0
            NNP_available=0
            IN_available=0
            NN_cnt=1
            endp = 1
            for parse in tokens_tag:# We successfully implement a meaninggul noun phrase for noun entry
                
                #print(parse)
                          
                if parse[1] == 'JJ':
                    noun_phrase_element.append(parse[0] + ' ')
                    JJ_available=1
                    endp = 1
                    #print(parse[1])
                    #print('Starting with adding JJ to the noun phrase...')
                    
                if parse[1] == 'NNP' and JJ_available == 1: 
                    noun_phrase_element.append(parse[0] + ' ')
                    NNP_available=1
                    endp = 1
                    #print('Continuing with adding NNP into the noun phrase if JJ is available...')
                    #print(parse[1])
                    
                if Plural:
                    if parse[1] == 'NN'and JJ_available == 1:
                        noun_phrase_element.append(parse[0] + 's')
                        NN_available=1
                        NN_cnt+=1
                        endp = 1
                
                
                if parse[1] == 'NN'and JJ_available == 1 and Plural == 0:
                    noun_phrase_element.append(parse[0] + ' ')
                    NN_available=1
                    NN_cnt+=1
                    
                    endp = 1
                    #print('Continuing with adding NN into the noun phrase if JJ is available...')
                    #print(parse[1])
                    
                
                if parse[1] == 'NNS'and NN_available == 0 and JJ_available == 1 and NN_cnt!=2:
                    noun_phrase_element.append(parse[0] + ' ')
                    NNS_available=1
                    endp = 1
                    #print('Continuing with adding NNS into the noun phrase if JJ is available but NN is not available...')
                    #print(parse[1])
                    
                if parse[1] == 'IN'  and (NNS_available == 1 or NN_available == 1):
                    noun_phrase_element.append(parse[0] + ' ')
                    IN_available=1
                    endp = 0
                    #print('Continuing with adding IN into the noun phrase if NN or NNS is available...')
                    #print(parse[1])
        
                    
                if JJ_available == 1 and (NNS_available == 1 or NN_available == 1) and IN_available == 1 and NN_cnt==3 and endp:
                    
                    JJ_available=1
                    NN_available=0
                    NNS_available=0
                    #print(NN_cnt)
                    break
            
            possibleClue=" "
            #print('NOUN PHRASE ELEMENT')
            #print(noun_phrase_element)
            
            i=0
            for word in noun_phrase_element:#omit similar wordings
                i+=1
                if porter.stem(word.strip().lower()) == porter.stem(entry.strip().lower()):
                        noun_phrase_element[i-1]="..."
                    
        
             
            
            possibleClue = possibleClue.join(noun_phrase_element)
            #print(noun_phrase_element)
            newClues=possibleClue
            #print('Possible Clue is: ' + possibleClue)
            #newClues.append(possibleClue)
            #print(newClues)
            if len(newClues) > 1:# if we can't find that means no JJ in the possible clue
                if Plural:
                    newClues = possibleClue + '(Plural)'
                    return newClues
                    #print('PLURAL')
                    #print(newClues)
                #return newClues
                #print('New clue found!')
                return newClues
            
            else:# JJ is not in the sentence then, start with NN or NNS to build noun phrase
                #print('Starting the search without JJ element...')
                NN_available=0
                NNS_available=0
                IN_available=0
                NN_cnt=1
                for parse in tokens_tag:# We successfully implement a meaninggul noun phrase for noun entry
                    
                    #print(parse)# parsing each tokens
            
                    if parse[1] == 'NN' and NN_cnt!=2:
                        noun_phrase_element.append(parse[0] + ' ')
                        NN_available=1
                        NN_cnt+=1
                        #print('Continuing with adding NN into the noun phrase if JJ is available...')
                        #print(parse[1])
                    if parse[1] == 'NNS'and NN_available == 0 and NN_cnt!=2:
                        noun_phrase_element.append(parse[0] + ' ')
                        NNS_available=1
                        NN_cnt+=1
                        #print('Continuing with adding NNS into the noun phrase if JJ is available but NN is not available...')
                        #print(parse[1])
                        
                    if parse[1] == 'IN'  and (NNS_available == 1 or NN_available == 1):
                        noun_phrase_element.append(parse[0] + ' ')
                        IN_available=1
                        #print('Continuing with adding IN into the noun phrase if NN or NNS is available...')
                        #print(parse[1])
                        
                    if parse[1] == 'NNP' and IN_available == 1:
                        noun_phrase_element.append(parse[0] + ' ')
                        #print('Found IN, finding NN word...')
                        ##print(parse[1])
                        IN_available=0
                        
                    if (NNS_available == 1 or NN_available == 1) and IN_available == 1:
                        #newClues.append(noun_phrase_element)
                        NN_available=0
                        NNS_available=0
                        #IN_available=1
                newClues=[]
                possibleClue=""
                ##print('NOUN PHRASE ELEMENT')
                ##print(noun_phrase_element)
                
                i=0
                for word in noun_phrase_element:#omit similar wordings
                    i+=1
                    if porter.stem(word.strip().lower()) == porter.stem(entry.strip().lower()):
                        noun_phrase_element[i-1]="..."
                        
        
                    
                possibleClue = possibleClue.join(noun_phrase_element)
                
                if Plural:
                    newClues = possibleClue + ' (Plural)'
                    ###print('PLURAL')
                    return newClues
                newClues=possibleClue
                return newClues
                    
                ##print('New Clue is: ' + newClues)
                #return newClues
                
         
        elif generate_noun_clue == 0:
            
            possibleClue=" "
            i=0
            for word in tokenized_possible_clue:#omit similar wordings
                i+=1
                if porter.stem(word.strip().lower()) == porter.stem(entry.strip().lower()):
                    tokenized_possible_clue[i-1]="..."
                    
        
                    
            if entry_present_tense==1:
                possibleClue = possibleClue.join(tokenized_possible_clue)
                possibleCLue = possibleClue + "(Present)"
                newClues=possibleClue
                return newClues
            elif entry_past_tense==1:
                possibleClue = possibleClue.join(tokenized_possible_clue)
                possibleClue = possibleClue + "(Past)"
                newClues=possibleClue
                return newClues
            elif Plural:
                possibleClue = possibleClue.join(tokenized_possible_clue)
                possibleClue = possibleClue + "(Plural)"
                newClues=possibleClue
                return newClues
                    
                                        
            
            possibleClue = possibleClue.join(tokenized_possible_clue)
                    
            newClues=possibleClue
    
            return newClues
        
        

    if len(possibleClues) > 0:
         
        l_np=[]
        for sentence in possibleClues:
            l_np.append(artificialnlp(sentence))   
            #l_np.append(sentence)
        closest=-1
        closest_len=999
        print('Candidate clues are: ')
        print(l_np)
        print('Choosing the optimal length...')
        for b in range(len(l_np)):
            if abs(20-len(l_np[b])) < closest_len:
                closest = b
                closest_len = abs(16-len(l_np[b]))
        
        
        print('Choosen: ', l_np[closest])
        return l_np[closest].capitalize()
     
    else:
        return replaceWithSynonyms(originalClue).capitalize()

    
    #return replaceWithSynonyms(originalClue)



#print(createNewClue("fast wheels for children", "Bus"))

