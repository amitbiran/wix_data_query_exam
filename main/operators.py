import operator
from abc import ABC, abstractmethod
from main.item import Item

class Operator(ABC):
    @abstractmethod
    def run(self, record: Item):
        pass

class Compare(Operator):
    ops = {'>': operator.gt,
           '<': operator.lt,
           '=': operator.eq}

    def __init__(self, op, property, value):
        self.op = self.ops[op]
        self.property = property
        self.value = value

    def run(self, record: Item):
        return self.op(getattr(record,self.property), self.value)

class Logic(Operator):
    ops = {'and': operator.and_,
           'or': operator.or_}

    def __init__(self, op, a: Operator, b: Operator):
        self.op = self.ops[op]
        self.a = a
        self.b = b

    def run(self, record: Item):
        return self.op(self.a.run(record), self.b.run(record))

class Not(Operator):
    def __init__(self, a: Operator):
        self.a = a

    def run(self, record: Item):
        return not self.a.run(record)


