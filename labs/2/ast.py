import enum
class ASTException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class AST:
    def copy(self)-> 'AST':
        raise NotImplemented
    
    def remove_iffs(self) -> None:
        return None
    
    def remove_ifs(self) -> None:
        return None
    
    def push_not(self) -> 'AST':
        return self
    
    def clean_double_not(self) -> 'AST':
        return self
    
    def distribute(self) -> None:
        return None

class BinaryTypes(enum):
    IFF = '<=>'
    IF = '=>'
    OR = '|'
    AND = '&'

class BinaryOperator(AST):
    def __init__(self, operator: BinaryTypes, left: AST, right: AST) -> None:
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
            self._left = BinaryOperator(BinaryTypes.IF, left=new_left_left, right=new_left_right)
            self._right= BinaryOperator(BinaryTypes.IF, left=new_right_left, right=new_right_right)
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
    
    def push_not(self) -> 'AST':
        self._left = self._left.push_not()
        self._right = self._right.push_not()
        return self
    
    def clean_double_not(self) -> 'AST':
        self._left = self._left.clean_double_not()
        self._right = self._right.clean_double_not()
        return self
    
    def distribute(self) -> None:
        # TODO: While loop
        # Call distribute on children
        # If this node fulfills conditions for loop
        # That is its a OR operator
        # With one children that is an and
        # Keep going

        pass
    
    @property
    def left(self) -> AST:
        return self._left
    
    @property
    def right(self) -> AST:
        return self._right
    
    @property
    def operator(self) -> BinaryTypes:
        return self._operator

class NegateOperator(AST):
    def __init__(self, child: AST) -> None:
        super().__init__()
        self._child = child
    
    def copy(self) -> 'NegateOperator':
        child = self._child.copy()
        return NegateOperator(child)
    
    def remove_iffs(self) -> None:
        return self._child.remove_iffs()
    
    def remove_ifs(self) -> None:
        return self._child.remove_ifs()
    
    def push_not(self) -> 'AST':
        if isinstance(self._child, Atom):
            return self
        if isinstance(self._child, BinaryOperator):
            curr_operator = self._child.operator
            new_left = NegateOperator(self._child.left)
            new_right = NegateOperator(self._child.right)
            if curr_operator == BinaryTypes.AND:
                return BinaryOperator(BinaryTypes.OR, left=new_left, right=new_right).push_not()
            elif curr_operator == BinaryTypes.OR:
                return BinaryOperator(BinaryTypes.AND, left=new_left, right=new_right).push_not()
            else:
                raise ASTException('Should not have non-AND/OR at this stage')
        raise ASTException('Child element is neither atom nor BinaryOperator')
    
    def clean_double_not(self) -> 'AST':
        if isinstance(self._child, NegateOperator):
            return self._child.child.clean_double_not()
        self._child = self._child.clean_double_not()
        return self
    
    def distribute(self) -> None:
        # By this point, all of the children should be atoms 
        if not isinstance(self._child, Atom):
            raise ASTException('Should not have non-Atom at this stage')
        return None
    
    @property
    def child(self) -> AST:
        return self._child

class Atom(AST):
    def __init__(self, atom: str) -> None:
        super().__init__()
        self._atom = atom
    
    def copy(self) -> 'Atom':
        return Atom(self._atom)
