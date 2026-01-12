from PADG_NB_lib.models import Clinic, Doctor, Patient, Client, get_coordinates_from_wikipedia
from tkinter import messagebox, Toplevel, Label, Entry, Button, Frame, Listbox, SINGLE, Scrollbar, VERTICAL


class Controller:
    def __init__(self, view, map_widget):
        self.view = view
        self.map_widget = map_widget

        self.clinics = []
        self.doctors = []
        self.free_patients = []
        self.free_doctors = []
        self.clients = []
        self.selected_patient_index = None
        self.selected_doctor_index = None
        self.selected_free_doctor_index = None
        self.selected_clinic_for_assign_index = None

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


        self.show_doctors_of_clinic()

    def show_add_clinic_dialog(self):
        dialog = Toplevel()
        dialog.title("Dodaj przychodnię")
        dialog.geometry("350x150")
        dialog.resizable(False, False)

        dialog.transient()
        dialog.grab_set()

        frame = Frame(dialog, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        Label(frame, text="Nazwa:").grid(row=0, column=0, sticky="w", pady=5)
        entry_name = Entry(frame, width=25)
        entry_name.grid(row=0, column=1, pady=5, padx=5)
        entry_name.focus()

        Label(frame, text="Miasto:").grid(row=1, column=0, sticky="w", pady=5)
        entry_city = Entry(frame, width=25)
        entry_city.grid(row=1, column=1, pady=5, padx=5)

        def save_clinic():
            name = entry_name.get().strip()
            city = entry_city.get().strip()

            if not name or not city:
                messagebox.showwarning("Ostrzeżenie", "Wypełnij wszystkie pola!")
                return

            c = Clinic(name, city)

            if c.coords is None:
                messagebox.showerror("Błąd", "Nie znaleziono miasta")
                return

            self.clinics.append(c)
            c.marker = self.map_widget.set_marker(*c.coords, text=c.name)
            self.show_clinics()
            self.show_clinics_for_assign()

            dialog.destroy()
            messagebox.showinfo("Sukces", "Przychodnia została dodana!")

        Button(frame, text="Zapisz", command=save_clinic, width=12).grid(
            row=2, column=0, pady=15, padx=5)
        Button(frame, text="Anuluj", command=dialog.destroy, width=12).grid(
            row=2, column=1, pady=15, padx=5)

    def show_edit_clinic_dialog(self):
        sel = self.view.list_box_clinics.curselection()

        if not sel:
            messagebox.showwarning("Ostrzeżenie", "Wybierz przychodnię do edycji!")
            return

        clinic = self.clinics[sel[0]]

        dialog = Toplevel()
        dialog.title("Edytuj przychodnię")
        dialog.geometry("350x150")
        dialog.resizable(False, False)

        dialog.transient()
        dialog.grab_set()

        frame = Frame(dialog, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        Label(frame, text="Nazwa:").grid(row=0, column=0, sticky="w", pady=5)
        entry_name = Entry(frame, width=25)
        entry_name.insert(0, clinic.name)
        entry_name.grid(row=0, column=1, pady=5, padx=5)
        entry_name.focus()

        Label(frame, text="Miasto:").grid(row=1, column=0, sticky="w", pady=5)
        entry_city = Entry(frame, width=25)
        entry_city.insert(0, clinic.city)
        entry_city.grid(row=1, column=1, pady=5, padx=5)

        def update_clinic():
            name = entry_name.get().strip()
            city = entry_city.get().strip()

            if not name or not city:
                messagebox.showwarning("Ostrzeżenie", "Wypełnij wszystkie pola!")
                return

            new_coords = get_coordinates_from_wikipedia(city)

            if new_coords is None:
                messagebox.showerror("Błąd", "Nie znaleziono miasta")
                return

            if hasattr(clinic, 'marker') and clinic.marker:
                try:
                    clinic.marker.delete()
                except:
                    pass
                clinic.marker = None

            clinic.name = name
            clinic.city = city
            clinic.coords = new_coords

            clinic.marker = self.map_widget.set_marker(*clinic.coords, text=clinic.name)

            self.show_clinics()
            dialog.destroy()
            messagebox.showinfo("Sukces", "Przychodnia została zaktualizowana!")

        Button(frame, text="Zapisz", command=update_clinic, width=12).grid(
            row=2, column=0, pady=15, padx=5)
        Button(frame, text="Anuluj", command=dialog.destroy, width=12).grid(
            row=2, column=1, pady=15, padx=5)

    def delete_clinic(self):
        sel = self.view.list_box_clinics.curselection()

        if not sel:
            messagebox.showwarning("Ostrzeżenie", "Wybierz przychodnię do usunięcia!")
            return

        clinic = self.clinics[sel[0]]

        result = messagebox.askyesno(
            "Potwierdzenie",
            f"Czy na pewno chcesz usunąć przychodnię {clinic.name}?"
        )

        if result:
            if hasattr(clinic, 'marker') and clinic.marker:
                try:
                    clinic.marker.delete()
                except:
                    pass


            for doctor in clinic.doctors:
                self.free_doctors.append(doctor)
                doctor.clinic = None

            self.clinics.pop(sel[0])

            self.view.label_clinic_name_value.config(text="")
            self.view.label_clinic_city_value.config(text="")

            self.show_clinics()
            self.show_doctors_of_clinic()
            self.show_all_free_doctors()
            self.show_clinics_for_assign()
            messagebox.showinfo("Sukces", "Przychodnia została usunięta, lekarze przeniesieni do listy głównej!")

    def show_doctors(self):
        self.view.list_box_doctors.delete(0, "end")

        for i, d in enumerate(self.doctors):
            self.view.list_box_doctors.insert(i, str(d))

        self.show_doctors_for_assign()

    def show_add_doctor_dialog(self):
        dialog = Toplevel()
        dialog.title("Dodaj lekarza")
        dialog.geometry("350x200")
        dialog.resizable(False, False)

        dialog.transient()
        dialog.grab_set()

        frame = Frame(dialog, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        Label(frame, text="Imię:").grid(row=0, column=0, sticky="w", pady=5)
        entry_first_name = Entry(frame, width=25)
        entry_first_name.grid(row=0, column=1, pady=5, padx=5)
        entry_first_name.focus()

        Label(frame, text="Nazwisko:").grid(row=1, column=0, sticky="w", pady=5)
        entry_last_name = Entry(frame, width=25)
        entry_last_name.grid(row=1, column=1, pady=5, padx=5)

        Label(frame, text="Miasto:").grid(row=2, column=0, sticky="w", pady=5)
        entry_city = Entry(frame, width=25)
        entry_city.grid(row=2, column=1, pady=5, padx=5)

        def save_doctor():
            first_name = entry_first_name.get().strip()
            last_name = entry_last_name.get().strip()
            city = entry_city.get().strip()

            if not first_name or not last_name or not city:
                messagebox.showwarning("Ostrzeżenie", "Wypełnij wszystkie pola!")
                return

            d = Doctor(first_name, last_name, city)

            if d.coords is None:
                messagebox.showerror("Błąd", "Nie znaleziono miasta")
                return

            self.doctors.append(d)
            self.free_doctors.append(d)
            d.marker = self.map_widget.set_marker(*d.coords, text=str(d))

            self.show_doctors()
            self.show_all_free_doctors()
            self.show_clinics_for_assign()
            dialog.destroy()
            messagebox.showinfo("Sukces", "Lekarz został dodany!")

        Button(frame, text="Zapisz", command=save_doctor, width=12).grid(
            row=3, column=0, pady=15, padx=5)
        Button(frame, text="Anuluj", command=dialog.destroy, width=12).grid(
            row=3, column=1, pady=15, padx=5)

    def show_edit_doctor_dialog(self):
        sel = self.view.list_box_all_free_doctors.curselection()

        if not sel:
            messagebox.showwarning("Ostrzeżenie", "Wybierz lekarza do edycji!")
            return

        doctor = self.free_doctors[sel[0]]

        dialog = Toplevel()
        dialog.title("Edytuj lekarza")
        dialog.geometry("350x200")
        dialog.resizable(False, False)

        dialog.transient()
        dialog.grab_set()

        frame = Frame(dialog, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        Label(frame, text="Imię:").grid(row=0, column=0, sticky="w", pady=5)
        entry_first_name = Entry(frame, width=25)
        entry_first_name.insert(0, doctor.first_name)
        entry_first_name.grid(row=0, column=1, pady=5, padx=5)
        entry_first_name.focus()

        Label(frame, text="Nazwisko:").grid(row=1, column=0, sticky="w", pady=5)
        entry_last_name = Entry(frame, width=25)
        entry_last_name.insert(0, doctor.last_name)
        entry_last_name.grid(row=1, column=1, pady=5, padx=5)

        Label(frame, text="Miasto:").grid(row=2, column=0, sticky="w", pady=5)
        entry_city = Entry(frame, width=25)
        entry_city.insert(0, doctor.city)
        entry_city.grid(row=2, column=1, pady=5, padx=5)

        def update_doctor():
            first_name = entry_first_name.get().strip()
            last_name = entry_last_name.get().strip()
            city = entry_city.get().strip()

            if not first_name or not last_name or not city:
                messagebox.showwarning("Ostrzeżenie", "Wypełnij wszystkie pola!")
                return

            new_coords = get_coordinates_from_wikipedia(city)

            if new_coords is None:
                messagebox.showerror("Błąd", "Nie znaleziono miasta")
                return

            if hasattr(doctor, 'marker') and doctor.marker:
                try:
                    doctor.marker.delete()
                except:
                    pass
                doctor.marker = None

            doctor.first_name = first_name
            doctor.last_name = last_name
            doctor.city = city
            doctor.coords = new_coords

            doctor.marker = self.map_widget.set_marker(*doctor.coords, text=str(doctor))

            self.show_doctors()
            self.show_all_free_doctors()
            dialog.destroy()
            messagebox.showinfo("Sukces", "Dane lekarza zostały zaktualizowane!")

        Button(frame, text="Zapisz", command=update_doctor, width=12).grid(
            row=3, column=0, pady=15, padx=5)
        Button(frame, text="Anuluj", command=dialog.destroy, width=12).grid(
            row=3, column=1, pady=15, padx=5)

    def delete_doctor(self):
        sel = self.view.list_box_all_free_doctors.curselection()

        if not sel:
            messagebox.showwarning("Ostrzeżenie", "Wybierz lekarza do usunięcia!")
            return

        doctor = self.free_doctors[sel[0]]

        result = messagebox.askyesno(
            "Potwierdzenie",
            f"Czy na pewno chcesz usunąć lekarza {doctor.first_name} {doctor.last_name}?"
        )

        if result:
            if hasattr(doctor, 'marker') and doctor.marker:
                try:
                    doctor.marker.delete()
                except:
                    pass

            for patient in doctor.patients:
                self.free_patients.append(patient)
                patient.doctor = None

            self.doctors.remove(doctor)
            self.free_doctors.pop(sel[0])

            self.show_doctors()
            self.show_all_patients()
            self.show_all_free_doctors()
            self.show_clinics_for_assign()
            messagebox.showinfo("Sukces", "Lekarz został usunięty, pacjenci przeniesieni do listy głównej!")

    def show_patients(self, event=None):
        self.view.list_box_patients.delete(0, "end")

        sel = self.view.list_box_doctors.curselection()
        if not sel:
            return

        doctor = self.doctors[sel[0]]

        if doctor.coords:
            self.map_widget.set_position(*doctor.coords)
            self.map_widget.set_zoom(13)

        for i, p in enumerate(doctor.patients):
            self.view.list_box_patients.insert(i, str(p))

    def show_all_patients(self):
        self.view.list_box_all_patients.delete(0, "end")

        for i, p in enumerate(self.free_patients):
            display_text = f"{p.first_name} {p.last_name} ({p.city})"
            self.view.list_box_all_patients.insert(i, display_text)

    def show_doctors_for_assign(self):
        self.view.list_box_doctors_for_assign.delete(0, "end")

        for i, d in enumerate(self.doctors):
            self.view.list_box_doctors_for_assign.insert(i, str(d))

    def on_patient_select(self, event):
        sel = self.view.list_box_all_patients.curselection()
        if sel:
            self.selected_patient_index = sel[0]
            patient = self.free_patients[sel[0]]
            if patient.coords:
                self.map_widget.set_position(*patient.coords)
                self.map_widget.set_zoom(13)

    def on_doctor_select(self, event):
        sel = self.view.list_box_doctors_for_assign.curselection()
        if sel:
            self.selected_doctor_index = sel[0]

    def show_add_patient_dialog(self):
        dialog = Toplevel()
        dialog.title("Dodaj pacjenta")
        dialog.geometry("350x200")
        dialog.resizable(False, False)

        dialog.transient()
        dialog.grab_set()

        frame = Frame(dialog, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        Label(frame, text="Imię:").grid(row=0, column=0, sticky="w", pady=5)
        entry_first_name = Entry(frame, width=25)
        entry_first_name.grid(row=0, column=1, pady=5, padx=5)
        entry_first_name.focus()

        Label(frame, text="Nazwisko:").grid(row=1, column=0, sticky="w", pady=5)
        entry_last_name = Entry(frame, width=25)
        entry_last_name.grid(row=1, column=1, pady=5, padx=5)

        Label(frame, text="Miasto:").grid(row=2, column=0, sticky="w", pady=5)
        entry_city = Entry(frame, width=25)
        entry_city.grid(row=2, column=1, pady=5, padx=5)

        def save_patient():
            first_name = entry_first_name.get().strip()
            last_name = entry_last_name.get().strip()
            city = entry_city.get().strip()

            if not first_name or not last_name or not city:
                messagebox.showwarning("Ostrzeżenie", "Wypełnij wszystkie pola!")
                return

            p = Patient(first_name, last_name, city)

            if p.coords is None:
                messagebox.showerror("Błąd", "Nie znaleziono miasta na mapie")
                return

            self.free_patients.append(p)
            p.marker = self.map_widget.set_marker(*p.coords, text=f"{p.first_name} {p.last_name}")

            self.show_all_patients()
            self.show_doctors_for_assign()
            dialog.destroy()
            messagebox.showinfo("Sukces", "Pacjent został dodany!")

        Button(frame, text="Zapisz", command=save_patient, width=12).grid(
            row=3, column=0, pady=15, padx=5)
        Button(frame, text="Anuluj", command=dialog.destroy, width=12).grid(
            row=3, column=1, pady=15, padx=5)

    def show_edit_patient_dialog(self):
        sel = self.view.list_box_all_patients.curselection()

        if not sel:
            messagebox.showwarning("Ostrzeżenie", "Wybierz pacjenta do edycji!")
            return

        patient = self.free_patients[sel[0]]

        dialog = Toplevel()
        dialog.title("Edytuj pacjenta")
        dialog.geometry("350x200")
        dialog.resizable(False, False)

        dialog.transient()
        dialog.grab_set()

        frame = Frame(dialog, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        Label(frame, text="Imię:").grid(row=0, column=0, sticky="w", pady=5)
        entry_first_name = Entry(frame, width=25)
        entry_first_name.insert(0, patient.first_name)
        entry_first_name.grid(row=0, column=1, pady=5, padx=5)
        entry_first_name.focus()

        Label(frame, text="Nazwisko:").grid(row=1, column=0, sticky="w", pady=5)
        entry_last_name = Entry(frame, width=25)
        entry_last_name.insert(0, patient.last_name)
        entry_last_name.grid(row=1, column=1, pady=5, padx=5)

        Label(frame, text="Miasto:").grid(row=2, column=0, sticky="w", pady=5)
        entry_city = Entry(frame, width=25)
        entry_city.insert(0, patient.city)
        entry_city.grid(row=2, column=1, pady=5, padx=5)

        def update_patient():
            first_name = entry_first_name.get().strip()
            last_name = entry_last_name.get().strip()
            city = entry_city.get().strip()

            if not first_name or not last_name or not city:
                messagebox.showwarning("Ostrzeżenie", "Wypełnij wszystkie pola!")
                return

            new_coords = get_coordinates_from_wikipedia(city)

            if new_coords is None:
                messagebox.showerror("Błąd", "Nie znaleziono miasta na mapie")
                return

            if hasattr(patient, 'marker') and patient.marker:
                try:
                    patient.marker.delete()
                except:
                    pass
                patient.marker = None

            patient.first_name = first_name
            patient.last_name = last_name
            patient.city = city
            patient.coords = new_coords

            patient.marker = self.map_widget.set_marker(*patient.coords,
                                                        text=f"{patient.first_name} {patient.last_name}")

            self.show_all_patients()
            dialog.destroy()
            messagebox.showinfo("Sukces", "Dane pacjenta zostały zaktualizowane!")

        Button(frame, text="Zapisz", command=update_patient, width=12).grid(
            row=3, column=0, pady=15, padx=5)
        Button(frame, text="Anuluj", command=dialog.destroy, width=12).grid(
            row=3, column=1, pady=15, padx=5)

    def delete_patient(self):
        sel = self.view.list_box_all_patients.curselection()

        if not sel:
            messagebox.showwarning("Ostrzeżenie", "Wybierz pacjenta do usunięcia!")
            return

        patient = self.free_patients[sel[0]]

        result = messagebox.askyesno(
            "Potwierdzenie",
            f"Czy na pewno chcesz usunąć pacjenta {patient.first_name} {patient.last_name}?"
        )

        if result:
            if hasattr(patient, 'marker') and patient.marker:
                try:
                    patient.marker.delete()
                except:
                    pass

            self.free_patients.pop(sel[0])

            self.show_all_patients()
            self.show_doctors_for_assign()
            messagebox.showinfo("Sukces", "Pacjent został usunięty!")

    def assign_patient_to_doctor(self):
        if self.selected_patient_index is None or self.selected_doctor_index is None:
            messagebox.showerror("Błąd", "Zaznacz pacjenta i lekarza")
            return

        if self.selected_patient_index >= len(self.free_patients) or self.selected_doctor_index >= len(self.doctors):
            messagebox.showerror("Błąd", "Nieprawidłowy wybór")
            return

        patient = self.free_patients.pop(self.selected_patient_index)
        doctor = self.doctors[self.selected_doctor_index]

        doctor.add_patient(patient)

        self.selected_patient_index = None
        self.selected_doctor_index = None

        self.show_all_patients()
        self.show_patients()

        messagebox.showinfo("Sukces",
                            f"Pacjent {patient.first_name} {patient.last_name} został przypisany do lekarza {doctor.first_name} {doctor.last_name}")

    def on_patient_of_doctor_select(self, event):
        sel = self.view.list_box_patients.curselection()
        if sel:
            sel_doc = self.view.list_box_doctors.curselection()
            if sel_doc:
                doctor = self.doctors[sel_doc[0]]
                patient = doctor.patients[sel[0]]
                if patient.coords:
                    self.map_widget.set_position(*patient.coords)
                    self.map_widget.set_zoom(13)

    def show_change_patient_doctor_dialog(self):
        sel = self.view.list_box_patients.curselection()

        if not sel:
            messagebox.showwarning("Ostrzeżenie", "Wybierz pacjenta do przeniesienia!")
            return

        sel_doc = self.view.list_box_doctors.curselection()
        if not sel_doc:
            messagebox.showwarning("Ostrzeżenie", "Najpierw wybierz lekarza z listy!")
            return

        current_doctor = self.doctors[sel_doc[0]]
        patient = current_doctor.patients[sel[0]]

        dialog = Toplevel()
        dialog.title("Zmień lekarza pacjenta")
        dialog.geometry("400x300")
        dialog.resizable(False, False)

        dialog.transient()
        dialog.grab_set()

        frame = Frame(dialog, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        Label(frame, text=f"Pacjent: {patient.first_name} {patient.last_name}", font=("Arial", 10, "bold")).grid(row=0,
                                                                                                                 column=0,
                                                                                                                 columnspan=2,
                                                                                                                 pady=10)
        Label(frame, text=f"Obecny lekarz: {current_doctor.first_name} {current_doctor.last_name}").grid(row=1,
                                                                                                         column=0,
                                                                                                         columnspan=2,
                                                                                                         pady=5)

        Label(frame, text="Wybierz nowego lekarza:", font=("Arial", 9, "bold")).grid(row=2, column=0, columnspan=2,
                                                                                     pady=(10, 5))

        listbox_frame = Frame(frame)
        listbox_frame.grid(row=3, column=0, columnspan=2, pady=5)

        scrollbar = Scrollbar(listbox_frame, orient=VERTICAL)
        doctors_listbox = Listbox(listbox_frame, height=6, selectmode=SINGLE, width=35, yscrollcommand=scrollbar.set)
        scrollbar.config(command=doctors_listbox.yview)

        doctors_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        available_doctors = [d for d in self.doctors if d != current_doctor]
        for d in available_doctors:
            doctors_listbox.insert("end", str(d))

        def change_doctor():
            sel_new = doctors_listbox.curselection()
            if not sel_new:
                messagebox.showwarning("Ostrzeżenie", "Wybierz nowego lekarza!")
                return

            new_doctor = available_doctors[sel_new[0]]

            current_doctor.patients.remove(patient)
            new_doctor.add_patient(patient)

            self.show_patients()
            dialog.destroy()
            messagebox.showinfo("Sukces",
                                f"Pacjent przeniesiony do lekarza {new_doctor.first_name} {new_doctor.last_name}!")

        def remove_from_doctor():
            current_doctor.patients.remove(patient)
            patient.doctor = None
            self.free_patients.append(patient)

            self.show_patients()
            self.show_all_patients()
            self.show_doctors_for_assign()
            dialog.destroy()
            messagebox.showinfo("Sukces", "Pacjent został przeniesiony do listy głównej!")

        Button(frame, text="Zmień lekarza", command=change_doctor, width=15).grid(
            row=4, column=0, pady=15, padx=5)
        Button(frame, text="Usuń z lekarza", command=remove_from_doctor, width=15).grid(
            row=4, column=1, pady=15, padx=5)



    def show_all_free_doctors(self):
        """Wyświetla wszystkich lekarzy nieprzypisanych do przychodni"""
        self.view.list_box_all_free_doctors.delete(0, "end")

        for i, d in enumerate(self.free_doctors):
            display_text = f"{d.first_name} {d.last_name} ({d.city})"
            self.view.list_box_all_free_doctors.insert(i, display_text)

    def show_doctors_of_clinic(self, event=None):
        """Wyświetla lekarzy przypisanych do wybranej przychodni"""
        self.view.list_box_doctors_of_clinic.delete(0, "end")

        sel = self.view.list_box_clinics.curselection()
        if not sel:
            return

        clinic = self.clinics[sel[0]]

        for i, d in enumerate(clinic.doctors):
            self.view.list_box_doctors_of_clinic.insert(i, str(d))

    def show_clinics_for_assign(self):
        """Wyświetla przychodnie dostępne do przypisania lekarza"""
        self.view.list_box_clinics_for_assign.delete(0, "end")

        for i, c in enumerate(self.clinics):
            self.view.list_box_clinics_for_assign.insert(i, f"{c.name} ({c.city})")

    def on_free_doctor_select(self, event):
        """Obsługa wyboru wolnego lekarza"""
        sel = self.view.list_box_all_free_doctors.curselection()
        if sel:
            self.selected_free_doctor_index = sel[0]
            doctor = self.free_doctors[sel[0]]
            if doctor.coords:
                self.map_widget.set_position(*doctor.coords)
                self.map_widget.set_zoom(13)

    def on_clinic_for_assign_select(self, event):
        """Obsługa wyboru przychodni do przypisania"""
        sel = self.view.list_box_clinics_for_assign.curselection()
        if sel:
            self.selected_clinic_for_assign_index = sel[0]

    def assign_doctor_to_clinic(self):
        """Przypisuje lekarza do przychodni"""
        if self.selected_free_doctor_index is None or self.selected_clinic_for_assign_index is None:
            messagebox.showerror("Błąd", "Zaznacz lekarza i przychodnię")
            return

        if self.selected_free_doctor_index >= len(self.free_doctors) or self.selected_clinic_for_assign_index >= len(self.clinics):
            messagebox.showerror("Błąd", "Nieprawidłowy wybór")
            return

        doctor = self.free_doctors.pop(self.selected_free_doctor_index)
        clinic = self.clinics[self.selected_clinic_for_assign_index]

        clinic.add_doctor(doctor)

        self.selected_free_doctor_index = None
        self.selected_clinic_for_assign_index = None

        self.show_all_free_doctors()
        self.show_doctors_of_clinic()
        self.show_clinics()

        messagebox.showinfo("Sukces",
                            f"Lekarz {doctor.first_name} {doctor.last_name} został przypisany do przychodni {clinic.name}")

    def on_doctor_of_clinic_select(self, event):
        """Obsługa wyboru lekarza przychodni na mapie"""
        sel = self.view.list_box_doctors_of_clinic.curselection()
        if sel:
            sel_clinic = self.view.list_box_clinics.curselection()
            if sel_clinic:
                clinic = self.clinics[sel_clinic[0]]
                doctor = clinic.doctors[sel[0]]
                if doctor.coords:
                    self.map_widget.set_position(*doctor.coords)
                    self.map_widget.set_zoom(13)

    def show_change_doctor_clinic_dialog(self):
        """Dialog do zmiany przychodni lekarza"""
        sel = self.view.list_box_doctors_of_clinic.curselection()

        if not sel:
            messagebox.showwarning("Ostrzeżenie", "Wybierz lekarza do przeniesienia!")
            return

        sel_clinic = self.view.list_box_clinics.curselection()
        if not sel_clinic:
            messagebox.showwarning("Ostrzeżenie", "Najpierw wybierz przychodnię z listy!")
            return

        current_clinic = self.clinics[sel_clinic[0]]
        doctor = current_clinic.doctors[sel[0]]

        dialog = Toplevel()
        dialog.title("Zmień przychodnię lekarza")
        dialog.geometry("400x300")
        dialog.resizable(False, False)

        dialog.transient()
        dialog.grab_set()

        frame = Frame(dialog, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        Label(frame, text=f"Lekarz: {doctor.first_name} {doctor.last_name}",
              font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        Label(frame, text=f"Obecna przychodnia: {current_clinic.name}").grid(
            row=1, column=0, columnspan=2, pady=5)

        Label(frame, text="Wybierz nową przychodnię:",
              font=("Arial", 9, "bold")).grid(row=2, column=0, columnspan=2, pady=(10, 5))

        listbox_frame = Frame(frame)
        listbox_frame.grid(row=3, column=0, columnspan=2, pady=5)

        scrollbar = Scrollbar(listbox_frame, orient=VERTICAL)
        clinics_listbox = Listbox(listbox_frame, height=6, selectmode=SINGLE,
                                  width=35, yscrollcommand=scrollbar.set)
        scrollbar.config(command=clinics_listbox.yview)

        clinics_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        available_clinics = [c for c in self.clinics if c != current_clinic]
        for c in available_clinics:
            clinics_listbox.insert("end", f"{c.name} ({c.city})")

        def change_clinic():
            sel_new = clinics_listbox.curselection()
            if not sel_new:
                messagebox.showwarning("Ostrzeżenie", "Wybierz nową przychodnię!")
                return

            new_clinic = available_clinics[sel_new[0]]

            current_clinic.doctors.remove(doctor)
            new_clinic.add_doctor(doctor)

            self.show_doctors_of_clinic()
            dialog.destroy()
            messagebox.showinfo("Sukces",
                                f"Lekarz przeniesiony do przychodni {new_clinic.name}!")

        def remove_from_clinic():
            current_clinic.doctors.remove(doctor)
            doctor.clinic = None
            self.free_doctors.append(doctor)

            self.show_doctors_of_clinic()
            self.show_all_free_doctors()
            self.show_clinics_for_assign()
            dialog.destroy()
            messagebox.showinfo("Sukces", "Lekarz został przeniesiony do listy głównej!")

        Button(frame, text="Zmień przychodnię", command=change_clinic, width=17).grid(
            row=4, column=0, pady=15, padx=5)
        Button(frame, text="Usuń z przychodni", command=remove_from_clinic, width=17).grid(
            row=4, column=1, pady=15, padx=5)

    def show_clients(self):
        self.view.list_box_clients.delete(0, "end")

        for i, c in enumerate(self.clients):
            self.view.list_box_clients.insert(i, f"{c.name} ({c.city})")

    def on_client_select(self, event):
        sel = self.view.list_box_clients.curselection()
        if sel:
            client = self.clients[sel[0]]
            if client.coords:
                self.map_widget.set_position(*client.coords)
                self.map_widget.set_zoom(13)

    def show_add_client_dialog(self):
        dialog = Toplevel()
        dialog.title("Dodaj klienta")
        dialog.geometry("350x150")
        dialog.resizable(False, False)

        dialog.transient()
        dialog.grab_set()

        frame = Frame(dialog, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        Label(frame, text="Nazwa:").grid(row=0, column=0, sticky="w", pady=5)
        entry_name = Entry(frame, width=25)
        entry_name.grid(row=0, column=1, pady=5, padx=5)
        entry_name.focus()

        Label(frame, text="Miasto:").grid(row=1, column=0, sticky="w", pady=5)
        entry_city = Entry(frame, width=25)
        entry_city.grid(row=1, column=1, pady=5, padx=5)

        def save_client():
            name = entry_name.get().strip()
            city = entry_city.get().strip()

            if not name or not city:
                messagebox.showwarning("Ostrzeżenie", "Wypełnij wszystkie pola!")
                return

            c = Client(name, city)

            if c.coords is None:
                messagebox.showerror("Błąd", "Nie znaleziono miasta na mapie")
                return

            self.clients.append(c)
            c.marker = self.map_widget.set_marker(*c.coords, text=c.name)

            self.show_clients()
            dialog.destroy()
            messagebox.showinfo("Sukces", "Klient został dodany!")

        Button(frame, text="Zapisz", command=save_client, width=12).grid(
            row=2, column=0, pady=15, padx=5)
        Button(frame, text="Anuluj", command=dialog.destroy, width=12).grid(
            row=2, column=1, pady=15, padx=5)

    def show_edit_client_dialog(self):
        sel = self.view.list_box_clients.curselection()

        if not sel:
            messagebox.showwarning("Ostrzeżenie", "Wybierz klienta do edycji!")
            return

        client = self.clients[sel[0]]

        dialog = Toplevel()
        dialog.title("Edytuj klienta")
        dialog.geometry("350x150")
        dialog.resizable(False, False)

        dialog.transient()
        dialog.grab_set()

        frame = Frame(dialog, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        Label(frame, text="Nazwa:").grid(row=0, column=0, sticky="w", pady=5)
        entry_name = Entry(frame, width=25)
        entry_name.insert(0, client.name)
        entry_name.grid(row=0, column=1, pady=5, padx=5)
        entry_name.focus()

        Label(frame, text="Miasto:").grid(row=1, column=0, sticky="w", pady=5)
        entry_city = Entry(frame, width=25)
        entry_city.insert(0, client.city)
        entry_city.grid(row=1, column=1, pady=5, padx=5)

        def update_client():
            name = entry_name.get().strip()
            city = entry_city.get().strip()

            if not name or not city:
                messagebox.showwarning("Ostrzeżenie", "Wypełnij wszystkie pola!")
                return

            new_coords = get_coordinates_from_wikipedia(city)

            if new_coords is None:
                messagebox.showerror("Błąd", "Nie znaleziono miasta na mapie")
                return

            if hasattr(client, 'marker') and client.marker:
                try:
                    client.marker.delete()
                except:
                    pass
                client.marker = None

            client.name = name
            client.city = city
            client.coords = new_coords

            client.marker = self.map_widget.set_marker(*client.coords, text=client.name)

            self.show_clients()
            dialog.destroy()
            messagebox.showinfo("Sukces", "Dane klienta zostały zaktualizowane!")

        Button(frame, text="Zapisz", command=update_client, width=12).grid(
            row=2, column=0, pady=15, padx=5)
        Button(frame, text="Anuluj", command=dialog.destroy, width=12).grid(
            row=2, column=1, pady=15, padx=5)

    def delete_client(self):
        sel = self.view.list_box_clients.curselection()

        if not sel:
            messagebox.showwarning("Ostrzeżenie", "Wybierz klienta do usunięcia!")
            return

        client = self.clients[sel[0]]

        result = messagebox.askyesno(
            "Potwierdzenie",
            f"Czy na pewno chcesz usunąć klienta {client.name}?"
        )

        if result:
            if hasattr(client, 'marker') and client.marker:
                try:
                    client.marker.delete()
                except:
                    pass

            self.clients.pop(sel[0])

            self.show_clients()
            messagebox.showinfo("Sukces", "Klient został usunięty!")