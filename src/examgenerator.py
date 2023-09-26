#!/media/marcel/2TBSSD/Coding/ExamGeneratorChatGPT/env/bin/python

import sys
sys.dont_write_bytecode = True

from lib.exam_prompt import ExamPrompt
from odf.opendocument import OpenDocumentText
from odf.text import P

engine = ExamPrompt()

try:

    name = engine.ask_exam_name()

    engine.ask_note_path()

    engine.ask_topic_number()

    toppic_notes = engine.give_topic_notes()

    engine.next_step()

    engine.give_initial_Exam_Message()

    engine.next_step()

    doc = OpenDocumentText()
    for topic in toppic_notes:
        engine.prompt_exam(topic, doc)
        engine.next_step()

    doc.save(name);

    engine.exit()

except KeyboardInterrupt:
    engine.exit()

