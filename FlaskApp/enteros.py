def maxValues(matRest, desigualdad):
  # valores mas grandes de X & Y
  valoresX = []
  valoresY = []

  valores = []

  # -- apend de filas sin z ni vector de resultados
  for i in matRest[1:]: # -- no FO
    for j in i[1:-1]: # -- no Z ni results
      valores.append(j)
  
  vlasX=[]
  vlasY=[]

  # -- append de quienes tengan un residuo 0
  for i in range(len(valores)):
    if i % 2 == 0:
      vlasX .append(int(valores[i]))
    if 1 % 2 != 0:
      vlasY.append(int(valores[i]))

  # -- append de quienes no sean inf
  for i in range(1,len(matRest)):
    if matRest[i][1] != 0: # columna que rep x1
      xRes = matRest[i][-1] / matRest[i][1]  # resultado / valor columna x
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

def puntos(xVals, yVals): # -- puntos posibles 
  pts = []
  for i in range(0, int(round(xVals)+1)): # valores x 
    for j in range(0, int(round(yVals)+1)): # valores y
      pts.append((i,j)) # append (x,y)
  return pts

def ptsReales(pts, matRest, desigualdad): # -- putnos dentro 
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