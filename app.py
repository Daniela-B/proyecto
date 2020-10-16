from flask import Flask, render_template, request, g, redirect, session, url_for,json,send_from_directory
import time
import re
import jinja2
from json import dumps, loads, JSONEncoder, JSONDecoder

import modelo as modelo

app = Flask(__name__)
app.secret_key='super secret key'
app.config['SESSION_TYPE']='filesystem'
@app.before_request
def before_request():
    g.user = None   
    if 'user' in session:
        g.user = modelo.buscarU(session['user'])

@app.route('/',methods=['GET','POST'])
def r():
    if g.user:
        return redirect(url_for('inicio'))
    if request.method=='POST': 
        session.pop('user',None)
        _user=request.form['email']
        _password=request.form['password']
        if (_user and _password):
            usuario=modelo.validarUsuario(_user,_password)
            if usuario == True:
                session['user']=_user
                modelo.Errores(_user,'Login','Se logra el login')
                return redirect(url_for('inicio'))
            else:
                modelo.Errores(_user,'Login.Fail','Datos erroneos')
                return render_template('login.html')
    return render_template('login.html')

@app.route('/cerrar')
def cerrar():
    session.clear()
    return redirect(url_for('r'))

@app.route('/inicio')
def inicio():
    return render_template("inicio.html")

@app.route('/encuesta',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        r = []
        contador = 0
        _p1 = request.form.get('1')
        _p2 = request.form.get('2')
        _p3 = request.form.get('3')
        _p4 = request.form.get('4')
        _p5 = request.form.get('5')
        _p6 = request.form.get('o')
        r.append(_p1)
        r.append(_p2)
        r.append(_p3)
        r.append(_p4)
        r.append(_p5)
        r.append(_p6)
        for cal in r:
            if cal == "Bien":
                contador += 1
                if cal == "Regular":
                    contador += .5
        consulta = modelo.InsertE(_p1,_p2,_p3,_p4,_p5,_p6,contador)
        if consulta:
            return("<h1>Gracias; Tu opinion es muy importante para nosotros</h1>")
        return ("<h2>Error al ingresar tus respuestas</h2>")
    return render_template("encuesta.html")

@app.route('/qr')
def codqr():
    return render_template('codigo.html')

@app.route('/lista')
def lista():
    if "user" in session:
        user = session['user']
        consulta=modelo.SelectVer()
        if consulta:
            modelo.Errores(user,'Lista.Success','Se logró ver la lista')
            return render_template('ver.html',encuestas=consulta)
        else:
            modelo.Errores(user,'Lista.Fail','No se logró ver la lista')
            return redirect(url_for('inicio'))
        return render_template('inicio.html')

@app.route('/edit/<string:id>')
def edit_cal(id):
        consulta=modelo.SelectUpdate(id)
        return render_template('edicion.html',datos=consulta[0])
       

@app.route('/update/<string:id>', methods=['POST'])
def update_cal(id):
    if request.method =='POST':
        cn = request.form['P7']
        if int(cn) < 10 and int(cn)> 0:
            modelo.UpdateCal(id,cn)
            return redirect(url_for("inicio"))
        return "El valor tiene que ser entre 1 y 10"
    return redirect(url_for(("lista")))

@app.route('/cargar/<string:id>')
def update_ch(id):
        consulta=modelo.UpdateCh(id)
        return render_template('inicio.html')


@app.route('/reporte')
def reportes():
    revisados = modelo.Ch1()
    nrevisados = modelo.Ch0()
    total =modelo.ChT()
    print (revisados)
    print (nrevisados)
    print (total)
    return render_template("reportes.html", revisado = revisados,norevisado = nrevisados, total = total)

if __name__ == '__main__':
    app.run(debug=True)