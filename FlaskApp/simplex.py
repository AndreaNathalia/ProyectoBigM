import numpy as np 
import sys 

def getPivot(mType, matrix):  
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

def simplex(matrix, indexFP, valorPivote, indexCP):
  matResults = matrix.copy()
  for i in range(1, len(matrix[indexFP])):
    matrix[indexFP][i] = matResults[indexFP][i] / valorPivote
  
  # OPERACIONES ENTE RENGLONES
  for i in range(len(matrix)):
    if i != indexFP:
      for j in range(len(matrix[0])):
        matrix[i][j] = matResults[i][j] - (matResults[i][indexCP] * matrix[indexFP][j])
  return matrix

def continueSimplex(mType, matrix):
  continueS = False
  if mType == 'min':
    for i in matrix[0][1:len(matrix[0])-1]:
      if i > 0:         # -- si es min ya no deben haber valores > 0
        continueS = True
  if mType == 'max':
    for i in matrix[0][1:len(matrix[0])-1]:
      if i < 0:         # -- si es max ya no deben haber valores < 0 
        continueS = True

  return continueS