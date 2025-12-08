from tkinter import Tk, Frame, Label, Entry, Button, Listbox, N, END
from tkintermapview import TkinterMapView
from PADG_NB_lib.controller import Controller


class View:
    def __init__(self):
        self.list_box_clinics = None
        self.label_clinic_name_value = None
        self.label_clinic_city_value = None
        self.entry_clinic_name = None
        self.entry_clinic_city = None

        self.list_box_doctors = None
        self.entry_doctor_first_name = None
        self.entry_doctor_last_name = None
        self.entry_doctor_city = None

        self.list_box_patients = None

        self.list_box_all_patients = None
        self.entry_all_patient_first_name = None
        self.entry_all_patient_last_name = None
        self.entry_all_patient_city = None
        self.list_box_doctors_for_assign = None
        self.button_assign_patient = None
        self.button_add_all_patient = None


def start_gui():
    root = Tk()
    root.title("System Zarządzania Przychodnią")
    root.geometry("1400x700")

    view = View()

    map_widget = TkinterMapView(root, width=600, height=600, corner_radius=0)
    map_widget.grid(row=0, column=4, rowspan=2, padx=10, pady=10, sticky=N)
    map_widget.set_position(52.2297, 21.0122)  # Warszawa
    map_widget.set_zoom(6)


    controller = Controller(view, map_widget)


    ramka_clinics = Frame(root)
    ramka_clinics.grid(row=0, column=0, padx=10, pady=5, sticky=N)

    Label(ramka_clinics, text="Przychodnie").grid(row=0, column=0, columnspan=2)

    view.list_box_clinics = Listbox(ramka_clinics, width=35, height=10)
    view.list_box_clinics.grid(row=1, column=0, columnspan=2)
    view.list_box_clinics.bind("<<ListboxSelect>>", controller.show_clinic_details)

    Label(ramka_clinics, text="Nazwa").grid(row=2, column=0)
    view.entry_clinic_name = Entry(ramka_clinics)
    view.entry_clinic_name.grid(row=2, column=1)

    Label(ramka_clinics, text="Miasto").grid(row=3, column=0)
    view.entry_clinic_city = Entry(ramka_clinics)
    view.entry_clinic_city.grid(row=3, column=1)

    Button(ramka_clinics, text="Dodaj przychodnię",
           command=controller.add_clinic).grid(row=4, column=0, pady=4, columnspan=2)


    Label(ramka_clinics, text="Szczegóły:").grid(row=5, column=0, columnspan=2, pady=(10, 0))
    Label(ramka_clinics, text="Nazwa:").grid(row=6, column=0, sticky="w")
    view.label_clinic_name_value = Label(ramka_clinics, text="", fg="blue")
    view.label_clinic_name_value.grid(row=6, column=1, sticky="w")

    Label(ramka_clinics, text="Miasto:").grid(row=7, column=0, sticky="w")
    view.label_clinic_city_value = Label(ramka_clinics, text="", fg="blue")
    view.label_clinic_city_value.grid(row=7, column=1, sticky="w")


    ramka_doctors = Frame(root)
    ramka_doctors.grid(row=0, column=1, padx=10, pady=5, sticky=N)

    Label(ramka_doctors, text="Lekarze").grid(row=0, column=0, columnspan=2)

    view.list_box_doctors = Listbox(ramka_doctors, width=35, height=10)
    view.list_box_doctors.grid(row=1, column=0, columnspan=2)
    view.list_box_doctors.bind("<<ListboxSelect>>", controller.show_patients)

    Label(ramka_doctors, text="Imię").grid(row=2, column=0)
    view.entry_doctor_first_name = Entry(ramka_doctors)
    view.entry_doctor_first_name.grid(row=2, column=1)

    Label(ramka_doctors, text="Nazwisko").grid(row=3, column=0)
    view.entry_doctor_last_name = Entry(ramka_doctors)
    view.entry_doctor_last_name.grid(row=3, column=1)

    Label(ramka_doctors, text="Miasto").grid(row=4, column=0)
    view.entry_doctor_city = Entry(ramka_doctors)
    view.entry_doctor_city.grid(row=4, column=1)

    Button(ramka_doctors, text="Dodaj lekarza",
           command=controller.add_doctor).grid(row=5, column=0, pady=4, columnspan=2)


    ramka_patients = Frame(root)
    ramka_patients.grid(row=0, column=2, padx=10, pady=5, sticky=N)

    Label(ramka_patients, text="Pacjenci wybranego lekarza").grid(row=0, column=0, columnspan=2)

    view.list_box_patients = Listbox(ramka_patients, width=35, height=10)
    view.list_box_patients.grid(row=1, column=0, columnspan=2)


    ramka_all_patients = Frame(root)
    ramka_all_patients.grid(row=0, column=3, padx=10, pady=5, sticky=N)

    Label(ramka_all_patients, text="Wszyscy pacjenci").grid(row=0, column=0, columnspan=2)

    view.list_box_all_patients = Listbox(ramka_all_patients, width=35, height=10)
    view.list_box_all_patients.grid(row=1, column=0, columnspan=2)

    Label(ramka_all_patients, text="Imię").grid(row=2, column=0)
    view.entry_all_patient_first_name = Entry(ramka_all_patients)
    view.entry_all_patient_first_name.grid(row=2, column=1)

    Label(ramka_all_patients, text="Nazwisko").grid(row=3, column=0)
    view.entry_all_patient_last_name = Entry(ramka_all_patients)
    view.entry_all_patient_last_name.grid(row=3, column=1)

    Label(ramka_all_patients, text="Miasto").grid(row=4, column=0)
    view.entry_all_patient_city = Entry(ramka_all_patients)
    view.entry_all_patient_city.grid(row=4, column=1)

    view.button_add_all_patient = Button(
        ramka_all_patients,
        text="Dodaj pacjenta",
        command=controller.add_patient_global
    )
    view.button_add_all_patient.grid(row=5, column=0, pady=4, columnspan=2)

    Label(ramka_all_patients, text="Przypisz do lekarza").grid(row=6, column=0, columnspan=2)

    view.list_box_doctors_for_assign = Listbox(ramka_all_patients, width=30, height=4)
    view.list_box_doctors_for_assign.grid(row=7, column=0, columnspan=2)

    view.button_assign_patient = Button(
        ramka_all_patients,
        text="Przypisz",
        command=controller.assign_patient_to_doctor
    )
    view.button_assign_patient.grid(row=8, column=0, pady=4, columnspan=2)

    root.mainloop()