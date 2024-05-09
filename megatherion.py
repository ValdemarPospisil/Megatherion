from abc import abstractmethod, ABC
from json import load
from numbers import Real
from pathlib import Path
from typing import Dict, Iterable, Iterator, Tuple, Union, Any, List, Callable
from enum import Enum
from collections.abc import MutableSequence


class Type(Enum):
    Float = 0
    String = 1


def to_float(obj) -> float:
    """
    cast object to float with support of None objects (None is cast to None)
    """
    return float(obj) if obj is not None else None


def to_str(obj) -> str:
    """
    cast object to float with support of None objects (None is cast to None)
    """
    return str(obj) if obj is not None else None


def common(iterator): # from ChatGPT
    try:
        # Nejprve zkusíme získat první prvek iterátoru
        iterator = iter(iterator)
        first_value = next(iterator)
    except StopIteration:
        # Vyvolá výjimku, pokud je iterátor prázdný
        raise ValueError("Iterator is empty")

    # Kontrola, zda jsou všechny další prvky stejné jako první prvek
    for value in iterator:
        if value != first_value:
            raise ValueError("Not all values are the same")

    # Vrací hodnotu, pokud všechny prvky jsou stejné
    return first_value


class Column(MutableSequence):  # implement MutableSequence (some method are mixed from abc)
    def __init__(self, data: Iterable, dtype: Type):
        self.dtype = dtype
        self._cast = to_float if self.dtype == Type.Float else to_str # cast function
        self._data = [self._cast(value) for value in data]

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, item: Union[int, slice]) -> Union[float, str]:
        return self._data[item]

    def __setitem__(self, key: Union[int, slice], value: Any) -> None:
        self._data[key] = self._cast(value)

    def append(self, item: Any) -> None:
        self._data.append(self._cast(item))

    def insert(self, index: int, value: Any) -> None:
        self._data.insert(index, self._cast(value))

    def __delitem__(self, index: Union[int, slice]) -> None:
        del self._data[index]

    def permute(self, indices: List[int]):
        assert len(indices) == len(self)
        # vytvořit nový sloupec
        # projít přes všechny zadané indexy
        # pro každý index vyberte odpovídající hodnotu sloupce self._data
        # hodnotu přidejte do nově vytvořeného sloupce
        new_column = Column([],self.dtype)
        for i in indices:
            new_column.append(self._data[i])
        return new_column

    def copy(self) -> 'Column':
        # FIXME: value is casted to the same type (minor optimisation problem)
        return Column(self._data, self.dtype)

    def get_formatted_item(self, index:int, *, width: int):
        assert width > 0
        if self._data[index] is None:
            return "n/a".rjust(width)
        return format(self._data[index],
                      f"{width}s" if self.dtype == Type.String else f"-{width}.2g")


class DataFrame:
    def __init__(self, columns: Dict[str, Column]):
        """
        :param columns: columns of dataframe (key: name of dataframe),
                        lengths of all columns has to be the same
        """
        assert len(columns) > 0, "Dataframe without columns is not supported"
        self._size = common(len(column) for column in columns.values())
        # deep copy od dict `columns`
        self._columns = {name: column.copy() for name, column in columns.items()}

    def __getitem__(self, index: int) -> Tuple[Union[str,float]]:
        pass

    def __iter__(self) -> Iterator[Tuple[Union[str, float]]]:
        """
        :return: iterator over lines of dataframe
        """
        for i in range(len(self)):
            yield tuple(c[i] for c in self._columns.values())

    def __len__(self) -> int:
        return self._size

    @property
    def columns(self) -> Iterable[str]:
        return self._columns.keys()

    def __repr__(self) -> str:
        lines = []
        lines.append(" ".join(f"{name:12s}" for name in self.columns))
        for i in range(len(self)):
            lines.append(" ".join(self._columns[cname].get_formatted_item(i, width=12)
                                     for cname in self.columns))
        return "\n".join(lines)

    def append_column(self,col_name: str, column: Column) -> None:
        if col_name == "":
            col_name = str(len(self._columns.keys()))
        elif col_name in self._columns:
            raise ValueError("Duplicate collumn")
        
        self._columns[col_name] = column.copy()

    def mutuate(self,column: Column,col_name: str) -> 'DataFrame':
        df_copy = self.copy()
        if col_name in df_copy.columns:
            self._columns[col_name]=column
        else:
            raise KeyError("Cant copy non-existent column")
        return df_copy

    def copy(self) -> 'DataFrame':
        return DataFrame(self._columns)

    def append_row(self, row: Iterable) -> None:
        """nutno ošetřit situaci kdy přidaný řádek má jiný počet hodnot než je počet sloupců tabulky
         -možná řešení:
            -> 1) vyhodím výjimku ValueError
            -> 2) pokud je řádek kratší, doplníme hodnoty None nebo NA, pokud je řádek delší, usekeneme
            hodnoty: -> uživatele upozorníme
            -> 3) pokud je řádek kratší, hodnoty cyklicky doplňujemetak ,aby nikde nebyly chybějící záznamy
                -> upozorníme uživatele
           """
        # zvolíme strategii 1)
        # nejprve kontrola počtu záznamu
        # iterace přes každý záznam iterable a přes všechny klíče dataframu
        # por každý klíč zavoláme sloupci append a přidáme hodnotu řádků
        row = tuple(row)
        if len(row) != len(self._columns):
            raise WrongSizeException(f"Expected row of length {len(self._columns)}, but got length {len(row)}.")
        
        first_type = type(row[0])
        for value in row:
            if type(value) != first_type:
                raise TypeError("Wrong data type")


        
        for column_name, value in zip(self._columns.keys(), row):
            print(column_name,value)
            self._columns[column_name].append(value)
        self._size=+1    



    def filter(self, col_name:str, predicate: Callable[[Union[int, str]], bool]) -> 'DataFrame':
        pass

    def sort(self, col_name:str, ascending=True) -> 'DataFrame':
        # aplikujete řadící algoritmus na zvolený sloupec
        # při řazení je nutné pamatovat si indexy řádů každé z hodnot
        # výsledkem řazení je seznam indexů řádků, jak mají jít ve správném pořadí
        # vytvoříte nový dataframe (kopii), na každý sloupec zavoláte permute(serazene_indexy)
        # vratite novy dataframe
        
        indices = self.__merge_sort(self._columns[col_name])
        df_new = self.copy()

        for key in self._columns:
            df_new.mutuate(df_new._columns[key].permute(indices),key)

        return df_new
    

    @staticmethod
    def __merge_sort(data: List[float]) -> List[int]:
        if len(data) < 2:
            return list(range(len(data)))

        def merge(left, right, left_indices, right_indices):
            sorted_list = []
            sorted_indices = []
            i = j = 0

            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    sorted_list.append(left[i])
                    sorted_indices.append(left_indices[i])
                    i += 1
                else:
                    sorted_list.append(right[j])
                    sorted_indices.append(right_indices[j])
                    j += 1

            while i < len(left):
                sorted_list.append(left[i])
                sorted_indices.append(left_indices[i])
                i += 1

            while j < len(right):
                sorted_list.append(right[j])
                sorted_indices.append(right_indices[j])
                j += 1

            return sorted_list, sorted_indices

        mid = len(data) // 2
        left_part = data[:mid]
        right_part = data[mid:]

        left_sorted, left_indices_sorted = DataFrame.__merge_sort(left_part)
        right_sorted, right_indices_sorted = DataFrame.__merge_sort(right_part)

        merged_data, merged_indices = merge(left_sorted, right_sorted, left_indices_sorted, right_indices_sorted)
        return merged_data, merged_indices

   

    def describe(self) -> str:
        """
        similar to pandas but only with min, max and avg statistics for floats and count"
        :return: string with decription
        """
        pass

    def inner_join(self, other: 'DataFrame', self_key_column: str,
                   other_key_column: str) -> 'DataFrame':
        """
            Inner join between self and other dataframe with join predicate
            `self.key_column == other.key_column`.

            Possible collision of column identifiers is resolved by prefixing `_other` to
            columns from `other` data table.
        """
        pass

    @staticmethod
    def read_csv(path: Union[str, Path]) -> 'DataFrame':
        return CSVReader(path).read()

    @staticmethod
    def read_json(path: Union[str, Path]) -> 'DataFrame':
        return JSONReader(path).read()


class Reader(ABC):
    def __init__(self, path: Union[Path, str]):
        self.path = Path(path)
    @abstractmethod
    def read(self) -> 'DataFrame':
        raise NotImplemented("Abstract method")


class JSONReader(Reader):
    def read(self) -> 'DataFrame':
        with open(self.path, "rt") as f:
            json = load(f)
        columns = {}
        for cname in json.keys():
            dtype = Type.Float if all(value is None or isinstance(value, Real)
                                      for value in json[cname]) else Type.String
            columns[cname] = Column(json[cname], dtype)
        return DataFrame(columns)


class CSVReader(Reader):
    def read(self) -> 'DataFrame':
        pass
    pass

class WrongSizeException(BaseException):
    def __init__(self, message) -> None:
        super().__init__(message)








if __name__ == "__main__":
    df = DataFrame(dict(
        a=Column([None, 3.1415], Type.Float),
        b=Column(["a", 2], Type.String),
        c=Column(range(2), Type.Float)
        ))
    #print(df)

    #df = DataFrame.read_json("data.json")

#c = Column(["Ota","Pavel"],dtype=Type.String)
#df.append_column("Autor",c)

#print(df)
#for line in df:

sloupec = Column([1,2,3,4,5,6,7],float)
indexy=[3,2,1,4,5,2,3]

sloupec2= sloupec.permute(indexy)

for value in sloupec2._data:
    print(value)