from random import randint, choice, shuffle
from time import time


class Experiment:

    def __init__(self, nr_trials: int = 5) -> None:
        """
        Input: how many trials it should run, default 10 trials 
        Output: nothing 
        Job: sets the trials up with default values
        """
        self.__nr_trials = nr_trials
        self.__participant = "anon"
        self.__trials = []    
        self.__COLORS = ["red", "green", "blue", "yellow"] # the first letter of the words such as r,g,b,y are the response keys
        self.randomize_color_ink(nr_trials=nr_trials)
        self.__results = []       # one entry per answered trial
        self.__current = 0
        self.__start_time = 0
        self.__total_congruent = 0
        self.__total_incongruent = 0
        self.__amount_congruent = 0
        self.__amount_incongruent = 0

    def randomize_color_ink(self, nr_trials: int) -> None:
            """
            Input: how many trials it should create
            Output: nothing
            Job: builds half incongruent trials and the other half congruent trials, then randomizes them
            """
            while len(self.__trials) < (self.__nr_trials/2):
                # continues to create random pairs until half of the trials are created
                word = choice(self.__COLORS)
                ink = choice(self.__COLORS)
                if word != ink:
                    self.__trials.append([word, ink]) 

            for _ in range(int(nr_trials/2)):
                word = choice(self.__COLORS)
                ink = word  # for congruent trials 
                self.__trials.append([word, ink]) 

            shuffle(self.__trials) # mixes congruent and incongruent trials, thus can not be predicted

    def reset_trial(self) -> None:
        """
        Input: nothing 
        Output: nothing 
        Job: it gives the current trial a new word and color of the same type
        """
        if self.get_current()[0] == self.get_current()[1]:
           # congruent, picks the same new color for the word and for the ink 
           word = choice(self.__COLORS)
           self.__trials[self.__current][0] = word
           self.__trials[self.__current][1] = word
        else:
            # incongruent trials, it keeps redrawing until the word and ink color are different
            self.__trials[self.__current][0] = choice(self.__COLORS)
            self.__trials[self.__current][1] = choice(self.__COLORS)
            while self.__trials[self.__current][0] == self.__trials[self.__current][1]:
                self.__trials[self.__current][0] = choice(self.__COLORS)
                self.__trials[self.__current][1] = choice(self.__COLORS)          

    def set_participant(self, name: str) -> None:
        """
        Input: the users ID number
        Output: nothing 
        Job: saves the ID and ignores the empty box
        """
        if name != "":
            self.__participant = name

    def get_participant(self) -> str:
        """
        Input: nothing 
        Output: the users ID
        Job: lets the file read the inputted ID
        """
        return self.__participant

    def has_next(self) -> bool:
        """
        Input: nothing
        Output: if there are trials next it will be true
        Job: checks whether the experiment can run the next trial, if there are some left
        """
        return self.__current <= len(self.__trials) - 1 #the last valid trial is len -1

    def start_trial(self) -> None:
        """
        Input: nothing
        Output: nothing
        Job: records the time the stimulus is on the screen
        """
        self.__start_time = time()

    def record_response(self, key: str) -> bool:
        """
        Input: the key pressed by the user
        Output: is true if the key pressed matches the ink color of the word
        Job: save the users responses and reaction time, then moves to the next trial
        """
        if not self.has_next():
            return False  
        rt = time() - self.__start_time

        # Judges key against first letter of ink color
        correct = (key == self.get_current()[1][0])

        # Appends all info into .txt file
        self.__results.append(self.__participant + "/"
                              + str(self.__current + 1) + "/" + key + "/"
                              + str(self.__current + 1) + "/" + self.get_current()[0] + "/" + self.get_current()[1] + "/" 
                              + f'{"Congruent" if self.current_is_congruent() else "Incongruent"}' + "/" + key + "/"
                              + str(correct) + "/" + str(round(rt, 3)))

        if self.get_current()[0] == self.get_current()[1] :
            # add the reaction time to the congruent running total 
            self.__total_congruent = self.__total_congruent + rt
            self.__amount_congruent = self.__amount_congruent + 1
        else:
            #add the reaction time to the incongruent running total
            self.__total_incongruent = self.__total_incongruent + rt
            self.__amount_incongruent = self.__amount_incongruent + 1

        self.__current = self.__current + 1 # moves on to the next trial 
        return correct

    def save_results(self, filename: str) -> bool:
        """
        Input: the file 
        Output: is true if saved and false if the file can not be written 
        Job: writes down the response to record them in the text file
        """
        try:
            with open(filename, "a") as f:  # A is append, so it repeats the run with the same ID to the file 
                for line in self.__results:
                    f.write(line + "\n")
            return True
        except OSError:
            return False

    def get_current(self) -> tuple[str, str]:
        """
        Input: nothing 
        Output: a word of a color and colored in a ink or "," if no trials are left
        Job: presents the stimulus for the present trial
        """
        if not self.has_next():
            return ("", "")
        return (self.__trials[self.__current][0], self.__trials[self.__current][1])

    def get_means(self) -> dict[str, float]:
        """
        Input: nothing
        Output: the dictionary with the users average reactions time for the congruent trials and for the incongruent trials
        Job: calculates the average reaction time of each trial type
        """
        # if no trials are answered then instead of dividing by 0 use 0
        congruent_mean = self.__total_congruent / self.__amount_congruent if self.__amount_congruent != 0 else 0
        incongruent_mean = self.__total_incongruent / self.__amount_incongruent if self.__amount_incongruent != 0 else 0
        return {'Congruent RT':congruent_mean, 'Incongruent RT':incongruent_mean,}

    def current_is_congruent(self) -> bool:
        '''Returns if current stimuli is congruent'''
        if self.get_current()[0] == self.get_current()[1]:
            return True
        else:
            return False