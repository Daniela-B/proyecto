from flask import Flask, render_template, request, json, redirect, url_for,flash
from flaskext.mysql import MySQL
import bcrypt
from json import dumps, loads, JSONEncoder, JSONDecoder

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['MYSQL_DATABASE_USER'] = 'sepherot_lorena'
app.config['MYSQL_DATABASE_PASSWORD'] = '9LwPFmj9QS'
app.config['MYSQL_DATABASE_DB'] = 'sepherot_lorenaBD'
app.config['MYSQL_DATABASE_HOST'] = 'sepheroth.com'

mysql = MySQL(app)
def validarUsuario(_email,_password):
    try:
        if _email and _password:
            print (_email,_password)
            conn=mysql.connect()
            cursor=conn.cursor()
            query="SELECT * FROM T_Usuarios WHERE Correo = %s"
            print (query)
            cursor.execute(query,(_email))
            data=cursor.fetchall()
            #print(data)
            if data:
                if data and data [0][4] == _password:
                    return True
                else:
                    return False
    except Exception as e:
        return e
    finally:
        cursor.close()
        conn.close()

def Errores(_user,_error,_errorInfo):
    try:
        conn=mysql.connect()
        cursor=conn.cursor()
        sql="INSERT INTO Entidad (User, Error, ErrorInfo) VALUES (%s,%s,%s)"
        query=cursor.execute(sql,(_user,_error,_errorInfo))
        conn.commit()
        if query:
            return True
        else:
            return False
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        conn.close()
        cursor.close()

def buscarU(_user):
    if _user:
        conn=mysql.connect()
        cursor=conn.cursor()
        query="SELECT * FROM T_Usuarios WHERE Correo = %s"
        try:
            cursor.execute(query,(_user))
            data=cursor.fetchall()
            if data:
                return data['Correo']
            else:
                return False
        except Exception as e:
            print (str(e))
            return e
            json.dumps({'erroooooooor':str(e)})
        finally:
            cursor.close()
            conn.close()

def SelectAll():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        _TABLA = "T_Usuarios"
        sqlSelectAllProcedure = "SELECT * FROM " + _TABLA
        cursor.execute(sqlSelectAllProcedure)
        data = cursor.fetchall()
        if data:
            return data
        else:
            return False
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

def InsertE(_p1,_p2,_p3,_p4,_p5,_p6,_cal):
    try:
        if _p1 and _p2:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Encuesta (ID_Tipo_Enc,P1, P2, P3, P4, P5, P6, Estatus, Calificación) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)", ('1',_p1, _p2, _p3, _p4, _p5, _p6,'0',_cal))
            conn.commit()
        return "success"
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

def SelectVer():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        _TABLA = "Encuesta"
        sqlSelectAllProcedure = "SELECT * FROM " + _TABLA+ " WHERE Estatus = 0"
        cursor.execute(sqlSelectAllProcedure)
        data = cursor.fetchall()
        #print (data)
        return data
        
    except Exception as e:
          print (str(e))
          return e
    finally:
        cursor.close()
        conn.close()

def SelectUpdate(_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        _TABLA = "Encuesta"
        sqlSelectAllProcedure = "SELECT * FROM " + _TABLA+ " WHERE ID_Encuesta = "+_id
        cursor.execute(sqlSelectAllProcedure)
        data = cursor.fetchall() 
        #print (data)
        return data
    except Exception as e:
         return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

def SelectReporte():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        _TABLA = "Encuesta"
        sqlSelectAllProcedure = "SELECT * FROM `Encuesta` WHERE Estatus = 0 "
        cursor.execute(sqlSelectAllProcedure)
        data = cursor.fetchall()
        return data
    except Exception as e:
        print (str(e))
        return e
    finally:
        cursor.close()
        conn.close()
    
def UpdateCal(_id,_cn):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlUpdateCal = "UPDATE Encuesta SET Calificación = {} WHERE ID_Encuesta = {}".format(_cn,_id)
        cursor.execute(sqlUpdateCal)
        conn.commit()
        data = cursor.fetchall()
        return data
    except Exception as e:
        print (str(e))
        return e
    finally:
        cursor.close()
        conn.close()

def UpdateCh(_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlUpdateCal = "UPDATE Encuesta SET Estatus = 1 WHERE ID_Encuesta = {0}".format(_id)
        cursor.execute(sqlUpdateCal)
        conn.commit()
        flash ('Encuesta Cargada')
        data = cursor.fetchall()
        return data
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

def Ch1():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlCh1 = "SELECT COUNT(*) FROM Encuesta WHERE Estatus=1"
        cursor.execute(sqlCh1)
        conn.commit()
        data = cursor.fetchone()
        return data
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()
    
def Ch0():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlCh1 = "SELECT COUNT(*) FROM Encuesta WHERE Estatus=0"
        cursor.execute(sqlCh1)
        conn.commit()
        data = cursor.fetchone()
        return data
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

def ChT():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sqlCh1 = "SELECT COUNT(*) FROM Encuesta"
        cursor.execute(sqlCh1)
        conn.commit()
        data = cursor.fetchone()
        return data
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()
