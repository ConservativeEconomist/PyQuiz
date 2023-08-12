# Copyrighted under GNU GPLv3 (c) 2023, - by ConservativeEconomist

import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import random
import json

"""
Load questions from the questions JSON file, "questions.json", should be located in the root directory with this file
Allow the user to select a quiz topic from a graphical drop-down list and return the corresponding questions.
Return a list of tuples containing the questions, answers, and topics, either for the selected topic or for all topics
"""
def select_topic():
    try:                                                            # Try block to catch errors
        with open('questions.json', 'r') as file:                   # Open the 'questions.json' file as read only
            data = json.load(file)                                  # Load the information from the json file as data
            all_questions = data['questions']                       # Load all questions into a dictionary
            master_title = data['title']                            # Load the title from the json and
            topics = list(all_questions.keys())                     # Create a list of the Topics
    except FileNotFoundError:                                       # Attempt to find the speficied file
        messagebox.showerror("File Not Found", "The 'questions.json' file was not found in the root directory.")    # Display an error message if the file is not found
        return None, None                                           # Return None if an error is found
    except json.JSONDecodeError:                                    # Attempt to validate the json file
        messagebox.showerror("File Error", "The 'questions.json' file is corrupted or not in the expected format.") # Display an error message if the file can't be validated
        return None, None                                           # Return None if an error is found
    selected_topic = None                                           # Initialize a variable to store the selected topic
    window = tk.Tk()                                                # Create the main window using tkinter
    window.title("Select a Topic")                                  # Add window title
    label = tk.Label(window, text="Select a Topic:")                # Add a label to the window with the text "Select a Topic:"
    label.pack(padx=10, pady=5)                                     # Pack the label with padding
    combo = ttk.Combobox(window, values=topics + ["All Topics"])    # Create a drop-down list (Combobox) with the available topics, including an "All Topics" option
    combo.current(0)                                                # Set the default selection to the first item in the list
    combo.pack(padx=10, pady=5)                                     # Pack the options into the combo box

    def on_ok():                                                    # Define a function to be called when the "OK" button we are about to create is clicked
        nonlocal selected_topic                                     # Refer to the selected_topic variable in the enclosing scope
        selected_topic = combo.get()                                # Retrieve the selected topic from the drop-down list
        window.destroy()                                            # Close the window

    ok_button = tk.Button(window, text="OK", command=on_ok)         # Create the "OK" button and link it to the on_ok function
    ok_button.pack(padx=10, pady=5)                                 # Pack the button with padding
    window.mainloop()                                               # Start the main loop to display the window and await user interaction
                                                                    # After the user selects a topic and clicks "OK," process the selected topic
    if selected_topic == "All Topics":                              # If "All Topics" is selected, combine all questions from different topics  
        questions = []                                              # Initialize an empty list to store all questions from different topics
        for topic, topic_questions in all_questions.items():        # Iterate through all topics and their corresponding questions in the dictionary
            questions += [(question, answer, topic) for question, answer in topic_questions.items()]    # Add a tuple containing question, answer, and topic to the questions list for each question in the current topic
        return questions, master_title                              # Return the combined list of questions from all topics and the quiz title
    else:                                                           # If a specific topic is selected: 
        return [(question, answer, selected_topic) for question, answer in all_questions[selected_topic].items()], master_title   # Return the corresponding questions and the quiz title

class QuizInterface:                                                # Define the user interface for the quiz; including question presentation, score tracking, and progress display.
    """
    Initialize the QuizInterface with the main window and a set of questions.
    master: The main window (tkinter.Tk instance) for the quiz
    questions: A list of tuples containing the questions, answers, and topics
    score: Variable which will be updated as the user answers questions correctly
    """
    def __init__(self, master, questions, required_score):          # Constructor for the QuizInterface class, initializing the main window (master), the set of questions, and the required score to pass the quiz.
        self.master = master                                        # Reference to the main window
        self.score = 0                                              # Initialize the score to 0
        self.questions = questions                                  # Store the provided questions
        self.required_score = required_score                        # Store the requried score calculated in main
        self.create_widgets()                                       # Call to create the user interface components
        self.ask_question()                                         # Call to present the first question

    def create_widgets(self):                                       # Create the user interface components, specifically the progress bar to display the quiz progress.
        self.progress = ttk.Progressbar(self.master, length=200, mode='determinate')    # Create a progress bar using tkinter.ttk, with a fixed length of 200 and determinate mode
        self.progress.pack()                                        # Pack the progress bar into the main window

    def update_progress(self):                                      # Update the progress bar's value based on the current score.
        progress_value = (self.score / self.required_score) * 100   # Calculate progress as a percentage of required score
        self.progress['value'] = progress_value                     # Each point expands the progress bar proportionally
        self.master.update_idletasks()                              # Update idle tasks to ensure that the progress bar reflects the change immediately

    def ask_question(self):                                         # Define a method to create the question window
        self.master.title("Craps Keys Quiz")                        # Set the title
        self.question, self.answer, topic = random.choice(self.questions)   # Randomly select a question, answer, and topic
        is_yes_no_question = self.answer.lower() in ["yes", "no"]   # Assign a function to check if the answer is "yes" or "no"
        if is_yes_no_question:                                      # Start If loop to check "yes" or "no"
            self.options = ["Yes", "No"]                            # If the answer is "yes" or "no", only present those options
        else:                                                       # If the answer is anything other than "yes" or "no":
            same_topic_questions = [value for q, value, t in self.questions if q != self.question and t == topic]   # Select incorrect answers from the same topic
            self.options = random.sample([opt for opt in same_topic_questions if opt.lower() not in ["yes", "no"]], 3) + [self.answer]  # Combine incorrect answers with the correct answer, but do not include any "Yes" or "No" options.
            random.shuffle(self.options)                            # Shuffle the options
        
        self.question_label = tk.Label(self.master, text=self.question, wraplength=400, font=("Arial", 12)) # Create the display area for the question with a maximum width of 400
        self.question_label.pack(ipadx=20, ipady=10)                # Pack the question into the display area and give it padding

        self.buttons = []                                           # Initialize an empty list to store buttons for each option
        for option in self.options:                                 # Iterate through each answer option in the current set of options
            button = tk.Button(self.master, text=option, wraplength=300, command=lambda option=option: self.check_answer(option))   # Create a button for the current option using the master window, setting the text to the option, and limiting the width to 300; also, specify the command to be called when the button is clicked, passing the current option
            button.pack(padx=5, pady=3)                             # Pack the button into the main window, including padding
            self.buttons.append(button)                             # Append the created button to the list of buttons
    
    def check_answer(self, option):                                 # Define a method to check if the selected answer is correct
        if option.lower() == self.answer.lower():                   # Check if the selected option matches the correct answer (case insensitive)
            self.score += 1                                         # If the answer is correct, increment the score by 1
            messagebox.showinfo("Correct", f"Correct! Your score is now {self.score}. You need {self.required_score} to pass.") # Display a message indicating a correct answer, current score, and the score needed to pass
        else:                                                       # If the answer is not correct:
            self.score -= 1                                         # Reduce the score by 1
            messagebox.showinfo("Incorrect", f"Incorrect. The correct answer was {self.answer}. Your score is now {self.score}. You need {self.required_score} to pass.")   # Display a message indicating a correct answer, current score, and the score needed to pass

        self.update_progress()                                      # Call to update the progress bar based on the current score

        for button in self.buttons:                                 # Iterate through the list of buttons
            button.destroy()                                        # Destroy each one to clear the options
        self.question_label.destroy()                               # Destroy the label displaying the current question to clear it for the next question

        if self.score < self.required_score:                        # Check if the current score is less than the computed required score
            self.ask_question()                                     # If the score is less than the required score, call the method to present a new question
        else:                                                       # If the score is more than required score:
            self.master.destroy()                                   # Destroy the main window to end the quiz

def main():                                                         # Define the main function to execute the quiz application
    questions, master_title = select_topic()                        # Call the select_topic function to allow the user to select a quiz topic and store the corresponding questions
    if questions is None:                                           # Check if the return value is None (indicating an error with the file)
        return                                                      # Return and end the program if there was an error
    required_score = int(len(questions) * 0.8)                      # 80% of total questions, rounded down to the nearest whole number
    root = tk.Tk()                                                  # Create the main window using tkinter
    title = tk.Label(root, text=master_title, font=("Arial", 24))   # Create a label to display the title of the quiz, with specific text and font size
    title.pack(pady=20)                                             # Pack the title label into the main window, providing vertical padding
    QuizInterface(root, questions, required_score)                  # Create an instance of the QuizInterface class, passing the main window, selected questions, and required score
    root.mainloop()                                                 # Start the main loop to display the window and handle user interactions

if __name__ == "__main__":                                          # Check if the script is being run directly (not imported as a module)
    main()                                                          # If the script is run directly, call the main function to execute the quiz application
