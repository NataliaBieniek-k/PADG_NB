from tkinter import Tk, Frame, Label, Listbox, Button, Canvas, Scrollbar
from tkintermapview import TkinterMapView
from PADG_NB_lib.controller import Controller


class View:
    def __init__(self, root):
        self.root = root

        self.list_box_clinics = None
        self.label_clinic_name_value = None
        self.label_clinic_city_value = None

        self.list_box_doctors = None
        self.list_box_doctors_of_clinic = None
        self.list_box_all_free_doctors = None
        self.list_box_clinics_for_assign = None

        self.list_box_patients = None
        self.list_box_patients_of_clinic = None

        self.list_box_all_patients = None
        self.list_box_doctors_for_assign = None
        self.list_box_clinics_for_patient_assign = None
        self.button_assign_patient = None
        self.button_edit_patient = None
        self.button_delete_patient = None

        self.list_box_clients = None
        self.list_box_clients_of_clinic = None
        self.list_box_clinics_for_client_assign = None

        self.menu_frame = Frame(root, bg="#2c3e50")
        self.menu_frame.pack(side="top", fill="x")

        self.content_frame = Frame(root, bg="#ecf0f1")
        self.content_frame.pack(fill="both", expand=True)

        self.frames = {}
        self.controller = Controller(self, None)

        self._create_menu()
        self._create_views()
        self.show_view("clinics")

    def _menu_button(self, text, view):
        Button(
            self.menu_frame,
            text=text,
            bg="#34495e",
            fg="white",
            activebackground="#1abc9c",
            width=16,
            command=lambda: self.show_view(view)
        ).pack(side="left", padx=2, pady=2)

    def _create_menu(self):
        self._menu_button("PRZYCHODNIE", "clinics")
        self._menu_button("LEKARZE", "doctors")
        self._menu_button("PACJENCI", "patients")
        self._menu_button("KLIENCI", "clients")
        self._menu_button("MAPA", "map")

    def _create_views(self):
        self.frames["clinics"] = self._create_clinics_view()
        self.frames["doctors"] = self._create_doctors_view()
        self.frames["patients"] = self._create_patients_view()
        self.frames["clients"] = self._create_clients_view()
        self.frames["map"] = self._create_map_view()

        for frame in self.frames.values():
            frame.place(relx=0.5, rely=0, anchor="n", relwidth=1, relheight=1)

    def show_view(self, name):
        self.frames[name].tkraise()

    def _section(self, parent, title, color):
        Label(parent, text=title, font=("Arial", 14, "bold"),
              bg=color, fg="white", pady=6).pack(fill="x", pady=(10, 5))

    def _create_clinics_view(self):
        frame = Frame(self.content_frame, bg="#ecf0f1")

        canvas = Canvas(frame, bg="#ecf0f1", highlightthickness=0)
        scroll = Scrollbar(frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)

        scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)


        inner_frame = Frame(canvas, bg="#ecf0f1")
        canvas.create_window((canvas.winfo_width() // 2, 0), window=inner_frame, anchor="n")


        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas.find_withtag("all")[0], width=canvas.winfo_width())
            canvas.coords(canvas.find_withtag("all")[0], canvas.winfo_width() // 2, 0)

        inner_frame.bind("<Configure>", on_configure)
        canvas.bind("<Configure>", on_configure)

        self._section(inner_frame, "PRZYCHODNIE", "#2980b9")
        self.list_box_clinics = Listbox(inner_frame, width=50, height=6, exportselection=False)
        self.list_box_clinics.pack(pady=5)
        self.list_box_clinics.bind("<<ListboxSelect>>", self.controller.show_clinic_details)

        buttons_frame = Frame(inner_frame, bg="#ecf0f1")
        buttons_frame.pack(pady=5)
        Button(buttons_frame, text="Dodaj", width=12, command=self.controller.show_add_clinic_dialog).pack(side="left",
                                                                                                           padx=2)
        Button(buttons_frame, text="Edytuj", width=12, command=self.controller.show_edit_clinic_dialog).pack(
            side="left", padx=2)
        Button(buttons_frame, text="Usuń", width=12, command=self.controller.delete_clinic).pack(side="left", padx=2)

        self._section(inner_frame, "LEKARZE PRZYCHODNI", "#27ae60")
        self.list_box_doctors_of_clinic = Listbox(inner_frame, width=50, height=5, exportselection=False)
        self.list_box_doctors_of_clinic.pack(pady=3)
        self.list_box_doctors_of_clinic.bind("<<ListboxSelect>>", self.controller.on_doctor_of_clinic_select)
        Button(inner_frame, text="Zmień / Usuń lekarza", command=self.controller.show_change_doctor_clinic_dialog).pack(
            pady=2)

        self._section(inner_frame, "PACJENCI PRZYCHODNI", "#e67e22")
        self.list_box_patients_of_clinic = Listbox(inner_frame, width=50, height=5, exportselection=False)
        self.list_box_patients_of_clinic.pack(pady=3)
        self.list_box_patients_of_clinic.bind("<<ListboxSelect>>", self.controller.on_patient_of_clinic_select)
        Button(inner_frame, text="Zmień / Usuń pacjenta",
               command=self.controller.show_change_patient_clinic_dialog).pack(pady=2)

        self._section(inner_frame, "KLIENCI PRZYCHODNI", "#8e44ad")
        self.list_box_clients_of_clinic = Listbox(inner_frame, width=50, height=5, exportselection=False)
        self.list_box_clients_of_clinic.pack(pady=3)
        self.list_box_clients_of_clinic.bind("<<ListboxSelect>>", self.controller.on_client_of_clinic_select)
        Button(inner_frame, text="Zmień / Usuń klienta", command=self.controller.show_change_client_clinic_dialog).pack(
            pady=2)

        return frame

    def _create_doctors_view(self):
        frame = Frame(self.content_frame, bg="#ecf0f1")

        self._section(frame, "LEKARZE", "#27ae60")

        self.list_box_all_free_doctors = Listbox(frame, width=50, height=10, exportselection=False)
        self.list_box_all_free_doctors.pack(pady=5)
        self.list_box_all_free_doctors.bind("<<ListboxSelect>>",
                                            self.controller.on_free_doctor_select)

        self.list_box_doctors = self.list_box_all_free_doctors

        Button(frame, text="Dodaj lekarza",
               command=self.controller.show_add_doctor_dialog).pack(pady=2)
        Button(frame, text="Edytuj lekarza",
               command=self.controller.show_edit_doctor_dialog).pack(pady=2)
        Button(frame, text="Usuń lekarza",
               command=self.controller.delete_doctor).pack(pady=2)

        Label(frame, text="Przypisz do przychodni", font=("Arial", 10, "bold"),
              bg="#ecf0f1").pack(pady=(10, 0))

        self.list_box_clinics_for_assign = Listbox(frame, width=48, height=5, exportselection=False)
        self.list_box_clinics_for_assign.pack(pady=5)
        self.list_box_clinics_for_assign.bind("<<ListboxSelect>>",
                                              self.controller.on_clinic_for_assign_select)

        Button(frame, text="Przypisz lekarza",
               command=self.controller.assign_doctor_to_clinic).pack(pady=5)

        self._section(frame, "PACJENCI WYBRANEGO LEKARZA", "#e67e22")

        self.list_box_patients = Listbox(frame, width=50, height=8, exportselection=False)
        self.list_box_patients.pack(pady=5)
        self.list_box_patients.bind("<<ListboxSelect>>",
                                    self.controller.on_patient_of_doctor_select)

        Button(frame, text="Zmień lekarza / Usuń pacjenta",
               command=self.controller.show_change_patient_doctor_dialog).pack(pady=5)

        return frame

    def _create_patients_view(self):
        frame = Frame(self.content_frame, bg="#ecf0f1")

        self._section(frame, "PACJENCI", "#e67e22")

        self.list_box_all_patients = Listbox(frame, width=50, height=12, exportselection=False)
        self.list_box_all_patients.pack(pady=5)
        self.list_box_all_patients.bind("<<ListboxSelect>>",
                                        self.controller.on_patient_select)

        Button(frame, text="Dodaj pacjenta",
               command=self.controller.show_add_patient_dialog).pack(pady=2)
        Button(frame, text="Edytuj pacjenta",
               command=self.controller.show_edit_patient_dialog).pack(pady=2)
        Button(frame, text="Usuń pacjenta",
               command=self.controller.delete_patient).pack(pady=2)

        Label(frame, text="Przypisz do lekarza", font=("Arial", 10, "bold"),
              bg="#ecf0f1").pack(pady=(10, 0))

        self.list_box_doctors_for_assign = Listbox(frame, width=48, height=5, exportselection=False)
        self.list_box_doctors_for_assign.pack(pady=5)
        self.list_box_doctors_for_assign.bind("<<ListboxSelect>>",
                                              self.controller.on_doctor_select)

        Button(frame, text="Przypisz do lekarza",
               command=self.controller.assign_patient_to_doctor).pack(pady=5)

        Label(frame, text="Przypisz do przychodni", font=("Arial", 10, "bold"),
              bg="#ecf0f1").pack(pady=(10, 0))

        self.list_box_clinics_for_patient_assign = Listbox(frame, width=48, height=5, exportselection=False)
        self.list_box_clinics_for_patient_assign.pack(pady=5)
        self.list_box_clinics_for_patient_assign.bind("<<ListboxSelect>>",
                                                      self.controller.on_clinic_for_patient_assign_select)

        Button(frame, text="Przypisz do przychodni",
               command=self.controller.assign_patient_to_clinic).pack(pady=5)

        return frame

    def _create_clients_view(self):
        frame = Frame(self.content_frame, bg="#ecf0f1")

        self._section(frame, "KLIENCI", "#8e44ad")

        self.list_box_clients = Listbox(frame, width=50, height=12, exportselection=False)
        self.list_box_clients.pack(pady=5)
        self.list_box_clients.bind("<<ListboxSelect>>",
                                   self.controller.on_client_select)

        Button(frame, text="Dodaj klienta",
               command=self.controller.show_add_client_dialog).pack(pady=2)
        Button(frame, text="Edytuj klienta",
               command=self.controller.show_edit_client_dialog).pack(pady=2)
        Button(frame, text="Usuń klienta",
               command=self.controller.delete_client).pack(pady=2)

        Label(frame, text="Przypisz do przychodni", font=("Arial", 10, "bold"),
              bg="#ecf0f1").pack(pady=(10, 0))

        self.list_box_clinics_for_client_assign = Listbox(frame, width=48, height=5, exportselection=False)
        self.list_box_clinics_for_client_assign.pack(pady=5)
        self.list_box_clinics_for_client_assign.bind("<<ListboxSelect>>",
                                                     self.controller.on_clinic_for_client_assign_select)

        Button(frame, text="Przypisz klienta",
               command=self.controller.assign_client_to_clinic).pack(pady=5)

        return frame


    def _create_map_view(self):
        frame = Frame(self.content_frame, bg="#ecf0f1")

        control_panel = Frame(frame, bg="#ecf0f1", width=200)
        control_panel.pack(side="left", fill="y", padx=10, pady=10)

        Label(control_panel, text="WYŚWIETL NA MAPIE", font=("Arial", 12, "bold"),
              bg="#ecf0f1").pack(pady=10)

        Button(control_panel, text="Wszystkie przychodnie", width=20,
               command=self.controller.show_all_clinics_on_map).pack(pady=5)
        Button(control_panel, text="Wszyscy lekarze", width=20,
               command=self.controller.show_all_doctors_on_map).pack(pady=5)
        Button(control_panel, text="Wszyscy pacjenci", width=20,
               command=self.controller.show_all_patients_on_map).pack(pady=5)
        Button(control_panel, text="Wszyscy klienci", width=20,
               command=self.controller.show_all_clients_on_map).pack(pady=5)
        Button(control_panel, text="Wyczyść mapę", width=20,
               command=self.controller.clear_map).pack(pady=20)

        map_frame = Frame(frame)
        map_frame.pack(side="right", fill="both", expand=True)

        map_widget = TkinterMapView(map_frame, width=1200, height=700)
        map_widget.pack(fill="both", expand=True)
        map_widget.set_position(52.2297, 21.0122)
        map_widget.set_zoom(6)

        self.controller.map_widget = map_widget
        return frame

    def clear_map(self):
        self.map_widget.delete_all_marker()


def start_gui():
    root = Tk()
    root.title("System Zarządzania Przychodnią")
    root.geometry("1700x900")
    View(root)
    root.mainloop()
