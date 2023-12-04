import requests
import json
import random

class Trivia:
    def __init__(self) -> None:
        self.amount = 1
        self.category = 21
        self.difficulty = "easy"
        self.typ = "multiple"

        self.url = f"https://opentdb.com/api.php?amount={self.amount}&category={self.category}&difficulty={self.difficulty}&type={self.typ}"

    def get_questions(self):
        response = requests.get(self.url)
        data = json.loads(response.text)
        questions_response = data['results']
                
        question_o = []
        all_options = []
        correct_option = []

        for question in questions_response:

            for i in range(len(question["incorrect_answers"])):
                all_options.append(question["incorrect_answers"][i])

            question_o.append(question['question'])
            all_options.append(question["correct_answer"])
            correct_option.append(question["correct_answer"])


        random.shuffle(all_options)
        #print(question_o, all_options, correct_option)
        return [question_o, all_options, correct_option]
    
