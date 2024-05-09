

class ConcreteError(Exception):
    pass


def g():
    raise ConcreteError("Concrete error")

def f():
    try:
        g()
    except ConcreteError as e:
        raise Exception("Internal error") from e

try:
    g
#except DataError as e:
 #   raise Exception("Internal error") from e
except ValueError as e:
    # obsluhy vyjímek neočekávaná nebo chybná hodnota
    pass


def main():
    try:
        pass
    except Exception as e:
        # typicky ukončení programu
        # uživatelsky rozumné ukončení
        pass

if __name__ == "__main__":
    try:
        f()
    except Exception as e:
        print(str(e))
        print("from error")
        print(e.__cause__)
        print(e.__cause__.__cause__)




# běžná vyjímky: Exception nebo podtřída
# BaseException (mimo Exception): systémové vyjímky

"""
BaseException : bázová třída všech vyjímek
    SyntaxError
    KeyboardInterrupt: Ctrl+C
    Exception - běžné vyjímky (běhové)
        TypeError
        ValueError
        KeyError
        ...

"""