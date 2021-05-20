def maximizacion(valores, punts):
  valor = valores[0]
  pO = punts[0]

  for i in range(len(valores)):
    if valores[i] > valor:
      valor = valores[i]
      pO = punts[i]
  
  answer = str(valor) # -- Z
  xy = pO             # -- Punto Optimo (x,y)
  return answer, xy

def resultados(punts, matRest):
  resu = [] # -- lista para enocntrar el punto opt
  for i in range(len(punts)):
    resuX = punts[i][0] * (matRest[0][1] *-1)
    resuY = punts[i][1] * (matRest[0][2] *-1)
    cantT = resuX + resuY
    resu.append(cantT)

  puntOpt, xy = maximizacion(resu, punts)
  return puntOpt, xy
