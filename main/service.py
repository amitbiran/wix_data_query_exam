from main.item import Item
from main.operators import *
from parse import parse

class Service():
    storage = {}

    def init(self):
        self.storage = {}

    def _parse_equal(self,query):
        property,value = parse("EQUAL({},{})", query)
        if property in ["id", "title", "content"]:
            value = value[1:len(value)-1]
        else:
            value = int(value)
        return Compare("=", property, value)

    def _parse(self,query: str):
        if query.startswith("EQUAL"):
            return self._parse_equal(query)
        elif query.startswith("GREATER_THAN"):
            property,value = parse("GREATER_THAN({},{})", query)
            return Compare(">", property, int(value))
        elif query.startswith("LESS_THAN"):
            property,value = parse("LESS_THAN({},{})", query)
            return Compare("<", property, int(value))
        elif query.startswith("AND"):
            a,b = parse("AND({},{})", query)
            return Logic("and", self._parse(a), self._parse(b))
        elif query.startswith("OR"):
            a,b = parse("OR({},{})", query)
            return Logic("or", self._parse(a), self._parse(b))
        elif query.startswith("NOT"):
            a, = parse("NOT({})", query)
            return Not( self._parse(a))
        else:
            raise Exception("Parse action not found")

    def query(self, query: str = None) -> [Item]:
        '''
        Your code should be here !
        Query function gets a query string and returns a list of items matching the query.
        '''
        if query is None:
            return self.storage.items()
        operator = self._parse(query)
        ans = []
        for id, item in self.storage.items():
            if operator.run(item):
                ans.append(item)
        return ans

    def save(self, item: Item) -> None:
        '''
        Your code should be here !
        Save item object to your data store.
        '''
        self.storage[item.id] = item

class ParseError(Exception):
    "Parse action not found"
    pass
