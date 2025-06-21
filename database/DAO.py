from database.DB_connect import DBConnect
from model.pilot import Pilot


class DAO():

    @staticmethod
    def getAllAnni():

        cnx= DBConnect.get_connection()
        cursor = cnx.cursor( dictionary=True )
        ris=[]

        query=""" select `year`
                  from seasons 
                  order by `year` DESC """

        cursor.execute(query)
        for row in cursor:
            ris.append(row["year"])

        cursor.close()
        cnx.close()
        return ris

    @staticmethod
    def getAllPilots():

        cnx = DBConnect.get_connection()
        cursor = cnx.cursor( dictionary=True )
        ris = []

        query = """ select *
                    from drivers """

        cursor.execute(query)
        for row in cursor:
            ris.append( Pilot(**row))

        cursor.close()
        cnx.close()
        return ris

    @staticmethod
    def getAllNodes(anno, idMap):

        cnx = DBConnect.get_connection()
        cursor = cnx.cursor( dictionary=True )
        ris = []

        query = """ select distinct r.driverId
                    from results r , races r2 
                    where r.raceId = r2.raceId
                    and r.`position` > 0
                    and year(r2.`date`) = %s"""

        cursor.execute(query, (anno,))
        for row in cursor:
            #if "driverId" in idMap:
            ris.append( idMap[row["driverId"]] )

        cursor.close()
        cnx.close()
        return ris

    @staticmethod
    def getAllEdgesWeigh( anno, idMap):

        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        ris = []

        query = """ select r1.driverId as d1, r2.driverId as d2, count(*) as vittorie
                    from results r1, results r2, races ra
                    where r1.raceId = r2.raceId
                    and r1.raceId = ra.raceId
                    and ra.`year` = %s
                    and r1.`position` > 0
                    and r2.`position` > 0
                    and r1.`position` < r2.`position`
                    group by d1, d2"""

        cursor.execute(query, (anno,))
        for row in cursor:
            ris.append( ( idMap[row["d1"]],
                          idMap[row["d2"]],
                          row["vittorie"])  )

        cursor.close()
        cnx.close()
        return ris
