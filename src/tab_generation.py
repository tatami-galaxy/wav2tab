fretboard ={
    'E4': {1: 0, 2: 5, 3: 9, 4: -1, 5: -1, 6: -1},
    'F4': {1: 1, 2: 6, 3: 10, 4: -1, 5: -1, 6: -1},
    'F#4': {1: 2, 2: 7, 3: 11, 4: -1, 5: -1, 6: -1},
    'G4': {1: 3, 2: 8, 3: 12, 4: -1, 5: -1, 6: -1},
    'G#4': {1: 4, 2: 9, 3: -1, 4: -1, 5: -1, 6: -1},
    'A4': {1: 5, 2: 10, 3: -1, 4: -1, 5: -1, 6: -1},
    'A#4': {1: 6, 2: 11, 3: -1, 4: -1, 5: -1, 6: -1},
    'B4': {1: 7, 2: 12, 3: -1, 4: -1, 5: -1, 6: -1},
    'C5': {1: 8, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1},
    'C#5': {1: 9, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1},
    'D5': {1: 10, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1},
    'D#5': {1: 11, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1},
    'E5': {1: 12, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1},
    'B3': {1: -1, 2: 0, 3: 4, 4: 9, 5: -1, 6: -1},
    'C4': {1: -1, 2: 1, 3: 5, 4: 10, 5: -1, 6: -1},
    'C#4': {1: -1, 2: 2, 3: 6, 4: 11, 5: -1, 6: -1},
    'D4': {1: -1, 2: 3, 3: 7, 4: 12, 5: -1, 6: -1},
    'D#4': {1: -1, 2: 4, 3: 8, 4: -1, 5: -1, 6: -1},
    'G3': {1: -1, 2: -1, 3: 0, 4: 5, 5: 10, 6: -1},
    'G#3': {1: -1, 2: -1, 3: 1, 4: 6, 5: 11, 6: -1},
    'A3': {1: -1, 2: -1, 3: 2, 4: 7, 5: 12, 6: -1},
    'A#3': {1: -1, 2: -1, 3: 3, 4: 8, 5: -1, 6: -1},
    'D3': {1: -1, 2: -1, 3: -1, 4: 0, 5: 5, 6: 10},
    'D#3': {1: -1, 2: -1, 3: -1, 4: 1, 5: 6, 6: 11},
    'E3': {1: -1, 2: -1, 3: -1, 4: 2, 5: 7, 6: 12},
    'F3': {1: -1, 2: -1, 3: -1, 4: 3, 5: 8, 6: -1},
    'F#3': {1: -1, 2: -1, 3: -1, 4: 4, 5: 9, 6: -1},
    'A2': {1: -1, 2: -1, 3: -1, 4: -1, 5: 0, 6: 5},
    'A#2': {1: -1, 2: -1, 3: -1, 4: -1, 5: 1, 6: 6},
    'B2': {1: -1, 2: -1, 3: -1, 4: -1, 5: 2, 6: 7},
    'C3': {1: -1, 2: -1, 3: -1, 4: -1, 5: 3, 6: 8},
    'C#3': {1: -1, 2: -1, 3: -1, 4: -1, 5: 4, 6: 9},
    'E2': {1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: 0},
    'F2': {1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: 1},
    'F#2': {1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: 2},
    'G2': {1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: 3},
    'G#2': {1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: 4},
}

class GuitarCMD:

    def __init__(self) -> None:

        self.strings = []
        self.string_length = 100
        self.tab_length = 50
        self.make_strings()


    def make_strings(self):

        E1 = 'E'+'-'*self.string_length
        B = 'B'+'-'*self.string_length
        G = 'G'+'-'*self.string_length
        D = 'D'+'-'*self.string_length
        A = 'A'+'-'*self.string_length
        E2 = 'E'+'-'*self.string_length

        self.strings.append(E1)
        self.strings.append(B)
        self.strings.append(G)
        self.strings.append(D)
        self.strings.append(A)
        self.strings.append(E2)


    def generate(self, note_events):
        gap = 0
        for i in range(self.tab_length):
            note = note_events[i][2]  # (start_time_s, end_time_s, pitch_midi, amplitude, bends)
            if note not in fretboard: continue
            for string, fret in fretboard[note].items():
                if fret != -1:
                    new_string = list(self.strings[string-1])
                    new_string[i+2+gap] = str(fret)
                    self.strings[string-1] = ''.join(new_string)
                    break
            gap += 1

        # print tab to cmd
        for string in self.strings:
            print(string)