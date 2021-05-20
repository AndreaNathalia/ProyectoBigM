import numpy as np 

# INPUT DATA
def inputFO(foX, foY, RestHtml):
  cantRest = int(RestHtml)
  ## TIPO DE PROBLEMA 
  pType = 'max'

  ## CANTIDAD DE VARIABLES Y RESTRICCIONES
  cantVars = 2

  ## VALORES FUNCION OBJETIVO
  objFunc = [0.0] * cantVars

  objFunc[0] = float(foX) * -1
  objFunc[1] = float(foY) * -1

  ursVars = [0] * cantVars # variables unrstricted
  
  return cantVars, objFunc, pType, cantRest, ursVars

def createMatrix(xVals, yVals, desigualdad, results, cantVars, objFunc, cantRest):
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

