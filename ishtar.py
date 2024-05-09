from time import sleep
from math import inf



def VystrojError(Exception):
    pass

class Vykoupeni(Exception):
    pass

class Buh:
    def __init__(self, jmeno:str,vystroj:list[str]) -> None:
        self.jmeno = jmeno
        self.vystroj = vystroj
    
    def __repr__(self) -> str:
        return f"{self.jmeno}: {self.vystroj}"
    
    def odevzdej(self) -> str:
        try:
            return self.vystroj.pop()
        except Exception:
            raise VystrojError("Nedostatek výstroje")


    def prijmi(self,vystroj_soucastka:str) -> None:
        self.vystroj.append(vystroj_soucastka)

class Podsveti:
    def __init__(self,osazenstvo:list[Buh]) -> None:
        self._osazenstvo = list(osazenstvo)

    def uvrzeni(self, obet:Buh, vykoupeny: Buh):
        assert obet not in self._osazenstvo
        assert vykoupeny in self._osazenstvo

        self._zatraceni(obet, False)
        self._osazenstvo.remove(vykoupeny)
        raise Vykoupeni(f"Vykoupeni uvržením boha {obet}")

    def vstup(self, buh:Buh):
        pruvodce = Buh("Anonym", [])
        self._osazenstvo.append(pruvodce)
        self._brana(buh,1,pruvodce)

    def _brana(self, buh:Buh,poradi_brany:int, pruvodce: Buh):
        try:
            pruvodce.prijmi(buh.odevzdej())
            if poradi_brany < 7:
                self._brana(buh, pruvodce,poradi_brany + 1)
            else:
                self._zatraceni(buh)
        finally:
            buh.prijmi(pruvodce.odevzdej())

    def _zatraceni(self, buh: Buh,vecne_cekani: bool = True):
        while buh.vystroj:
            buh.odevzdej()
        self._osazenstvo.append(buh)
        print(f"nový přírustek: {buh}, osazenstvo: {self._osazenstvo}")
        if vecne_cekani:
            while True:
                try:
                    sleep(1)
                    self.uvrzeni(damuzi,ishtar)
                    print("Pokus o vykoupení")
                except Vykoupeni as e:
                    raise e
                except:
                    pass


ishtar = Buh("Ištar", ["rouška_cudnosti","náramky","pás","ozdoby","náhrdelník","náušnice","koruna","deštník"])
eres = Buh("Ereškigal", [])

damuzi = Buh("Damuzi", [])

podsveti = Podsveti([eres])
try:
    podsveti.vstup(ishtar)
except Exception as e:
    print(f"výstup: ")
    print(ishtar)
