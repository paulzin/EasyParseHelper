from docx import Document

file_path = 'input/module1.docx'
question_title = "Запитання"


class Question:
    def __init__(self, title, question=None, correct_answers_list=[], answers_list=[]):
        self.title = title
        self.question = question
        self.correct_answers_list = correct_answers_list
        self.answers_list = answers_list


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
                paragraph_index = 0
                while paragraph_text != "\n\n":
                    try:
                        iterator = next(paragraphs_iter)

                        if not iterator.runs:
                            continue

                        if paragraph_index == 1:
                            question.question = paragraph_text

                        #print(paragraph_text)

                        if iterator.runs[0].bold:
                            # question.correct_answers_list.append(iterator.text)
                            paragraph_text = "*** " + iterator.text + " ***"
                        else:
                            # question.answers_list.append(iterator.text)
                            paragraph_text = iterator.text

                        paragraph_index += 1
                    except StopIteration:
                        break
                questions.append(question)
                #print("\n\n")
                continue

        for item in questions:
            print(item.title + "\n" + item.question + "\n\n")


parse_helper = ParseHelper(file_path)
