Varun Shourie, Project Mental Anguish
Date: 11/29/2020

OVERVIEW:
This program serves as a trivia quiz management quiz system, where users can view, add, edit/modify, delete,
and search for questions. When the user is ready, they can switch to a quiz mode where
a random sample of 3 unique questions are chosen from the question pool provided by the user.
For more information on each portion of the game, refer to the sections below.

OPENING FILES:
The program will automatically open and read in a file called 'questions.csv' if it exists in the directory. If not
named as above, none of the user's questions will be loaded.
Another key requirement for the question file is that the question data have a header with comma separated values.
All question data and the header should be in order as listed below, separated by commas:
(1) Question Text - alphanumeric characters
(2) Point Value - one number, between 1-3
(3) Correct Choice Number - one number, between 1-4
(4) Choice 1 - alphanumeric characters
(5) Choice 2 - alphanumeric characters
(6) Choice 3 - alphanumeric characters
(7) Choice 4 - alphanumeric characters
(8) Feedback for Correct Answer - alphanumeric characters
(9) Feedback for Incorrect Answer - alphanumeric characters.
If there is no header or the question data is not listed in this order precisely, question data may be
excluded and/or corrupted when they are converted from the comma separated values.

SAVING DATA:
Your question data will be saved when you exit the program to a csv file also called 'questions.csv'. This means your
previous 'questions.csv' file will be overwritten with the newly generated 'questions.csv' file.
However, it will maintain the same appearance as your previous 'questions.csv' file, including the data headers
and the order of data as stated in the OPENING DATA section. For this reason, it is absolutely crucial that
the 'questions.csv' file is provided as stipulated in the OPENING DATA section. If not provided as stipulated,
your question data will be corrupted.

NOTE: if you prematurely stop the program execution using methods not covered in the section
titled EXITING THE PROGRAM, your changes to question data will not be saved.

EXITING THE PROGRAM:
To exit the program, please click the X in the top right hand corner OR click File -> Exit
in the top left hand menu dropdown.

FIRST SCREEN -- VIEWING QUESTIONS:
Upon bootup of the program, you will be directed to the View Questions portion of the program.
If there are more than 12 questions in your 'questions.csv' file, you must scroll with your mouse or click on
the scrollbar and drag up/down to view more questions. If a question is too long for the listbox,
use the horizontal scrollbar and drag to the left or right to gain a full view of the question.

Double click on a question in the listbox to view the question text, choices, correct choice number, point value,
and feedback for correct/wrong answers. Since this is a read-only mode, the user can only use their left/right
arrow keys and mouse clicks to look through long responses. The comboboxes to choose the correct choice and question
point value also have been disabled. Also, you cannot press the "clear input" and "save question" buttons --
you can only click "cancel your selection", which hides the question data until you double click on another question.

If you wish to come back to this first screen, click Manage Questions -> View All Questions on the window menu.

ADDING QUESTIONS:
If the user wishes to add any questions to their question list, they can click Manage Questions --> Add Questions
on the window menu. The screen will shift to a form with the same listbox of questions from the View Questions
screen. Except, the user cannot click on the questions to view the data only this time; they must go back to
View mode to do so.

In this form, the user can enter question text, choices, and the feedback by typing in the text via keyboard.
However, none of the responses can be blank (i.e. no response or only spaces in the response). If any
response is blank when pressing "Save Question", then the blank fields will be highlighted red, and
the user will be prompted to reenter the blank fields until all fields are not blank.

The comboboxes cannot be typed into to preserve data integrity; however, by clicking on the dropdown list arrow,
the user can select values (1-4 for correct choice and 1-3 for question point value) using a mouse click.
Upon opening the form, the values default to 1 for both comboboxes to prevent bad data.

If none of the fields are blank, clicking "Save Question" will save the question to the question list
and recreate the question listbox with your added question. This way, you can confirm the question was added.
Clicking the "Clear Input" button and clicking Manage Questions --> Add Questions on the window menu
will reset the Add Questions form to its initial state, even if the user is in the middle of providing input.

NOTE: While the trivia quiz game is responsive to larger text entries by the user for question text, choices,
and feedback in terms of formatting, the user should ensure responses are not unreasonably long (>300 characters).

MODIFY QUESTIONS:
To modify questions, click Manage Questions --> Modify Questions on the window menu.
The listbox of questions from View Mode and Add Mode is retained; if you double click on a question,
a form very similar to the one found in Add Questions mode opens up. This form also contains
fields for entering question text, choices, correct choice number, question point value, and feedback for correct/
wrong answers. Enter your changes into these fields via keyboard if a textbox, or via mouse click if a combobox.

Form input follows the same rules as Add Mode; there can be no blanks in text boxes when saving to your list
of questions, and users must click the dropdown list (the arrow) to select from the permitted values for
correct choice number and question point value. If there are blanks, the user will be re-prompted with the highlighted
blanks until all fields are not blanks.

Clicking on the "Cancel Selection" button will yield the same result as in View Mode - the question data entry
form will be hidden from sight until the user double clicks another question in the listbox to edit.
Another alternative option to reset the Modify Questions page is to click Manage Questions --> Modify Questions.

Clicking on the "Clear Input" button will yield the same result as in Add Mode - the data entry fields will
be completely erased in case the user wants to replace the existing question with a different question altogether.

Clicking on the "Edit Question" button will replace the selected question with the new data provided by the user and
re-initialize the listbox so you can ensure your data has been fully edited. The data entry form is also hidden
to show editing is complete. Unless you press "Edit Question", none of your changes to data in the form
will be saved to the question AT ALL.

DELETE QUESTIONS:
To delete questions, click Manage Questions --> Delete Questions on the window menu. To reset this page
to its initial state, you can also click this sequence. This page consists of a listbox similar to View Mode;
double click a question in the listbox to view the selected question's data and possibly delete it.

Since this is a read-only mode, similar rules apply from View Mode except for the buttons. Users can only use
left/right arrow keys and their mouse clicks to look through longer textbox responses. Comboboxes are also disabled for
data integrity.

Clicking on the button labeled "No" will cancel your selection and hide the question data until you double click
another question to possibly delete. Clicking on the button labeled "Yes" will delete the selected question and
readjust the listbox, allowing you to confirm the question has been deleted.

SEARCH FOR QUESTIONS:
To search for questions, click Search --> Search for Questions on the window menu.
Where prompted, enter a question's text, answer choice, or feedback that you remember from the question.
The program will update its matches as you type; there is no need to press a "Search" button or anything.
If there is at least a 30% match between your search and a question's text, answer choice, or feedback, it'll
be displayed into the listbox. The search results retain the original question number from
functionality within 'Manage Questions', in case the user wants them for later reference.

Double clicking on search results in the listbox will open up a read-only data entry form exactly like in View Mode.
You are allowed only to use your left/right arrow keys and mouses to look through longer text responses.
Comboboxes are disabled from manipulation by the user.  Clicking "Cancel Selection" will hide the data entry form
from user view until the user clicks on another search result populated in the searchbox. You cannot click
"Save Question" and "Clear Input".

If you wish to clear your listbox/search query and start over, you can either press "Clear search" or
Search --> Search for Questions on the window menu.

TAKE THE QUIZ:
To take a quiz, click Play --> Play Quiz Game on the menu. Every time you click in this sequence, a new quiz will be
generated with 3 unique questions randomly drawn from question data you have provided/modified throughout the program.
Therefore, this sequence also serves as a quiz reset mechanism.

Upon opening this quiz mode, you will be presented with information such as points earned out of the
total quiz points, the total number of questions asked, and the point value of the question. Below this information,
you will be presented with the question and 4 answer choices. You MUST select a choice to get the question right.

To select a choice, click the vicinity around the radiobutton for each choice (the same row as the button) or
the radiobutton itself, and the radiobutton should get selected.
Click "submit choice" to receive feedback on your selection.

Upon submitting, the total points earned out of the point total and total questions asked are updated.
The user is updated as to how many points they have earned on the question. The choices are highlighted red if
incorrect and green if correct. Lastly, a couple of sentences of feedback will let the user know of the
correct choice and provide them witty feedback regarding if they got the question wrong/right.

When they click "Next question", they will be prompted with information for the next question as mentioned in
paragraph 2 of this section; the steps in paragraphs 2-4 repeat until the user completely finishes the quiz,
at which point the game will present the total points earned out of the point total, the total questions asked,
and feedback for the quiz based on the user's score.

The user can transition to manage questions mode through either clicking on the 'Manage Questions' button
or clicking Manage Questions --> View All Questions to start back at square one of the application.
Similarly, they can take the quiz again by clicking on the button titled "Take the Quiz Again" or clicking
Play --> Play Quiz Game.

GRAPHICS:
Throughout the application a series of window icon graphics are utilized to signal certain events. They include:
Message symbol with dots -- used to signify you are answering a question in quiz mode or are in manage questions mode.
Green circle with checkmark -- when receiving feedback on a question, along with the window title and the
quiz screen, it signals that you got the question correct.
Red circle with X -- when receiving feedback on a question, along with the window title and quiz screen, it
signals that you got the question wrong.
Notification bell -- this signals you have reached the end of the quiz.

The images for these graphics were created by resizing royalty and attribution free .png files into small
.ico files for use as icons using Pillow. If the user wishes to replace these graphics with their own pictures,
they are welcome to change the arguments to the resize_photo function in the main application code with their own
files in the format '<filename>.<file_format>', and then change the thumbnail constants' values into
"thumbnail_<filename>.ico".

For the user's convenience, only pre-manipulation images have been provided since the window icons
are generated upon running the application.
