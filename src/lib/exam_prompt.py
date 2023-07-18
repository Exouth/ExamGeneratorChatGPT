from lib.prompting import Prompt
from lib.joplin_api import JoplinAPI

class ExamPrompt():

    def __init__(self, joplin_api):
        self.name = ""
        self.topic_number = ""
        self.prompt_instance = Prompt()
        self.api_instance = JoplinAPI(joplin_api)

    def ask_exam_name(self):
        self.name = self.prompt_instance.promp_user_return("What is the Exam Name?", "You set the Exam name to")

    def ask_topic_number(self):
        self.topic_number = self.prompt_instance.promp_user_return("What is the Topic Number?", "You set the Topic Number to")

    def give_topic_notes(self):
        matching_notes = self.api_instance.find_all_topic_notes(self.topic_number)

        for note in matching_notes:
            page, note_id, title = note
            self.prompt_instance.write_message(f"Used Note - Page: {page}, ID: {note_id}, Title: {title}")

        return matching_notes