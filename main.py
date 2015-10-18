from docx import Document
import json

file_path_1 = 'input/module1.docx'
file_path_2 = 'input/module1_305.docx'
question_title = "Запитання"


class Question:
    def __init__(self, title, question=None, correct_answers_list=None, wrong_answers_list=None):
        self.title = title
        self.question = question
        self.correct_answers_list = correct_answers_list
        self.wrong_answers_list = wrong_answers_list


class ParseHelper:
    def __init__(self, document_path):
        self.document_path = document_path

    def parse_doc(self):
        paragraph_divider = "\n\n" if self.document_path == file_path_1 else "\n"
        questions = []
        document = Document(self.document_path)
        paragraphs_iter = iter(document.paragraphs)
        for paragraph in paragraphs_iter:
            if paragraph.text.startswith(question_title):
                paragraph_text = paragraph.text
                question = Question(title=paragraph_text)
                correct_answers = []
                wrong_answers = []
                paragraph_index = 0

                while paragraph_text != paragraph_divider:
                    try:
                        iterator = next(paragraphs_iter)
                        paragraph_text = iterator.text

                        if not iterator.runs:
                            continue

                        if paragraph_index == 0:
                            paragraph_index += 1

                        if paragraph_index == 1:
                            question.question = paragraph_text
                            paragraph_index += 1
                            continue

                        if iterator.runs[0].bold:
                            correct_answers.append(iterator.text)
                            wrong_answers.append(iterator.text)
                        else:
                            if iterator.text != paragraph_divider:
                                wrong_answers.append(iterator.text)

                        paragraph_text = iterator.text

                        paragraph_index += 1
                    except StopIteration:
                        break

                question.wrong_answers_list = wrong_answers
                question.correct_answers_list = correct_answers
                if correct_answers:
                    questions.append(question)
                continue

        return questions


class JsonMaker:
    default_file_name = 'result.json'

    def __init__(self, objects, result_file_name=default_file_name):
        self.objects = objects
        self.result_file_name = result_file_name

    def get_json_array(self):
        json_array = []
        for item in self.objects:
            json_array.append({'question': item.question,
                               'answer': item.correct_answers_list[0],
                               'answers': item.wrong_answers_list
                               }
                              )

        return json_array

    def make_json_file(self):
        with open(self.result_file_name, 'w') as fp:
            json.dump(self.get_json_array(), fp=fp, indent=4, ensure_ascii=False)
            print('Successfully created ' + fp.name)


helper = ParseHelper(file_path_1)
questions_list_one = helper.parse_doc()

helper = ParseHelper(file_path_2)
questions_list_two = helper.parse_doc()

all_questions = questions_list_one + questions_list_two

json_maker = JsonMaker(all_questions)
json_maker.make_json_file()
