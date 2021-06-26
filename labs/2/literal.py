class Literal():

    def __init__(self, atom: str, negation: bool = False) -> None:
        self._negation = negation
        self._atom = atom

    def evaluate(self, atom: str, value: bool) -> bool:
        """
        If literal is not applicable, returns None
        else evaluates the value against the literal and returns the result
        """
        if atom != self._atom:
            return None
        if self._negation:
            return not value
        return value

    @property
    def atom(self) -> str:
        return self._atom

    @property
    def negation(self) -> bool:
        return self._negation

    def __str__(self) -> str:
        if self._negation:
            return '!{}'.format(self._atom)
        return self._atom

