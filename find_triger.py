import numpy as np


class StateTransitionAnalyzer:
    def __init__(self, arr, off_to_on_min_duration=0, on_to_off_min_duration=0):
        self.arr = np.array(arr)
        self.off_to_on_min_duration = off_to_on_min_duration
        self.on_to_off_min_duration = on_to_off_min_duration

    def get_off_to_on_transitions(self):
        """
        Returns the indices where the state changed from off (0) to on (1).
        """
        return np.where(np.diff(self.arr) == 1)[0]

    def get_first_off_to_on_transition(self):
        """
        Returns the index of the first off to on transition.
        """
        transitions = self.get_off_to_on_transitions()
        if len(transitions) > 0:
            return transitions[0]
        else:
            return None

    def get_last_off_to_on_transition(self):
        """
        Returns the index of the last off to on transition.
        """
        transitions = self.get_off_to_on_transitions()
        if len(transitions) > 0:
            return transitions[-1]
        else:
            return None

    def get_off_to_on_transitions_after_min_duration(self):
        """
        Returns the indices where the state changed from off (0) to on (1) after the specified minimum duration in off state.
        """
        if self.off_to_on_min_duration > 0:
            transitions = self.get_off_to_on_transitions()
            durations = np.diff(np.concatenate(([0], transitions)))
            return transitions[durations[:-1] >= self.off_to_on_min_duration]
        else:
            return self.get_off_to_on_transitions()

    def get_on_to_off_transitions(self):
        """
        Returns the indices where the state changed from on (1) to off (0).
        """
        return np.where(np.diff(self.arr) == -1)[0]

    def get_first_on_to_off_transition(self):
        """
        Returns the index of the first on to off transition.
        """
        transitions = self.get_on_to_off_transitions()
        if len(transitions) > 0:
            return transitions[0]
        else:
            return None

    def get_last_on_to_off_transition(self):
        """
        Returns the index of the last on to off transition.
        """
        transitions = self.get_on_to_off_transitions()
        if len(transitions) > 0:
            return transitions[-1]
        else:
            return None

    def get_on_to_off_transitions_after_min_duration(self):
        """
        Returns the indices where the state changed from on (1) to off (0) after the specified minimum duration in on state.
        """
        if self.on_to_off_min_duration > 0:
            transitions = self.get_on_to_off_transitions()
            durations = np.diff(np.concatenate(([0], transitions)))
            return transitions[durations[:-1] >= self.on_to_off_min_duration]
        else:
            return self.get_on_to_off_transitions()


import numpy as np
import pandas as pd
from scipy.signal import find_peaks


class TransitionAnalyzer:
    def __init__(self, arr: [pd.Series | np.ndarray | list]) -> None:
        self.arr = np.array(arr)

    def offon_arr(self) -> np.ndarray:
        """Return the indices where the state changed from off (0) to on (1)."""
        peaks, _ = find_peaks(self.arr)
        return peaks

    def offon_header(self) -> float:
        """Return the index of the first off to on transition."""
        transitions = self.offon_arr()
        if len(transitions) > 0:
            return transitions[0]
        return None

    def offon_end(self) -> float:
        """Return the index of the last off to on transition."""
        transitions = self.offon_arr()
        if len(transitions) > 0:
            return transitions[-1]
        return None

    def offon_off_duration(self, off_duration: int = 0) -> np.ndarray:
        """Return the indices where the state changed from off (0) to on (1) after the specified minimum duration in off state."""
        if self.off_to_on_min_duration > 0:
            transitions = self.offon_arr()
            durations = np.diff(np.concatenate(([0], transitions)))
            return transitions[durations[:-1] >= off_duration]
        return self.offon_arr()

    def onoff_arr(self) -> np.ndarray:
        """Return the indices where the state changed from on (1) to off (0)."""
        valleys, _ = find_peaks(-self.arr, negated=True)
        return valleys

    def onoff_header(self):
        """Return the index of the first on to off transition."""
        transitions = self.onoff_arr()
        if len(transitions) > 0:
            return transitions[0]
        return None

    def get_last_on_to_off_transition(self):
        """Return the index of the last on to off transition."""
        transitions = self.onoff_arr()
        if len(transitions) > 0:
            return transitions[-1]
        return None

    def get_on_to_off_transitions_after_min_duration(self):
        """Return the indices where the state changed from on (1) to off (0) after the specified minimum duration in on state."""
        if self.on_to_off_min_duration > 0:
            transitions = self.onoff_arr()
            durations = np.diff(np.concatenate(([0], transitions)))
            return transitions[durations[:-1] >= self.on_to_off_min_duration]
        return self.onoff_arr()


import numpy as np
import ruptures as rpt


class StateTransitionAnalyzer:
    def __init__(self, arr, off_to_on_min_duration=0, on_to_off_min_duration=0):
        self.arr = np.array(arr)
        self.off_to_on_min_duration = off_to_on_min_duration
        self.on_to_off_min_duration = on_to_off_min_duration

    def get_off_to_on_transitions(self):
        """
        Returns the indices where the state changed from off (0) to on (1).
        """
        algo = rpt.KernelCPD(kernel="linear").fit(self.arr)
        transitions = algo.predict(pen=1)
        return transitions

    def get_first_off_to_on_transition(self):
        """
        Returns the index of the first off to on transition.
        """
        transitions = self.get_off_to_on_transitions()
        if len(transitions) > 0:
            return transitions[0]
        else:
            return None

    def get_last_off_to_on_transition(self):
        """
        Returns the index of the last off to on transition.
        """
        transitions = self.get_off_to_on_transitions()
        if len(transitions) > 0:
            return transitions[-1]
        else:
            return None

    def get_off_to_on_transitions_after_min_duration(self):
        """
        Returns the indices where the state changed from off (0) to on (1) after the specified minimum duration in off state.
        """
        if self.off_to_on_min_duration > 0:
            transitions = self.get_off_to_on_transitions()
            durations = np.diff(np.concatenate(([0], transitions)))
            return transitions[durations[:-1] >= self.off_to_on_min_duration]
        else:
            return self.get_off_to_on_transitions()

    def get_on_to_off_transitions(self):
        """
        Returns the indices where the state changed from on (1) to off (0).
        """
        algo = rpt.KernelCPD(kernel="linear").fit(-self.arr)
        transitions = algo.predict(pen=1)
        return transitions

    def get_first_on_to_off_transition(self):
        """
        Returns the index of the first on to off transition.
        """
        transitions = self.get_on_to_off_transitions()
        if len(transitions) > 0:
            return transitions[0]
        else:
            return None

    def get_last_on_to_off_transition(self):
        """
        Returns the index of the last on to off transition.
        """
        transitions = self.get_on_to_off_transitions()
        if len(transitions) > 0:
            return transitions[-1]
        else:
            return None

    def get_on_to_off_transitions_after_min_duration(self):
        """
        Returns the indices where the state changed from on (1) to off (0) after the specified minimum duration in on state.
        """
        if self.on_to_off_min_duration > 0:
            transitions = self.get_on_to_off_transitions()
            durations = np.diff(np.concatenate(([0], transitions)))
            return transitions[durations[:-1] >= self.on_to_off_min_duration]
        else:
            return self.get_on_to_off_transitions()
