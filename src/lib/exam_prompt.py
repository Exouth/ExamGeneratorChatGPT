import sys
from pyperclip import copy
from lib.prompting import Prompt
from lib.joplin_api import JoplinAPI
from odf.text import P, Span, List, ListItem
from odf.style import Style, TextProperties
from odf import easyliststyle

class ExamPrompt():

    def __init__(self, joplin_api):
        self.name = ""
        self.topic_number = ""
        self.prompt_instance = Prompt()
        self.api_instance = JoplinAPI(joplin_api)

    def ask_exam_name(self):
        self.name = self.prompt_instance.promp_user_return("What is the Exam Name?", "You set the Exam name to")
        return self.name

    def ask_topic_number(self):
        self.topic_number = self.prompt_instance.promp_user_return("What is the Topic Number?", "You set the Topic Number to")

    def give_topic_notes(self):
        matching_notes = self.api_instance.find_all_topic_notes(self.topic_number)

        for note in matching_notes:
            page, note_id, title = note
            self.prompt_instance.write_message(f"Used Note - Page: {page}, ID: {note_id}, Title: {title}")

        return matching_notes
    
    def give_initial_Exam_Message(self):
        message = "Hey so i just got a Topic finished from a book and made notes of it. Can you analyze my notes, read it and make an Detailed exam out if it?"
        copy(message)
        self.prompt_instance.write_message(message)

    def next_step(self):
        self.prompt_instance.prompt_user("Are you ready to go to the next step? Click a Button")
        self.prompt_instance.send_logo()

    def prompt_exam(self, topic_id, document):
        markdown_file = self.api_instance.get_note_text(topic_id)

        # Multiplie Choice Questions
        message = "Here is my Markdown Text. Can you give me 15 Multiplie Choices Questions based on this Note? Also put the Characters '+++' after each Multiplie Choice at the end without the Answer just the Characters! Here is my Markdown File: " + markdown_file["body"]
        copy(message)
        self.prompt_instance.write_message(message)

        self.next_step()

        output = self.prompt_instance.prompt_user("Enter the Output of ChatGPT:")

        self.write_topic(output, "Multiplie Choices Questions", document)

        self.next_step()

        # True or False Questions
        message = "Here is my Markdown Text. Can you give me 10 True or False Questions based on this Note? Also put the Characters '+++' after each True or False Question at the end without the Answer just the Characters! Here is my Markdown File: " + markdown_file["body"]
        copy(message)
        self.prompt_instance.write_message(message)

        self.next_step()

        output = self.prompt_instance.prompt_user("Enter the Output of ChatGPT:")

        self.write_topic(output, "True or False Questions", document)

        self.next_step()

        # Full Sentence Answers
        message = "Here is my Markdown Text. Can you give me 15 Full Sentence Questions, where i need to answer with an Full Sentence based on this Note? Also put the Characters '+++' after each Full Sentence Question at the end without the Answer just the Characters! Here is my Markdown File: " + markdown_file["body"]
        copy(message)
        self.prompt_instance.write_message(message)

        self.next_step()

        output = self.prompt_instance.prompt_user("Enter the Output of ChatGPT:")

        self.write_topic(output, "Full Sentence Answer", document)

        self.next_step()

    def write_topic(self, text, capital, document):
        splitted = text.split("+++")

        bold_style = Style(name="BoldText", family="text")
        bold_props = TextProperties(fontweight="bold")
        bold_style.addElement(bold_props)
        document.styles.addElement(bold_style)

        listStyle = easyliststyle.styleFromList('num1', "1", '0.25in', easyliststyle.SHOW_ALL_LEVELS)
        document.styles.addElement(listStyle)

        para = P()
        bold_span = Span(text=capital, stylename=bold_style)
        para.addElement(bold_span)
        
        listElement = self.createList(splitted, "", "num1")

        document.text.addElement(para)
        document.text.addElement(listElement)

        paraWhitespace = P()
        paraWhitespace.addText(" ")

        document.text.addElement(paraWhitespace)

    def createList(self, itemList, indentDelim, styleName):
        listArray = []
        listItem = ListItem()
        level = 0
        lastLevel = 0

        for levCount in range(0,10):
            listArray.append(None)
        listArray[0] = List()

        for item in itemList:
            level = 0;
            while (level < len(item) and item[level] == indentDelim):
                level +=1
            item = item[level:]

            if (level > lastLevel):    # open the sub-levels
                for levCount in range(lastLevel+1, level+1):
                    listArray[levCount] = List()
            elif (level < lastLevel):    # close off the intervening lists
                for levCount in range(lastLevel, level, -1):
                    listArray[levCount-1].childNodes[-1].addElement(listArray[levCount])

            # now that we are at the proper level, add the item.
            listArray[level].setAttribute( 'stylename', styleName );
            listItem = ListItem()

            para = P(text=item);
            listItem.addElement(para);
            listArray[level].addElement(listItem);
            lastLevel = level;

        # close off any remaining open lists
        for levCount in range(lastLevel, 0, -1):
            listArray[levCount-1].childNodes[-1].addElement(listArray[levCount])
        return listArray[0]
    
    def exit(self):
        self.prompt_instance.write_message("Exam sucessfully generated! Exiting now!")
        sys.exit(1)