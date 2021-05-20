#Andrea Reyes 20190265
#Katherine Garcia 20190418

#PROYECTO FINAL
#BIG M con ENTEROS

## ----------- BACKEND ----------------------
import numpy as np # manejo de matrices
import sys
import pandas as pd

# INPUT DATA
def inputFO(foX, foY, RestHtml):
  cantRest = int(RestHtml)
  ## TIPO DE PROBLEMA 
  pType = 'max'

  ## CANTIDAD DE VARIABLES Y RESTRICCIONES
  cantVars = 2

  ## VALORES FUNCION OBJETIVO
  objFunc = [0.0] * cantVars

  print("\n--  Función Objetivo: -- \n")
  objFunc[0] = float(foX) * -1
  objFunc[1] = float(foY) * -1

  ursVars = [0] * cantVars # variables unrstricted
  
  return cantVars, objFunc, pType, cantRest, ursVars


def createMatrix(xVals, yVals, desigualdad, results):
  matrix = np.zeros([cantRest+1, cantVars+2], dtype = float )
  desigual = []

  matrix[0][0] = 1 # rep de Z

  for i in range(1,cantVars+1): #FO to matrix
    matrix[0][i] = objFunc[i-1]

  for i in range(1, cantRest+1): # no fila 0
    matrix[i][1] = xVals[i-1] # var 1
    matrix[i][2] = yVals[i-1] # var 2
    matrix[i][3] = results[i-1] # results
    desigual.append(desigualdad[i-1])
  
  return matrix, desigualdad

# TRANSPUESTA
def transpuesta():
  global slackVarsP
  global cantVarsP
  global cantRestP

  global matTranspose
  global slackDual
  global cantVarsD
  global cantRestD
  global dType
  global desigualD
  global ursDual

  cantVarsP = len(matrixP[0]) -2
  cantRestP = len(matrixP) -1
  slackVarsP = 0

  for i in desigual:
    if i != '=':
      slackVarsP += 1

  matTranspose = matrixP.copy()
  matTranspose = np.delete(matTranspose, 0, 1)

  dType = "min"
  if pType == "min":
    dType = "max"

  normal = 1 # 1 si es normal, 0 no es normal

  if pType == "max":
    for i in desigual:
      if i != '<=': # si hay uno diferente ya no es normal
        normal = 0
        
  if pType == "min":
    for i in desigual:
      if i != '>=':
        normal = 0

  ursDual = [0] * cantRestP
  desigualD = []
  
  # Si es normal
  if normal == 1:

    if dType == "max":
      for i in range(cantVarsP):
        desigualD.append('<=')
    if dType == "min":
      for i in range(cantVarsP):
        desigualD.append('>=')
  
  # No es normal
  elif normal == 0:

    if pType == "max":
      for i in range(len(desigual)):
        if desigual[i] == ">=":
          matTranspose[i+1] = matTranspose[i+1] *-1            # multiplicamos la fila *-1

        elif desigual[i] == "=":
          ursDual[i] = 1                              # solo agreagamos un 1 las urs
          
        desigualD.append('>=')                     # si es >= o = en tranpuesta es >=

        if i < len(ursVars):
          if ursVars[i] == 1:                       # variable urs pasa como =
            desigualD.append('=')

    if pType == "min":
      for i in range(len(desigual)):
        if desigual[i] == "<=":
          matTranspose[i+1] = matTranspose[i+1] *-1            # multiplicamos la fila *-1

        elif desigual[i] == "=":
          ursDual[i] = 1                              # solo agreagamos un 1 las urs
          
        desigualD.append('<=')                     # si es >= o = en tranpuesta es >=

        if i < len(ursVars):
          if ursVars[i] == 1:                       # variable urs pasa como =
            desigualD.append('=')  

  while len(desigualD) > cantVarsP:
    desigualD.pop()
  
  while len(desigualD) < cantVarsP:
    if pType == 'max':
      desigualD.append('>=')
    elif pType == 'min':
      desigualD.append('<=')

  matTranspose = np.roll(matTranspose, -1, 0)
  matTranspose = matTranspose.T
  matTranspose = np.roll(matTranspose, 1, 0)

  matTranspose = np.insert(matTranspose, 0,0,1)
  matTranspose[0][0] = 1

  for i in range(len(matTranspose)): 
    matTranspose[i][-1] *= -1 #vector de resultados
  
  for i in range(1,len(matTranspose[0])-1): #ignora z y results
    matTranspose[0][i] *= -1 #FO *-1

  cantVarsD = cantRestP
  cantRestD = cantVarsP

  # print("Primal Matrix")
  # print(matrixP.round())
  # print(desigual)
  # print(ursVars)
  # print("Dual Matrix")
  # print(matTranspose)
  # print(desigualD)
  # print(ursDual)

  slackDual = 0
  for i in desigualD:
    if i != '=':
      slackDual = slackDual + 1
  print(slackDual)

# BIG M
def bigM(matrix, slackVars, cantVars, cantRest, mType, desigualdad, urs):
  for i in range(len(matrix)): # filas
    if matrix[i][-1] < 0:
      for j in range(1, len(matrix[0])+1): # columnas
        matrix[i][j] *= -1
      if desigualdad[i-1] == '<=': # i-1 para que empieze de 0
        desigualdad[i-1] = '>='
      elif desigualdad[i-1] == '>=': # i-1 para que empieze de 0
        desigualdad[i-1] = '<='
  
  for i in range(slackVars):
    matrix = np.insert(matrix,1+cantVars, 0, 1)
  
  # ---------------- DECLARAMOS M
  m = 10**10
  if mType == 'max':
    m = m *1
  elif mType == 'min':
    m = m *-1
  
  accion = 1
  columna = 1 + cantVars
  artifQ = 0
  artifIndex = []

  for i in range(1, len(matrix)):
    if desigualdad[i-1] == '<=':
      matrix[i][columna + accion -1] = 1

    elif desigualdad[i-1] == '>=':
      matrix[i][columna + accion -1] = -1

      matrix = np.insert(matrix, len(matrix[0])-1, 0, 1) # creamos var artif
      matrix[i][len(matrix[0])-2] = 1
      matrix[0][len(matrix[0])-2] = m

      artifIndex.append(i)
      artifQ += 1
    
    elif desigualdad[i-1] == '=':
      matrix = np.insert(matrix, len(matrix[0])-1, 0, 1) # creamos var artif
      matrix[i][len(matrix[0])-2] = 1
      matrix[0][len(matrix[0])-2] = m

      artifIndex.append(i)
      artifQ += 1
      accion -= 1
    accion += 1
  
  for i in range(len(urs)):
    if urs[i] == 1:
      matrix = np.insert(matrix, len(matrix[0])-1, 0,1)
      for j in range(len(matrix)):
        matrix[j][-2] = matrix[j][i+1] *-1
  
  for i in range(1,len(matrix[0])):
    for j in range(len(matrix)):
      if j in artifIndex:
        matrix[0][i] += (matrix[j][i] *m * -1)

  return matrix, mType, cantVars

# SIMPLEX
def getPivot():  
  if mType == 'min':
    indexCP = np.argmax(matrix[0][1:]) + 1
  if mType == "max":
    indexCP = np.argmin(matrix[0][1:]) + 1

  divi = float('inf')
  for i in range(1,len(matrix)):
    if (matrix[i][indexCP] > 0) and ((matrix[i][-1]/matrix[i][indexCP])< divi) and ((matrix[i][-1]/matrix[i][indexCP]) >= 0):
      divi = (matrix[i][-1]/matrix[i][indexCP])
      valorPivote = matrix[i][indexCP]
      indexFP = i

  if divi == float('inf'):
    sys.exit("No solution")

  return indexCP, indexFP, valorPivote

def simplex():
  matResults = matrix.copy()
  for i in range(1, len(matrix[indexFP])):
    matrix[indexFP][i] = matResults[indexFP][i] / valorPivote
  
  # OPERACIONES ENTE RENGLONES
  for i in range(len(matrix)):
    if i != indexFP:
      for j in range(len(matrix[0])):
        matrix[i][j] = matResults[i][j] - (matResults[i][indexCP] * matrix[indexFP][j])

def continueSimplex():
  continueS = False
  if mType == 'min':
    for i in matrix[0][1:len(matrix[0])-1]:
      if i > 0:
        continueS = True
  if mType == 'max':
    for i in matrix[0][1:len(matrix[0])-1]:
      if i < 0:
        continueS = True
  
  return continueS

# PARA ENTEROS
def maxValues():
  valoresX = []
  valoresY = []
  valores = []
  for i in matRest[1:]:
    for j in i[1:-1]:
      valores.append(j)
  
  vlasX=[]
  vlasY=[]

  for i in range(len(valores)):
    if i % 2 == 0:
      vlasX .append(int(valores[i]))
    if 1 % 2 != 0:
      vlasY.append(int(valores[i]))

  for i in range(1,len(matRest)):
    if matRest[i][1] != 0: # columna que rep x1
      xRes = matRest[i][-1] / matRest[i][1]  # resultado / valor columna y
      if xRes != float('inf'):
        valoresX.append(xRes)
    
    if matRest[i][2] != 0: # columna que rep a y1
      yRes = matRest[i][-1] / matRest[i][2]  # resultado / valor columna y
      if yRes != float('inf'):
        valoresY.append(yRes)
  
  if ">=" in desigualdad:
    xVals = max(valoresX)
    yVals = max(valoresY)
  else:
    xVals = min(valoresX)
    yVals = min(valoresY)
  
  return xVals, yVals

def puntos():
  pts = []
  for i in range(0, int(round(xVals)+1)): # valores x 
    for j in range(0, int(round(yVals)+1)): # valores y
      pts.append((i,j)) # append (x,y)
  return pts

def ptsReales():
  punts = pts.copy()

  for i in range(len(pts)):
    cant = 0
    for j in range(1,len(matRest)): #filas sin FO
      varX1 = pts[i][0] * matRest[j][1] 
      varX2 = pts[i][1] * matRest[j][2]
      cant = varX1 + varX2

      if desigualdad[j-1] == "<=":
        if cant > matRest[j][-1]:
          punts[i] = 0      
      
      if desigualdad[j-1] == ">=":
        if cant < matRest[j][-1]:
          punts[i] = 0

  p = []
  for i in punts:
    try:
      int(i)
    except:
      p.append(i)

  punts = p
  return punts

# RESULTADOS
def maximizacion(valores):
  valor = valores[0]
  pI = punts[0]

  for i in range(len(valores)):
    if valores[i] > valor:
      valor = valores[i]
      pI = punts[i]
  
  answer = str(valor)
  xy = pI
  print("---------- answer   ")
  print(answer)
  return answer, xy

def resultados(punts):
  resu = []
  for i in range(len(punts)):
    resuX = punts[i][0] * (matRest[0][1] *-1)
    resuY = punts[i][1] * (matRest[0][2] *-1)
    cantT = resuX + resuY
    resu.append(cantT)

  puntOpt, xy = maximizacion(resu)
  return puntOpt, xy



## ----------- FLASK - WEB ----------------------
from flask import Flask, render_template, request
app = Flask(__name__)

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
  
  cantVars, objFunc, pType, cantRest, ursVars = inputFO(foX, foY, RestHtml)
  print(foX, foY)

  Restricciones = [1]*int(cantRest)
  return render_template('data.html', Restricciones = Restricciones)


# renderizar a resultado
@app.route('/resultado', methods=['POST'])
def resultado():
  xValsHtml = request.form.getlist('xVals')
  yValsHtml = request.form.getlist('yVals')
  
  desigualdadHtml = request.form.getlist('desigualdad')
  results = request.form.getlist('results')

  global matrixP
  global desigual

  matrixP, desigual = createMatrix(xValsHtml, yValsHtml, desigualdadHtml, results)
  transpuesta()
  
  global matRest, desigualdad, matrix, mType, cantVars, valorPivote, indexFP, indexCP, matrixD, mTypeD, cantVarsD, valorPivoteD, indexFOD, indexCPD
  matRest = matrixP
  desigualdad = desigual

  matrix, mType, cantVars = bigM(matrixP, slackVarsP, cantVarsP, cantRestP, pType, desigual, ursVars)
  continueSimp = continueSimplex()
  
  while continueSimp == True:
    indexCP, indexFP, valorPivote = getPivot()

    simplex()
    continueSimp = continueSimplex()

  
  print("\nSOLUCION PRIMAL: ", matrix[0][-1], "\n") # ---------------------- BORRAR ----------------------

  matrixD, mTypeD, cantVarsD = bigM(matTranspose, slackDual, cantVarsD, cantRestD, dType, desigualD, ursDual)
  continueSimp = continueSimplex()

  while continueSimp == True:
    valorPivoteD, indexFOD, indexCPD = getPivot()

    simplex()
    continueSimp = continueSimplex()

  print("\nSOLUCION DUAL: ", matrix[0][-1]) # ---------------------- BORRAR ----------------------

  global xVals, yVals, pts, punts

  xVals, yVals = maxValues()
  pts = puntos()
  punts = ptsReales()
  resultadosP, xy = resultados(punts)

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

    matrix = matrix,
    matrixD = matrixD,
    sol = matrix[0][-1],

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