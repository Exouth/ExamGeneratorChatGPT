from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import clear
from pyfiglet import figlet_format

class Prompt(PromptSession):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logo = figlet_format("ExamGenerator", font="cybermedium")
        self.prompt_Symbol = "[ExamGenerator] >"

        self.send_logo()

    def send_logo(self):
        self.clear_prompt()

        print(self.logo)
    
    def clear_prompt(self):
        clear()
    
    def promp_user_return(self, input_text, output_text):
        user_input = self.prompt_symbolic(input_text)
        self.write_message(output_text + 
                                 " " + 
                                 str(user_input))
        
        print("")

        return user_input
    
    def prompt_user(self, input_text):
        user_input = self.prompt_symbolic(input_text)
        print("")

        return user_input
    
    def write_message(self, message):
        print(self.prompt_Symbol + 
              " " + 
              message + 
              " ")

    def prompt_symbolic(self, text):
        output = self.prompt(self.prompt_Symbol + 
                             " " + 
                             text + 
                             " ")

        return output