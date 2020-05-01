import  requests 
from bs4 import BeautifulSoup
word = input("Enter a word: ")#take use input and store
r = requests.get("https://www.merriam-webster.com/dictionary/{}".format(word))
#Line 4: you ente any website you want to scrape. So up there i have Merriam-Webster site and ".format(word)" is basically telling programm to search the link and at the add word variable.
#{} mean that where we are going to paste our word variable

soup = BeautifulSoup(r.content, "html.parser")
#storing bs4 into soup and telling what to do.
#"html.parser tells which parser we are using..."


mean = soup.find("span",attrs={"class":"dtText"}).text
#soup, where bs4 is saved
#"span" tell which section in html to look for...you did have body, div, etc...instead of span
#attrs....being more specific to where to look for
#"class":"dtText"...tells program to go inside span tag and find class with name dtText
#you can find class, span, div and pther info in html. by highlighting the text...then right-mouse click and then click inspect
#.text is just going to print text without html tags...


print("The definition of " + word + " is" +mean)
#print mean....it will print any word definition that is stored in word variable.ca