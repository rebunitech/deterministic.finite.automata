"""
*  DFA Implementation and Solution to a given problem
*
* 	Section: 4
* 	Group: 1
*
*			Name						ID
*	 --------------------------------------------
* 	 1. Wendirad Demelash 			UGR/17757/11
* 	 2. Getabalew Temesgen			UGR/17153/11
* 	 3. Ashenafi Zenebe 			UGR/16813/11
* 	 4. Ashebir Wondmeneh			UGR/16809/11
* 	 5. Yemisrach Mengstu			UGR/17801/11
*
*   Submited to: Ms. Fetlework kedir
*   Submission date: 12/12/12
*
"""


class DFAError(Exception):
    """Custom exception for DFA."""


class DFA:
    """
    A Class that perform DFA process, and determin the state for a given input.
    """

    TUPLES = [
        "states",
        "symbols",
        "final_states",
    ]  # Tuples of DFA that needs to be in set

    def __init__(self, states, symbols, **kwargs):
        """
        DFA is defined over a five tuple (Q, S, T, I, S) that described as
        Q: A finite set of states
        S: A finte set of symbol
        T: Transiton function
        I: Intial state
        F: A set of final state
        """
        self.states = states
        self.symbols = symbols
        self.transition_function = kwargs["transition_function"]
        self.intial_state = kwargs["intial_state"]
        self.final_states = kwargs["final_states"]
        self.transition_table = None
        self.setup()
        self.verfiy_dfa()

    def _setup_intial_state(self):
        """
        A function that verify intial state of the a give DFA is valid.
        Verfiy only one intial state in a given DFA, (not set or list).
        An intial state of a given DFA must be in the given finite set of states.
        """

        if not isinstance(self.intial_state, (int, str)):
            raise DFAError(
                f"Intial state must be integer or symbol, {type(self.intial_state)} given."
            )
        if self.intial_state not in self.states:
            raise DFAError(
                f"A given intial state {self.intial_state} is not a part of DFA states"
            )

    def _setup_final_state(self):
        """
        A function that verify final state of the a give DFA is valid.
        A final state of a given DFA must be in the given finite set of states.
        """
        for state in self.final_states:
            if state not in self.states:
                raise DFAError(
                    f"A given final state {state} is not a part of DFA states"
                )

    def _setup_transition_function(self):
        """
        A function that checks a given transition function is valid function
        that maps input and output or a valid mapping object that shows valid relation ship
        """
        if isinstance(self.transition_function, dict):
            self.transition_table = self.transition_function
            self.transition_function = (
                lambda current_state, input_symbol: self.transition_table[
                    current_state
                ].get(input_symbol, None)
            )
        elif not callable(self.transition_function):
            raise DFAError(
                f"Transition function must be callable, {type(self.transition_function)} given"
            )

    def setup(self):
        """A function that setup DFA."""
        for attr in self.TUPLES:
            item = getattr(self, attr)
            if not isinstance(item, set):
                if not isinstance(item, (list, tuple)):
                    item = [item]
                setattr(self, attr, set(item))
        self._setup_transition_function()
        self._setup_intial_state()
        self._setup_final_state()

    def verfiy_dfa(self):
        """Verify a given DFA is a deterministic."""
        for state in self.states:
            for symbol in self.symbols:
                if self.transition_function(state, symbol) is None:
                    raise DFAError(
                        "DFA transition function must map every states for every symbols. "
                        f"Map for state {state} accepting input {symbol} is not found."
                    )

    def is_accepted(self, state):
        """A function that check a give state is in the final state (accepted state)"""
        return state in self.final_states

    def _run_dfa(self, input_symbol, current_state):
        """A recursion function that checkes a given input is accepted or not."""
        if len(input_symbol) == 0:
            return self.is_accepted(current_state)

        current_input = input_symbol[0]
        next_state = self.transition_function(current_state, current_input)
        return self._run_dfa(input_symbol[1:], next_state)

    def check_state(self, input_symbol):
        """A function that prepare a given input symbol to process DFA"""
        for inp in input_symbol:
            if inp not in self.symbols:
                raise DFAError("Input symbol must be in DFA states.")
        return self._run_dfa(input_symbol, self.intial_state)


if __name__ == "__main__":
    # L(M) = {x | x is in {0, 1}* which when interpreted as binary it is divisible by 3}

    STATES = (0, 1, 2)
    SYMBOLS = ("0", "1")
    TRANSITIONS = {0: {"0": 0, "1": 1}, 1: {"0": 2, "1": 0}, 2: {"0": 1, "1": 2}}
    
    dfa = DFA(
        STATES,
        SYMBOLS,
        transition_function=TRANSITIONS,
        intial_state=0,
        final_states=0,
    )
    fails = 0
    for number in range(10000): # Test using the first 10000 natural number
        number_binary = bin(number).lstrip('0b')
        checker = (number % 3 == 0)
        if dfa.check_state(number_binary) != checker:
            fails += 1
    print(f'> {fails} Fails')
