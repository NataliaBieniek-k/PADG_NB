from tkinter import Toplevel, Label, Entry, Button, Listbox, messagebox, END
from PADG_NB_lib.models import Clinic, Doctor, Patient, Client


class Controller:
    def __init__(self, view, map_widget):
        self.view = view
        self.map_widget = map_widget
        self.clinics = []
        self.doctors = []
        self.patients = []
        self.clients = []

        self.selected_clinic_for_assign = None
        self.selected_doctor_for_assign = None
        self.selected_clinic_for_client_assign = None


    def show_clinic_details(self, event):
        selection = self.view.list_box_clinics.curselection()
        if not selection:
            return

        clinic = self.clinics[selection[0]]
        self.view.label_clinic_name_value.config(text=clinic.name)
        self.view.label_clinic_city_value.config(text=clinic.city)

        self.view.list_box_doctors_of_clinic.delete(0, END)
        for doctor in clinic.doctors:
            self.view.list_box_doctors_of_clinic.insert(END, f"{doctor.first_name} {doctor.last_name} ({doctor.city})")

        self.refresh_clients_lists()

    def show_add_clinic_dialog(self):
        dialog = Toplevel()
        dialog.title("Dodaj przychodnię")
        dialog.geometry("300x150")

        Label(dialog, text="Nazwa:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_name = Entry(dialog, width=25)
        entry_name.grid(row=0, column=1, padx=10, pady=5)

        Label(dialog, text="Miasto:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entry_city = Entry(dialog, width=25)
        entry_city.grid(row=1, column=1, padx=10, pady=5)

        def add_clinic():
            name = entry_name.get().strip()
            city = entry_city.get().strip()

            if not name or not city:
                messagebox.showwarning("Błąd", "Wszystkie pola są wymagane!")
                return

            clinic = Clinic(name, city)
            self.clinics.append(clinic)

            if clinic.coords:
                clinic.marker = self.map_widget.set_marker(
                    clinic.coords[0],
                    clinic.coords[1],
                    text=clinic.name
                )

            self.refresh_clinics_lists()
            dialog.destroy()
            messagebox.showinfo("Sukces", f"Dodano przychodnię: {name}")

        Button(dialog, text="Dodaj", command=add_clinic).grid(row=2, column=0, columnspan=2, pady=10)

    def show_edit_clinic_dialog(self):
        selection = self.view.list_box_clinics.curselection()
        if not selection:
            messagebox.showwarning("Błąd", "Wybierz przychodnię do edycji!")
            return

        clinic = self.clinics[selection[0]]

        dialog = Toplevel()
        dialog.title("Edytuj przychodnię")
        dialog.geometry("300x150")

        Label(dialog, text="Nazwa:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_name = Entry(dialog, width=25)
        entry_name.insert(0, clinic.name)
        entry_name.grid(row=0, column=1, padx=10, pady=5)

        Label(dialog, text="Miasto:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entry_city = Entry(dialog, width=25)
        entry_city.insert(0, clinic.city)
        entry_city.grid(row=1, column=1, padx=10, pady=5)

        def save_changes():
            name = entry_name.get().strip()
            city = entry_city.get().strip()

            if not name or not city:
                messagebox.showwarning("Błąd", "Wszystkie pola są wymagane!")
                return

            if clinic.marker:
                clinic.marker.delete()

            clinic.name = name
            clinic.city = city
            clinic.coords = clinic.get_coordinates()

            if clinic.coords:
                clinic.marker = self.map_widget.set_marker(
                    clinic.coords[0],
                    clinic.coords[1],
                    text=clinic.name
                )

            self.refresh_clinics_lists()
            dialog.destroy()
            messagebox.showinfo("Sukces", "Zaktualizowano przychodnię")

        Button(dialog, text="Zapisz", command=save_changes).grid(row=2, column=0, columnspan=2, pady=10)

    def delete_clinic(self):
        selection = self.view.list_box_clinics.curselection()
        if not selection:
            messagebox.showwarning("Błąd", "Wybierz przychodnię do usunięcia!")
            return

        clinic = self.clinics[selection[0]]

        result = messagebox.askyesno("Potwierdzenie",
                                     f"Czy na pewno usunąć przychodnię: {clinic.name}?")
        if not result:
            return

        for doctor in clinic.doctors[:]:
            doctor.clinic = None

        for client in clinic.clients[:]:
            client.clinic = None

        if clinic.marker:
            clinic.marker.delete()

        self.clinics.remove(clinic)

        self.refresh_clinics_lists()
        self.refresh_doctors_lists()
        self.refresh_clients_lists()
        messagebox.showinfo("Sukces", "Usunięto przychodnię")

    def refresh_clinics_lists(self):
        self.view.list_box_clinics.delete(0, END)
        for clinic in self.clinics:
            self.view.list_box_clinics.insert(END, clinic.name)

        self.view.list_box_clinics_for_assign.delete(0, END)
        for clinic in self.clinics:
            self.view.list_box_clinics_for_assign.insert(END, clinic.name)


    def on_doctor_of_clinic_select(self, event):
        pass

    def on_free_doctor_select(self, event):
        pass

    def on_clinic_for_assign_select(self, event):
        selection = self.view.list_box_clinics_for_assign.curselection()
        if selection:
            self.selected_clinic_for_assign = self.clinics[selection[0]]

    def show_add_doctor_dialog(self):
        dialog = Toplevel()
        dialog.title("Dodaj lekarza")
        dialog.geometry("300x200")

        Label(dialog, text="Imię:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_first_name = Entry(dialog, width=25)
        entry_first_name.grid(row=0, column=1, padx=10, pady=5)

        Label(dialog, text="Nazwisko:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entry_last_name = Entry(dialog, width=25)
        entry_last_name.grid(row=1, column=1, padx=10, pady=5)

        Label(dialog, text="Miasto:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        entry_city = Entry(dialog, width=25)
        entry_city.grid(row=2, column=1, padx=10, pady=5)

        def add_doctor():
            first_name = entry_first_name.get().strip()
            last_name = entry_last_name.get().strip()
            city = entry_city.get().strip()

            if not first_name or not last_name or not city:
                messagebox.showwarning("Błąd", "Wszystkie pola są wymagane!")
                return

            doctor = Doctor(first_name, last_name, city)
            self.doctors.append(doctor)

            if doctor.coords:
                doctor.marker = self.map_widget.set_marker(
                    doctor.coords[0],
                    doctor.coords[1],
                    text=f"{doctor.first_name} {doctor.last_name}"
                )

            self.refresh_doctors_lists()
            dialog.destroy()
            messagebox.showinfo("Sukces", f"Dodano lekarza: {first_name} {last_name}")

        Button(dialog, text="Dodaj", command=add_doctor).grid(row=3, column=0, columnspan=2, pady=10)

    def show_edit_doctor_dialog(self):
        selection = self.view.list_box_all_free_doctors.curselection()
        if not selection:
            messagebox.showwarning("Błąd", "Wybierz lekarza do edycji!")
            return

        doctor = self.doctors[selection[0]]

        dialog = Toplevel()
        dialog.title("Edytuj lekarza")
        dialog.geometry("300x200")

        Label(dialog, text="Imię:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_first_name = Entry(dialog, width=25)
        entry_first_name.insert(0, doctor.first_name)
        entry_first_name.grid(row=0, column=1, padx=10, pady=5)

        Label(dialog, text="Nazwisko:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entry_last_name = Entry(dialog, width=25)
        entry_last_name.insert(0, doctor.last_name)
        entry_last_name.grid(row=1, column=1, padx=10, pady=5)

        Label(dialog, text="Miasto:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        entry_city = Entry(dialog, width=25)
        entry_city.insert(0, doctor.city)
        entry_city.grid(row=2, column=1, padx=10, pady=5)

        def save_changes():
            first_name = entry_first_name.get().strip()
            last_name = entry_last_name.get().strip()
            city = entry_city.get().strip()

            if not first_name or not last_name or not city:
                messagebox.showwarning("Błąd", "Wszystkie pola są wymagane!")
                return

            if doctor.marker:
                doctor.marker.delete()

            doctor.first_name = first_name
            doctor.last_name = last_name
            doctor.city = city
            doctor.coords = doctor.get_coordinates()

            if doctor.coords:
                doctor.marker = self.map_widget.set_marker(
                    doctor.coords[0],
                    doctor.coords[1],
                    text=f"{doctor.first_name} {doctor.last_name}"
                )

            self.refresh_doctors_lists()
            dialog.destroy()
            messagebox.showinfo("Sukces", "Zaktualizowano lekarza")

        Button(dialog, text="Zapisz", command=save_changes).grid(row=3, column=0, columnspan=2, pady=10)

    def delete_doctor(self):
        selection = self.view.list_box_all_free_doctors.curselection()
        if not selection:
            messagebox.showwarning("Błąd", "Wybierz lekarza do usunięcia!")
            return

        doctor = self.doctors[selection[0]]

        result = messagebox.askyesno("Potwierdzenie",
                                     f"Czy na pewno usunąć lekarza: {doctor.first_name} {doctor.last_name}?")
        if not result:
            return

        if doctor.clinic:
            doctor.clinic.doctors.remove(doctor)

        for patient in doctor.patients[:]:
            patient.doctor = None

        if doctor.marker:
            doctor.marker.delete()

        self.doctors.remove(doctor)

        self.refresh_doctors_lists()
        self.refresh_patients_lists()
        messagebox.showinfo("Sukces", "Usunięto lekarza")

    def assign_doctor_to_clinic(self):
        doctor_selection = self.view.list_box_all_free_doctors.curselection()

        if not doctor_selection:
            messagebox.showwarning("Błąd", "Wybierz lekarza!")
            return

        if not self.selected_clinic_for_assign:
            messagebox.showwarning("Błąd", "Wybierz przychodnię!")
            return

        doctor = self.doctors[doctor_selection[0]]

        if doctor.clinic:
            doctor.clinic.doctors.remove(doctor)

        self.selected_clinic_for_assign.add_doctor(doctor)

        self.refresh_doctors_lists()
        self.refresh_clinics_lists()
        messagebox.showinfo("Sukces",
                            f"Przypisano lekarza {doctor.first_name} {doctor.last_name} do {self.selected_clinic_for_assign.name}")

    def show_change_doctor_clinic_dialog(self):
        selection = self.view.list_box_doctors_of_clinic.curselection()
        if not selection:
            messagebox.showwarning("Błąd", "Wybierz lekarza z listy!")
            return

        clinic_selection = self.view.list_box_clinics.curselection()
        if not clinic_selection:
            messagebox.showwarning("Błąd", "Najpierw wybierz przychodnię!")
            return

        current_clinic = self.clinics[clinic_selection[0]]
        doctor = current_clinic.doctors[selection[0]]

        dialog = Toplevel()
        dialog.title(f"Zmień przychodnię: {doctor.first_name} {doctor.last_name}")
        dialog.geometry("400x300")

        Label(dialog, text="Wybierz nową przychodnię lub usuń z obecnej:",
              font=("Arial", 10, "bold")).pack(pady=10)

        listbox_clinics = Listbox(dialog, width=50, height=10)
        listbox_clinics.pack(padx=10, pady=5)

        for clinic in self.clinics:
            if clinic != current_clinic:
                listbox_clinics.insert(END, clinic.name)

        def change_clinic():
            new_selection = listbox_clinics.curselection()
            if not new_selection:
                messagebox.showwarning("Błąd", "Wybierz przychodnię!")
                return

            current_clinic.doctors.remove(doctor)

            new_clinic = [c for c in self.clinics if c != current_clinic][new_selection[0]]
            new_clinic.add_doctor(doctor)

            self.refresh_doctors_lists()
            self.refresh_clinics_lists()
            dialog.destroy()
            messagebox.showinfo("Sukces", f"Przeniesiono do {new_clinic.name}")

        def remove_from_clinic():
            result = messagebox.askyesno("Potwierdzenie",
                                         f"Usunąć lekarza z {current_clinic.name}?")
            if result:
                current_clinic.doctors.remove(doctor)
                doctor.clinic = None
                self.refresh_doctors_lists()
                self.refresh_clinics_lists()
                dialog.destroy()
                messagebox.showinfo("Sukces", "Usunięto z przychodni")

        Button(dialog, text="Zmień przychodnię", command=change_clinic).pack(pady=5)
        Button(dialog, text="Usuń z przychodni", command=remove_from_clinic).pack(pady=5)

    def refresh_doctors_lists(self):
        self.view.list_box_all_free_doctors.delete(0, END)
        for doctor in self.doctors:
            display_text = f"{doctor.first_name} {doctor.last_name} ({doctor.city})"
            if doctor.clinic:
                display_text += f" - {doctor.clinic.name}"
            self.view.list_box_all_free_doctors.insert(END, display_text)

        self.view.list_box_doctors.delete(0, END)
        for doctor in self.doctors:
            self.view.list_box_doctors.insert(END, f"{doctor.first_name} {doctor.last_name} ({doctor.city})")

        self.view.list_box_doctors_for_assign.delete(0, END)
        for doctor in self.doctors:
            self.view.list_box_doctors_for_assign.insert(END, f"{doctor.first_name} {doctor.last_name} ({doctor.city})")

    def show_patients(self, event):
        selection = self.view.list_box_doctors.curselection()
        if not selection:
            return

        doctor = self.doctors[selection[0]]

        self.view.list_box_patients.delete(0, END)
        for patient in doctor.patients:
            self.view.list_box_patients.insert(END, f"{patient.first_name} {patient.last_name} ({patient.city})")

    def on_patient_of_doctor_select(self, event):
        pass

    def on_patient_select(self, event):
        pass

    def on_doctor_select(self, event):
        selection = self.view.list_box_doctors_for_assign.curselection()
        if selection:
            self.selected_doctor_for_assign = self.doctors[selection[0]]

    def show_add_patient_dialog(self):
        dialog = Toplevel()
        dialog.title("Dodaj pacjenta")
        dialog.geometry("300x200")

        Label(dialog, text="Imię:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_first_name = Entry(dialog, width=25)
        entry_first_name.grid(row=0, column=1, padx=10, pady=5)

        Label(dialog, text="Nazwisko:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entry_last_name = Entry(dialog, width=25)
        entry_last_name.grid(row=1, column=1, padx=10, pady=5)

        Label(dialog, text="Miasto:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        entry_city = Entry(dialog, width=25)
        entry_city.grid(row=2, column=1, padx=10, pady=5)

        def add_patient():
            first_name = entry_first_name.get().strip()
            last_name = entry_last_name.get().strip()
            city = entry_city.get().strip()

            if not first_name or not last_name or not city:
                messagebox.showwarning("Błąd", "Wszystkie pola są wymagane!")
                return

            patient = Patient(first_name, last_name, city)
            self.patients.append(patient)

            if patient.coords:
                patient.marker = self.map_widget.set_marker(
                    patient.coords[0],
                    patient.coords[1],
                    text=f"{patient.first_name} {patient.last_name}"
                )

            self.refresh_patients_lists()
            dialog.destroy()
            messagebox.showinfo("Sukces", f"Dodano pacjenta: {first_name} {last_name}")

        Button(dialog, text="Dodaj", command=add_patient).grid(row=3, column=0, columnspan=2, pady=10)

    def show_edit_patient_dialog(self):
        selection = self.view.list_box_all_patients.curselection()
        if not selection:
            messagebox.showwarning("Błąd", "Wybierz pacjenta do edycji!")
            return

        patient = self.patients[selection[0]]

        dialog = Toplevel()
        dialog.title("Edytuj pacjenta")
        dialog.geometry("300x200")

        Label(dialog, text="Imię:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_first_name = Entry(dialog, width=25)
        entry_first_name.insert(0, patient.first_name)
        entry_first_name.grid(row=0, column=1, padx=10, pady=5)

        Label(dialog, text="Nazwisko:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entry_last_name = Entry(dialog, width=25)
        entry_last_name.insert(0, patient.last_name)
        entry_last_name.grid(row=1, column=1, padx=10, pady=5)

        Label(dialog, text="Miasto:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        entry_city = Entry(dialog, width=25)
        entry_city.insert(0, patient.city)
        entry_city.grid(row=2, column=1, padx=10, pady=5)

        def save_changes():
            first_name = entry_first_name.get().strip()
            last_name = entry_last_name.get().strip()
            city = entry_city.get().strip()

            if not first_name or not last_name or not city:
                messagebox.showwarning("Błąd", "Wszystkie pola są wymagane!")
                return

            if patient.marker:
                patient.marker.delete()

            patient.first_name = first_name
            patient.last_name = last_name
            patient.city = city
            patient.coords = patient.get_coordinates()

            if patient.coords:
                patient.marker = self.map_widget.set_marker(
                    patient.coords[0],
                    patient.coords[1],
                    text=f"{patient.first_name} {patient.last_name}"
                )

            self.refresh_patients_lists()
            dialog.destroy()
            messagebox.showinfo("Sukces", "Zaktualizowano pacjenta")

        Button(dialog, text="Zapisz", command=save_changes).grid(row=3, column=0, columnspan=2, pady=10)

    def delete_patient(self):
        selection = self.view.list_box_all_patients.curselection()
        if not selection:
            messagebox.showwarning("Błąd", "Wybierz pacjenta do usunięcia!")
            return

        patient = self.patients[selection[0]]

        result = messagebox.askyesno("Potwierdzenie",
                                     f"Czy na pewno usunąć pacjenta: {patient.first_name} {patient.last_name}?")
        if not result:
            return

        if patient.doctor:
            patient.doctor.patients.remove(patient)

        if patient.marker:
            patient.marker.delete()

        self.patients.remove(patient)

        self.refresh_patients_lists()
        messagebox.showinfo("Sukces", "Usunięto pacjenta")

    def assign_patient_to_doctor(self):
        patient_selection = self.view.list_box_all_patients.curselection()

        if not patient_selection:
            messagebox.showwarning("Błąd", "Wybierz pacjenta!")
            return

        if not self.selected_doctor_for_assign:
            messagebox.showwarning("Błąd", "Wybierz lekarza!")
            return

        patient = self.patients[patient_selection[0]]

        if patient.doctor:
            patient.doctor.patients.remove(patient)

        self.selected_doctor_for_assign.add_patient(patient)

        self.refresh_patients_lists()
        messagebox.showinfo("Sukces",
                            f"Przypisano pacjenta {patient.first_name} {patient.last_name} do lekarza {self.selected_doctor_for_assign.first_name} {self.selected_doctor_for_assign.last_name}")

    def show_change_patient_doctor_dialog(self):
        selection = self.view.list_box_patients.curselection()
        if not selection:
            messagebox.showwarning("Błąd", "Wybierz pacjenta z listy!")
            return

        doctor_selection = self.view.list_box_doctors.curselection()
        if not doctor_selection:
            messagebox.showwarning("Błąd", "Najpierw wybierz lekarza!")
            return

        current_doctor = self.doctors[doctor_selection[0]]
        patient = current_doctor.patients[selection[0]]

        dialog = Toplevel()
        dialog.title(f"Zmień lekarza: {patient.first_name} {patient.last_name}")
        dialog.geometry("400x300")

        Label(dialog, text="Wybierz nowego lekarza lub usuń od obecnego:",
              font=("Arial", 10, "bold")).pack(pady=10)

        listbox_doctors = Listbox(dialog, width=50, height=10)
        listbox_doctors.pack(padx=10, pady=5)

        for doctor in self.doctors:
            if doctor != current_doctor:
                listbox_doctors.insert(END, f"{doctor.first_name} {doctor.last_name} ({doctor.city})")

        def change_doctor():
            new_selection = listbox_doctors.curselection()
            if not new_selection:
                messagebox.showwarning("Błąd", "Wybierz lekarza!")
                return

            current_doctor.patients.remove(patient)

            new_doctor = [d for d in self.doctors if d != current_doctor][new_selection[0]]
            new_doctor.add_patient(patient)

            self.refresh_patients_lists()
            dialog.destroy()
            messagebox.showinfo("Sukces", f"Przeniesiono do lekarza {new_doctor.first_name} {new_doctor.last_name}")

        def remove_from_doctor():
            result = messagebox.askyesno("Potwierdzenie",
                                         f"Usunąć pacjenta od lekarza {current_doctor.first_name} {current_doctor.last_name}?")
            if result:
                current_doctor.patients.remove(patient)
                patient.doctor = None
                self.refresh_patients_lists()
                dialog.destroy()
                messagebox.showinfo("Sukces", "Usunięto od lekarza")

        Button(dialog, text="Zmień lekarza", command=change_doctor).pack(pady=5)
        Button(dialog, text="Usuń od lekarza", command=remove_from_doctor).pack(pady=5)

    def refresh_clients_lists(self):
        self.view.list_box_clients.delete(0, END)
        for client in self.clients:
            display_text = f"{client.name} ({client.city})"
            if client.clinic:
                display_text += f" - {client.clinic.name}"
            self.view.list_box_clients.insert(END, display_text)

        self.view.list_box_clinics_for_client_assign.delete(0, END)
        for clinic in self.clinics:
            self.view.list_box_clinics_for_client_assign.insert(END, clinic.name)

        self.view.list_box_clients_of_clinic.delete(0, END)
        clinic_selection = self.view.list_box_clinics.curselection()
        if clinic_selection:
            clinic = self.clinics[clinic_selection[0]]
            for client in clinic.clients:
                self.view.list_box_clients_of_clinic.insert(END, f"{client.name} ({client.city})")


    def on_client_of_clinic_select(self, event):
        pass

    def on_clinic_for_client_assign_select(self, event):
        selection = self.view.list_box_clinics_for_client_assign.curselection()
        if selection:
            self.selected_clinic_for_client_assign = self.clinics[selection[0]]

    def on_client_select(self, event):
        pass

    def show_add_client_dialog(self):
        dialog = Toplevel()
        dialog.title("Dodaj klienta")
        dialog.geometry("300x150")

        Label(dialog, text="Nazwa:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_name = Entry(dialog, width=25)
        entry_name.grid(row=0, column=1, padx=10, pady=5)

        Label(dialog, text="Miasto:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entry_city = Entry(dialog, width=25)
        entry_city.grid(row=1, column=1, padx=10, pady=5)

        def add_client():
            name = entry_name.get().strip()
            city = entry_city.get().strip()

            if not name or not city:
                messagebox.showwarning("Błąd", "Wszystkie pola są wymagane!")
                return

            client = Client(name, city)
            self.clients.append(client)

            if client.coords:
                client.marker = self.map_widget.set_marker(
                    client.coords[0],
                    client.coords[1],
                    text=client.name
                )

            self.refresh_clients_lists()
            dialog.destroy()
            messagebox.showinfo("Sukces", f"Dodano klienta: {name}")

        Button(dialog, text="Dodaj", command=add_client).grid(row=2, column=0, columnspan=2, pady=10)

    def show_edit_client_dialog(self):
        selection = self.view.list_box_clients.curselection()
        if not selection:
            messagebox.showwarning("Błąd", "Wybierz klienta do edycji!")
            return

        client = self.clients[selection[0]]

        dialog = Toplevel()
        dialog.title("Edytuj klienta")
        dialog.geometry("300x150")

        Label(dialog, text="Nazwa:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_name = Entry(dialog, width=25)
        entry_name.insert(0, client.name)
        entry_name.grid(row=0, column=1, padx=10, pady=5)

        Label(dialog, text="Miasto:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entry_city = Entry(dialog, width=25)
        entry_city.insert(0, client.city)
        entry_city.grid(row=1, column=1, padx=10, pady=5)

        def save_changes():
            name = entry_name.get().strip()
            city = entry_city.get().strip()

            if not name or not city:
                messagebox.showwarning("Błąd", "Wszystkie pola są wymagane!")
                return

            if client.marker:
                client.marker.delete()

            client.name = name
            client.city = city
            client.coords = client.get_coordinates()

            if client.coords:
                client.marker = self.map_widget.set_marker(
                    client.coords[0],
                    client.coords[1],
                    text=client.name
                )

            self.refresh_clients_lists()
            dialog.destroy()
            messagebox.showinfo("Sukces", "Zaktualizowano klienta")

        Button(dialog, text="Zapisz", command=save_changes).grid(row=2, column=0, columnspan=2, pady=10)

    def delete_client(self):
        selection = self.view.list_box_clients.curselection()
        if not selection:
            messagebox.showwarning("Błąd", "Wybierz klienta do usunięcia!")
            return

        client = self.clients[selection[0]]

        result = messagebox.askyesno("Potwierdzenie",
                                     f"Czy na pewno usunąć klienta: {client.name}?")
        if not result:
            return

        if client.clinic:
            client.clinic.clients.remove(client)

        if client.marker:
            client.marker.delete()

        self.clients.remove(client)

        self.refresh_clients_lists()
        messagebox.showinfo("Sukces", "Usunięto klienta")

    def assign_client_to_clinic(self):
        client_selection = self.view.list_box_clients.curselection()

        if not client_selection:
            messagebox.showwarning("Błąd", "Wybierz klienta!")
            return

        if not self.selected_clinic_for_client_assign:
            messagebox.showwarning("Błąd", "Wybierz przychodnię!")
            return

        client = self.clients[client_selection[0]]

        if client.clinic:
            client.clinic.clients.remove(client)

        self.selected_clinic_for_client_assign.add_client(client)

        self.refresh_clients_lists()
        messagebox.showinfo("Sukces",
                            f"Przypisano klienta {client.name} do {self.selected_clinic_for_client_assign.name}")

    def show_change_client_clinic_dialog(self):
        selection = self.view.list_box_clients_of_clinic.curselection()
        if not selection:
            messagebox.showwarning("Błąd", "Wybierz klienta z listy!")
            return

        clinic_selection = self.view.list_box_clinics.curselection()
        if not clinic_selection:
            messagebox.showwarning("Błąd", "Najpierw wybierz przychodnię!")
            return

        current_clinic = self.clinics[clinic_selection[0]]
        client = current_clinic.clients[selection[0]]

        dialog = Toplevel()
        dialog.title(f"Zmień przychodnię: {client.name}")
        dialog.geometry("400x300")

        Label(dialog, text="Wybierz nową przychodnię lub usuń z obecnej:",
              font=("Arial", 10, "bold")).pack(pady=10)

        listbox_clinics = Listbox(dialog, width=50, height=10)
        listbox_clinics.pack(padx=10, pady=5)

        for clinic in self.clinics:
            if clinic != current_clinic:
                listbox_clinics.insert(END, clinic.name)

        def change_clinic():
            new_selection = listbox_clinics.curselection()
            if not new_selection:
                messagebox.showwarning("Błąd", "Wybierz przychodnię!")
                return

            current_clinic.clients.remove(client)

            new_clinic = [c for c in self.clinics if c != current_clinic][new_selection[0]]
            new_clinic.add_client(client)

            self.refresh_clients_lists()
            dialog.destroy()
            messagebox.showinfo("Sukces", f"Przeniesiono do {new_clinic.name}")

        def remove_from_clinic():
            result = messagebox.askyesno("Potwierdzenie",
                                         f"Usunąć klienta z {current_clinic.name}?")
            if result:
                current_clinic.clients.remove(client)
                client.clinic = None
                self.refresh_clients_lists()
                dialog.destroy()
                messagebox.showinfo("Sukces", "Usunięto z przychodni")

        Button(dialog, text="Zmień przychodnię", command=change_clinic).pack(pady=5)
        Button(dialog, text="Usuń z przychodni", command=remove_from_clinic).pack(pady=5)

    def refresh_clients_lists(self):
        self.view.list_box_clients.delete(0, END)
        for client in self.clients:
            display_text = f"{client.name} ({client.city})"
            if client.clinic:
                display_text += f" - {client.clinic.name}"
            self.view.list_box_clients.insert(END, display_text)

        self.view.list_box_clinics_for_client_assign.delete(0, END)
        for clinic in self.clinics:
            self.view.list_box_clinics_for_client_assign.insert(END, clinic.name)

        self.view.list_box_clients_of_clinic.delete(0, END)
        clinic_selection = self.view.list_box_clinics.curselection()
        if clinic_selection:
            clinic = self.clinics[clinic_selection[0]]
            for client in clinic.clients:
                self.view.list_box_clients_of_clinic.insert(END, f"{client.name} ({client.city})")