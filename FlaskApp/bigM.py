import numpy as np 

# BIG M
def bigM(matrix, slackVars, cantVars, cantRest, mType, desigualdad, urs):
  
  # MODIFY CONTRAINTS
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
  
  contSt = 1 # -- CANT SLACK
  columna = 1 + cantVars
  artifQ = 0
  artifIndex = []

  # -- SE AGREGAN VARIABLES DE EXCESO, HOLGURA Y ARTIFICIALES   

  for i in range(1, len(matrix)):
    if desigualdad[i-1] == '<=':
      matrix[i][columna + contSt -1] = 1 #si es < se agrega var de holgura

    elif desigualdad[i-1] == '>=':
      matrix[i][columna + contSt -1] = -1 # si es > se agrega var de exceso

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
      contSt -= 1
    contSt += 1

  # -- URS VARS
  for i in range(len(urs)):
    if urs[i] == 1:
      matrix = np.insert(matrix, len(matrix[0])-1, 0,1)
      for j in range(len(matrix)):
        matrix[j][-2] = matrix[j][i+1] *-1
  
  # -- OPERACIONES PARA ELIMINAR M
  for i in range(1,len(matrix[0])):
    for j in range(len(matrix)):
      if j in artifIndex:
        matrix[0][i] += (matrix[j][i] *m * -1)

  return matrix, mType, cantVars, desigualdad