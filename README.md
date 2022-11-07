# Crossword Clue Generator - CS461 Final Project

This program generates new clues for daily NYT mini crossword puzzle by Joel Fagliano. Uses web scraping from dictionaries and Wikipedia for finding a clue template and uses NLP to create a short realistic clue from that template.

## Getting Started

Program runs by just running MINI_demo.py in src. Note that there are some dependencies.

## Dependencies

* **Tkinter**

Used to create a GUI.
* **Selenium**

Used to get the puzzle from the nyt mini website.
* **ChromeDriver**

Works with selenium. To make the operations in chrome.
* **nltk**

An NLP library. We used WorNet in it.

## Source Summary

* **MINI_demo.py**

Gets the date from the internet and creates the GUI.

* **clueGenerator.py**

Generates a new clue by using the original clue and the answer (entry).

## Authors

CS-461 MINI Project Team

* **Yusuf Avci**
* **Mert Alagözlü**
* **Tuğçe Kavakderesi**
