# Varun Shourie, CIS345, Tuesday/Thursday, 12:00PM-1:15PM, Project Mental Anguish
from tkinter import *
from tkinter import ttk
from tkinter import font
from difflib import SequenceMatcher
import csv
import os
import random
from PIL import Image


class Question:
    """A question provides read/write access to question text, points, choices, and feedback with validation
    as necessary."""

    def __init__(self, qstn_text='', qtn_points=1, crct_choice=0, choices=None, fdback=None):
        """Defines a question object to be used for easy storage with attributes such as the question text, the point
        value of the question in the game, a dictionary of choices, and a list of feedback."""

        self.question_text = qstn_text
        self.point_value = qtn_points
        self.correct_choice = crct_choice

        if choices is None:
            self.choices = []
        else:
            self.choices = choices

        if fdback is None:
            self.feedback = []
        else:
            self.feedback = fdback

    @property
    def choices(self):
        """Returns all question choices stripped of trailing and leading whitespace."""
        return [choice.strip() for choice in self.__question_choices]

    @choices.setter
    def choices(self, new_choices):
        """If 4 choices are not provided in the choices list, all choices are set to N/A. Else, if a choice
        is blank, then the choice is set to N/A to protect data integrity."""
        if len(new_choices) != 4:
            self.__question_choices = ['N/A', 'N/A', 'N/A', 'N/A']
        else:
            self.__question_choices = []
            for choice in new_choices:
                if choice.strip() == '':
                    self.__question_choices.append('N/A')
                else:
                    self.__question_choices.append(choice)

    @property
    def correct_choice(self):
        """Returns the choice number which indexes the correct answer in the choices list when decremented by 1. """
        return self.__correct_choice

    @correct_choice.setter
    def correct_choice(self, new_answer):
        """Sets the choice number selected by the user to the provided number if between 1 and 4."""
        if new_answer not in range(1, 5):
            self.__correct_choice = -1
        else:
            self.__correct_choice = new_answer

    @property
    def csv_representation(self):
        """Returns a list of values which can be appended to another list for storage in a .csv file. """
        csv_values = [f'{self.question_text}', self.point_value, f'{self.correct_choice}']
        for choice in self.choices:
            csv_values.append(f'{choice}')
        for statement in self.feedback:
            csv_values.append(f'{statement}')
        return csv_values

    @property
    def feedback(self):
        """Provides feedback for correct/incorrect responses without leading/trailing whitespace."""
        return [statement.strip() for statement in self.__feedback]

    @feedback.setter
    def feedback(self, new_feedback):
        """Validates the new feedback to ensure the list is 2 elements & does not contains blank string elements."""
        if len(new_feedback) != 2:
            self.__feedback = ['N/A', 'N/A']
        else:
            self.__feedback = []
            for statement in new_feedback:
                if statement.strip() == '':
                    self.__feedback.append('N/A')
                else:
                    self.__feedback.append(statement)

    @property
    def point_value(self):
        return self.__question_points

    @point_value.setter
    def point_value(self, new_qtn_points):
        """If the number of points the question is worth is not between 1-3, then it'll be automatically set to 1."""
        if new_qtn_points not in range(1, 4):
            self.__question_points = 1
        else:
            self.__question_points = new_qtn_points

    @property
    def question_text(self):
        """Returns the question text without trailing/leading whitespace. """
        return self.__question_text.strip()

    @question_text.setter
    def question_text(self, new_question):
        """Sets question text to invalid if newly provided question is blank."""
        if len(new_question) < 1:
            self.__question_text = 'Invalid Question'
        else:
            self.__question_text = new_question

    @classmethod
    def parse_question_info(cls, qtn_info):
        """Parses info from a list containing all question information and creates a question object."""
        if len(qtn_info) == 9:
            qtn_text = qtn_info[0]
            qtn_point_val = int(qtn_info[1])
            qtn_correct_choice = int(qtn_info[2])
            qtn_choices = [qtn_info[3], qtn_info[4], qtn_info[5], qtn_info[6]]
            feedback = [qtn_info[7], qtn_info[8]]

            return cls(qtn_text, qtn_point_val, qtn_correct_choice, qtn_choices, feedback)

    @staticmethod
    def format_text(text, max_chars):
        """Adds newlines to a string every max_chars characters to help label widgets display data correctly."""
        char_count = 0
        text = text.split(' ')
        formatted_text = ''

        for word in text:
            char_count = char_count + len(word) + 1
            if char_count < max_chars:
                formatted_text += f'{word} '
            else:
                formatted_text += f'\n{word} '
                char_count = 0

        return formatted_text

    @staticmethod
    def yield_random_questions(list_of_questions):
        """Yields the sum of the question set's points and then all of the randomly sampled questions."""
        pt_total = 0
        random_question_set = random.sample(list_of_questions, k=3)

        for qtn in random_question_set:
            pt_total += qtn.point_value
        yield pt_total

        for qtn in random_question_set:
            yield qtn

    def __str__(self):
        """Overrides string representation of a question to show its basic headline."""
        return f'{self.question_text}   Points: {self.point_value}'


class CSVFile:
    """Modular functionality relating to CSV file I/O easily accessible in one location. """

    @staticmethod
    def read_questions(filename):
        """Reads in the csv file of questions at the beginning of the program without the header."""
        try:
            with open(filename, 'r') as file:
                qtn_list = []
                qtn_count = 0
                temp_questions = csv.reader(file)

                for qtn in temp_questions:
                    if qtn_count != 0:
                        qtn_list.append(Question.parse_question_info(qtn))
                    qtn_count += 1
                return qtn_list
        except (FileNotFoundError, IOError):
            return list()

    @staticmethod
    def write_questions(filename, questions):
        """Writes the provided list of question objects after the user terminates the window into a csv file."""
        csv_questions = [qtn.csv_representation for qtn in questions]

        with open(filename, 'w', newline='') as file:
            write_data = csv.writer(file)
            write_data.writerow(['Question Text', 'Point Value', 'Correct Choice Number', 'Choice 1', 'Choice 2',
                                 'Choice 3', 'Choice 4', 'Feedback for Correct Answer',
                                 'Feedback for Incorrect Answer'])
            write_data.writerows(csv_questions)


class WidgetModifier:
    """Modular functionality used to modify widgets' characteristics and appearance."""

    @staticmethod
    def alter_variables(content, *widget_vars):
        """Sets StringVars to a provided string or IntVars to a provided integer."""
        for variable in widget_vars:
            if isinstance(variable, StringVar) and type(content) is str:
                variable.set(content)
            elif isinstance(variable, IntVar) and type(content) is int:
                variable.set(content)

    @staticmethod
    def check_for_blanks(text_variables_list, text_widget_list, regular_color):
        """When provided parallel lists of text variables and entry widgets, this method will change the color
         of the blank widgets and un-highlight non-blank widgets back to the regular color."""
        blank_widget_found = False

        for i in range(0, len(text_variables_list)):
            if text_variables_list[i].get().strip() == '':
                text_widget_list[i].config(bg='light salmon')
                blank_widget_found = True
            else:
                text_widget_list[i].config(bg=regular_color)
        return blank_widget_found

    @staticmethod
    def change_window_icon(window_name, icon_file_name):
        """Changes the window icon to the provided file name - must be '<filename>.ico'"""
        if os.path.isfile(icon_file_name):
            window_name.iconbitmap(icon_file_name)

    @staticmethod
    def change_titles(window_name, title_lbl, text=''):
        """Changes the window and application title label's text to ensure congruence between titles."""
        window_name.title(text)
        title_lbl.config(text=text)

    @staticmethod
    def initialize_listbox(listbox, list_of_questions, is_search_results):
        """Refills a list box with a list of questions provided by the user depending on the type of list provided."""
        listbox.delete(0, END)
        question_count = 0

        for qtn in list_of_questions:
            question_count += 1
            if not is_search_results:
                listbox.insert(END, f'Question {question_count}: {qtn}')
            else:
                listbox.insert(END, f'Question {qtn[0]}: {qtn[1]}')

    @staticmethod
    def pack(formatting_desired=False, *widgets):
        """Attempts to pack zero to many widgets as provided in sequential order. Packs to the RIGHT with 20px of
        horizontal padding if desired by the user."""
        for widget in widgets:
            if formatting_desired:
                widget.pack(side=RIGHT, padx=20)
            else:
                widget.pack()

    @staticmethod
    def pack_forget(*widgets):
        """Attempts to pack_forget zero to many widgets that are packed to its master widget."""
        for widget in widgets:
            widget.pack_forget()

    @staticmethod
    def wire_event(event, event_handler, widgets):
        """Wires the event to the event_handler function for all widgets provided in a list."""
        for widget in widgets:
            widget.bind(event, event_handler)


def add_menu():
    """Builds a comprehensive menu system for the Mental Anguish application's Main Window. """
    global window, app_font
    menu_bar = Menu(window, font=app_font)
    window.config(menu=menu_bar)

    # Add dropdown lists for each mode of the application
    file_menu = Menu(menu_bar, tearoff=False, font=app_font)
    manage_qstn_menu = Menu(menu_bar, tearoff=False, font=app_font)
    search_menu = Menu(menu_bar, tearoff=False, font=app_font)
    play_menu = Menu(menu_bar, tearoff=False, font=app_font)
    menu_bar.add_cascade(label='File', menu=file_menu)
    menu_bar.add_cascade(label='Manage Questions', menu=manage_qstn_menu)
    menu_bar.add_cascade(label='Search', menu=search_menu)
    menu_bar.add_cascade(label='Play', menu=play_menu)

    # Add commands which switch between different modes of the form and helps switch to quiz mode as well.
    file_menu.add_command(label='Exit', command=window_closing)
    manage_qstn_menu.add_command(label='View All Questions', command=toggle_view_mode)
    manage_qstn_menu.add_command(label='Add Questions', command=toggle_add_mode)
    manage_qstn_menu.add_command(label='Modify Questions', command=toggle_modify_mode)
    manage_qstn_menu.add_command(label='Delete Questions', command=toggle_delete_mode)
    search_menu.add_command(label='Search for Questions', command=toggle_search_mode)
    play_menu.add_command(label='Play Quiz Game', command=toggle_quiz_mode)


def add_question():
    """When the user presses the save/edit question button, this function inserts the question object to the
    questions list in the application and inserts the string representation of the object into the list box.
    If any blank fields exist, the question object is not constructed and the user is prompted again to reenter."""
    global points, question, choice1, choice2, choice3, choice4, correct_answer, correct_fback, incorrect_fback
    global question_list, question_listbox, input_feedback_lbl, edit_mode, listbox_index, entry_color
    global text_widgets, text_variables

    if WidgetModifier.check_for_blanks(text_variables, text_widgets, entry_color):
        input_feedback_lbl.config(text='Please fill in the red fields and try again.')
        input_feedback_lbl.pack(side=LEFT)
    else:
        temp_choices = [choice1.get(), choice2.get(), choice3.get(), choice4.get()]
        temp_feedback = [correct_fback.get(), incorrect_fback.get()]
        temp_question = Question(question.get(), points.get(), correct_answer.get(), temp_choices, temp_feedback)

        if edit_mode:
            question_list[listbox_index] = temp_question
            cancel_selection()
        else:
            question_list.append(temp_question)
        clear_form()
        WidgetModifier.initialize_listbox(question_listbox, question_list, False)


def cancel_selection():
    """Hides the form frame when the user opts to not view, edit, or delete the question."""
    global intake_form_frame, window
    window.geometry('800x400')
    clear_form()
    intake_form_frame.pack_forget()


def clear_form():
    """Resets the intake form to its initial state, most notably when a user presses the save/clear button."""
    global question, choice1, choice2, choice3, choice4, correct_fback, incorrect_fback, question_textbox
    global points_combobox, correct_answer_combobox, text_variables, text_widgets, entry_color, input_feedback_lbl

    # Resets colors of entry widgets back to its previous, regular color by temporarily filling them.
    WidgetModifier.alter_variables('a', question, choice1, choice2, choice3, choice4, correct_fback, incorrect_fback)
    WidgetModifier.check_for_blanks(text_variables, text_widgets, entry_color)

    input_feedback_lbl.pack_forget()
    question_textbox.focus()
    points_combobox.current(0)
    correct_answer_combobox.current(0)
    WidgetModifier.alter_variables('', question, choice1, choice2, choice3, choice4, correct_fback, incorrect_fback)


def clear_searches():
    """Resets the search for questions form to its initial state."""
    global question_listbox, search
    search.set('')
    question_listbox.delete(0, END)
    cancel_selection()


def delete_question():
    """Deletes the user's selected question when the user selects 'Yes' in the delete questions form."""
    global listbox_index, question_list, question_listbox
    question_list.pop(listbox_index)
    WidgetModifier.initialize_listbox(question_listbox, question_list, False)
    cancel_selection()


def end_game():
    """Provides the user with their quiz results once all questions have been exhausted, providing different
    feedback depending on the user's score."""
    global question_pts_label, question_label, radbuttons_frame, quiz_fback_label, pts_earned_total
    global point_total, window, thumbnail_alert, form_title_label, quiz_end_frame
    WidgetModifier.change_titles(window, form_title_label, 'Mental Anguish - End of Trivia Quiz')
    WidgetModifier.change_window_icon(window, thumbnail_alert)

    score = pts_earned_total / point_total
    if score > 0.85:
        feedback = 'Yay! You crushed it. You are a trivia master!'
    else:
        feedback = 'Try again to improve your score.'
    quiz_fback_label.config(text='\n| END OF QUIZ |\n\n' +
                                 f' You scored {pts_earned_total} points out of {point_total} points. {feedback}\n')

    WidgetModifier.pack_forget(question_pts_label, question_label, radbuttons_frame)
    quiz_fback_label.pack(ipadx=5)
    quiz_end_frame.pack(pady=10)


def move_to_next_question():
    """Automatically moves to the next random question, ending the game if questions are exhausted."""
    global quiz_qtn_generator
    try:
        populate_quiz_data(next(quiz_qtn_generator))
    except StopIteration:
        end_game()


def populate_quiz_data(qtn):
    """Populates all quiz widgets with a question's information when the quiz game has started or after
    the user receives feedback for a previous question."""
    global pts_earned_total, point_total, qstns_asked, pts_earned_label, qstns_asked_label, question_pts_label
    global question_label, choice1_radbutton, choice2_radbutton, choice3_radbutton, choice4_radbutton, quiz_submit_btn
    global radbuttons, user_selection, window, thumbnail_think, quiz_color, form_title_label, quiz_fback_label
    WidgetModifier.change_titles(window, form_title_label, f'Mental Anguish - Trivia Quiz Question {qstns_asked + 1}')
    WidgetModifier.change_window_icon(window, thumbnail_think)

    # Reset radio buttons back to normal color and clickable state, and remove feedback for the previous question.
    for choice in radbuttons:
        radbuttons[choice].config(bg=quiz_color, state=NORMAL)
    quiz_fback_label.pack_forget()
    user_selection.set(0)

    pts_earned_label.config(text=f'Points earned out of point total: {pts_earned_total}/{point_total}')
    question_pts_label.config(text=f'Point worth: {qtn.point_value}')
    question_label.config(text=f'Question: {Question.format_text(qtn.question_text, 80)}')
    choice1_radbutton.config(text=f'Choice 1: {Question.format_text(qtn.choices[0], 60)}')
    choice2_radbutton.config(text=f'Choice 2: {Question.format_text(qtn.choices[1], 60)}')
    choice3_radbutton.config(text=f'Choice 3: {Question.format_text(qtn.choices[2], 60)}')
    choice4_radbutton.config(text=f'Choice 4: {Question.format_text(qtn.choices[3], 60)}')
    quiz_submit_btn.config(text='Submit choice', command=lambda: provide_quiz_feedback(qtn))


def provide_quiz_feedback(qstn):
    """Provides prominent feedback to the user with the use of graphics (icons) and labels to show if they
     got a question (qstn) correct or wrong."""
    global pts_earned_total, qstns_asked, quiz_fback_label, question_pts_label, radbuttons, quiz_submit_btn
    global user_selection, thumbnail_green_check, thumbnail_red_x, window, form_title_label, qstns_asked_label
    global pts_earned_label
    qstns_asked += 1

    # Adjusts values based on whether if the user got a question right or wrong.
    if user_selection.get() == qstn.correct_choice:
        feedback = Question.format_text(qstn.feedback[0], 60)
        pts_earned = qstn.point_value
        pts_earned_total += qstn.point_value
        WidgetModifier.change_window_icon(window, thumbnail_green_check)
        title = f'Mental Anguish - Trivia Quiz Question {qstns_asked} - CORRECT'
    else:
        feedback = Question.format_text(qstn.feedback[1], 60)
        pts_earned = 0
        WidgetModifier.change_window_icon(window, thumbnail_red_x)
        title = f'Mental Anguish - Trivia Quiz Question {qstns_asked} - INCORRECT'
    WidgetModifier.change_titles(window, form_title_label, title)

    for choice in radbuttons:
        if choice == qstn.correct_choice:
            radbuttons[choice].config(bg='pale green', state=DISABLED)
        else:
            radbuttons[choice].config(bg='light salmon', state=DISABLED)

    if qstns_asked == 3:
        quiz_submit_btn.config(text=f'Finish Quiz', command=move_to_next_question)
    else:
        quiz_submit_btn.config(text=f'Next question', command=move_to_next_question)

    qstns_asked_label.config(text=f'Total questions asked: {qstns_asked}/3')
    pts_earned_label.config(text=f'Points earned out of point total: {pts_earned_total}/{point_total}')
    quiz_fback_label.config(text=f'Correct choice number: {qstn.correct_choice} - '
                                 f'{Question.format_text(feedback, 60)}')
    question_pts_label.config(text=f'Points earned: +{pts_earned} pts.')
    quiz_fback_label.pack(pady=10)


def resize_photo(*filenames):
    """Creates and saves an icon of files provided by the user. File names should be 'filename.extension'."""
    thumbnail_size = (32, 32)

    try:
        for filename in filenames:
            new_filename = filename.split('.')[0]
            picture = Image.open(filename)
            picture.thumbnail(thumbnail_size)
            picture.save(f'thumbnail_{new_filename}.ico')
    except (IOError, SyntaxError, TypeError):
        pass


def search_for_question(event):
    """Searches for a question based on its text, answer choices, or correct/wrong answer feedback and populates
    it in the question listbox whenever a user types a character in the Search Questions form."""
    global search, question_listbox, question_list, search_results_found
    question_listbox.delete(0, END)
    search_query = search.get()
    search_results_found = []
    question_count = 0

    for qstn in question_list:
        search_parameters = (qstn.question_text, qstn.choices[0], qstn.choices[1], qstn.choices[2], qstn.choices[3],
                             qstn.feedback[0], qstn.feedback[1])
        match_not_found = True
        search_parameter_num = 0

        # Loop only until a match has been found between the query and any part of the question's data.
        while match_not_found and search_parameter_num < len(search_parameters):
            if SequenceMatcher(None, search_query, search_parameters[search_parameter_num]).ratio() >= 0.3:
                match_not_found = False
            search_parameter_num += 1
        if not match_not_found:
            search_results_found.append((question_count + 1, qstn))

        question_count += 1
    WidgetModifier.initialize_listbox(question_listbox, search_results_found, True)


def toggle_add_mode():
    """Shifts the user's view of the Form from other modes (view, edit, delete, search, etc.) to Add Questions mode."""
    global intake_form_frame, question_listbox, form_title_label, listbox_label, save_button, clear_button, window

    toggle_modes(add=True)
    window.geometry('800x600')
    WidgetModifier.change_titles(window, form_title_label, 'Mental Anguish - Add Questions')
    listbox_label.config(text='Here is a list of current questions already present in memory for your reference.')
    save_button.config(state=NORMAL, text='Save Question', command=add_question)
    clear_button.config(state=NORMAL, text='Clear Input')

    # Change order of widgets in which they are packed and disable the listbox double click since we are in add mode.
    WidgetModifier.pack(True, save_button, clear_button)
    intake_form_frame.pack()
    question_listbox.bind('<Double-Button-1>', lambda event: 'break')


def toggle_modes(view=False, add=False, modify=False, delete=False, searching=False):
    """Toggles all modes and adjusts widgets common among the modes throughout the application."""
    global edit_mode, view_mode, delete_mode, search_mode, add_mode, intake_form_frame, question_section_frame
    global search_mode_frame, save_button, clear_button, cancel_button, question_listbox, window, points_combobox
    global question_list, quiz_end_frame, quiz_frame, thumbnail_think, text_widgets, correct_answer_combobox

    view_mode = view
    add_mode = add
    edit_mode = modify
    delete_mode = delete
    search_mode = searching

    clear_form()
    WidgetModifier.pack_forget(intake_form_frame, question_section_frame, search_mode_frame, save_button,
                               clear_button, cancel_button, quiz_end_frame, quiz_frame)

    # Permits only left/right arrow keypresses if in a read-only mode with question data.
    if view_mode or delete_mode or search_mode:
        WidgetModifier.wire_event('<Key>', validate_key, text_widgets)
        correct_answer_combobox.config(state=DISABLED)
        points_combobox.config(state=DISABLED)
    else:
        WidgetModifier.wire_event('<Key>', lambda event: None, text_widgets)
        correct_answer_combobox.config(state=NORMAL)
        points_combobox.config(state=NORMAL)

    # Series of non-mutually exclusive conditions in which widgets are reused and altered in similar ways.
    if not add_mode:
        window.geometry('800x400')
    if view_mode or edit_mode or search_mode:
        WidgetModifier.pack(True, save_button, clear_button, cancel_button)
        cancel_button.config(command=cancel_selection, text='Cancel Selection')
    if add_mode or view_mode or edit_mode or delete_mode or search_mode:
        question_listbox.bind('<Double-Button-1>', view_question)
        WidgetModifier.change_window_icon(window, thumbnail_think)
    if add_mode or view_mode or edit_mode or delete_mode:
        question_section_frame.pack()
    if not search_mode:
        question_listbox.config(height=12)
        WidgetModifier.initialize_listbox(question_listbox, question_list, False)
    if search_mode or view_mode:
        save_button.config(state=DISABLED, text='Save Question')
        clear_button.config(state=DISABLED, text='Clear Input')


def toggle_modify_mode():
    """Toggles edit mode on the form on, allowing users to double click a question to view contents like view
    mode on top of being able to edit the question and save it."""
    global window, form_title_label, save_button, clear_button, listbox_label
    toggle_modes(modify=True)
    WidgetModifier.change_titles(window, form_title_label, 'Mental Anguish - Modify Questions')
    listbox_label.config(text='Double click on a question to view and edit its existing data.')
    save_button.config(state=NORMAL, text='Edit Question', command=add_question)
    clear_button.config(state=NORMAL, text='Clear Input')


def toggle_delete_mode():
    """Switches on delete mode, which allows users to delete a question when they double click on the listbox."""
    global window, form_title_label, listbox_label, save_button, cancel_button, input_feedback_lbl
    toggle_modes(delete=True)
    WidgetModifier.change_titles(window, form_title_label, 'Mental Anguish - Delete Questions')
    listbox_label.config(text='Double click on a question to view and then delete its existing data.')
    save_button.config(state=NORMAL, text='Yes', command=delete_question)
    cancel_button.config(command=cancel_selection, text='No')
    input_feedback_lbl.config(text='Do you want to delete this question?')
    WidgetModifier.pack(True, save_button, cancel_button, input_feedback_lbl)


def toggle_quiz_mode():
    """Toggles the window to quiz mode, switching and packing widgets to show quiz information as necessary.
    Generates quiz data for the first question on boot up of quiz mode by the user."""
    global quiz_frame, question_list, point_total, quiz_submit_btn, quiz_qtn_generator, pts_earned_total
    global qstns_asked, window, qstns_asked_label, quiz_end_frame, pts_earned_label, question_pts_label
    global question_label, radbuttons_frame
    pts_earned_total = 0
    point_total = 0
    qstns_asked = 0

    toggle_modes()
    window.geometry('800x600')
    qstns_asked_label.config(text=f'Total questions asked: {qstns_asked}/3')

    # Gather the point totals of randomized question set and populate the first question's data.
    quiz_qtn_generator = Question.yield_random_questions(question_list)
    point_total = next(quiz_qtn_generator)
    populate_quiz_data(next(quiz_qtn_generator))

    quiz_end_frame.pack_forget()
    WidgetModifier.pack(False, quiz_frame, pts_earned_label)
    qstns_asked_label.pack(pady=10)
    question_pts_label.pack(anchor=E, pady=10)
    question_label.pack(pady=10)
    radbuttons_frame.pack()


def toggle_search_mode():
    """Switches on search mode, which allows users to search for questions and view questions when clicked on
    in the question listbox. """
    global window, form_title_label, question_listbox, search_mode_frame, question_section_frame
    toggle_modes(searching=True)
    clear_searches()
    WidgetModifier.change_titles(window, form_title_label, 'Mental Anguish - Search For Questions')
    question_listbox.config(height=7)
    WidgetModifier.pack(False, search_mode_frame, question_section_frame)


def toggle_view_mode():
    """Changes the visual layout of the form to View Questions Mode, enabling users to double click on a listbox
    element to populate the Main Window with user entries. """
    global window, form_title_label, listbox_label
    toggle_modes(view=True)
    window.geometry('800x400')
    WidgetModifier.change_titles(window, form_title_label, 'Mental Anguish - View Questions')
    listbox_label.config(text='Double click on a question to view its existing data.')


def validate_key(event):
    """Only permits left arrow or right arrow keys on the keyboard."""
    if event.keycode not in (37, 39):
        return 'break'


def view_question(event):
    """Accesses a question's data when the user selects it from the listbox and displays the entered contents
    below the list box in the View Questions section of the Main Window. """
    global question_listbox, question_list, intake_form_frame, points, question, choice1, choice2, choice3, choice4
    global correct_fback, incorrect_fback, correct_answer, view_mode, search_mode, edit_mode, listbox_index
    global search_results_found, window, delete_mode
    window.geometry('800x600')

    if edit_mode or delete_mode or view_mode or search_mode:
        listbox_index = question_listbox.curselection()[0]
    if not delete_mode:
        input_feedback_lbl.pack_forget()

    if not search_mode:
        temp_question = question_list[listbox_index]
    else:
        temp_question = search_results_found[listbox_index][1]

    # Set all fields to the user's previously provided input.
    question.set(temp_question.question_text)
    points.set(temp_question.point_value)
    correct_answer.set(temp_question.correct_choice)
    choice1.set(temp_question.choices[0])
    choice2.set(temp_question.choices[1])
    choice3.set(temp_question.choices[2])
    choice4.set(temp_question.choices[3])
    correct_fback.set(temp_question.feedback[0])
    incorrect_fback.set(temp_question.feedback[1])

    intake_form_frame.pack()


def window_closing():
    """Before the window closes and the app terminates, all questions are saved to a csv file."""
    global question_file, question_list
    CSVFile.write_questions(question_file, question_list)
    window.quit()


# Resize and save photo images to be used throughout the application.
thumbnail_think = 'thumbnail_think.ico'
thumbnail_alert = 'thumbnail_alert.ico'
thumbnail_red_x = 'thumbnail_red_x.ico'
thumbnail_green_check = 'thumbnail_green_checkmark.ico'
resize_photo('think.png', 'alert.png', 'red_x.png', 'green_checkmark.png')

# Used to track questions before, during, and after the application's execution.
question_file = 'questions.csv'
question_list = CSVFile.read_questions(question_file)
quiz_qtn_generator = iter([])

window_color = 'sky blue'
entry_color = 'light cyan'
btn_color = 'lavender'
quiz_color = 'light yellow'

# Flag values used for altering widgets between form modes.
view_mode = False
add_mode = False
edit_mode = False
delete_mode = False
search_mode = False

window = Tk()
window.config(bg=window_color)

# Objects used to hold/access/display user input responses currently or previously provided in widgets.
question = StringVar()
choice1 = StringVar()
choice2 = StringVar()
choice3 = StringVar()
choice4 = StringVar()
points = IntVar()
correct_answer = IntVar()
correct_fback = StringVar()
incorrect_fback = StringVar()
search = StringVar()
search_results_found = []
listbox_index = 0
user_selection = IntVar()

# Objects used to track figures during the trivia quiz game.
point_total = 0
pts_earned_total = 0
qstns_asked = 1

# Values to be stored in combo boxes for easy user selection.
point_values = [1, 2, 3]
choice_numbers = [1, 2, 3, 4]

# Font constants used to style all widgets with text.
title_font = font.Font(family='Cambria', size=13)
prompt_font = font.Font(family='Cambria', size=11)
app_font = font.Font(family='Calibri', size=11)

add_menu()

form_title_label = Label(window, bg=window_color, font=title_font)
form_title_label.pack()

# Frame which groups input widgets such as labels, comboboxes, and text boxes for gathering and displaying user input.
intake_form_frame = Frame(window, bg=window_color, width=800, height=600)
question_label = Label(intake_form_frame, text='Enter your question: ', bg=window_color, font=prompt_font)
question_label.grid(row=2, column=0, sticky=W, padx=10, pady=5)
question_textbox = Entry(intake_form_frame, justify=LEFT, textvariable=question, bg=entry_color, font=app_font,
                         width=76)
question_textbox.grid(row=2, column=1, sticky=W)

# Frame used to simulate creating a row in a grid with 4 widgets in 4 columns, with 2 textboxes and 2 labels.
choices_row1_frame = Frame(intake_form_frame, bg=window_color, width=800)
choices_row1_frame.grid(row=3, column=0, columnspan=2, sticky=W, padx=10)
choice1_label = Label(choices_row1_frame, text='Enter choice 1: ', bg=window_color, font=prompt_font)
choice1_label.pack(side=LEFT)
choice1_textbox = Entry(choices_row1_frame, justify=LEFT, bg=entry_color, textvariable=choice1, font=app_font,
                        width=35)
choice1_textbox.pack(side=LEFT, padx=10)
choice2_label = Label(choices_row1_frame, text='Enter choice 2: ', bg=window_color, font=prompt_font)
choice2_label.pack(side=LEFT)
choice2_textbox = Entry(choices_row1_frame, justify=LEFT, bg=entry_color, textvariable=choice2, font=app_font,
                        width=35)
choice2_textbox.pack(side=LEFT, padx=10)

# Frame used to simulate creating a row in a grid with 4 widgets in 4 columns, with 2 textboxes and 2 labels involved.
choices_row2_frame = Frame(intake_form_frame, bg=window_color, width=800)
choices_row2_frame.grid(row=4, column=0, columnspan=2, sticky=W, padx=10)
choice3_label = Label(choices_row2_frame, text='Enter choice 3: ', bg=window_color, font=prompt_font)
choice3_label.pack(side=LEFT, pady=10)
choice3_textbox = Entry(choices_row2_frame, justify=LEFT, bg=entry_color, textvariable=choice3, font=app_font,
                        width=35)
choice3_textbox.pack(side=LEFT, padx=10)
choice4_label = Label(choices_row2_frame, text='Enter choice 4: ', bg=window_color, font=prompt_font)
choice4_label.pack(side=LEFT)
choice4_textbox = Entry(choices_row2_frame, justify=LEFT, bg=entry_color, textvariable=choice4, font=app_font,
                        width=35)
choice4_textbox.pack(side=LEFT, padx=10)

# Frame used to simulate creating a row in a grid with 4 widgets in 4 columns, 2 of them containing combo boxes.
combo_boxes_frame = Frame(intake_form_frame, intake_form_frame, bg=window_color, width=800)
combo_boxes_frame.grid(row=5, column=0, columnspan=2, sticky=W, padx=10)

correct_ans_label = Label(combo_boxes_frame, text='Select the correct choice number: ', font=prompt_font,
                          bg=window_color)
correct_ans_label.pack(side=LEFT)
correct_answer_combobox = ttk.Combobox(combo_boxes_frame, values=choice_numbers, font=app_font,
                                       textvariable=correct_answer, width=16, justify=CENTER)
correct_answer_combobox.pack(side=LEFT, padx=10)
correct_answer_combobox.bind('<Key>', lambda event: 'break')

points_label = Label(combo_boxes_frame, text='Select the question point value:', font=prompt_font, bg=window_color)
points_label.pack(side=LEFT)
points_combobox = ttk.Combobox(combo_boxes_frame, values=point_values, justify=CENTER, font=app_font,
                               textvariable=points, width=18)
points_combobox.pack(side=LEFT, padx=10)
points_combobox.bind('<Key>', lambda event: 'break')

# Widgets used to gather user input for feedback on correct/incorrect responses.
fback_lbl = Label(intake_form_frame, text='Enter your feedback for when the user gets a question correct or wrong.',
                  bg=window_color, font=prompt_font)
fback_lbl.grid(row=6, column=0, columnspan=2, sticky=W, padx=10, pady=10)

correct_fback_lbl = Label(intake_form_frame, text='Correct answer feedback:', bg=window_color, font=prompt_font)
correct_fback_lbl.grid(row=7, column=0, sticky=W, padx=10)
correct_fback_textbox = Entry(intake_form_frame, justify=LEFT, bg=entry_color, textvariable=correct_fback,
                              font=app_font, width=76)
correct_fback_textbox.grid(row=7, column=1, sticky=W)

incorrect_fback_lbl = Label(intake_form_frame, text='Wrong answer feedback:', bg=window_color, font=prompt_font)
incorrect_fback_lbl.grid(row=8, column=0, sticky=W, padx=10, pady=5)
incorrect_fback_textbox = Entry(intake_form_frame, justify=LEFT, bg=entry_color, textvariable=incorrect_fback,
                                font=app_font, width=76)
incorrect_fback_textbox.grid(row=8, column=1, sticky=W)

# Groups all buttons and input validation feedback into one perceived row in the user interface.
button_frame = Frame(intake_form_frame, bg=window_color)
button_frame.grid(row=9, column=0, columnspan=2, pady=5)
save_button = Button(button_frame, text='Save Question', font=prompt_font, command=add_question, bg=btn_color)
clear_button = Button(button_frame, text='Clear Input', font=prompt_font, command=clear_form, bg=btn_color)
input_feedback_lbl = Label(button_frame, font=prompt_font, bg=window_color)
cancel_button = Button(button_frame, text='Cancel Selection', font=prompt_font, bg=btn_color)

# A listbox used throughout the question viewing, modification, addition, search, and removal processes
question_section_frame = Frame(window, bg=window_color)
question_section_frame.pack()
listbox_label = Label(question_section_frame, bg=window_color, font=prompt_font)
listbox_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
question_listbox_frame = Frame(question_section_frame, bg=window_color)
question_listbox_frame.grid(row=1, column=0, padx=10)
question_scrollbar = Scrollbar(question_listbox_frame)
question_horizontal_scrollbar = Scrollbar(question_listbox_frame, orient=HORIZONTAL)
question_listbox = Listbox(question_listbox_frame, width=105, height=12, font=app_font, bg='bisque',
                           yscrollcommand=question_scrollbar.set, xscrollcommand=question_horizontal_scrollbar.set)
question_horizontal_scrollbar.pack(side=BOTTOM, fill=BOTH)
question_listbox.pack(side=LEFT, fill=BOTH)
question_scrollbar.config(command=question_listbox.yview)
question_horizontal_scrollbar.config(command=question_listbox.xview)
question_scrollbar.pack(side=RIGHT, fill=Y)

# Series of widgets used to search for specific questions stored in memory.
search_mode_frame = Frame(window, bg=window_color)
search_label = Label(search_mode_frame, bg=window_color, font=prompt_font, text='Enter a question, answer choice, or '
                                                                                'answer\'s feedback:')
search_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
search_textbox = Entry(search_mode_frame, font=app_font, width=56, textvariable=search, bg=entry_color)
search_textbox.grid(row=0, column=1, sticky=W)
search_textbox.bind('<Key>', search_for_question)
clear_search_button = Button(search_mode_frame, font=prompt_font, width=20, text='Clear search', command=clear_searches,
                             bg=btn_color)
clear_search_button.grid(row=1, column=0, columnspan=2)

# Frame which encapsulates entire quiz game, provides general info about the ongoing quiz as well.
quiz_frame = Frame(window, bg=window_color, pady=10)
pts_earned_label = Label(quiz_frame, bg=quiz_color, font=prompt_font, relief=SUNKEN)
qstns_asked_label = Label(quiz_frame, bg=quiz_color, font=prompt_font, relief=SUNKEN)

# Displays specific information about the quiz as well.
question_pts_label = Label(quiz_frame, bg=quiz_color, font=prompt_font, relief=SUNKEN)
question_label = Label(quiz_frame, bg=quiz_color, font=prompt_font, justify=LEFT, relief=SUNKEN)
radbuttons_frame = Frame(quiz_frame, bg=quiz_color)
choice1_radbutton = Radiobutton(radbuttons_frame, variable=user_selection, value=1, font=app_font,
                                bg=quiz_color, width=70, justify=CENTER)
choice2_radbutton = Radiobutton(radbuttons_frame, variable=user_selection, value=2, font=app_font,
                                bg=quiz_color, width=70, justify=CENTER)
choice3_radbutton = Radiobutton(radbuttons_frame, variable=user_selection, value=3, font=app_font,
                                bg=quiz_color, width=70, justify=CENTER)
choice4_radbutton = Radiobutton(radbuttons_frame, variable=user_selection, value=4, font=app_font,
                                bg=quiz_color, width=70, justify=CENTER)
WidgetModifier.pack(False, choice1_radbutton, choice2_radbutton, choice3_radbutton, choice4_radbutton)
quiz_submit_btn = Button(radbuttons_frame, font=prompt_font, bg=btn_color)
quiz_submit_btn.pack(pady=10)
quiz_fback_label = Label(quiz_frame, bg=quiz_color, font=prompt_font, relief=SUNKEN, justify=LEFT)

# Two buttons which display at the end of the quiz game.
quiz_end_frame = Frame(window, bg=window_color)
play_quiz_btn = Button(quiz_end_frame, text='Take the Quiz Again', command=toggle_quiz_mode, font=prompt_font,
                       bg=btn_color)
manage_questions_btn = Button(quiz_end_frame, text='Manage Questions', command=toggle_view_mode, font=prompt_font,
                              bg=btn_color)
WidgetModifier.pack(True, manage_questions_btn, play_quiz_btn)

text_widgets = [question_textbox, choice1_textbox, choice2_textbox, choice3_textbox, choice4_textbox,
                correct_fback_textbox, incorrect_fback_textbox]
text_variables = [question, choice1, choice2, choice3, choice4, correct_fback, incorrect_fback]
radbuttons = {1: choice1_radbutton, 2: choice2_radbutton, 3: choice3_radbutton, 4: choice4_radbutton}

toggle_view_mode()
window.protocol('WM_DELETE_WINDOW', window_closing)
window.mainloop()
