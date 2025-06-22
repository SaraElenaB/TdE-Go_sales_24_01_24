import flet as ft
from UI.view import View
from database.DAO import DAO
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._metodoSelected=None

    #-------------------------------------------------------------------------------------------------------------------------------------
    def fillDDAnno(self):

        self._view.ddAnno.options.append( ft.dropdown.Option("2015") )
        self._view.ddAnno.options.append( ft.dropdown.Option("2016") )
        self._view.ddAnno.options.append( ft.dropdown.Option("2017") )
        self._view.ddAnno.options.append( ft.dropdown.Option("2018") )

    def fillDDMethod(self):

        metodoOrdinazione = DAO.getAllMetodiOrdinazione()
        for m in metodoOrdinazione:
            self._view.ddMetodo.options.append( ft.dropdown.Option( key= m.Order_method_type,
                                                                    data=m,
                                                                    on_click= self._readMetodoOrdinazione))

    def _readMetodoOrdinazione(self, e):
        self._metodoSelected = e.control.data

    # -------------------------------------------------------------------------------------------------------------------------------------
    def handle_graph(self, e):

        anno = self._view.ddAnno.value
        metodo = self._view.ddMetodo.value
        numeroS = self._view.txtInS.value

        if anno == "":
            self._view.txtOut.controls.clear()
            self._view.txtOut.controls.append( ft.Text(f"Attenzione, selezionare un anno per poter continuare!", color="red"))
            self._view.update_page()
            return

        if metodo == "":
            self._view.txtOut.controls.clear()
            self._view.txtOut.controls.append( ft.Text(f"Attenzione, selezionare un metodo per poter continuare!", color="red"))
            self._view.update_page()
            return

        if numeroS == "":
            self._view.txtOut.controls.clear()
            self._view.txtOut.controls.append( ft.Text(f"Attenzione, selezionare un numero per poter continuare!", color="red"))
            self._view.update_page()
            return

        try:
            numeroSFloat = float(numeroS)
        except ValueError:
            self._view.txtOut.controls.clear()
            self._view.txtOut.controls.append( ft.Text(f"Attenzione, selezionare un numero per poter continuare!", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph( int(anno), self._metodoSelected.Order_method_code , numeroSFloat)
        numNodi, numArchi = self._model.getDetailsGraph()
        self._view.txtOut.controls.clear()
        self._view.txtOut.controls.append( ft.Text(f"Grafo creato. \nCi sono {numNodi} vertici. \nCi sono {numArchi} archi."))
        self._view.update_page()

    # -------------------------------------------------------------------------------------------------------------------------------------
    def handleProdottiRedditizi(self, e):

        lista = self._model.getRedditizzi()
        self._view.txtOut.controls.append(ft.Text(f"I prodotti più redditizzi sono:"))
        for t in lista:
            self._view.txtOut.controls.append(
                ft.Text(f"Prodotto: {t[0]}      Archi Entranti = {t[1]}     Ricavo = {t[2]}"))

        self._view.update_page()

    # -------------------------------------------------------------------------------------------------------------------------------------
    def handle_path(self, e):

        bestPath = self._model.getCamminoOttimo()

        if len(bestPath) == 0:
            self._view.txtOut.controls.clear()
            self._view.txtOut.controls.append( ft.Text(f"Attenzione, non è stato trovato nessun cammino ottimo", color="red"))
            self._view.update_page()
            return

        self._view.txtOut.controls.clear()
        self._view.txtOut.controls.append(ft.Text(f"E' stato trovato un cammino ottimo con lunghezza massima {len(bestPath)} "))
        self._view.txtOut.controls.append( ft.Text(f"Di seguito i nodi che compongono il cammino"))
        for p in bestPath:
            self._view.txtOut.controls.append(ft.Text(f"Prodotto: {p[0]}        Ricavo: {p[1]} "))

        self._view.update_page()

    # -------------------------------------------------------------------------------------------------------------------------------------

