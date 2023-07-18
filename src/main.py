import sys
sys.dont_write_bytecode = True

from lib.exam_prompt import ExamPrompt

engine = ExamPrompt("180bdc1f34ea46a48abaf34f2c121cb05391263a49a1b3c246c6241df172bf8dc06dd27d4c0b8edbc60eed6380be8b27566c6bcd7dfa34578efe5e0113605839")


engine.ask_exam_name()

engine.ask_topic_number()

engine.give_topic_notes()