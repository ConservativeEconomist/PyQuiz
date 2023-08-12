# PyQuiz
This is a very lightweight quiz/flashcard app written while I was trying to learn python. It uses a .json file to store the questions in the following format:

    {
    "title": "Quiz Title Here",
    "questions":{
      "Topic 1": {
        "Question 1": "Answer 1",
        "Question 2": "Answer 2",
        "Question 3": "Answer 3",
        "Question 4": "Answer 4",
        },
      "Topic 2": {
        "Question 5": "Answer 5",
        "Question 6": "Answer 6",
        "Question 7": "Answer 7",
        "Question 8": "Answer 8",
        }
      }
    }


The program loads the title of the quiz from the json, it presents the user with a combobox of topics to select from and then displays a question, one correct answer and three random answers from each topic, unless the question has a yes or no answer, then it presents yes or no. The user has to be careful to not duplicate answers in the dictionary, there is no sanitaziation of the answers at this stage. I found this program very helpful when going through school, I would write questions and answers down throughout the day and then load them into the json file, when I wanted to review I could run the program and drill myself on the questions. Changing subjects is easy, I simply maintained different json files for each subject and loaded the one I wanted when I was ready to use the program. It keeps track of your score and requires you achieve a score equal to 80% of the questions in a given topic.

With generative AI, it should be even easier to generate questions these days. I thought someone else might get some use out of the project so it's here under GNU GPLv3.
