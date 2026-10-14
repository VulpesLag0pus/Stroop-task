from random import randint, choice, shuffle
from time import time


class Experiment:

    def __init__(self, nr_trials: int = 10) -> None:
        # In - nr_trials, the trials it needs to run
        #  nothing 
        # Born valid: every attribute exists with a safe default.
        self.__nr_trials = nr_trials
        self.__participant = "anon"
        self.__trials = []    
        self.__COLORS = ["red", "green", "blue", "yellow"]
        self.randomize_color_ink(nr_trials=nr_trials)
        self.__results = []       # one entry per answered trial
        self.__current = 0
        self.__start_time = 0
        self.__total_congruent = 0
        self.__total_incongruent = 0
        self.__amount_congruent = 0
        self.__amount_incongruent = 0

    def randomize_color_ink(self, nr_trials: int) -> None:
            while len(self.__trials) < (self.__nr_trials/2):
                word = choice(self.__COLORS)
                ink = choice(self.__COLORS)
                if word != ink:
                    self.__trials.append([word, ink]) 

            for _ in range(int(nr_trials/2)):
                word = choice(self.__COLORS)
                ink = word
                self.__trials.append((word, ink)) 

            shuffle(self.__trials)


    def reset_trial(self) -> None:
        if self.get_current()[0] == self.get_current()[1]:
           word = choice(self.__COLORS)
           self.__trials[self.__current][0] = word
           self.__trials[self.__current][1] = word
        else:
            self.__trials[self.__current][0] = choice(self.__COLORS)
            self.__trials[self.__current][1] = choice(self.__COLORS)
            while self.__trials[self.__current][0] == self.__trials[self.__current][1]:
                self.__trials[self.__current][0] = choice(self.__COLORS)
                self.__trials[self.__current][1] = choice(self.__COLORS)          

    def set_participant(self, name: str) -> None:
        # in: str / out: nothing - a SETTER with a guard
        if name != "":
            self.__participant = name

    def get_participant(self) -> str:
        # in: nothing / out: str, returned
        return self.__participant

    def has_next(self) -> bool:
        # in: nothing / out: bool - are there trials left?
        return self.__current <= len(self.__trials) - 1

    def start_trial(self) -> None:
        # in: nothing / out: nothing - the stimulus is on screen NOW.
        self.__start_time = time()

    def record_response(self, key: str) -> bool:
        '''Saves data, determines if correct and tracks amount and total of incongruent and congruent'''
        if not self.has_next():
            return False  
        rt = time() - self.__start_time

        # Judges key against first letter of ink color
        correct = (key == self.get_current()[1][0])

        # Appends all info into .txt file
        self.__results.append(self.__participant + "/"
                              + str(self.__current + 1) + "/" + self.get_current()[0] + "/" + self.get_current()[1] + "/" 
                              + f'{"Congruent" if self.current_is_congruent() else "Incongruent"}' + "/" + key + "/"
                              + str(correct) + "/" + str(round(rt, 3))) 
        
        if self.current_is_congruent():
            self.__total_congruent = self.__total_congruent + rt
            self.__amount_congruent = self.__amount_congruent + 1
        else:
            self.__total_incongruent = self.__total_incongruent + rt
            self.__amount_incongruent = self.__amount_incongruent + 1

        self.__current = self.__current + 1
        return correct

    def save_results(self, filename: str) -> bool:
        try:
            with open(filename, "a") as f:
                for line in self.__results:
                    f.write(line + "\n")
            return True
        except OSError:
            return False

    def get_current(self) -> tuple[str, str]:
        '''Outputs a tuple with (word, ink)'''
        if not self.has_next():
            return ("", "")
        return (self.__trials[self.__current][0], self.__trials[self.__current][1])

    def get_means(self) -> dict[str, float]:
        congruent_mean = self.__total_congruent / self.__amount_congruent if self.__amount_congruent != 0 else 0
        incongruent_mean = self.__total_incongruent / self.__amount_incongruent if self.__amount_incongruent != 0 else 0
        return {'Congruent RT':congruent_mean, 'Incongruent RT':incongruent_mean,}

    def current_is_congruent(self) -> bool:
        '''Returns if current stimuli is congruent'''
        if self.get_current()[0] == self.get_current()[1]:
            return True
        else:
            return False