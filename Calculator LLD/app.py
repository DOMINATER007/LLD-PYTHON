from abc import ABC, abstractmethod
import sys


class Operator(ABC):
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        """Give the logic of the operator"""
        pass

    @abstractmethod
    def Priority(self) -> tuple[int, int]:
        """Returns the precedence and associativity"""
        pass


class AdditionOperator(Operator):
    def execute(self, a, b): return a+b
    def Priority(self): return (1, 1)


class SubtractionOperator(Operator):
    def execute(self, a, b): return a-b
    def Priority(self): return (1, 1)


class MultiplicationOperator(Operator):
    def execute(self, a, b): return a*b
    def Priority(self): return (2, 1)


class DivisionOperator(Operator):
    def execute(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Cant divide with zero")
        return a/b

    def Priority(self): return (2, 1)


class ExponentiationOperator(Operator):
    def execute(self, a, b): return a**b
    def Priority(self): return (3, 0)


class OperationFactory:
    _operatorList = {
        '+': AdditionOperator(),
        '-': SubtractionOperator(),
        '*': MultiplicationOperator(),
        '/': DivisionOperator(),
        '^': ExponentiationOperator(),
    }

    @classmethod
    def getOperator(cls, symbol: str) -> Operator:
        op = cls._operatorList.get(symbol)
        if not op:
            raise ValueError("Not supported operator")
        return op


def isfloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class ExpressionSolver:
    def __init__(self, expr):
        self.exp = expr

    def InfixToPostfix(self):
        i = 0
        ans = []
        st = []
        while i < len(self.exp):
            ch = self.exp[i]
            if ch == '(':
                st.append(ch)
                i += 1
            elif ch == '.' or ch.isdigit():
                tmp = ""
                while i < len(self.exp) and (self.exp[i] == '.' or self.exp[i].isdigit()):
                    tmp += self.exp[i]
                    i += 1
                if isfloat(tmp):
                    ans.append(tmp)
                else:
                    raise ValueError("Invalid value in the expression")
            elif ch == ')':
                while len(st) > 0 and st[-1] != '(':
                    ans.append(st.pop())

                _ = st.pop()
                i += 1

            elif ch in OperationFactory._operatorList:
                cur_op = OperationFactory.getOperator(ch)
                # print(cur_op.Priority[0])
                cur_prec, cur_asoc = cur_op.Priority()
              #  print(cur_op.Priority())
                while len(st) > 0 and st[-1] != '(':
                    top_op = OperationFactory.getOperator(st[-1])
                    top_prec, top_asoc = top_op.Priority()
                 #   print(top_op.Priority())
                    if top_prec > cur_prec or (top_prec == cur_prec and cur_asoc == 1):
                        ans.append(st.pop())
                    else:
                        break
                st.append(ch)
                i += 1
            else:
               # print(ch)
                raise ValueError("Invalid character")
          #  print(ans)
        while len(st) > 0:
            if st[-1] == ')' or st[-1] == '(':
                raise ValueError("Invalid Expression")
            ans.append(st.pop())
        return ans

    def EvaluateExp(slef, arr):
        st = []
        for x in arr:
            if isfloat(x):
                st.append(float(x))
            elif x in OperationFactory._operatorList:
                b = st.pop()
                a = st.pop()
                op = OperationFactory.getOperator(x)
                val = op.execute(a, b)
                st.append(val)
            else:
                raise ValueError("Unknown char")
        if len(st) <= 0:
            raise ValueError("Something went wrong")
        return st[-1]

    def solve(self):
        postfix = self.InfixToPostfix()
       # print(postfix)
        return self.EvaluateExp(postfix)


if __name__ == "__main__":

   # print(sys.argv)
    exp = sys.argv[1]
    res = ExpressionSolver(exp)
    print(res.solve())
