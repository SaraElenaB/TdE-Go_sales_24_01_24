import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    #--------------------------------------------------------------------------------------------------------------------------------------------
    def fillDDYear(self):

        anni = self._model.getAllAnni()
        for a in anni:
            self._view._ddAnno.options.append( ft.dropdown.Option(a) )

    # --------------------------------------------------------------------------------------------------------------------------------------------
    def handleCreaGrafo(self,e):

        anno = self._view._ddAnno.value

        if anno == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append( ft.Text(f"Attenzione, inserire un anno per continuare!"))
            self._view.update_page()
            return

        self._model.buildGraph(anno)
        numNodi, numArchi = self._model.getDetailsGraph()
        bestPilota, bestScore = self._model.getBestScore()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato: "))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {numNodi} \nNumero di archi: {numArchi}"))
        self._view.txt_result.controls.append(ft.Text(f"Best driver: {bestPilota} with score: {bestScore} "))
        self._view.update_page()

    # --------------------------------------------------------------------------------------------------------------------------------------------
    def handleCerca(self, e):

        numPiloti = self._view._txtIntK.value

        if numPiloti == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append( ft.Text(f"Attenzione, inserire un numero min di piloti per continuare!"))
            self._view.update_page()
            return

        try:
            numPilotiInt = int(numPiloti)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append( ft.Text(f"Attenzione, inserire un numero intero per continuare!"))
            self._view.update_page()
            return

        bestPath, bestScore = self._model.getDreamTeam(numPiloti)
        self._view.txt_result.controls.append(ft.Text(f"Dream Team trovato!"))
        self._view.txt_result.controls.append(ft.Text(f"Dream Team composto da: {numPilotiInt} ha tasso di sconfitta: {bestScore}"))
        for p in bestPath:
            self._view.txt_result.controls.append( ft.Text(p))

        self._view.update_page()
    # --------------------------------------------------------------------------------------------------------------------------------------------

