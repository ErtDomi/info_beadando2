import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from abc import ABC, abstractmethod


# Szoba absztrakt osztály és leszármazottak
class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar

    @abstractmethod
    def get_info(self):
        pass


class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar):
        super().__init__(szobaszam, ar)

    def get_info(self):
        return f"Egyágyas szoba, szám: {self.szobaszam}, ár: {self.ar} Ft"


class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar):
        super().__init__(szobaszam, ar)

    def get_info(self):
        return f"Kétagyas szoba, szám: {self.szobaszam}, ár: {self.ar} Ft"


# Szálloda osztály
class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []

    def add_szoba(self, szoba):
        self.szobak.append(szoba)

    def get_info(self):
        info = f"Szálloda: {self.nev}\n"
        for szoba in self.szobak:
            info += szoba.get_info() + "\n"
        return info


# Foglalás kezelő osztály
class Foglalas:
    def __init__(self):
        self.foglalasok = {}

    def foglal(self, szoba, datum):
        if datum < datetime.now().date():
            return "A foglalás dátuma múltbeli, ezért nem érvényes."
        if datum in self.foglalasok and szoba.szobaszam in self.foglalasok[datum]:
            return "Ez a szoba már foglalt ezen a napon."
        self.foglalasok.setdefault(datum, {})[szoba.szobaszam] = szoba
        return f"Foglalás rögzítve: {datum} - {szoba.get_info()}"

    def lemondas(self, szoba, datum):
        if datum in self.foglalasok and szoba.szobaszam in self.foglalasok[datum]:
            del self.foglalasok[datum][szoba.szobaszam]
            if not self.foglalasok[datum]:
                del self.foglalasok[datum]
            return "Foglalás lemondva."
        return "Nincs ilyen foglalás."

    def list_foglalasok(self):
        if not self.foglalasok:
            return "Nincsenek foglalások."
        lista = "Foglalások listája:\n"
        for datum, szobak in self.foglalasok.items():
            lista += f"Dátum: {datum}\n"
            for szoba in szobak.values():
                lista += szoba.get_info() + "\n"
        return lista


# GUI alkalmazás osztály
class Application(tk.Tk):
    def __init__(self, szalloda, foglalas_kezelo):
        super().__init__()
        self.szalloda = szalloda
        self.foglalas_kezelo = foglalas_kezelo
        self.title("Szálloda Foglalási Rendszer")
        self.geometry("400x300")  # Az ablak mérete
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self, text="Üdvözöljük a szálloda foglalási rendszerében!")
        self.label.pack(pady=10)

        self.szoba_label = ttk.Label(self, text="Válassza ki a szobát:")
        self.szoba_label.pack(pady=5)

        self.szoba_combobox = ttk.Combobox(self, state="readonly")
        self.szoba_combobox["values"] = [f"Szoba {szoba.szobaszam}" for szoba in self.szalloda.szobak]
        self.szoba_combobox.pack(pady=5)

        self.datum_label = ttk.Label(self, text="Adja meg a foglalás dátumát (ÉÉÉÉ-HH-NN):")
        self.datum_label.pack(pady=5)

        self.datum_entry = ttk.Entry(self)
        self.datum_entry.pack(pady=5)

        self.foglal_button = ttk.Button(self, text="Foglalás", command=self.foglal)
        self.foglal_button.pack(pady=5)

        self.lemond_button = ttk.Button(self, text="Lemondás", command=self.lemond)
        self.lemond_button.pack(pady=5)

        self.list_button = ttk.Button(self, text="Foglalások Listázása", command=self.list_foglalasok)
        self.list_button.pack(pady=5)

    def foglal(self):
        szoba_index = self.szoba_combobox.current()
        datum = self.datum_entry.get()
        try:
            datum = datetime.strptime(datum, "%Y-%m-%d").date()
            szoba = self.szalloda.szobak[szoba_index]
            eredmeny = self.foglalas_kezelo.foglal(szoba, datum)
            messagebox.showinfo("Foglalás Eredménye", eredmeny)
        except ValueError:
            messagebox.showerror("Hiba", "Érvénytelen dátum formátum.")

    def lemond(self):
        szoba_index = self.szoba_combobox.current()
        datum = self.datum_entry.get()
        try:
            datum = datetime.strptime(datum, "%Y-%m-%d").date()
            szoba = self.szalloda.szobak[szoba_index]
            eredmeny = self.foglalas_kezelo.lemondas(szoba, datum)
            messagebox.showinfo("Lemondás Eredménye", eredmeny)
        except ValueError:
            messagebox.showerror("Hiba", "Érvénytelen dátum formátum.")

    def list_foglalasok(self):
        eredmeny = self.foglalas_kezelo.list_foglalasok()
        messagebox.showinfo("Foglalások Listája", eredmeny)


# A főprogram indítása
if __name__ == "__main__":
    szalloda = Szalloda("Hotel Budapest")
    szalloda.add_szoba(EgyagyasSzoba(101, 15000))
    szalloda.add_szoba(KetagyasSzoba(102, 20000))
    szalloda.add_szoba(EgyagyasSzoba(103, 18000))

    foglalas_kezelo = Foglalas()

    # Alapértelmezett foglalások hozzáadása
    foglalas_kezelo.foglal(szalloda.szobak[0], datetime(2024, 5, 20).date())
    foglalas_kezelo.foglal(szalloda.szobak[1], datetime(2024, 5, 21).date())
    foglalas_kezelo.foglal(szalloda.szobak[2], datetime(2024, 5, 22).date())
    foglalas_kezelo.foglal(szalloda.szobak[0], datetime(2024, 5, 23).date())

    app = Application(szalloda, foglalas_kezelo)
    app.mainloop()