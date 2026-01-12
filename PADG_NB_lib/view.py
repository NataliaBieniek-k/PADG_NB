from tkinter import Tk, Frame, Label, Entry, Button, Listbox, N, END, Toplevel
from tkintermapview import TkinterMapView
from PADG_NB_lib.controller import Controller


class View:
    def __init__(self):
        self.list_box_clinics = None
        self.label_clinic_name_value = None
        self.label_clinic_city_value = None

        self.list_box_doctors = None
        self.list_box_doctors_of_clinic = None
        self.list_box_all_free_doctors = None
        self.list_box_clinics_for_assign = None

        self.list_box_patients = None

        self.list_box_all_patients = None
        self.list_box_doctors_for_assign = None
        self.button_assign_patient = None
        self.button_add_all_patient = None
        self.button_edit_patient = None
        self.button_delete_patient = None

        self.list_box_clients = None


def start_gui():
    root = Tk()
    root.title("System Zarządzania Przychodnią")
    root.geometry("2400x750")

    view = View()

    map_widget = TkinterMapView(root, width=550, height=650, corner_radius=0)
    map_widget.grid(row=0, column=6, rowspan=2, padx=10, pady=10, sticky=N)
    map_widget.set_position(52.2297, 21.0122)
    map_widget.set_zoom(6)

    controller = Controller(view, map_widget)


    ramka_clinics = Frame(root, relief="ridge", borderwidth=2)
    ramka_clinics.grid(row=0, column=0, padx=5, pady=5, sticky=N)

    Label(ramka_clinics, text="PRZYCHODNIE", font=("Arial", 12, "bold"), bg="lightblue").pack(fill="x", pady=5)

    view.list_box_clinics = Listbox(ramka_clinics, width=30, height=10, exportselection=False)
    view.list_box_clinics.pack(padx=5, pady=5)
    view.list_box_clinics.bind("<<ListboxSelect>>", controller.show_clinic_details)

    buttons_frame_clinics = Frame(ramka_clinics)
    buttons_frame_clinics.pack(pady=5)

    Button(buttons_frame_clinics, text="Dodaj", width=8,
           command=controller.show_add_clinic_dialog).grid(row=0, column=0, padx=2)
    Button(buttons_frame_clinics, text="Edytuj", width=8,
           command=controller.show_edit_clinic_dialog).grid(row=0, column=1, padx=2)
    Button(buttons_frame_clinics, text="Usuń", width=8,
           command=controller.delete_clinic).grid(row=0, column=2, padx=2)

    details_frame = Frame(ramka_clinics)
    details_frame.pack(pady=10, padx=5)

    Label(details_frame, text="Szczegóły:", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
    Label(details_frame, text="Nazwa:").grid(row=1, column=0, sticky="w")
    view.label_clinic_name_value = Label(details_frame, text="", fg="blue")
    view.label_clinic_name_value.grid(row=1, column=1, sticky="w")

    Label(details_frame, text="Miasto:").grid(row=2, column=0, sticky="w")
    view.label_clinic_city_value = Label(details_frame, text="", fg="blue")
    view.label_clinic_city_value.grid(row=2, column=1, sticky="w")


    ramka_doctors_of_clinic = Frame(root, relief="ridge", borderwidth=2)
    ramka_doctors_of_clinic.grid(row=0, column=1, padx=5, pady=5, sticky=N)

    Label(ramka_doctors_of_clinic, text="LEKARZE PRZYCHODNI",
          font=("Arial", 12, "bold"), bg="lightgreen").pack(fill="x", pady=5)

    view.list_box_doctors_of_clinic = Listbox(ramka_doctors_of_clinic, width=30, height=10, exportselection=False)
    view.list_box_doctors_of_clinic.pack(padx=5, pady=5)
    view.list_box_doctors_of_clinic.bind("<<ListboxSelect>>", controller.on_doctor_of_clinic_select)

    Button(ramka_doctors_of_clinic, text="Zmień przychodnię / Usuń", width=28,
           command=controller.show_change_doctor_clinic_dialog).pack(pady=5, padx=5)


    ramka_all_free_doctors = Frame(root, relief="ridge", borderwidth=2)
    ramka_all_free_doctors.grid(row=0, column=2, padx=5, pady=5, sticky=N)

    Label(ramka_all_free_doctors, text="WSZYSCY LEKARZE",
          font=("Arial", 12, "bold"), bg="lightyellow").pack(fill="x", pady=5)

    view.list_box_all_free_doctors = Listbox(ramka_all_free_doctors, width=30, height=10, exportselection=False)
    view.list_box_all_free_doctors.pack(padx=5, pady=5)
    view.list_box_all_free_doctors.bind("<<ListboxSelect>>", controller.on_free_doctor_select)

    buttons_frame_doctors = Frame(ramka_all_free_doctors)
    buttons_frame_doctors.pack(pady=5)

    Button(buttons_frame_doctors, text="Dodaj", width=8,
           command=controller.show_add_doctor_dialog).grid(row=0, column=0, padx=2)
    Button(buttons_frame_doctors, text="Edytuj", width=8,
           command=controller.show_edit_doctor_dialog).grid(row=0, column=1, padx=2)
    Button(buttons_frame_doctors, text="Usuń", width=8,
           command=controller.delete_doctor).grid(row=0, column=2, padx=2)

    Label(ramka_all_free_doctors, text="Przypisz do przychodni",
          font=("Arial", 10, "bold")).pack(pady=(10, 5))

    view.list_box_clinics_for_assign = Listbox(ramka_all_free_doctors, width=28, height=5, exportselection=False)
    view.list_box_clinics_for_assign.pack(padx=5)
    view.list_box_clinics_for_assign.bind("<<ListboxSelect>>", controller.on_clinic_for_assign_select)

    Button(ramka_all_free_doctors, text="Przypisz wybranego lekarza", width=28,
           command=controller.assign_doctor_to_clinic).pack(pady=8, padx=5)


    ramka_doctors = Frame(root, relief="ridge", borderwidth=2)
    ramka_doctors.grid(row=0, column=3, padx=5, pady=5, sticky=N)

    Label(ramka_doctors, text="WSZYSCY LEKARZE", font=("Arial", 12, "bold"), bg="lightgreen").pack(fill="x", pady=5)

    view.list_box_doctors = Listbox(ramka_doctors, width=30, height=15, exportselection=False)
    view.list_box_doctors.pack(padx=5, pady=5)
    view.list_box_doctors.bind("<<ListboxSelect>>", controller.show_patients)


    ramka_patients = Frame(root, relief="ridge", borderwidth=2)
    ramka_patients.grid(row=0, column=4, padx=5, pady=5, sticky=N)

    Label(ramka_patients, text="PACJENCI LEKARZA", font=("Arial", 12, "bold"), bg="lightyellow").pack(fill="x", pady=5)

    view.list_box_patients = Listbox(ramka_patients, width=30, height=10, exportselection=False)
    view.list_box_patients.pack(padx=5, pady=5)
    view.list_box_patients.bind("<<ListboxSelect>>", controller.on_patient_of_doctor_select)

    Button(ramka_patients, text="Zmień lekarza / Usuń z lekarza", width=28,
           command=controller.show_change_patient_doctor_dialog).pack(pady=5, padx=5)

    ramka_all_patients = Frame(root, relief="ridge", borderwidth=2)
    ramka_all_patients.grid(row=1, column=3, padx=5, pady=5, sticky=N)

    Label(ramka_all_patients, text="WSZYSCY PACJENCI", font=("Arial", 12, "bold"), bg="lightcoral").pack(fill="x",
                                                                                                         pady=5)

    view.list_box_all_patients = Listbox(ramka_all_patients, width=30, height=10, exportselection=False)
    view.list_box_all_patients.pack(padx=5, pady=5)
    view.list_box_all_patients.bind("<<ListboxSelect>>", controller.on_patient_select)

    buttons_frame = Frame(ramka_all_patients)
    buttons_frame.pack(pady=5)

    Button(buttons_frame, text="Dodaj", width=8,
           command=controller.show_add_patient_dialog).grid(row=0, column=0, padx=2)

    view.button_edit_patient = Button(buttons_frame, text="Edytuj", width=8,
                                      command=controller.show_edit_patient_dialog)
    view.button_edit_patient.grid(row=0, column=1, padx=2)

    view.button_delete_patient = Button(buttons_frame, text="Usuń", width=8,
                                        command=controller.delete_patient)
    view.button_delete_patient.grid(row=0, column=2, padx=2)

    Label(ramka_all_patients, text="Przypisz do lekarza", font=("Arial", 10, "bold")).pack(pady=(10, 5))

    view.list_box_doctors_for_assign = Listbox(ramka_all_patients, width=28, height=5, exportselection=False)
    view.list_box_doctors_for_assign.pack(padx=5)
    view.list_box_doctors_for_assign.bind("<<ListboxSelect>>", controller.on_doctor_select)

    view.button_assign_patient = Button(
        ramka_all_patients,
        text="Przypisz wybranego pacjenta",
        width=28,
        command=controller.assign_patient_to_doctor
    )
    view.button_assign_patient.pack(pady=8, padx=5)

    ramka_clients = Frame(root, relief="ridge", borderwidth=2)
    ramka_clients.grid(row=0, column=5, padx=5, pady=5, sticky=N)

    Label(ramka_clients, text="KLIENCI", font=("Arial", 12, "bold"), bg="lightpink").pack(fill="x", pady=5)

    view.list_box_clients = Listbox(ramka_clients, width=30, height=10, exportselection=False)
    view.list_box_clients.pack(padx=5, pady=5)
    view.list_box_clients.bind("<<ListboxSelect>>", controller.on_client_select)

    buttons_frame_clients = Frame(ramka_clients)
    buttons_frame_clients.pack(pady=5)

    Button(buttons_frame_clients, text="Dodaj", width=8,
           command=controller.show_add_client_dialog).grid(row=0, column=0, padx=2)
    Button(buttons_frame_clients, text="Edytuj", width=8,
           command=controller.show_edit_client_dialog).grid(row=0, column=1, padx=2)
    Button(buttons_frame_clients, text="Usuń", width=8,
           command=controller.delete_client).grid(row=0, column=2, padx=2)

    root.mainloop()