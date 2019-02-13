import sys, os, re
from enum import Enum
import query_processor
import Preprocessor

class Type(Enum):
    KEYWORD = 1
    AND = 2
    OR = 3
    NOT = 4
    SEMICOLON = 5

class Parser:

    def __init__(self, tokens, path):
        self.tokens = tokens
        self.tokenPtr = 0
        self.processor = query_processor.Processor(path)

    def error(self):
        print("Error at token: "+self.tokens[self.tokenPtr]["token"])
        os._exit(0)

    def eat(self, keyType):
        if keyType == self.tokens[self.tokenPtr]["type"]:
            token = self.tokens[self.tokenPtr]["token"]
            self.tokenPtr += 1
            return token
        else:
            self.error()
    
    def parseBasicExpression(self):
        # print("ParseBasicExpression: "+self.tokens[self.tokenPtr]["token"])
        if self.tokenPtr < len(self.tokens):
            if self.tokens[self.tokenPtr]["type"] == Type.NOT:
                self.eat(Type.NOT)
                keyword = self.eat(Type.KEYWORD)
                # print("Not: "+str(self.processor.notKeyword(keyword)))
                return self.processor.notKeyword(keyword)
        
        keyword = self.eat(Type.KEYWORD)
        # print("Keyword: "+str(self.processor.getPostingList(keyword)))
        return self.processor.getPostingList(keyword)
        

    def parseFactor(self):
        # print("ParseFactor: "+self.tokens[self.tokenPtr]["token"])
        list1 = self.parseBasicExpression()
        if self.tokenPtr < len(self.tokens):
            if self.tokens[self.tokenPtr]["type"] == Type.AND:
                self.eat(Type.AND)
                list2 = self.parseBasicExpression()
                # print("List1: "+str(list1))
                # print("List2: "+str(list2))
                output = self.processor.andMerge(list1, list2)

                if self.tokens[self.tokenPtr]["type"] == Type.AND:
                    self.eat(Type.AND)
                    list3 = self.parseTerm()
                    output = self.processor.andMerge(list3, output)
                # print("And: "+str(output))
                return output
        return list1
    
    def parseTerm(self):
        # print("ParseTerm: "+self.tokens[self.tokenPtr]["token"])
        list1 = self.parseFactor()
        if self.tokenPtr < len(self.tokens):
            if self.tokens[self.tokenPtr]["type"] == Type.OR:
                self.eat(Type.OR)
                list2 = self.parseFactor()
                output = self.processor.orMerge(list1, list2)

                if self.tokens[self.tokenPtr]["type"] == Type.OR:
                    self.eat(Type.OR)
                    list3 = self.parseTerm()
                    output = self.processor.andMerge(list3, output)
                # print("Or: "+str(output))
                return output
            self.eat(Type.SEMICOLON)
        return list1
    


def lexer(query):
    keywords = ["and", "or", "not", ";"]
    query = query.lower()
    query = re.sub("[^A-Za-z0-9_]", " ", query)
    query = re.sub(" +", " ", query)
    query += " ;"
    tokens = query.split(" ")
    tokensList = []
    i = 0
    while i < len(tokens):
        if tokens[i] == "and":
            tokensList.append({"token": tokens[i], "type": Type.AND})
        elif tokens[i] == "not":
            tokensList.append({"token": tokens[i], "type": Type.NOT})
        elif tokens[i] == "or":
            tokensList.append({"token": tokens[i], "type": Type.OR})
        elif tokens[i] == ";":
            tokensList.append({"token": tokens[i], "type": Type.SEMICOLON})
        else:
            phrase = ""
            while tokens[i] not in keywords:
                phrase = phrase + " " + tokens[i]
                i = i + 1
            i -= 1
            tokensList.append({"token": phrase.strip(), "type": Type.KEYWORD})
        i += 1
    
    return tokensList

while True:
    query = input()
    query = Preprocessor.Preprocessor().lemmetize(query)
    if "exit" in query:
        break
    print(lexer(query))
    queryParser = Parser(lexer(query), './biword-index.json').parseTerm()
    print(queryParser)


