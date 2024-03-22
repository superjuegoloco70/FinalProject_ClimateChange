import speech_recognition as sr
import time
import random
from scrapping import summarization, scrap
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func



engine = create_engine('sqlite:///facts.db', echo=True)

Base = declarative_base()

class DB(Base):
    __tablename__ = 'facts'

    id = Column(Integer, primary_key=True)
    fact = Column(String)

Session = sessionmaker(bind=engine)
session = Session()

def recognize_audio():
    global said
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    said = r.recognize_google(audio)

    try:
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    
def chat_bot_VC():
    while True:
        print("Hello, what do you want to do?")
        print("1: Tell me a random fact\n2: Add a fact\n3: exit")
        recognize_audio()
        if said == "first":
            random_entry = session.query(DB).order_by(func.random()).first()
            print("Random fact:", random_entry.fact)
        elif said == "second":
            recognize_audio()
            new_fact = said
            user = DB(fact=new_fact)
            session.add(user)
            session.commit()
        elif said == "third":
            cs_input = input("1:With a class, 2:Without a class: ")
            if cs_input == "1":
                link = input("Input an URL: ")
                tag = input("Input a tag:" )
                cs = input("Input a class: ")
                summarization(scrap(link, tag, cs))
            elif cs_input == "2":
                link = input("Input an URL: ")
                tag = input("Input a tag:" )
                summarization(scrap(link, tag))
        elif said == "fourth":
            break
        else:
            print("error")
        time.sleep(1)

def chat_bot():
    while True:
        print("Hello, what do you want to do?")
        print("1: Tell me a random fact\n2: Add a fact\n3: Resume a text\n4: exit")
        said = input("Choose one: ")
        if said == "1":
            n = random.randint(1,5)
            if n == 3:
                summarization()
            else:
                random_entry = session.query(DB).order_by(func.random()).first()
                print("Random fact:", random_entry.fact)
        elif said == "2":
            new_fact = input("Write a new fact: ")
            user = DB(fact=new_fact)
            session.add(user)
            session.commit()
        elif said == "3":
            cs_input = input("1:With a class, 2:Without a class: ")
            if cs_input == "1":
                link = input("Input an URL: ")
                tag = input("Input a tag:" )
                cs = input("Input a class: ")
                summarization(scrap(link, tag, cs))
            elif cs_input == "2":
                link = input("Input an URL: ")
                tag = input("Input a tag:" )
                summarization(scrap(link, tag))
        elif said == "4":
            break
        else:
            print("error")
        time.sleep(1)


def menu():
    while True:
        print("Chat bot")
        print("1: Write")
        print("2: Voice (May cause errors)")
        print("3: How to use voice")
        print("4: exit")
        select = input("Choose one: ")
        if select == "1":
                chat_bot()
        elif select == "2":
                chat_bot_VC()
        elif select == "3":
            print("To enter a function say first, second, third or fourth")
            print("If you want to resume a text, you will have to use the keyboard.")
            time.sleep(1)
        elif select == "4":
            break


menu()

