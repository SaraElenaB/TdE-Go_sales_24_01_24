import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None


    def load_interface(self):
        # title
        self._title = ft.Text("TdP 2024 - Esame 24/1/24", color="purple", size=24)
        self._page.controls.append(self._title)

        #ROW with some controls
        self.ddAnno = ft.Dropdown(label="Anno", width=300)
        self._controller.fillDDAnno()
        self.btn_graph = ft.ElevatedButton(text="Crea Grafo", width=200, on_click=self._controller.handle_graph)
        row1= ft.Row([self.ddAnno, self.btn_graph], alignment=ft.MainAxisAlignment.CENTER)

        self.ddMetodo = ft.Dropdown(label="Metodo", width=300)
        self._controller.fillDDMethod()
        self.btnProdottiRedditizi = ft.ElevatedButton(text="Prodotto Redditizi", width=200, on_click=self._controller.handleProdottiRedditizi)
        row2 = ft.Row([self.ddMetodo, self.btnProdottiRedditizi], alignment=ft.MainAxisAlignment.CENTER)

        self.txtInS = ft.TextField(label="S", width=300)
        self.btnCammino = ft.ElevatedButton(text="Calcola Cammino", width=200, on_click=self._controller.handle_path)
        row3 = ft.Row([self.txtInS, self.btnCammino], alignment=ft.MainAxisAlignment.CENTER)

        self._page.add(row1,row2,row3)

        self.txtOut = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txtOut)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()