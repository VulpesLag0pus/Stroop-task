
import tkinter as tk
from random import randint
from time import time
import engine

#                  ----Window and Widgets----

experiment = engine.Experiment()

window = tk.Tk()
window.title("My Stroop experiment")
window.minsize(width=600, height=400)

hearts_label = tk.Label(window, text="❤️❤️❤️❤️❤️", font=("Arial", 40))
hearts_label.pack(pady=20) # pady adds a space around the widget 

Stroop_test_label = tk.Label(window, text= 
                                        "STROOP TEST",
                                     font=("Arial", 32)   )
Stroop_test_label.pack(pady=20)


instructions_label = tk.Label(window, text= 
                                            "\n"
                                            "Words will appear in different colors. \n"
                                            "You will press the key that corresponds to the ink color, not the word. \n"
                                            "For example, press R = red     G = green   B = blue    Y = yellow. \n"
                                            "Respond fast as your reaction time is being measured. \n"
                                            "You have five hearts; if you get 5 answers wrong, the test will stop."
                                            "\n",   
                                            font=("Arial", 25))
instructions_label.pack(pady=20)                 

stimulus_label = tk.Label(window, text= (
    "Type your participant ID,\nthen click Start"
), 
                          font=("Arial", 32))
stimulus_label.pack(expand=True)    #allows the text to take up the extra space in the window
stimulus_label_correct = tk.Label(window, text="", fg='black', font=("Arial", 20))
stimulus_label_correct.pack(expand=True)

id_entry = tk.Entry(window, width=20)
id_entry.pack()

button_frame = tk.Frame(window)           # a Frame groups the buttons
button_frame.pack(pady=10)
start_button = tk.Button(button_frame, text="Start")
start_button.pack(side="left", padx=5)

pause_button = tk.Button(button_frame, text="Pause")
pause_button.pack(side="left", padx=5)

quit_button = tk.Button(button_frame, text="Quit")
quit_button.pack(side="right", padx=5)

#               ----Global variables----

accepting_keys: bool = False            # True if the stimulus is on screen waiting for user to press a key
pause_pressed: bool = False             # True if the experiment is paused
started: bool = False                   # It changes to be true if the start button is clicked
hearts: int = 5                         # shows the lives that user has left, ending the test once it reaches 0
after_id: str | None = None             # Allows the Pause function to cancel the current stimulus
retry_entry: tk.Entry | None = None     # Creates a new box to enter ID, if the previous ID save fails   
retry_button: tk.Button | None = None   # Is a button that retries saving with th enew inputted ID


#           ----Trials----

def next_trial() -> None: 
    """
    Input: nothing
    Output: nothing
    Job: starts the next trials or ends the experiment if none are there
    """
    global after_id
    if not experiment.has_next() or hearts == 0: 
        # Stops te experiments once the trials reaches ten or the user lost all their hearts/lives
        finish()
        if hearts == 0:
            # if the hearts run out it replaces the end window with the message 'done' with the message below 
            stimulus_label.config(text= "Your hearts ran out, you made too many mistakes!", fg="black")
        return
    stimulus_label.config(text="+", fg="black") # creates an addition sign inbetween trials
    after_id = window.after(randint(800, 1500), show_stimulus)

def color_stimulus() -> None:
    """
    Input: nothing
    Output: nothing
    Job: put the colored word on the screen
    """
    word, color = experiment.get_current()
    stimulus_label.config(text=experiment.get_current()[0], fg=experiment.get_current()[1])

def start_timer() -> None:
    """
    Input: nothing
    Output: nothing
    Job: starts the trial stopclock
    """
    global accepting_keys
    experiment.start_trial()
    accepting_keys = True

def show_stimulus() -> None:
    """
    Input: nothing
    Output: nothing
    Job: show word and start clock
    """
    color_stimulus()
    start_timer() 

def update_hearts() -> None:
    """
    Input: nothing
    Output: nothing
    Job: replaces the hearts to match the current heart count
    """
    global hearts
    text = []
    for _ in range(hearts):
        text.append("❤️")
    hearts_label.config(text=f'{"".join(text)}')

#           ----Answers----

def records_pressed_key(event: tk.Event) -> bool:
    """
    Input: the event: tk.Event, the key being pressed
    Output: checking if answer is true, if the key matched the ink color and false if not
    Job: to record the pressed key and feed to the engine
    """
    return experiment.record_response(event.keysym.lower())

def displays_answer(correct: bool) -> None:
    """
    Input: correct value, as true if the users input was right
    Output: nothing
    Job: shows if correct or not and will delete a heart if not
    """
    global hearts
    if correct:
        stimulus_label_correct.config(text="Your last answer was right")
    else:
        stimulus_label_correct.config(text="Your last answer was wrong")
        hearts -= 1
        update_hearts()

def key_pressed(event: tk.Event) -> None:
    """
    Input: event: tk.Event
    Output: nothing
    Job: it moves on from last key press, while recording answers
    """                         
    global accepting_keys
    if not accepting_keys:
        return                         # too early / between trials: ignore
    accepting_keys = False

    correct = records_pressed_key(event)
    displays_answer(correct)
    
    if pause_pressed is False:
        next_trial()

#           ----Saving and Quitting Experiment----
def is_valid_id(pid: str) -> bool:
    """
    Input: a participant ID
    Output: True if the ID is not empty and only has letters, numbers, - or _
    Job: checks that the ID is safe to use as a file name
    """
    return pid != "" and all(c.isalnum() or c in "-_" for c in pid)

def accept_id() -> bool:
    """
    Input: nothing
    Output: true if the ID is valid or false if it is empty or has special characters
    Job: validates the inputted ID and saves it
    """
    pid = id_entry.get().strip()
    if pid == "":
        stimulus_label.config(text="Please enter a participant ID!")
        return False
    if not is_valid_id(pid):
        stimulus_label.config(text="Use only letters, numbers, - or _")
        return False
    experiment.set_participant(pid)
    return True

def beginning_the_test() -> None:
    """
    Input: nothing
    Output: nothing
    Job: destroys screen and instructions to begin the test
    """
    global pause_pressed
    global started        
    id_entry.destroy()        # the form leaves the stage
    start_button.destroy()
    instructions_label.destroy()
    Stroop_test_label.destroy()
    pause_pressed = False     # a Pause clicked before Start must not carry over
    started = True
    next_trial()

def start() -> None:
    """
    Input: nothing
    Output: nothing
    Job: begins test
    """
    if accept_id():
        beginning_the_test()                      

    
def clear_screen() -> None:
    """
    Input: nothing
    Output: nothing
    Job: removes the test screen
    """
    pause_button.destroy()
    start_button.destroy()
    quit_button.destroy()
    stimulus_label_correct.destroy()

def results() -> None:
    """
    Input: nothing
    Output: nothing
    Job: displays the average reaction time for each condition and allows user to destroy window
    """
    means = experiment.get_means()
    for key in experiment.get_means():
            text = tk.Label(
                window,
                text=f"{key}: {round(experiment.get_means()[key], 3)}",
                fg="black",
                font=("Arial", 20)
            )
            text.pack()
    
    destroy_button = tk.Button(window, text="Destroy window")
    destroy_button.config(command=quit_experiment)
    destroy_button.pack(pady=20)

def finish() -> None:
    """
    Input: nothing
    Output: nothing
    Job: ends the test and shows results
    """
    stimulus_label.config(text="Done! Thank you.", fg="black")
    clear_screen()
    results()                                

def pause() -> None:
    """
    Input: nothing
    Output: nothing
    Job: stops current stimulus and resumes the ecperiment to the next trial
    """
    global pause_pressed 
    global accepting_keys
    global after_id
    if not started:
        return                          # Pause does nothing before Start
    if pause_pressed is False:
        stimulus_label.config(text="Paused", foreground="black")
        if after_id is not None:
            window.after_cancel(after_id)   # stop a pending stimulus
            after_id = None
        experiment.reset_trial() # ignores the unfinished trial's running time, thus it is not included in the recordings
        pause_pressed = True
        accepting_keys = False
    else:
        pause_pressed = False
        next_trial()

def quit_experiment() -> None:
    """
    Input: nothing
    Output: nothing
    Job: saves the results and closes the test window
    """
    global retry_entry, retry_button
    clear_screen()

    if experiment.save_results(experiment.get_participant() + ".txt"):
        window.destroy()
        return

    stimulus_label.config(
        text="Something went wrong with saving your data,\n"
             "please input an ID without special characters",
        fg="black")

    if retry_entry is None:
        retry_entry = tk.Entry(window, width=20)
        retry_entry.pack()
        retry_button = tk.Button(window, text="Save with new ID",
                                 command=save_with_new_id)
        retry_button.pack(pady=5)

def save_with_new_id() -> None:
    """
    Input: nothing
    Output: nothing
    Job: accepts a replacement ID and retries the save
    """
    if retry_entry is None:
        return
    new_id = retry_entry.get().strip()
    if not is_valid_id(new_id):
        stimulus_label.config(text="Use only letters, numbers, - or _",
                              fg="black")
        return
    experiment.set_participant(new_id)


    quit_experiment()

#               ----Butons and Bindings----

start_button.config(command=start) # connects the widget buttons on th ewindow screen to its written function
pause_button.config(command=pause)
quit_button.config(command=quit_experiment)

# it connects the key press with a responce in the functions above
window.bind("r", key_pressed)
window.bind("g", key_pressed)   
window.bind("b", key_pressed)
window.bind("y", key_pressed)

window.bind("R", key_pressed)
window.bind("G", key_pressed)   
window.bind("B", key_pressed)
window.bind("Y", key_pressed)

window.protocol("WM_DELETE_WINDOW", quit_experiment)

window.mainloop()

