import numpy as np 

def normalP(pType, desigual):
  normal = 1 # 1 si es normal, 0 no es normal
  if pType == "max":
    for i in desigual:
      if i != '<=': # si hay uno diferente ya no es normal
        normal = 0
        
  if pType == "min":
    for i in desigual:
      if i != '>=':
        normal = 0

  return normal

# slackVarsP = None
# TRANSPUESTA
def transpuesta(matrixP, desigual, pType, ursVars):
  # Variables globales de Primal
#   global slackVarsP
#   global cantVarsP
#   global cantRestP

#   # Variables globales de DUAL
#   global matTranspose
#   global slackDual
#   global cantVarsD
#   global cantRestD
#   global dType
#   global desigualD
#   global ursDual

  cantVarsP = len(matrixP[0]) -2
  cantRestP = len(matrixP) -1
  slackVarsP = 0

  # Variables de exceso y holgura de PRIMAL
  for i in desigual:
    if i != '=':
      slackVarsP += 1

  matTranspose = matrixP.copy()
  matTranspose = np.delete(matTranspose, 0, 1)
  
  # tipo de problema para DUAL
  dType = ""

  if pType == "max":
    dType = "min"
  if pType == "min":
    dType = "max"

  normal = normalP(pType, desigual)

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
  
  # -- Transpuesta de la matriz
  matTranspose = np.roll(matTranspose, -1, 0)
  matTranspose = matTranspose.T
  matTranspose = np.roll(matTranspose, 1, 0)
  
  # -- fila Z
  matTranspose = np.insert(matTranspose, 0,0,1)
  matTranspose[0][0] = 1

  # -- multiplicamos * -1
  for i in range(len(matTranspose)): 
    matTranspose[i][-1] *= -1 #vector de resultados
  
  for i in range(1,len(matTranspose[0])-1): #ignora z y results
    matTranspose[0][i] *= -1 #FO *-1

  cantVarsD = cantRestP
  cantRestD = cantVarsP

  # Variables de exceso y holgura de PRIMAL
  slackDual = 0
  for i in desigualD:
    if i != '=':
      slackDual = slackDual + 1

  return slackVarsP, cantVarsP, cantRestP, matTranspose, slackDual, cantVarsD, cantRestD, dType, desigualD, ursDual