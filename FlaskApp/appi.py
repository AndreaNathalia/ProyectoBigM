from flask import Flask, render_template, request
import numpy as np 
import inputData as inp
import transpuesta as tp
import bigM as bM
import simplex as sp
import enteros as ent
import resultados as rs

app = Flask(__name__)

cantVars = 0 
cantRest = 0 
cantVarsD = 0
valorPivote = 0
indexFP = 0
indexCP = 0
valorPivoteD = 0
indexFOD = 0
indexCPD = 0

objFunc = [] 
ursVars = [] 
desigualdad = [] 
desigual = []
xVals = [] 
yVals = [] 
pts = [] 
punts = [] 

pType = ""
mType = ""
mTypeD = ""

# matRest = np.empty
# matrix = np.empty
# matrixD = np.empty
# matrixP = np.empty


# renderizar a index (input de FO)
@app.route('/')
def index():
  return render_template('index.html', Restricciones = [])

# renderizar a data (input de coeficientes de las restricciones)
@app.route('/data', methods=['POST'])
def data():
  foX = request.form['foX']
  foY = request.form['foY']
  RestHtml = request.form['cantRest']

  global cantVars, objFunc, pType, cantRest, ursVars

  cantVars = inp.inputFO(foX, foY, RestHtml)[0]
  objFunc = inp.inputFO(foX, foY, RestHtml)[1]
  pType = inp.inputFO(foX, foY, RestHtml)[2]
  cantRest = inp.inputFO(foX, foY, RestHtml)[3]
  ursVars = inp.inputFO(foX, foY, RestHtml)[4]

  Restricciones = [1]*int(cantRest)
  return render_template('data.html', Restricciones = Restricciones)


# renderizar a resultado
@app.route('/resultado', methods=['POST'])
def resultado():
  xValsHtml = request.form.getlist('xVals')
  yValsHtml = request.form.getlist('yVals')
  
  desigualdadHtml = request.form.getlist('desigualdad')
  results = request.form.getlist('results')

  global cantVars
  global desigual
  global desigualdad, mType, valorPivote, indexFP, indexCP
  global mTypeD, cantVarsD, valorPivoteD, indexFOD, indexCPD

  matrixP, desigual = inp.createMatrix(xValsHtml, yValsHtml, desigualdadHtml, results, cantVars, objFunc, cantRest)
  slackVarsP, cantVarsP, cantRestP, matTranspose, slackDual, cantVarsD, cantRestD, dType, desigualD, ursDual = tp.transpuesta(matrixP, desigual, pType, ursVars)

  matRest = matrixP
  desigualdad = desigual

  matrixP, mType, cantVars, desigual = bM.bigM(matrixP, slackVarsP, cantVarsP, cantRestP, pType, desigual, ursVars)
  continueSimp = sp.continueSimplex(mType, matrixP)
  
  while continueSimp == True:
    indexCP, indexFP, valorPivote = sp.getPivot(mType, matrixP)

    matrixP = sp.simplex(matrixP, indexFP, valorPivote, indexCP)
    continueSimp = sp.continueSimplex(mType, matrixP)
  
  print("\nSOLUCION PRIMAL: ", matrixP[0][-1], "\n") 

  matrixD, mTypeD, cantVarsD, desigualD = bM.bigM(matTranspose, slackDual, cantVarsD, cantRestD, dType, desigualD, ursDual)
  continueSimp = sp.continueSimplex(mTypeD, matrixD)


  while continueSimp == True:
    indexCPD, indexFOD, valorPivoteD   = sp.getPivot(mTypeD, matrixD)

    matrixD = sp.simplex(matrixD, indexFOD, valorPivoteD, indexCPD)
    continueSimp = sp.continueSimplex(mTypeD, matrixD)

  print("\nSOLUCION DUAL: ", matrixD[0][-1]) 

  global xVals, yVals, pts, punts

  xVals, yVals = ent.maxValues(matRest, desigualdad)

  pts = ent.puntos(xVals, yVals)
  
  punts = ent.ptsReales(pts, matRest, desigualdad)
  
  resultadosP, xy = rs.resultados(punts, matRest)

  print("\nresultss: ") #--------------- BORRAR ----------------------------
  print(resultadosP)
  
  return render_template('resultado.html',
    cantVarsP = cantVarsP,
    cantRestP = cantRestP,
    pType = pType,
    desigual = desigual,
    matrixP = matrixP,

    cantVarsD = cantVarsD,
    cantRestD = cantRestD,
    dType = dType,
    desigualD = desigualD,
    matTranspose = matTranspose,

    matrix = matrixP,
    matrixD = matrixD,
    sol = matrixP[0][-1],

    xVals = xy[0],
    yVals = xy[1],
    resultadosP = resultadosP
  )


##---- RUTAS PARA VER LAS PÁGINAS
@app.route('/data')
def test():
  return render_template('data.html')

@app.route('/resultado')
def testR():
  return render_template('resultado.html')

 
if __name__ == "__main__":
  app.run()