from pyperclip import copy
from lib.prompting import Prompt
from lib.joplin_api import JoplinAPI
from odf.text import P, Span
from odf.style import Style, TextProperties

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
        message = "Enter this Message to the ChatGPT Prompt: Hey so i just got a Topic finished from a book and made notes of it. Can you analyze my notes, read it and make an Detailed exam out if it?"
        copy(message)
        self.prompt_instance.write_message(message)

    def next_step(self):
        self.prompt_instance.prompt_user("Are you ready to go to the next step? Click a Button")
        self.prompt_instance.send_logo()

    def prompt_exam(self, topic_id, document):
        markdown_file = self.api_instance.get_note_text(topic_id)

        message = "Here is my Markdown Text. Can you give me 15 Multiplie Choices Questions based on this Note? Here is my Markdown File: " + markdown_file["body"]
        copy(message)
        self.prompt_instance.write_message(message)

        self.next_step()

        output = self.prompt_instance.prompt_user("Enter the Output of ChatGPT:")

        self.write_topic(output, "Multiplie Choices Questions", document)

    def write_topic(self, text, capital, document):
        bold_style = Style(name="BoldText", family="text")
        bold_props = TextProperties(fontweight="bold")
        bold_style.addElement(bold_props)
        document.styles.addElement(bold_style)

        para = P()
        bold_span = Span(text=capital, stylename=bold_style)
        para.addElement(bold_span)
        para.addText(text)

        document.text.addElement(para)