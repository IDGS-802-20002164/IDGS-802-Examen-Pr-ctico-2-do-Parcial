from .dbs import get_connection


class getAllTabla:
    def getall():
        try:
            connection  = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call getAll()')
                resutset = cursor.fetchall()
                cursor.close()
                
        except Exception as ex:
            print(ex)
        
        return resutset

class getAllName:
    def getallName(id):
        try:
            connection  = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call searchItem(%s)',(id,))
                resutset = cursor.fetchall()
                cursor.close()
                
        except Exception as ex:
            print(ex)
        
        return resutset

class buy:
    def buyG(id):
        try:
            connection  = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call buyGame(%s)',(id,))
                resutset = cursor.fetchall()
                cursor.close()
                
        except Exception as ex:
            print(ex)
        
        return resutset


class insertJuego:
    def insertjuego(name,description,img,unidades):
        try:
            connection  = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call insertGame(%s,%s,%s,%s)',(name,description,img,unidades))
            connection.commit()
            connection.close()
        except Exception as ex:
            print(ex)


