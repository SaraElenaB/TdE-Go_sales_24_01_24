from database.DB_connect import DBConnect
from model.metodo import Metodo
from model.prodotto import Prodotto


class DAO():

    @staticmethod
    def getAllMetodiOrdinazione():

        cnx= DBConnect.get_connection()
        cursor = cnx.cursor( dictionary=True )
        ris=[]

        query="""select distinct *
                 from go_methods gm """

        cursor.execute(query)
        for row in cursor:
            ris.append( Metodo(**row))

        cursor.close()
        cnx.close()
        return ris

    # -------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getAllProdotti():

        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        ris = []

        query = """select *
                    from go_products gp  """

        cursor.execute(query)
        for row in cursor:
            ris.append(Prodotto(**row))

        cursor.close()
        cnx.close()
        return ris

    # -------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getAllNodes(anno, metodoCode, mappa):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        ris = []

        query = """select gp.Product_number, sum(gds.Unit_sale_price * gds.Quantity) as RicavoTotale
                   from go_products gp , go_daily_sales gds 
                   where gp.Product_number = gds.Product_number
                   and year(gds.`Date`) = %s
                   and gds.Order_method_code = %s
                   group by gp.Product_number"""
                    #non puoi usare distinct, quindi group by e poi metti nel select

        cursor.execute(query, (anno, metodoCode))
        for row in cursor:
            prodotto = mappa[row['Product_number']]
            ris.append(prodotto)
            prodotto.RicavoTotale = row["RicavoTotale"]

        cursor.close()
        cnx.close()
        return ris

    # -------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getRicavoTotalePerProdotto( pNum, anno, metodoCode):

        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        ris = []

        query = """ select sum(gds.Unit_sale_price * gds.Quantity) as ricavoTot
                    from go_daily_sales gds 
                    where gds.Product_number = %s
                    and year(gds.`Date`) = %s
                    and gds.Order_method_code = %s """

        cursor.execute(query, (pNum, anno, metodoCode))
        for row in cursor:
            ris.append( row["ricavoTot"])

        cursor.close()
        cnx.close()

        #capire come comportarsi nei casi in cui non hai ricavo
        return ris
    #-------------------------------------------------------------------------------------------------------------------------------------