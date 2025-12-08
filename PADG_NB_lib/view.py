from tkinter import Tk, Frame, Label, Entry, Button, Listbox, N, END, Toplevel
from tkintermapview import TkinterMapView
from PADG_NB_lib.controller import Controller


class View:
    def __init__(self):
        self.list_box_clinics = None
        self.label_clinic_name_value = None
        self.label_clinic_city_value = None

        self.list_box_doctors = None

        self.list_box_patients = None

        self.list_box_all_patients = None
        self.list_box_doctors_for_assign = None
        self.button_assign_patient = None
        self.button_add_all_patient = None
        self.button_edit_patient = None
        self.button_delete_patient = None


def start_gui():
    root = Tk()
    root.title("System Zarządzania Przychodnią")
    root.geometry("1600x700")

    view = View()

    map_widget = TkinterMapView(root, width=600, height=600, corner_radius=0)
    map_widget.grid(row=0, column=4, rowspan=2, padx=10, pady=10, sticky=N)
    map_widget.set_position(52.2297, 21.0122)
    map_widget.set_zoom(6)

    controller = Controller(view, map_widget)

    ramka_clinics = Frame(root)
    ramka_clinics.grid(row=0, column=0, padx=10, pady=5, sticky=N)

    Label(ramka_clinics, text="Przychodnie", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2)

    view.list_box_clinics = Listbox(ramka_clinics, width=35, height=10)
    view.list_box_clinics.grid(row=1, column=0, columnspan=2, pady=(0, 5))
    view.list_box_clinics.bind("<<ListboxSelect>>", controller.show_clinic_details)

    buttons_frame_clinics = Frame(ramka_clinics)
    buttons_frame_clinics.grid(row=2, column=0, columnspan=2, pady=5)

    Button(buttons_frame_clinics, text="Dodaj", width=10,
           command=controller.show_add_clinic_dialog).grid(row=0, column=0, padx=2)
    Button(buttons_frame_clinics, text="Edytuj", width=10,
           command=controller.show_edit_clinic_dialog).grid(row=0, column=1, padx=2)
    Button(buttons_frame_clinics, text="Usuń", width=10,
           command=controller.delete_clinic).grid(row=0, column=2, padx=2)

    Label(ramka_clinics, text="Szczegóły:", font=("Arial", 10, "bold")).grid(row=3, column=0, columnspan=2,
                                                                             pady=(10, 5))
    Label(ramka_clinics, text="Nazwa:").grid(row=4, column=0, sticky="w")
    view.label_clinic_name_value = Label(ramka_clinics, text="", fg="blue")
    view.label_clinic_name_value.grid(row=4, column=1, sticky="w")

    Label(ramka_clinics, text="Miasto:").grid(row=5, column=0, sticky="w")
    view.label_clinic_city_value = Label(ramka_clinics, text="", fg="blue")
    view.label_clinic_city_value.grid(row=5, column=1, sticky="w")

    ramka_doctors = Frame(root)
    ramka_doctors.grid(row=0, column=1, padx=10, pady=5, sticky=N)

    Label(ramka_doctors, text="Lekarze", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2)

    view.list_box_doctors = Listbox(ramka_doctors, width=35, height=10)
    view.list_box_doctors.grid(row=1, column=0, columnspan=2, pady=(0, 5))
    view.list_box_doctors.bind("<<ListboxSelect>>", controller.show_patients)

    buttons_frame_doctors = Frame(ramka_doctors)
    buttons_frame_doctors.grid(row=2, column=0, columnspan=2, pady=5)

    Button(buttons_frame_doctors, text="Dodaj", width=10,
           command=controller.show_add_doctor_dialog).grid(row=0, column=0, padx=2)
    Button(buttons_frame_doctors, text="Edytuj", width=10,
           command=controller.show_edit_doctor_dialog).grid(row=0, column=1, padx=2)
    Button(buttons_frame_doctors, text="Usuń", width=10,
           command=controller.delete_doctor).grid(row=0, column=2, padx=2)

    ramka_patients = Frame(root)
    ramka_patients.grid(row=0, column=2, padx=10, pady=5, sticky=N)

    Label(ramka_patients, text="Pacjenci wybranego lekarza", font=("Arial", 12, "bold")).grid(row=0, column=0,
                                                                                              columnspan=2)

    view.list_box_patients = Listbox(ramka_patients, width=35, height=10)
    view.list_box_patients.grid(row=1, column=0, columnspan=2, pady=(0, 5))

    Button(ramka_patients, text="Zmień lekarza / Usuń z lekarza",
           command=controller.show_change_patient_doctor_dialog).grid(row=2, column=0, columnspan=2, pady=5)

    ramka_all_patients = Frame(root)
    ramka_all_patients.grid(row=0, column=3, padx=10, pady=5, sticky=N)

    Label(ramka_all_patients, text="Wszyscy pacjenci", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2)

    view.list_box_all_patients = Listbox(ramka_all_patients, width=35, height=10)
    view.list_box_all_patients.grid(row=1, column=0, columnspan=2, pady=(0, 5))
    view.list_box_all_patients.bind("<<ListboxSelect>>", controller.on_patient_select)

    buttons_frame = Frame(ramka_all_patients)
    buttons_frame.grid(row=2, column=0, columnspan=2, pady=5)

    Button(buttons_frame, text="Dodaj", width=10,
           command=controller.show_add_patient_dialog).grid(row=0, column=0, padx=2)

    view.button_edit_patient = Button(buttons_frame, text="Edytuj", width=10,
                                      command=controller.show_edit_patient_dialog)
    view.button_edit_patient.grid(row=0, column=1, padx=2)

    view.button_delete_patient = Button(buttons_frame, text="Usuń", width=10,
                                        command=controller.delete_patient)
    view.button_delete_patient.grid(row=0, column=2, padx=2)

    Label(ramka_all_patients, text="Przypisz do lekarza", font=("Arial", 10, "bold")).grid(row=3, column=0,
                                                                                           columnspan=2, pady=(10, 5))

    view.list_box_doctors_for_assign = Listbox(ramka_all_patients, width=30, height=5)
    view.list_box_doctors_for_assign.grid(row=4, column=0, columnspan=2)
    view.list_box_doctors_for_assign.bind("<<ListboxSelect>>", controller.on_doctor_select)

    view.button_assign_patient = Button(
        ramka_all_patients,
        text="Przypisz wybranego pacjenta",
        command=controller.assign_patient_to_doctor
    )
    view.button_assign_patient.grid(row=5, column=0, pady=8, columnspan=2)

    root.mainloop()