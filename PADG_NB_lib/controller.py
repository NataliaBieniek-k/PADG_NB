from PADG_NB_lib.model import User
import psycopg2

class Controller:
    def __init__(self, view, map_widget):
        self.view = view
        self.map_widget = map_widget
        self.users = []

    def add_user(self):
        db_engine = psycopg2.connect(
            user="postgres",
            database="postgres",
            password="postgres",
            port="5432",
            host="localhost"
        )
        cursor = db_engine.cursor()

        name = self.view.entry_name.get()
        location = self.view.entry_lokalizacja.get()
        posts = int(self.view.entry_posty.get())
        img_url = self.view.entry_img_url.get()

        user = User(name, location, posts, img_url, self.map_widget)
        self.users.append(user)

        SQL = f"INSERT INTO public.users(name, location, posts, img_url, geometry) VALUES ('{name}', '{location}', {posts}, '{img_url}', 'SRID=4326;POINT({user.coords[0]} {user.coords[1]})');"

        self.user_info()

        self.view.entry_name.delete(0, "end")
        self.view.entry_lokalizacja.delete(0, "end")
        self.view.entry_posty.delete(0, "end")
        self.view.entry_img_url.delete(0, "end")
        self.view.entry_name.focus()

        cursor.execute(SQL)
        db_engine.commit()

    def user_info(self):
        self.view.list_box_lista_obiektow.delete(0, "end")
        for idx, user in enumerate(self.users):
            self.view.list_box_lista_obiektow.insert(
                idx, f"{user.name} {user.location} {user.posts} posty"
            )

    def delete_user(self):
        i = self.view.list_box_lista_obiektow.index("active")
        self.users[i].marker.delete()
        self.users.pop(i)
        self.user_info()

    def user_details(self):
        i = self.view.list_box_lista_obiektow.index("active")

        self.view.label_imie_szczegoly_obiektu_wartosc.config(text=self.users[i].name)
        self.view.label_lokalizacja_szczegoly_obiektu_wartosc.config(text=self.users[i].location)
        self.view.label_posty_szczegoly_obiektu_wartosc.config(text=self.users[i].posts)

        self.map_widget.set_position(
            self.users[i].coords[0],
            self.users[i].coords[1]
        )
        self.map_widget.set_zoom(14)

    def edit_user(self):
        i = self.view.list_box_lista_obiektow.index("active")

        self.view.entry_name.insert(0, self.users[i].name)
        self.view.entry_lokalizacja.insert(0, self.users[i].location)
        self.view.entry_posty.insert(0, self.users[i].posts)
        self.view.entry_img_url.insert(0, self.users[i].img_url)

        self.view.button_dodaj_obiekt.config(
            text="Zapisz zmiany",
            command=lambda: self.update_user(i)
        )

    def update_user(self, i):
        self.users[i].name = self.view.entry_name.get()
        self.users[i].location = self.view.entry_lokalizacja.get()
        self.users[i].posts = self.view.entry_posty.get()
        self.users[i].img_url = self.view.entry_img_url.get()
        self.users[i].coords = self.users[i].get_coordinates()

        self.users[i].marker.set_position(
            self.users[i].coords[0],
            self.users[i].coords[1]
        )
        self.users[i].marker.set_text(text=self.users[i].name)

        self.user_info()

        self.view.button_dodaj_obiekt.config(
            text="Dodaj obiekt",
            command=self.add_user
        )

        self.view.entry_name.delete(0, "end")
        self.view.entry_lokalizacja.delete(0, "end")
        self.view.entry_posty.delete(0, "end")
        self.view.entry_img_url.delete(0, "end")
        self.view.entry_name.focus()
