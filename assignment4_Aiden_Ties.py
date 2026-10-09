# assignment4_skeleton.py
# Starter skeleton for Assignment 4 - the SAME start for every variation.
#
# This runs AS-IS: type an ID, click Start, 3 fake trials, data saved.
# Every pattern you need appears here ONCE - your job is to replace the
# fake parts with the real Stroop task, and to replicate the patterns
# for what is missing (see the grading table in the assignment!):
# real trials, judging, the means, Pause, Quit, try/except, your variation.
#
# Remember the ritual for every method you add:
#   what goes IN? what comes OUT (return or print)? what is its ONE job?

import tkinter as tk
from random import randint, choice
from time import time


# ====================================================================
# PART 1: THE ENGINE - your experiment class (no tkinter in here!)
# ====================================================================


class Experiment:

    def __init__(self, nr_trials=10):
        # Born valid: every attribute exists with a safe default.
        self.__participant = "anon"
        self.__trials = []    
        self.__COLORS = ["red", "green", "blue"]
        for _ in range(nr_trials):
            word = choice(self.__COLORS)
            ink = choice(self.__COLORS)
            self.__trials.append((word, ink))    

        self.__results = []       # one entry per answered trial
        self.__current = 0
        self.__start_time = 0
        self.__total_congruent = 0
        self.__total_incongruent = 0
        self.__amount_congruent = 0
        self.__amount_incongruent = 0

#TODO Add type indicators in all functions 

    def set_participant(self, name: int):
        # in: str / out: nothing - a SETTER with a guard
        if name != "":
            self.__participant = name

    def get_participant(self) -> str:
        # in: nothing / out: str, returned
        return self.__participant

    def has_next(self) -> bool:
        # in: nothing / out: bool - are there trials left?
        return self.__current <= len(self.__trials) - 1

    def start_trial(self):
        # in: nothing / out: nothing - the stimulus is on screen NOW.
        self.__start_time = time()

    def record_response(self, key:str) -> bool:
        # in: str / out: bool - was the response correct?
        rt = time() - self.__start_time

        # Judges key against first letter of ink color
        correct = (key == self.get_current()[1][0])

        # Appends all info into .txt file
        self.__results.append(self.__participant + "/"
                              + str(self.__current + 1) + "/" + key + "/"
                              + str(correct) + "/" + str(round(rt, 3)))

        if correct:
            self.__total_congruent = self.__total_congruent + rt
            self.__amount_congruent = self.__amount_congruent + 1
        else:
            self.__total_incongruent = self.__total_incongruent + rt
            self.__amount_incongruent = self.__amount_incongruent + 1

        self.__current = self.__current + 1
        return correct

    def save_results(self, filename: str):
        # in: str / out: nothing - one line per trial, appended.
        with open(filename, "a") as f:
            for line in self.__results:
                f.write(line + "\n")

    def get_current(self):
        return (self.__trials[self.__current][0], self.__trials[self.__current][1])

    def get_means(self):
        congruent_mean = self.__total_congruent / self.__amount_congruent
        incongruent_mean = self.__total_incongruent / self.__amount_incongruent
        total_mean = (self.__total_congruent + self.__total_incongruent)/(self.__amount_congruent + self.__amount_incongruent)
        return {'General mean':total_mean, 'Congruent mean':congruent_mean, 'Incongruent mean':incongruent_mean,}

    
    



# ====================================================================
# PART 2: THE GUI - talks to the human, USES the engine
# ====================================================================

experiment = Experiment()

window = tk.Tk()
window.title("My Stroop experiment")
window.minsize(width=600, height=400)

stimulus_label = tk.Label(window, text="Type your participant ID,\nthen click Start",
                          font=("Arial", 32))
stimulus_label.pack(expand=True)
stimulus_label_correct = tk.Label(window, text="", fg='white', font=("Arial", 20))
stimulus_label_correct.pack(expand=True)

id_entry = tk.Entry(window, width=20)     # tkinter, not turtle: a text field
id_entry.pack()

button_frame = tk.Frame(window)           # a Frame groups the buttons
button_frame.pack(pady=10)
start_button = tk.Button(button_frame, text="Start")
start_button.pack(side="left", padx=5)

pause_button = tk.Button(button_frame, text="Pause")
pause_button.pack(side="left", padx=5)

quit_button = tk.Button(button_frame, text="Quit")
quit_button.pack(side="right", padx=5)

# TODO:
#   Pause must take effect BETWEEN trials (think: where does the trial
#   chain decide to continue?). Quit must SAVE first, then window.destroy().

# Only react to response keys while a stimulus is on screen - without
# this guard, a key during the fixation cross records a garbage RT!
accepting_keys = False



def next_trial():
    # Shows the next stimulus - or ends the experiment.
    if not experiment.has_next():
        finish()
        return
    stimulus_label.config(text="+", fg="black")      # fixation first
    window.after(randint(800, 1500), show_stimulus)  # then the stimulus


def show_stimulus():
    global accepting_keys
    stimulus_label.config(text=experiment.get_current()[0], fg=experiment.get_current()[1])
    experiment.start_trial()           # the clock starts NOW
    accepting_keys = True


def key_pressed(event):
    global accepting_keys
    if not accepting_keys:
        return                         # too early / between trials: ignore
    accepting_keys = False
    correct = experiment.record_response(event.keysym.lower())

    # Showing feedback Right/Wrong
    if correct:
        stimulus_label_correct.config(text="Your last answer was right")
    else:
        stimulus_label_correct.config(text="Your last answer was wrong")

    next_trial()


def start():
    # reads the Entry, guards it, hands the ID to the ENGINE
    pid = id_entry.get().strip()
    if pid == "":
        stimulus_label.config(text="Please enter a participant ID!")
        return
    experiment.set_participant(pid)
    id_entry.destroy()        # the form leaves the stage
    start_button.destroy()
    next_trial()


def finish():
    experiment.save_results(experiment.get_participant() + ".txt")
    stimulus_label.config(text="Done! Thank you.", fg="white")

    pause_button.destroy()
    start_button.destroy()
    quit_button.destroy()
    stimulus_label_correct.destroy()

    for key in experiment.get_means():
        text = tk.Label(
            window,
            text=f"{key}: {round(experiment.get_means()[key], 3)}",
            fg="white",
            font=("Arial", 20)
        )
        text.pack()

    destroy_button = tk.Button(window, text="Destroy window")
    destroy_button.config(command=window.destroy)
    destroy_button.pack(pady=20)


start_button.config(command=start)
quit_button.config(command="") #TODO build a Quit function

window.bind("r", key_pressed)
window.bind("g", key_pressed)   
window.bind("b", key_pressed)

window.mainloop()
