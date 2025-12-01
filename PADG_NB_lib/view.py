from tkinter import *
import tkintermapview
from PADG_NB_lib.controller import Controller


def start_gui():
    root = Tk()
    root.title("Mapbook")
    root.geometry("1025x760")


    ramka_lista_obiektow = Frame(root)
    ramka_formularz = Frame(root)
    ramka_szczegoly = Frame(root)
    ramka_mapa = Frame(root)

    ramka_lista_obiektow.grid(row=0, column=0, padx=10, pady=5, sticky=N)
    ramka_formularz.grid(row=0, column=1, padx=10, pady=5, sticky=N)
    ramka_szczegoly.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
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


    Label(ramka_lista_obiektow, text="Lista przychodni").grid(row=0, column=0, columnspan=2)

    view.list_box_clinics = Listbox(ramka_lista_obiektow, width=40)
    view.list_box_clinics.grid(row=1, column=0, columnspan=2, pady=5)

    Label(ramka_formularz, text="Nazwa przychodni:").grid(row=0, column=0, sticky=W)
    view.entry_clinic_name = Entry(ramka_formularz)
    view.entry_clinic_name.grid(row=0, column=1)

    Label(ramka_formularz, text="Miasto:").grid(row=1, column=0, sticky=W)
    view.entry_clinic_city = Entry(ramka_formularz)
    view.entry_clinic_city.grid(row=1, column=1)


    Label(ramka_szczegoly, text="Szczegóły przychodni").grid(row=0, column=0, columnspan=2)

    Label(ramka_szczegoly, text="Nazwa:").grid(row=1, column=0, sticky=W)
    view.label_clinic_name_value = Label(ramka_szczegoly, text="...")
    view.label_clinic_name_value.grid(row=1, column=1, sticky=W)

    Label(ramka_szczegoly, text="Miasto:").grid(row=2, column=0, sticky=W)
    view.label_clinic_city_value = Label(ramka_szczegoly, text="...")
    view.label_clinic_city_value.grid(row=2, column=1, sticky=W)


    controller = Controller(view, map_widget)

    view.list_box_clinics.bind("<<ListboxSelect>>", controller.show_clinic_details)


    view.button_add_clinic = Button(
        ramka_formularz,
        text="Dodaj przychodnię",
        command=controller.add_clinic
    )
    view.button_add_clinic.grid(row=2, column=0, columnspan=2, pady=5)

    view.button_edit_clinic = Button(
        ramka_formularz,
        text="Edytuj przychodnię",
        command=controller.edit_clinic
    )
    view.button_edit_clinic.grid(row=3, column=0, columnspan=2, pady=5)

    view.button_delete_clinic = Button(
        ramka_formularz,
        text="Usuń przychodnię",
        command=controller.delete_clinic
    )
    view.button_delete_clinic.grid(row=4, column=0, columnspan=2, pady=5)

    ramka_lista_doctor = Frame(root)
    ramka_formularz_doctor = Frame(root)

    ramka_lista_doctor.grid(row=0, column=2, padx=10, pady=5, sticky=N)
    ramka_formularz_doctor.grid(row=1, column=2, padx=10, pady=5, sticky=N)

    Label(ramka_lista_doctor, text="Lista lekarzy").grid(row=0, column=0, columnspan=2)
    view.list_box_doctors = Listbox(ramka_lista_doctor, width=40)
    view.list_box_doctors.grid(row=1, column=0, columnspan=2, pady=5)

    Label(ramka_formularz_doctor, text="Imię:").grid(row=0, column=0, sticky=W)
    view.entry_doctor_first_name = Entry(ramka_formularz_doctor)
    view.entry_doctor_first_name.grid(row=0, column=1)

    Label(ramka_formularz_doctor, text="Nazwisko:").grid(row=1, column=0, sticky=W)
    view.entry_doctor_last_name = Entry(ramka_formularz_doctor)
    view.entry_doctor_last_name.grid(row=1, column=1)

    Label(ramka_formularz_doctor, text="Miasto:").grid(row=2, column=0, sticky=W)
    view.entry_doctor_city = Entry(ramka_formularz_doctor)
    view.entry_doctor_city.grid(row=2, column=1)

    view.button_add_doctor = Button(
        ramka_formularz_doctor,
        text="Dodaj lekarza",
        command=lambda: controller.add_doctor()
    )
    view.button_add_doctor.grid(row=3, column=0, columnspan=2, pady=5)

    view.button_edit_doctor = Button(
        ramka_formularz_doctor,
        text="Edytuj lekarza",
        command=lambda: controller.edit_doctor()
    )
    view.button_edit_doctor.grid(row=4, column=0, columnspan=2, pady=5)

    view.button_delete_doctor = Button(
        ramka_formularz_doctor,
        text="Usuń lekarza",
        command=lambda: controller.delete_doctor()
    )
    view.button_delete_doctor.grid(row=5, column=0, columnspan=2, pady=5)

    root.mainloop()