from tkinter import *
import tkintermapview
from PADG_NB_lib.controller import Controller

def start_gui():
    root = Tk()
    root.title("Mapbook")
    root.geometry("1025x760")

    ramka_lista_obiektow = Frame(root)
    ramka_formularz = Frame(root)
    ramka_mapa = Frame(root)

    ramka_lista_obiektow.grid(row=0, column=0)
    ramka_formularz.grid(row=0, column=1)
    ramka_mapa.grid(row=1, column=0, columnspan=2)

    map_widget = tkintermapview.TkinterMapView(
        ramka_mapa, width=1025, height=600, corner_radius=0
    )
    map_widget.set_position(52.0, 21.0)
    map_widget.set_zoom(6)
    map_widget.grid(row=0, column=0)

    class View:
        pass

    view = View()

    Label(ramka_lista_obiektow, text="Lista przychodni").grid(row=0, column=0, columnspan=2)
    view.list_box_clinics = Listbox(ramka_lista_obiektow, width=40)
    view.list_box_clinics.grid(row=1, column=0, columnspan=2)

    Label(ramka_formularz, text="Nazwa przychodni:").grid(row=0, column=0, sticky=W)
    view.entry_clinic_name = Entry(ramka_formularz)
    view.entry_clinic_name.grid(row=0, column=1)

    Label(ramka_formularz, text="Miasto:").grid(row=1, column=0, sticky=W)
    view.entry_clinic_city = Entry(ramka_formularz)
    view.entry_clinic_city.grid(row=1, column=1)

    controller = Controller(view, map_widget)

    view.button_add_clinic = Button(ramka_formularz, text="Dodaj przychodnię", command=controller.add_clinic)
    view.button_add_clinic.grid(row=2, column=0, columnspan=2, pady=5)

    view.button_edit_clinic = Button(ramka_formularz, text="Edytuj przychodnię", command=controller.edit_clinic)
    view.button_edit_clinic.grid(row=3, column=0, columnspan=2, pady=5)

    view.button_delete_clinic = Button(ramka_formularz, text="Usuń przychodnię", command=controller.delete_clinic)
    view.button_delete_clinic.grid(row=4, column=0, columnspan=2, pady=5)

    root.mainloop()
