from PADG_NB_lib.models import Clinic, Doctor, Patient, Client, get_coordinates_from_wikipedia
from tkinter import messagebox


class Controller:
    def __init__(self, view, map_widget):
        self.view = view
        self.map_widget = map_widget
        self.clinics = []
        self.doctors=  []

    def show_clinics(self):
        self.view.list_box_clinics.delete(0, "end")
        for idx, clinic in enumerate(self.clinics):
            self.view.list_box_clinics.insert(idx, f"{clinic.name} ({clinic.city})")

    def show_clinic_details(self, event=None):
        selection = self.view.list_box_clinics.curselection()

        if not selection:
            return

        index = selection[0]
        clinic = self.clinics[index]

        self.selected_index = index

        self.view.label_clinic_name_value.config(text=clinic.name)
        self.view.label_clinic_city_value.config(text=clinic.city)

        self.map_widget.set_position(
            clinic.coords[0],
            clinic.coords[1]
        )
        self.map_widget.set_zoom(14)

    def add_clinic(self):
        name = self.view.entry_clinic_name.get()
        city = self.view.entry_clinic_city.get()

        clinic = Clinic(name, city)

        if clinic.coords is None:
            messagebox.showerror(
                "Błąd lokalizacji",
                f"Nie znaleziono miasta: {city}"
            )
            return

        self.clinics.append(clinic)

        clinic.marker = self.map_widget.set_marker(
            clinic.coords[0],
            clinic.coords[1],
            text=clinic.name
        )

        self.show_clinics()
        self.clear_clinic_entries()

    def delete_clinic(self):
        i = self.view.list_box_clinics.curselection()
        if not i:
            return
        index = i[0]

        if hasattr(self.clinics[index], "marker"):
            self.clinics[index].marker.delete()

        self.clinics.pop(index)
        self.show_clinics()

    def edit_clinic(self):
        i = self.view.list_box_clinics.curselection()
        if not i:
            return
        index = i[0]
        clinic = self.clinics[index]

        self.view.entry_clinic_name.delete(0, "end")
        self.view.entry_clinic_name.insert(0, clinic.name)
        self.view.entry_clinic_city.delete(0, "end")
        self.view.entry_clinic_city.insert(0, clinic.city)

        self.view.button_add_clinic.config(
            text="Zapisz zmiany",
            command=lambda: self.update_clinic(index)
        )

    def update_clinic(self, index):
        clinic = self.clinics[index]

        name = self.view.entry_clinic_name.get()
        city = self.view.entry_clinic_city.get()

        coords = get_coordinates_from_wikipedia(city)
        if coords is None:
            from tkinter import messagebox
            messagebox.showerror(
                "Błąd lokalizacji",
                f"Nie znaleziono miasta: {city}"
            )
            return

        clinic.name = name
        clinic.city = city
        clinic.coords = coords

        if hasattr(clinic, "marker"):
            clinic.marker.set_position(coords[0], coords[1])
            clinic.marker.set_text(name)

        self.show_clinics()
        self.clear_clinic_entries()

        self.view.button_add_clinic.config(
            text="Dodaj przychodnię",
            command=self.add_clinic
        )

    def clear_clinic_entries(self):
        self.view.entry_clinic_name.delete(0, "end")
        self.view.entry_clinic_city.delete(0, "end")
        self.view.entry_clinic_name.focus()



    def show_doctors(self):
        self.view.list_box_doctors.delete(0, "end")
        for idx, doctor in enumerate(self.doctors):
            self.view.list_box_doctors.insert(idx, f"{doctor.first_name} {doctor.last_name} ({doctor.city})")

    def show_doctor_details(self, event=None):
        selection = self.view.list_box_doctors.curselection()
        if not selection:
            return

        index = selection[0]
        doctor = self.doctors[index]
        self.selected_doctor_index = index

        self.view.label_doctor_first_name_value.config(text=doctor.first_name)
        self.view.label_doctor_last_name_value.config(text=doctor.last_name)
        self.view.label_doctor_city_value.config(text=doctor.city)

        if doctor.coords:
            self.map_widget.set_position(doctor.coords[0], doctor.coords[1])
            self.map_widget.set_zoom(14)

    def add_doctor(self):
        first_name = self.view.entry_doctor_first_name.get()
        last_name = self.view.entry_doctor_last_name.get()
        city = self.view.entry_doctor_city.get()

        doctor = Doctor(first_name, last_name, city)
        if doctor.coords is None:
            messagebox.showerror("Błąd lokalizacji", f"Nie znaleziono miasta: {city}")
            return

        self.doctors.append(doctor)


        doctor.marker = self.map_widget.set_marker(
            doctor.coords[0], doctor.coords[1], text=f"{first_name} {last_name}"
        )

        self.show_doctors()
        self.clear_doctor_entries()

    def edit_doctor(self):
        i = self.view.list_box_doctors.curselection()
        if not i:
            return
        index = i[0]
        doctor = self.doctors[index]

        self.view.entry_doctor_first_name.delete(0, "end")
        self.view.entry_doctor_first_name.insert(0, doctor.first_name)
        self.view.entry_doctor_last_name.delete(0, "end")
        self.view.entry_doctor_last_name.insert(0, doctor.last_name)
        self.view.entry_doctor_city.delete(0, "end")
        self.view.entry_doctor_city.insert(0, doctor.city)

        self.view.button_add_doctor.config(text="Zapisz zmiany", command=lambda: self.update_doctor(index))

    def update_doctor(self, index):
        doctor = self.doctors[index]

        first_name = self.view.entry_doctor_first_name.get()
        last_name = self.view.entry_doctor_last_name.get()
        city = self.view.entry_doctor_city.get()

        coords = get_coordinates_from_wikipedia(city)
        if coords is None:
            messagebox.showerror("Błąd lokalizacji", f"Nie znaleziono miasta: {city}")
            return

        doctor.first_name = first_name
        doctor.last_name = last_name
        doctor.city = city
        doctor.coords = coords

        if hasattr(doctor, "marker"):
            doctor.marker.set_position(coords[0], coords[1])
            doctor.marker.set_text(f"{first_name} {last_name}")

        self.show_doctors()
        self.clear_doctor_entries()

        self.view.button_add_doctor.config(text="Dodaj lekarza", command=self.add_doctor)

    def delete_doctor(self):
        i = self.view.list_box_doctors.curselection()
        if not i:
            return
        index = i[0]

        if hasattr(self.doctors[index], "marker"):
            self.doctors[index].marker.delete()

        self.doctors.pop(index)
        self.show_doctors()

    def clear_doctor_entries(self):
        self.view.entry_doctor_first_name.delete(0, "end")
        self.view.entry_doctor_last_name.delete(0, "end")
        self.view.entry_doctor_city.delete(0, "end")
        self.view.entry_doctor_first_name.focus()

    def show_patients(self, event=None):
        self.view.list_box_patients.delete(0, "end")

        sel = self.view.list_box_doctors.curselection()
        if not sel:
            return

        index = sel[0]
        doctor = self.doctors[index]

        for i, p in enumerate(doctor.patients):
            self.view.list_box_patients.insert(
                i,
                f"{p.first_name} {p.last_name} ({p.city})"
            )

    def add_patient(self):
        sel = self.view.list_box_doctors.curselection()
        if not sel:
            messagebox.showerror("Błąd", "Wybierz lekarza")
            return

        doctor = self.doctors[sel[0]]

        fn = self.view.entry_patient_first_name.get()
        ln = self.view.entry_patient_last_name.get()
        city = self.view.entry_patient_city.get()

        p = Patient(fn, ln, city)

        if p.coords is None:
            messagebox.showerror("Błąd", f"Nie znaleziono miasta: {city}")
            return

        doctor.add_patient(p)

        p.marker = self.map_widget.set_marker(
            p.coords[0], p.coords[1],
            text=f"{fn} {ln}"
        )

        self.show_patients()
        self.clear_patient_entries()

    def delete_patient(self):
        sel_d = self.view.list_box_doctors.curselection()
        sel_p = self.view.list_box_patients.curselection()

        if not sel_d or not sel_p:
            return

        doctor = self.doctors[sel_d[0]]
        idx = sel_p[0]

        patient = doctor.patients[idx]

        if hasattr(patient, "marker"):
            patient.marker.delete()

        doctor.patients.pop(idx)

        self.show_patients()

    def edit_patient(self):
        sel_d = self.view.list_box_doctors.curselection()
        sel_p = self.view.list_box_patients.curselection()

        if not sel_d or not sel_p:
            return

        self.edit_patient_index = sel_p[0]

        doctor = self.doctors[sel_d[0]]
        p = doctor.patients[self.edit_patient_index]

        self.view.entry_patient_first_name.delete(0, "end")
        self.view.entry_patient_first_name.insert(0, p.first_name)

        self.view.entry_patient_last_name.delete(0, "end")
        self.view.entry_patient_last_name.insert(0, p.last_name)

        self.view.entry_patient_city.delete(0, "end")
        self.view.entry_patient_city.insert(0, p.city)

        self.view.button_add_patient.config(
            text="Zapisz zmiany",
            command=self.update_patient
        )

    def update_patient(self):
        sel_d = self.view.list_box_doctors.curselection()
        if not sel_d:
            return

        doctor = self.doctors[sel_d[0]]
        p = doctor.patients[self.edit_patient_index]

        fn = self.view.entry_patient_first_name.get()
        ln = self.view.entry_patient_last_name.get()
        city = self.view.entry_patient_city.get()

        coords = get_coordinates_from_wikipedia(city)

        if coords is None:
            messagebox.showerror("Błąd", f"Nie znaleziono miasta: {city}")
            return

        p.first_name = fn
        p.last_name = ln
        p.city = city
        p.coords = coords

        p.marker.set_position(coords[0], coords[1])
        p.marker.set_text(f"{fn} {ln}")

        self.view.button_add_patient.config(
            text="Dodaj pacjenta",
            command=self.add_patient
        )

        self.show_patients()
        self.clear_patient_entries()

    def clear_patient_entries(self):
        self.view.entry_patient_first_name.delete(0, "end")
        self.view.entry_patient_last_name.delete(0, "end")
        self.view.entry_patient_city.delete(0, "end")


