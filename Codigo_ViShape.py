
# coding: utf-8

# In[1]:


#Módulo para importar el archivo .shp
import shapefile
import numpy as np
import pandas as pd
from math import ceil, floor
import matplotlib.pyplot as plt


# In[2]:


# Especificar que las gráficas queden aquí en el documento
get_ipython().magic(u'pylab inline')


# In[3]:


#Se importa el archivo
sf = shapefile.Reader("C:\\Red_de_Carreteras_Col.shp")


# In[4]:


#Con esto pudes obtener la cantidad de vectores
shapes = sf.shapes()

#Obtener las características de los vectores (atributos)
shapeRecs = sf.shapeRecords()

print 'Cantidad de vectores =', len(shapeRecs)


# In[ ]:


#Obtener la cantidad de tipos de caminos diferentes
cantidad = 0
tipo = 0
for i in range(len(shapes)):
    ok = shapeRecs[i].record[0:3]
    if tipo != ok[0]:
        tipo = ok[0]
        cantidad = cantidad + 1
print 'Cantidad de tipos diferentes de caminos =', cantidad


# In[ ]:


#Se crea la tabla para la información
vectores = np.zeros([cantidad,5],int)
caminos = pd.DataFrame(vectores, columns=['Tipo de camino','Cantidad Vectores',
                                            'Maximo', 'Medio', 'Minimo'])
caminos



# In[ ]:


#Se hace la tabla para las longitudes
j = 0
longi = np.zeros([len(shapes),1])
longitudes = pd.DataFrame(longi, columns=['len'])



# In[ ]:


#Se ingresa el tipo de camino
for i in range(len(shapes)):
    ok2 = shapeRecs[i].record[0:3]
    longitudes.loc[i,'len']=ok2[1]
    if tipo != ok2[0]:
        tipo = ok2[0]
        caminos.loc[j,'Tipo de camino'] = ok2[0]
        j = j + 1
    caminos.loc[j-1,'Cantidad Vectores'] = caminos.loc[j-1,'Cantidad Vectores'] + 1
caminos


# In[ ]:


#Se ordenan las longitudes
k = 0
h = 0
p = 0
cantcam = 0
for i in range(cantidad):
    lon = float(pd.DataFrame(np.zeros(caminos.loc[i,'Cantidad Vectores']),columns=['len']))
    for h in range(len(lon)):
        ok3 = shapeRecs[h+p].record[0:3]
        lon.loc[h,'len'] = ok3[1]
    p = p + h + 1
    for j in range(cantidad):
        #Variables
        j = 0
        n = len(lon)
        #Ordenamiento
        while j <= n-2:
            if lon.loc[j,'len'] > lon.loc[j+1,'len']:
                vt = lon.loc[j,'len']
                lon.loc[j,'len'] = lon.loc[j+1,'len']
                lon.loc[j+1,'len'] = vt
                j = 0
            else:
                j = j + 1
    val = len(lon)-1
    #Se obtienen los valores máximos, mínimos y medios de las longitudes
    caminos.loc[i,'Maximo'] = lon.loc[val,'len']
    caminos.loc[i,'Medio'] = (lon.loc[val-floor(val/2),'len']+lon.loc[val-ceil(val/2),'len'])/2
    caminos.loc[i,'Minimo'] = lon.loc[val-val,'len']
caminos


# In[ ]:


x=[]
y=[]
plt.figure()
for shape in sf.shapeRecords():
    x = [i[0] for i in shape.shape.points[:]]
    y = [i[1] for i in shape.shape.points[:]]
    plt.plot(x,y)
plt.show()


# In[ ]:


#Se muestra la tabla
caminos

