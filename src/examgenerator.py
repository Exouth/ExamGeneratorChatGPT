#!/media/marcel/2TBSSD/Coding/ExamGeneratorChatGPT/env/bin/python

import sys
sys.dont_write_bytecode = True

from lib.exam_prompt import ExamPrompt
from odf.opendocument import OpenDocumentText
from odf.text import P

engine = ExamPrompt("180bdc1f34ea46a48abaf34f2c121cb05391263a49a1b3c246c6241df172bf8dc06dd27d4c0b8edbc60eed6380be8b27566c6bcd7dfa34578efe5e0113605839")

try:

    name = engine.ask_exam_name()

    engine.ask_topic_number()

    toppic_notes = engine.give_topic_notes()

    engine.next_step()

    engine.give_initial_Exam_Message()

    engine.next_step()

    doc = OpenDocumentText()
    for topic in toppic_notes:
        page, note_id, title = topic
        engine.prompt_exam(note_id, title, doc)
        engine.next_step()

    doc.save(name);

    engine.exit()
    
except KeyboardInterrupt:
    engine.exit()