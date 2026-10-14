
# TODO what goes IN? what comes OUT (return or print)? what is its ONE job?

import tkinter as tk
from random import randint, choice, shuffle
from time import time
import engine

experiment = engine.Experiment()

window = tk.Tk()
window.title("My Stroop experiment")
window.minsize(width=600, height=400)

hearts_label = tk.Label(window, text="❤️❤️❤️❤️❤️", font=("Arial", 40))
hearts_label.pack(pady=20)

Stroop_test_label = tk.Label(window, text= 
                                        "STROOP TEST",
                                     font=("Ariel", 32)   )
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
stimulus_label.pack(expand=True)
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


accepting_keys: bool = False
pause_pressed: bool = False
started: bool = False
hearts: int = 5
after_id: str | None = None   
retry_entry: tk.Entry | None = None    
retry_button: tk.Button | None = None 



def next_trial() -> None:
    # Shows the next stimulus - or ends the experiment.
    """Job: starts the next trials cross or end the next trial if none are there"""
    global after_id
    if not experiment.has_next() or hearts == 0: 
        finish()
        if hearts == 0:
            stimulus_label.config(text= "Your hearts ran out, you made too many mistakes!")
        return
    stimulus_label.config(text="+", fg="black")
    after_id = window.after(randint(800, 1500), show_stimulus)

def color_stimulus() -> None:
    """Job: put the colored word on the screen"""
    word, color = experiment.get_current()
    stimulus_label.config(text=experiment.get_current()[0], fg=experiment.get_current()[1])

def start_timer() -> None:
    """Job: start the timer after pressing start"""
    global accepting_keys
    experiment.start_trial()
    accepting_keys = True

def show_stimulus() -> None:
    """Job: show word and start clock"""
    color_stimulus()
    start_timer() 

def update_hearts() -> None:
    # In - nothing
    # Out - nothing
    """Job: replaces the hearts to match the current heart count"""
    global hearts
    text = []
    for _ in range(hearts):
        text.append("❤️")
    hearts_label.config(text=f'{"".join(text)}')

def records_pressed_key(event: tk.Event) -> bool:
    """Job: to record the pressed key and feed to the engine"""
    return experiment.record_response(event.keysym.lower())

def displays_answer(correct: bool) -> None:
    """Job: shows if correct or not and will delete a heart if not"""
    global hearts
    if correct:
        stimulus_label_correct.config(text="Your last answer was right")
    else:
        stimulus_label_correct.config(text="Your last answer was wrong")
        hearts -= 1
        update_hearts()

def key_pressed(event: tk.Event) -> None:
    """Job: it moves on from last press while recording answers"""                         
    global accepting_keys
    if not accepting_keys:
        return                         # too early / between trials: ignore
    accepting_keys = False

    correct = records_pressed_key(event)
    displays_answer(correct)
    
    if pause_pressed is False:
        next_trial()

def accept_id() -> bool:
    """ Job: validates the inputted ID, and returns try"""
    pid = id_entry.get().strip()
    if pid == "":
        stimulus_label.config(text="Please enter a participant ID!")
        return False
    experiment.set_participant(pid)
    return True

def begining_the_test() -> None:
    """Job: destrys ID format and structions to begin the test"""
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
    """Job: begins test"""
    if accept_id():
        begining_the_test()                      

def save_data() -> None:
    """Job: save the results in a file"""
    saved = experiment.save_results(experiment.get_participant() + ".txt")
    stimulus_label.config(text="Done! Thank you." if saved else "Done! But your data could not be saved.",fg="black")
    
def clear_screen() -> None:
    """Job: removes the test screen"""
    pause_button.destroy()
    start_button.destroy()
    quit_button.destroy()
    stimulus_label_correct.destroy()

def results() -> None:
    """Job: displays the average reaction time"""
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
    """ Job: ends the test and shows results"""
    save_data()
    clear_screen()
    results()                                

def pause() -> None:
    """ Job: stops and starts the program"""
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
        experiment.reset_trial()
        pause_pressed = True
        accepting_keys = False
    else:
        pause_pressed = False
        next_trial()    # show_stimulus turns accepting_keys back on

def quit_experiment() -> None:
    """Job:  closes the test window"""
    global retry_entry, retry_button
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
    """Job: accepts a replacement ID and retrys the save"""
    if retry_entry is None:
        return
    new_id = retry_entry.get().strip()
    if new_id == "" or not all(c.isalnum() or c in "-_" for c in new_id):
        stimulus_label.config(text="Use only letters, numbers, - or _",
                              fg="black")
        return
    experiment.set_participant(new_id)
    quit_experiment()
    
start_button.config(command=start)
pause_button.config(command=pause)
quit_button.config(command=quit_experiment)

window.bind("r", key_pressed)
window.bind("g", key_pressed)   
window.bind("b", key_pressed)
window.bind("y", key_pressed)

window.mainloop()

#TODO We need to add comments in throughout the whole file after we finish it