from enum import Enum


class PropositionalASTException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class PropositionalAST:
    def copy(self) -> 'PropositionalAST':
        raise NotImplemented

    def remove_iffs(self) -> None:
        return None

    def remove_ifs(self) -> None:
        return None

    def push_not(self) -> 'PropositionalAST':
        return self

    def clean_double_not(self) -> 'PropositionalAST':
        return self

    def distribute(self) -> None:
        return None
    
    def to_cnf(self) -> 'PropositionalAST':
        node = self.copy()
        node = self.clean_double_not()
        node.remove_iffs()
        node.remove_ifs()
        node = node.push_not()
        node.distribute()
        return node


class BinaryTypes(Enum):
    IFF = '<=>'
    IF = '=>'
    OR = '|'
    AND = '&'


class BinaryOperator(PropositionalAST):
    def __init__(self, operator: BinaryTypes, left: PropositionalAST,
                 right: PropositionalAST) -> None:
        super().__init__()
        self._operator = operator
        self._left = left
        self._right = right

    def copy(self) -> 'BinaryOperator':
        new_right = self._right.copy()
        new_left = self._left.copy()
        return BinaryOperator(self._operator, new_left, new_right)

    def remove_iffs(self) -> None:
        if self._operator == BinaryTypes.IFF:
            self._operator = BinaryTypes.AND
            new_left_right = self._left.copy()
            new_left_left = self._right.copy()
            new_right_right = self._right.copy()
            new_right_left = self._left.copy()
            self._left = BinaryOperator(
                BinaryTypes.IF,
                left=new_left_left,
                right=new_left_right)
            self._right = BinaryOperator(
                BinaryTypes.IF,
                left=new_right_left,
                right=new_right_right)
        self._left.remove_iffs()
        self._right.remove_iffs()
        return None

    def remove_ifs(self) -> None:
        if self._operator == BinaryTypes.IF:
            self._operator = BinaryTypes.OR
            # Account for double negation here
            if isinstance(self._left, NegateOperator):
                self._left = self._left.child
            else:
                self._left = NegateOperator(self._left)
        self._left.remove_ifs()
        self._right.remove_ifs()
        return None

    def push_not(self) -> 'PropositionalAST':
        self._left = self._left.push_not()
        self._right = self._right.push_not()
        return self

    def clean_double_not(self) -> 'PropositionalAST':
        self._left = self._left.clean_double_not()
        self._right = self._right.clean_double_not()
        return self

    def distribute(self) -> None:
        self._left.distribute()
        self._right.distribute()
        if self._operator == BinaryTypes.AND:
            return
        if self._operator != BinaryTypes.OR:
            raise PropositionalASTException(
                'Should not have non-AND/OR at this stage')
        and_child = None
        to_distribute_child = None
        if isinstance(
                self._left, BinaryOperator) and self._left.operator == BinaryTypes.AND:
            and_child = self._left
            to_distribute_child = self._right
        elif isinstance(self._right, BinaryOperator) and self._right.operator == BinaryTypes.AND:
            and_child = self._right
            to_distribute_child = self._left
        if and_child is not None and to_distribute_child is not None:
            self._operator = BinaryTypes.AND
            and_child_left_child = and_child.left
            and_child_right_child = and_child.right
            new_left = BinaryOperator(
                BinaryTypes.OR,
                to_distribute_child,
                and_child_left_child)
            new_right = BinaryOperator(
                BinaryTypes.OR,
                to_distribute_child,
                and_child_right_child)
            self._left = new_left
            self._right = new_right
            self._left.distribute()
            self._right.distribute()

    @property
    def left(self) -> PropositionalAST:
        return self._left

    @property
    def right(self) -> PropositionalAST:
        return self._right

    @property
    def operator(self) -> BinaryTypes:
        return self._operator


class NegateOperator(PropositionalAST):
    def __init__(self, child: PropositionalAST) -> None:
        super().__init__()
        self._child = child

    def copy(self) -> 'NegateOperator':
        child = self._child.copy()
        return NegateOperator(child)

    def remove_iffs(self) -> None:
        return self._child.remove_iffs()

    def remove_ifs(self) -> None:
        return self._child.remove_ifs()

    def push_not(self) -> 'PropositionalAST':
        if isinstance(self._child, Atom):
            return self
        if isinstance(self._child, BinaryOperator):
            curr_operator = self._child.operator
            new_left = NegateOperator(self._child.left)
            new_right = NegateOperator(self._child.right)
            if curr_operator == BinaryTypes.AND:
                return BinaryOperator(
                    BinaryTypes.OR, left=new_left, right=new_right).push_not()
            elif curr_operator == BinaryTypes.OR:
                return BinaryOperator(
                    BinaryTypes.AND, left=new_left, right=new_right).push_not()
            else:
                raise PropositionalASTException(
                    'Should not have non-AND/OR at this stage')
        if isinstance(self._child, NegateOperator):
            return self._child.child.push_not()
        raise PropositionalASTException(
            'Child element is neither atom nor BinaryOperator')

    def clean_double_not(self) -> 'PropositionalAST':
        if isinstance(self._child, NegateOperator):
            return self._child.child.clean_double_not()
        self._child = self._child.clean_double_not()
        return self

    def distribute(self) -> None:
        # By this point, all of the children should be atoms
        if not isinstance(self._child, Atom):
            raise PropositionalASTException(
                'Should not have non-Atom at this stage')
        return None

    @property
    def child(self) -> PropositionalAST:
        return self._child


class Atom(PropositionalAST):
    def __init__(self, atom: str) -> None:
        super().__init__()
        self._atom = atom

    def copy(self) -> 'Atom':
        return Atom(self._atom)
    
    @property
    def atom(self) -> str:
        return self._atom
