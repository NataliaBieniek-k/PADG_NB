from PADG_NB_lib.models import Clinic

class Controller:
    def __init__(self, view, map_widget):
        self.view = view
        self.map_widget = map_widget
        self.clinics = []

    def show_clinics(self):
        self.view.list_box_clinics.delete(0, "end")
        for idx, clinic in enumerate(self.clinics):
            self.view.list_box_clinics.insert(idx, f"{clinic.name} ({clinic.city})")

    def add_clinic(self):
        name = self.view.entry_clinic_name.get()
        city = self.view.entry_clinic_city.get()
        clinic = Clinic(name, city)
        self.clinics.append(clinic)

        clinic.marker = self.map_widget.set_marker(clinic.coords[0], clinic.coords[1], text=clinic.name)

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
        clinic.name = self.view.entry_clinic_name.get()
        clinic.city = self.view.entry_clinic_city.get()
        clinic.coords = clinic.get_coordinates()
        if hasattr(clinic, "marker"):
            clinic.marker.set_position(clinic.coords[0], clinic.coords[1])
            clinic.marker.set_text(clinic.name)

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
