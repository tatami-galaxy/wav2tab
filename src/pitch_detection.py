from basic_pitch.inference import predict
import librosa

# outputs overtones

class BasicPitchLib:

    def __init__(self) -> None:
        pass


    def pitch_to_note(self, note_events):
        ret_list = []
        for event in note_events:
            l = list(event)
            note = librosa.midi_to_note(event[2], unicode=False)  # event[2] is pitch
            l[2] = note
            ret_list.append(l)
        return ret_list


    def get_midi_events(self, outfile_path):

        model_output, midi_data, note_events = predict(outfile_path)
        # sort note events according to start time 
        sorted_events = sorted(note_events, key=lambda x: x[0])  # x[0] is start time
        # midi pitch to note
        # each event is now a list [start_time_s, end_time_s, pitch_midi, amplitude, bends]
        note_events = self.pitch_to_note(sorted_events)

        return note_events
