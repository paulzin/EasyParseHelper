from docx import Document

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
        self.parse_doc()

    def parse_doc(self):
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

                while paragraph_text != "\n\n":
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
                        else:
                            if iterator.text != "\n\n":
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

        for item in questions:
            print(item.title + "\n" + item.question + "\n" +
                  "WRONG: " + str(item.wrong_answers_list) + "\n" +
                  "CORRECT: " + str(item.correct_answers_list) + "\n\n")


# FIXME: file_path_2 parsing is not correct and it won't work
ParseHelper(file_path_1)
