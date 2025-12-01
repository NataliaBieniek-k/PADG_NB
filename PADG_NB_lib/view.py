from tkinter import *
import tkintermapview
from PADG_NB_lib.controller import Controller

def start_gui():
    root = Tk()
    root.title("Mapbook")
    root.geometry("1025x760")

    ramka_lista_obiektow = Frame(root)
    ramka_formularz = Frame(root)
    ramka_szczegoly_obiektu = Frame(root)
    ramka_mapa = Frame(root)

    ramka_lista_obiektow.grid(row=0, column=0)
    ramka_formularz.grid(row=0, column=1)
    ramka_szczegoly_obiektu.grid(row=1, column=0, columnspan=2)
    ramka_mapa.grid(row=2, column=0, columnspan=2)

    map_widget = tkintermapview.TkinterMapView(
        ramka_mapa, width=1025, height=600, corner_radius=0
    )
    map_widget.set_position(52.0, 21.0)
    map_widget.set_zoom(6)
    map_widget.grid(row=0, column=0)

    class View:
        pass

    view = View()

    Label(ramka_lista_obiektow, text="Lista obiektów").grid(row=0, column=0, columnspan=3)
    view.list_box_lista_obiektow = Listbox(ramka_lista_obiektow)
    view.list_box_lista_obiektow.grid(row=1, column=0, columnspan=3)

    label_formularz = Label(ramka_formularz, text="Formularz: ")
    label_formularz.grid(row=0, column=0, columnspan=2)

    Label(ramka_formularz, text="Imie: ").grid(row=1, column=0, sticky=W)
    Label(ramka_formularz, text="Lokalizacja: ").grid(row=2, column=0, sticky=W)
    Label(ramka_formularz, text="Posty: ").grid(row=3, column=0, sticky=W)
    Label(ramka_formularz, text="Obrazek: ").grid(row=4, column=0, sticky=W)

    view.entry_name = Entry(ramka_formularz)
    view.entry_name.grid(row=1, column=1)

    view.entry_lokalizacja = Entry(ramka_formularz)
    view.entry_lokalizacja.grid(row=2, column=1)

    view.entry_posty = Entry(ramka_formularz)
    view.entry_posty.grid(row=3, column=1)

    view.entry_img_url = Entry(ramka_formularz)
    view.entry_img_url.grid(row=4, column=1)

    Label(ramka_szczegoly_obiektu, text="Szczegóły obiektu: ").grid(row=0, column=0, sticky=W)
    Label(ramka_szczegoly_obiektu, text="Imie: ").grid(row=1, column=0)
    view.label_imie_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektu, text="...")
    view.label_imie_szczegoly_obiektu_wartosc.grid(row=1, column=1)

    Label(ramka_szczegoly_obiektu, text="Lokalizacja: ").grid(row=1, column=3)
    view.label_lokalizacja_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektu, text="...")
    view.label_lokalizacja_szczegoly_obiektu_wartosc.grid(row=1, column=4)

    Label(ramka_szczegoly_obiektu, text="Posty: ").grid(row=1, column=5)
    view.label_posty_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektu, text="...")
    view.label_posty_szczegoly_obiektu_wartosc.grid(row=1, column=6)

    controller = Controller(view, map_widget)

    Button(
        ramka_lista_obiektow,
        text="Pokaż szczegóły",
        command=controller.user_details
    ).grid(row=2, column=0)

    Button(
        ramka_lista_obiektow,
        text="Usuń obiekt",
        command=controller.delete_user
    ).grid(row=2, column=1)

    Button(
        ramka_lista_obiektow,
        text="Edytuj obiekt",
        command=controller.edit_user
    ).grid(row=2, column=2)

    view.button_dodaj_obiekt = Button(
        ramka_formularz,
        text="Dodaj obiekt",
        command=controller.add_user
    )
    view.button_dodaj_obiekt.grid(row=5, column=0, columnspan=2)

    root.mainloop()
