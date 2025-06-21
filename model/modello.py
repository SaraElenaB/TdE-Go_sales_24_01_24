import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):

        self._grafo = nx.DiGraph()
        self._nodes = []

        self._piloti = DAO.getAllPilots()
        self._mapIdPiloti = {}
        for p in self._piloti:
            self._mapIdPiloti[p.driverId] = p

        self.bestPath = []
        self.bestTassoSconfitta = 100000

    # --------------------------------------------------------------------------------------------------------------------------------------------
    def getAllAnni(self):
        return DAO.getAllAnni()

    def getIdMap(self):
        return self._mapIdPiloti

    # --------------------------------------------------------------------------------------------------------------------------------------------
    def buildGraph(self, anno):

        self._grafo.clear()
        self._nodes = DAO.getAllNodes(anno, self._mapIdPiloti)
        self._grafo.add_nodes_from(self._nodes)

        for tupla in DAO.getAllEdgesWeigh(anno, self._mapIdPiloti):
            d1 = tupla[0]
            d2 = tupla[1]
            peso = tupla[2]
            if d1 in self._nodes and d2 in self._nodes and peso > 0:
                self._grafo.add_edge(d1, d2, weight=peso)

        return self._grafo

    def getDetailsGraph(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    # --------------------------------------------------------------------------------------------------------------------------------------------
    def getBestScore(self):

        bestScore=0
        bestPilota = None

        for nodo in self._grafo.nodes():
            pesoVittorie = 0
            pesoSconfitte = 0

            for succ in self._grafo.successors(nodo):
                pesoVittorie += self._grafo[nodo][succ]["weight"]
            for pre in self._grafo.predecessors(nodo):
                pesoSconfitte += self._grafo[pre][nodo]["weight"]

            score = pesoVittorie - pesoSconfitte
            if score > bestScore:
                bestScore = score
                bestPilota = nodo.surname

        return bestPilota, bestScore

    # --------------------------------------------------------------------------------------------------------------------------------------------
    def getDreamTeam(self, numPiloti):

        self.bestPath = []
        self.bestTassoSconfitta = 100000
        parziale = []
        self._ricorsione(parziale, numPiloti)
        return self.bestPath, self.bestTassoSconfitta

        #ATTENZIONE --> con il metodo sotto ottieni delle permutazioni ("A","B" diverso da "B","A")
        #           --> fai delle combinazioni direttamente nella ricorsione
        # for node in self._nodes:
        #     parziale.append(node)
        #     self._ricorsione( parziale, numPiloti)
        #     parziale.pop()

    # --------------------------------------------------------------------------------------------------------------------------------------------
    def _ricorsione(self, parziale, numPiloti):

        #è ammissibile?
        if len(parziale) == numPiloti:
            #è la migliore?
            print(f"Testing team")
            tasso = self.calcolaTassoSconfitta(parziale)
            if tasso < self.bestTassoSconfitta:
                print(f"Soluzione migliore trovata")
                self.bestTassoSconfitta = tasso
                self.bestPath = copy.deepcopy(parziale)
            return

        else:
            #continua a cercare altre opzioni
            for node in self._nodes:
                if node not in parziale:
                    print(f"Ricorsione: {parziale}")
                    parziale.append(node)
                    self._ricorsione(parziale, numPiloti)
                    parziale.pop()

    # --------------------------------------------------------------------------------------------------------------------------------------------
    def calcolaTassoSconfitta(self, listaNodi):

        print("called funzione tasso")
        #2 --> archi
        tasso=0
        for edge in self._grafo.edges( data=True):
            if edge[0] not in listaNodi and edge[1] in listaNodi: #arco( noTeam-Team) = vittoria
                tasso += self._grafo[edge[2]]["weight"]
        return tasso

        #2 --> NODO
        # tasso=0
        # for n in self._nodes:
        #     for p in listaNodi:
        #         if n not in listaNodi:
        #             if self._grafo.has_edge(n, p):
        #                 tasso += self._grafo[n][p]["weight"] #arco escluso--team: vittoria
        # return tasso



    #modo 2:
    # def getScore(self, team):
    #     score = 0
    #     for e in self._graph.edges(data=True):
    #         if e[0] not in team and e[1] in team:
    #             score += e[2]["weight"]
    #     return score


if __name__ == "__main__":
    m = Model()
    mappa = m.getIdMap()
    m.buildGraph(1951)
    print( f"aaaa: {mappa.get(498)} ")
    print( m.getDetailsGraph() )
