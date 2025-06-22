import copy
import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):

        self._grafo = nx.DiGraph()
        self._nodes= []

        self._idMapProdotti = {}
        self._prodotto = DAO.getAllProdotti()
        for p in self._prodotto:
            self._idMapProdotti[p.Product_number]=p

        self._mapProdottoRicavo={}

        self._bestPath = []

    # -------------------------------------------------------------------------------------------------------------------------------------
    def getIdMapProdotti(self):
        return self._idMapProdotti

    def buildGraph(self, anno, metodoCode, numeroSFloat):

        self._grafo.clear()
        self._nodes = DAO.getAllNodes(anno, metodoCode, self._idMapProdotti)
        self._grafo.add_nodes_from(self._nodes)

        #METODO 1: crea attributo
        for p1 in self._nodes:
            for p2 in self._nodes:
                if p1 != p2:
                    add = float(1+numeroSFloat)
                    if float(p2.RicavoTotale) >= float(p1.RicavoTotale)*add:
                        self._grafo.add_edge(p1, p2)
                    elif float(p1.RicavoTotale) >= float(p2.RicavoTotale)*add:
                        self._grafo.add_edge(p2, p1)
        return self._grafo

        #METODO 2: LUNGO MA FUNZIONA
        # for p1 in self._nodes:
        #     for p2 in self._nodes:
        #         if p1 != p2:
        #
        # #for p1, p2 in itertools.combinations(self._nodes, 2):
        #             ricavoP1 = DAO.getRicavoTotalePerProdotto(p1.Product_number, anno, metodoCode) #ATTENZIONE!!!!!!!!
        #             ricavoP2 = DAO.getRicavoTotalePerProdotto(p2.Product_number, anno, metodoCode)
        #             self._mapProdottoRicavo[p1.Product_number]= ricavoP1
        #             self._mapProdottoRicavo[p2.Product_number] = ricavoP2
        #
        #             #if ricavoP1 is not None and ricavoP2 is not None and len(ricavoP1)>0 and len(ricavoP2)>0:
        #             add = float((1 + numeroSFloat))
        #             if float(ricavoP2[0]) >= float(ricavoP1[0])*add:
        #                 self._grafo.add_edge(p1, p2)
        #             elif float(ricavoP1[0]) >= float(ricavoP2[0])*add:
        #                 self._grafo.add_edge(p2, p1)

    def getDetailsGraph(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    # -------------------------------------------------------------------------------------------------------------------------------------
    def getRedditizzi(self):

        lista = [] #[ (p1, numEntranti)] --> imposto numUscente=0
        nodiGiaVisti=[]

        for n in self._nodes:
            if n not in nodiGiaVisti:
                nodiGiaVisti.append(n)
                numUscenti = 0
                for succ in  self._grafo.successors(n):
                    numUscenti += 1
                    if numUscenti > 0:
                        break
                numEntranti = 0
                for pre in self._grafo.predecessors(n):
                    numEntranti +=1
                lista.append( (n, numEntranti, n.RicavoTotale) )
            else:
                continue

        lista.sort( key=lambda x: x[1], reverse=True)
        return lista[:5]

    # -------------------------------------------------------------------------------------------------------------------------------------
    #punto 2
    def getCamminoOttimo(self):

        self._bestPath = [] #lista di nodi
        parziale=[]

        setNodesWithNoPredecessors = set()
        setNodesWithNoSuccessor = set()

        for n in self._nodes:
            if len(list(self._grafo.predecessors(n))) == 0:
                setNodesWithNoPredecessors.add(n)

        for n in self._nodes:
            if len(list(self._grafo.successors(n))) == 0:
                setNodesWithNoSuccessor.add(n)

        for n in setNodesWithNoPredecessors:
            parziale.append(n)
            print(f"Inizio con nodo: {n}")
            self._ricorsione(parziale, setNodesWithNoSuccessor)
            parziale.pop()

        ris = []
        if len(self._bestPath) > 0:
            for p in self._bestPath:
                ris.append( (p, p.RicavoTotale) )

        return ris #altrimenti fai un mappa {prodotto: ricavo}

    # -------------------------------------------------------------------------------------------------------------------------------------
    def _ricorsione(self, parziale, setNodesWithNoSuccessor):

        #ammissibile? --> quindi controllo l'ultimo se va bene
        if parziale[-1] in setNodesWithNoSuccessor:
            if len(parziale) > len(self._bestPath): #archi = nodi-1, ma tanto sia parziale che bestPath sono nodi, quindi basta che la lunghezza nodi >, allora lunghezza archi >
                print("Nuova soluzione migliore trovata! ")
                self._bestPath = copy.deepcopy(parziale)
            return #serve per risalire quando trovi una soluzione ottima
        ultimo= parziale[-1]
        #vincolo solo adiacenti
        for succ in self._grafo.successors(ultimo):
            print( f"Ricorsione: {parziale}")
            parziale.append(succ)
            self._ricorsione(parziale, setNodesWithNoSuccessor)
            parziale.pop()

    # -------------------------------------------------------------------------------------------------------------------------------------
    def hasArchiUscenti(self, nodo):

        print("Called function x ultimo nodo")
        numUscenti = 0
        for succ in self._grafo.successors(nodo):
            numUscenti += 1
        if numUscenti > 0:
            return True

    def hasArchiEntranti(self, nodo):

        numEntranti = 0
        for pre in self._grafo.predecessors(nodo):
            numEntranti += 1
        if numEntranti > 0:
            return True
    #-------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    m = Model()
    mappa = m.getIdMapProdotti()
    print(mappa)
    m.buildGraph(2017, 3, 0.57)
    print( m.getDetailsGraph())
    print( m.getRedditizzi())
    print(m.getCamminoOttimo())