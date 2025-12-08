from PADG_NB_lib.models import Clinic, Doctor, Patient, Client, get_coordinates_from_wikipedia
from tkinter import messagebox


class Controller:
    def __init__(self, view, map_widget):
        self.view = view
        self.map_widget = map_widget

        self.clinics = []
        self.doctors = []
        self.free_patients = []      # GLOBALNA LISTA PACJENTÓW

    # ================================
    # PRZYCHODNIE
    # ================================
    def show_clinics(self):
        self.view.list_box_clinics.delete(0, "end")
        for i, c in enumerate(self.clinics):
            self.view.list_box_clinics.insert(i, f"{c.name} ({c.city})")

    def show_clinic_details(self, event=None):
        sel = self.view.list_box_clinics.curselection()
        if not sel:
            return

        c = self.clinics[sel[0]]

        self.view.label_clinic_name_value.config(text=c.name)
        self.view.label_clinic_city_value.config(text=c.city)

        if c.coords:
            self.map_widget.set_position(*c.coords)
            self.map_widget.set_zoom(13)

    def add_clinic(self):
        c = Clinic(
            self.view.entry_clinic_name.get(),
            self.view.entry_clinic_city.get()
        )

        if c.coords is None:
            messagebox.showerror("Błąd", "Nie znaleziono miasta")
            return

        self.clinics.append(c)

        c.marker = self.map_widget.set_marker(*c.coords, text=c.name)
        self.show_clinics()

        self.view.entry_clinic_name.delete(0, "end")
        self.view.entry_clinic_city.delete(0, "end")

    # ================================
    # LEKARZE
    # ================================
    def show_doctors(self):
        self.view.list_box_doctors.delete(0, "end")

        for i, d in enumerate(self.doctors):
            self.view.list_box_doctors.insert(i, str(d))

        # Aktualizacja combo do przypisywania pacjentów
        self.show_doctors_for_assign()

    def add_doctor(self):
        d = Doctor(
            self.view.entry_doctor_first_name.get(),
            self.view.entry_doctor_last_name.get(),
            self.view.entry_doctor_city.get()
        )

        if d.coords is None:
            messagebox.showerror("Błąd", "Nie znaleziono miasta")
            return

        self.doctors.append(d)
        d.marker = self.map_widget.set_marker(*d.coords, text=str(d))

        self.show_doctors()

        self.view.entry_doctor_first_name.delete(0, "end")
        self.view.entry_doctor_last_name.delete(0, "end")
        self.view.entry_doctor_city.delete(0, "end")

    # ================================
    # PACJENCI PRZYPISANI DO LEKARZA
    # ================================
    def show_patients(self, event=None):
        self.view.list_box_patients.delete(0, "end")

        sel = self.view.list_box_doctors.curselection()
        if not sel:
            return

        doctor = self.doctors[sel[0]]

        for i, p in enumerate(doctor.patients):
            self.view.list_box_patients.insert(i, str(p))

    # ================================
    # GLOBALNA LISTA PACJENTÓW
    # ================================
    def show_all_patients(self):
        self.view.list_box_all_patients.delete(0, "end")

        for i, p in enumerate(self.free_patients):
            self.view.list_box_all_patients.insert(i, str(p))

        self.show_doctors_for_assign()

    def show_doctors_for_assign(self):
        self.view.list_box_doctors_for_assign.delete(0, "end")

        for i, d in enumerate(self.doctors):
            self.view.list_box_doctors_for_assign.insert(i, str(d))

    def add_patient_global(self):
        p = Patient(
            self.view.entry_all_patient_first_name.get(),
            self.view.entry_all_patient_last_name.get(),
            self.view.entry_all_patient_city.get()
        )

        if p.coords is None:
            messagebox.showerror("Błąd", "Nie znaleziono miasta")
            return

        self.free_patients.append(p)
        p.marker = self.map_widget.set_marker(*p.coords, text=str(p))

        self.show_all_patients()

        self.view.entry_all_patient_first_name.delete(0, "end")
        self.view.entry_all_patient_last_name.delete(0, "end")
        self.view.entry_all_patient_city.delete(0, "end")

    def assign_patient_to_doctor(self):
        sel_p = self.view.list_box_all_patients.curselection()
        sel_d = self.view.list_box_doctors_for_assign.curselection()

        if not sel_p or not sel_d:
            messagebox.showerror("Błąd", "Zaznacz pacjenta i lekarza")
            return

        patient = self.free_patients.pop(sel_p[0])
        doctor = self.doctors[sel_d[0]]

        doctor.add_patient(patient)

        self.show_all_patients()
        self.show_patients()
