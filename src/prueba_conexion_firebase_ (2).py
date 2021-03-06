# # -*- coding: utf-8 -*-
# """PRUEBA_CONEXION_FIREBASE_.ipynb

# Automatically generated by Colaboratory.

# Original file is located at
#     https://colab.research.google.com/drive/1e95-bAH-6RTNt-IfI7y8AvVLlrqOUbi0

# ## **PASO 0**:* Ingresamos las variables de busqueda
# """

# Edad=5 
# grado_formacion=2  
# estado_estudios=3  
# rubro_carrera=3
# Experiencia_laboral=3
# ATC=1
# Ventas=0
# BO=0
# RS=0
# Tiempo_experiencia=2

# Puntuación=Edad*(grado_formacion*estado_estudios*rubro_carrera)*(Experiencia_laboral*ATC*Tiempo_experiencia)+(Experiencia_laboral*Ventas*Tiempo_experiencia)+(Experiencia_laboral*BO*Tiempo_experiencia)+(Experiencia_laboral*RS*Tiempo_experiencia)

# """---


# # **CONEXION GOOGLE COLAB CON FIREBASE**


# ---

# ## **PASO 1**:* Instalamos los paquetes necesarios *
# """

##conexión con firebase
!pip install six python-firebase

"""## **PASO 2**:* hacemos la llamada a los paquetes necesarios para correr todo el proceso *"""

## Pandas
import pandas as pd
from pandas import DataFrame
import json
from firebase import firebase
from datetime import datetime
import datetime
from datetime import date
from datetime import datetime

"""## **PASO 3**:* Generamos la cadena de conexión *"""

firebase = firebase.FirebaseApplication('https://konectase-522d7.firebaseio.com/', None)

"""## **PASO 4**:* Cargamos la base de firebase como Json *"""

## TABLA POSTULANTES
postulantes= firebase.get('/POSTULANTES', None)
postulantes=json.dumps(postulantes)

## TABLA DATOS PROFESIONALES
profesional= firebase.get('/DATOS_PROFESIONALES', None)
profesional=json.dumps(profesional)

## TABLA DATOS EXPERIENCIA
experiencia= firebase.get('/DATOS_EXPERIENCIA', None)
experiencia=json.dumps(experiencia)

"""## **PASO 5**:* Convertimos json a data frame *"""

###TABLA POSTULANTES
data_postulantes=json.loads(postulantes)
dfpostulantes = DataFrame(data_postulantes).T

###TABLA PROFESIONAL
data_profesional=json.loads(profesional)
dfprofesional = DataFrame(data_profesional).T

###TABLA PROFESIONAL
data_experiencia=json.loads(experiencia)
dfexperiencia = DataFrame(data_experiencia).T

dfpostulantes

# """## **PASO 6**:* Damos el formato a cada tabla para obtener el tablon de perfil *"""

# #################################################################################################################################################################################
# ## A) Tabla datos personales del postulante
# #################################################################################################################################################################################

# #-(1)Tomamos las columnas  que nos van a servir de la tabla
# df_Rpostulantes=DataFrame(dfpostulantes[['RegistradoDate','fecha_nac', 'numdoc']])
# #-(2)Convertimos fecha de nacimiento a valor datetime
# df_Rpostulantes['fecha_nac'] = df_Rpostulantes.fecha_nac.astype('datetime64[ns]') 
# #-(3)Extraemos la fecha de registro principal y convertimos fecha de registro a valor datetime
# df_Rpostulantes['FechaRegistro'] = df_Rpostulantes.RegistradoDate.str['date'].astype('datetime64[ns]')
# #-(4)Extraemos la hora de registroprincipal
# df_Rpostulantes['HoraRegistro'] = (df_Rpostulantes.RegistradoDate.str['hour'])
# #-(5)Obtenemos la fecha de hoy (analisis)
# df_Rpostulantes['Fechahoy'] =date.today() 
# #-(6)llevamos el indice a una columna que es el id unico de postulante
# df_Rpostulantes ['id_postulante']= df_Rpostulantes.index 
# #-(7)Reseteamos el valor de los indices
# df_Rpostulantes.reset_index(level=0, inplace=True)
# #-(8)Convertimos la fecha hoy a datetime
# df_Rpostulantes['Fechahoy'] = df_Rpostulantes.Fechahoy.astype('datetime64[ns]')
# #-(9)Calculamos la edad del postulante
# df_Rpostulantes['Edad']=((df_Rpostulantes['Fechahoy']- df_Rpostulantes['fecha_nac']).astype('timedelta64[Y]')).astype(int)

# #################################################################################################################################################################################
# ## B) Tabla datos profesiones
# #################################################################################################################################################################################

# #-(1) Tomamos las columnas que nos sirven para la tabla
# df_Rprofesional=DataFrame(dfprofesional[['id_postulante','grado_formacion', 'estado_estudios','rubro_carrera']])
# #-(1) Reseteamos los indices
# df_Rprofesional.reset_index(level=0,inplace=True)

# #################################################################################################################################################################################
# ## A) Tabla datos experiencia
# #################################################################################################################################################################################

# #///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// sin experiencia profesional

# #-(1)Seleccionando columnas para los registros sin experiencia.
# sinexperiencia=DataFrame(dfexperiencia[['id_postulante','flag_se','se_p_ventas','se_p_backof','se_p_redes','se_p_atc']])
# #-(2)Le damos valores numericos a las respuestas de la pregunta de ventas
# sinexperiencia['se_p_ventas']=sinexperiencia['se_p_ventas'].replace('A',4)
# sinexperiencia['se_p_ventas']=sinexperiencia['se_p_ventas'].replace('B',3)
# sinexperiencia['se_p_ventas']=sinexperiencia['se_p_ventas'].replace('C',2)
# sinexperiencia['se_p_ventas']=sinexperiencia['se_p_ventas'].replace('D',1)
# sinexperiencia['se_p_ventas']=sinexperiencia['se_p_ventas'].fillna(0)
# #-(3)Le damos valores numericos a las respuestas de la pregunta de atc
# sinexperiencia['se_p_atc']=sinexperiencia['se_p_atc'].replace('5',5)
# sinexperiencia['se_p_atc']=sinexperiencia['se_p_atc'].replace('4',4)
# sinexperiencia['se_p_atc']=sinexperiencia['se_p_atc'].replace('3',3)
# sinexperiencia['se_p_atc']=sinexperiencia['se_p_atc'].replace('2',2)
# sinexperiencia['se_p_atc']=sinexperiencia['se_p_atc'].replace('1',1)
# sinexperiencia['se_p_atc']=sinexperiencia['se_p_atc'].fillna(0)
# #-(4)Le damos valores numericos a las respuestas de la pregunta de BO
# sinexperiencia['se_p_backof']=sinexperiencia['se_p_backof'].replace('A',4)
# sinexperiencia['se_p_backof']=sinexperiencia['se_p_backof'].replace('B',3)
# sinexperiencia['se_p_backof']=sinexperiencia['se_p_backof'].replace('C',2)
# sinexperiencia['se_p_backof']=sinexperiencia['se_p_backof'].replace('D',1)
# sinexperiencia['se_p_backof']=sinexperiencia['se_p_backof'].fillna(0)
# sinexperiencia
# #-(5)Le damos valores numericos a las respuestas de la pregunta de BO
# sinexperiencia['se_p_redes']=sinexperiencia['se_p_redes'].replace('A',5)
# sinexperiencia['se_p_redes']=sinexperiencia['se_p_redes'].replace('B',4)
# sinexperiencia['se_p_redes']=sinexperiencia['se_p_redes'].replace('C',3)
# sinexperiencia['se_p_redes']=sinexperiencia['se_p_redes'].replace('D',2)
# sinexperiencia['se_p_redes']=sinexperiencia['se_p_redes'].replace('E',1)
# sinexperiencia['se_p_redes']=sinexperiencia['se_p_redes'].fillna(0)
# sinexperiencia=sinexperiencia[sinexperiencia['flag_se']=='1']
# #-(6)Le damos valor Int a flag_se
# sinexperiencia['flag_se']=sinexperiencia['flag_se'].astype(int)

# #///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// con experiencia en call center

# ### OBTENEMOS LA TABLA SUMARIZADA DE EXPERIENCIA
# #-(1)Seleccionando columnas para los registros con experiencia call.
# dataprev=DataFrame(dfexperiencia[['id_postulante','flag_ec','ec_segmento','ec_tiempo_exp']])
# #-(2) Filtramos los datos que tienen experiencia en call
# dataprev= dataprev[dataprev['flag_ec']==1]
# #-(3) La variable tiempo de experiencia en call la convertimos en entera (numerica)
# dataprev['ec_tiempo_exp']=dataprev['ec_tiempo_exp'].astype(int)
# dataprev['flag_ec']=dataprev['flag_ec'].astype(int)
# #-(4) hacemos un pivot de la tabla para obtener la sumatoria de la experiencia por cada segmento.
# dataprev2=dataprev.pivot_table(index='id_postulante', columns='ec_segmento', values=('ec_tiempo_exp'), aggfunc='sum').fillna(0) 
# #-(5) Renombramos las columnas de la tabla pivoteada. 
# dataprev2.rename(columns={'Atención al cliente':'qec_ATC','Ventas':'qec_Ventas','Back Office':'qec_BO','Crosseling':'qec_Cross','Redes Sociales':'qec_RS'},inplace=True)

# ### OBTENEMOS LA TABLA SUMARIZADA DE LOS SEGMENTOS A LOS CUALES HA ATENDIDO
# #-(6) Generamos una tabla dummies con todos los segmentos
# dummies= pd.get_dummies(dataprev['ec_segmento']) 
# #-(7)tomamos de la tabla inicial dataprev  solo el Id del postulante para unirla con la tabla dummies que no tiene ID, servira en el siguiente paso.
# Rev=DataFrame(dataprev[['id_postulante','flag_ec']])
# #-(8) Cruzamos la tabla REV con dummies para obtener la llave.el cruce se hace con los indices
# union=pd.merge(Rev,dummies,left_index=True,right_index=True)
# #-(9) Renombramos las columnas de esta tabla denominada union.
# union.rename(columns={'Atención al cliente':'ec_ATC','Ventas':'ec_Ventas','Back Office':'ec_BO','Crosseling':'ec_Cross','Redes Sociales':'ec_RS'},inplace=True)
# #-(10) Generamos un pivot con esta tabla union para obtener por cada ID los segmentos en los cuales ha tenido experiencia.
# union2=union.pivot_table(index='id_postulante', values=('flag_ec','ec_ATC','ec_Ventas','ec_BO','ec_Cross','ec_RS'), aggfunc='sum').fillna(0) 

# ### CRUCE DE TABLAS.
# #-(11) se hace un join entre el sumarizado de experiencia y el sumarizado de segmento.
# conexperienciacall=pd.merge(union2, dataprev2,left_on='id_postulante',right_on='id_postulante')

# #///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// con experiencia en otro rubro

# ### OBTENEMOS LA TABLA SUMARIZADA DE EXPERIENCIA
# #-(1)Seleccionando columnas para los registros con experiencia call.
# datapreveo=DataFrame(dfexperiencia[['id_postulante','flag_eo','eo_puesto','eo_tiempo_exp']])
# #-(2) Filtramos los datos que tienen experiencia en call
# datapreveo= datapreveo[datapreveo['flag_eo']==1]
# datapreveo['flag_eo']=datapreveo['flag_eo'].astype(int)
# #-(3)Categorizamos los puestos de acuerdo a los segmentos del call
# datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Atención al cliente','eo_ATC')
# datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Ventas','eo_Ventas')
# datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Impulsador de productos','eo_Ventas')
# datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Cajero','eo_ATC')
# datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Reponedor','eo_ATC')
# datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Almacén, Distribución y Reparto','eo_BO')
# datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Soporte Técnico','eo_ATC')
# datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Atención en Salud','eo_ATC')
# datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Administrativo y Tramites','eo_BO')
# datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Servicio de Transporte','eo_ATC')
# datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Operario','eo_BO')
# datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Profesor','eo_Ventas')
# datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Desarrollo de contenido(audiovisual, escrito, edición','eo_RS')
# datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Community Manager y Redes Sociales','eo_RS')
# datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Asistente','eo_BO')
# datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Secretaria','eo_ATC')
# datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Otros','eo_ATC')

# #-(4) hacemos un pivot de la tabla para obtener la sumatoria de la experiencia por cada segmento.
# datapreveo2=datapreveo.pivot_table(index='id_postulante', columns='eo_puesto', values='eo_tiempo_exp', aggfunc='sum').fillna(0) 
# #-(5) Renombramos las columnas de la tabla pivoteada. 
# datapreveo2.rename(columns={'eo_ATC':'qeo_ATC','eo_Ventas':'qeo_Ventas','eo_BO':'qeo_BO','eo_RS':'qeo_RS'},inplace=True)

# ### OBTENEMOS LA TABLA SUMARIZADA DE LOS SEGMENTOS A LOS CUALES HA ATENDIDO
# #-(6) Generamos una tabla dummies con todos los segmentos
# dummies2= pd.get_dummies(datapreveo['eo_puesto']) 
# #-(7)tomamos de la tabla inicial datapreveo  solo el Id del postulante para unirla con la tabla dummies que no tiene ID, servira en el siguiente paso.
# Rev2=DataFrame(datapreveo[['id_postulante','flag_eo']])
# #-(8) Cruzamos la tabla REV2 con dummies2 para obtener la llave.el cruce se hace con los indices
# unioneo=pd.merge(Rev2,dummies2,left_index=True,right_index=True)
# #-(9) Generamos un pivot con esta tabla unioneo para obtener por cada ID los segmentos en los cuales ha tenido experiencia.
# unioneo=unioneo.pivot_table(index='id_postulante', values=('flag_eo','eo_ATC','eo_Ventas','eo_BO','eo_RS'), aggfunc='sum').fillna(0) 

# ### CRUCE DE TABLAS.
# #-(10) se hace un join entre el sumarizado de experiencia y el sumarizado de segmento.
# conexperienciaotros=pd.merge(unioneo, datapreveo2,left_on='id_postulante',right_on='id_postulante')

# """## **PASO 7**:* Construimos el tablon *"""

# #-(0) Cruzamos la tabla postulantes con la experiencia call 
# tablonperfil=pd.merge(df_Rpostulantes, df_Rprofesional,left_on='id_postulante',right_on='id_postulante',how='left').fillna(0) 
# #-(1) Cruzamos la tabla postulantes con la experiencia call 
# tablonperfil=pd.merge(tablonperfil, conexperienciacall,left_on='id_postulante',right_on='id_postulante',how='left').fillna(0) 
# #-(2) Cruzamos la tabla postulantes con la experiencia otros
# tablonperfil=pd.merge(tablonperfil, conexperienciaotros,left_on='id_postulante',right_on='id_postulante',how='left').fillna(0) 
# #-(3) Cruzamos la tabla postulantes con la experiencia otros
# tablonperfil=pd.merge(tablonperfil, sinexperiencia,left_on='id_postulante',right_on='id_postulante',how='left').fillna(0) 
# #-(4)Seleccionando columnas necesarias para el analisis
# tablonperfil=DataFrame(tablonperfil[['id_postulante','numdoc','FechaRegistro','HoraRegistro','Fechahoy','Edad','grado_formacion','estado_estudios','rubro_carrera',
#                                      'flag_se','flag_ec','flag_eo','ec_ATC','ec_BO','ec_Cross','ec_RS','ec_Ventas','qec_ATC','qec_BO','qec_Cross','qec_RS','qec_Ventas',
#                                      'eo_ATC','eo_BO','eo_RS','eo_Ventas','qeo_ATC','qeo_BO','qeo_RS','qeo_Ventas',
#                                      'se_p_ventas','se_p_backof','se_p_redes','se_p_atc']])

# #-(5)La columna edad convertirla a categorias
# bins=[-1,17,22,37,58,73,100]
# names=['[0-17]','[18-22]','[23-37]','[38-58]','[59-73]','[74-100]']
# tablonperfil['Edad']=pd.cut(tablonperfil['Edad'],bins,labels=names)
# tablonperfil['Edad']=tablonperfil['Edad'].replace('[0-17]',1)
# tablonperfil['Edad']=tablonperfil['Edad'].replace('[18-22]',5)
# tablonperfil['Edad']=tablonperfil['Edad'].replace('[23-37]',4)
# tablonperfil['Edad']=tablonperfil['Edad'].replace('[38-58]',3)
# tablonperfil['Edad']=tablonperfil['Edad'].replace('[59-73]',2)
# tablonperfil['Edad']=tablonperfil['Edad'].replace('[74-100]',1)

# #-(6)grado de formacion en valor numerico
# tablonperfil['grado_formacion']=tablonperfil['grado_formacion'].replace('Secundaria',1)
# tablonperfil['grado_formacion']=tablonperfil['grado_formacion'].replace('Técnica',2)
# tablonperfil['grado_formacion']=tablonperfil['grado_formacion'].replace('Universitaria',3)

# #-(7)estado_estudios en valor numerico
# tablonperfil['estado_estudios']=tablonperfil['estado_estudios'].replace('Tuve que dejarlo',1)
# tablonperfil['estado_estudios']=tablonperfil['estado_estudios'].replace('En curso',2)
# tablonperfil['estado_estudios']=tablonperfil['estado_estudios'].replace('Completa',3)

# #-(8)las columnas flag que tengan un valor 1 si es mayor que 1.
# tablonperfil['flag_se']=tablonperfil['flag_se'].where(tablonperfil['flag_se']<2, 1)
# tablonperfil['flag_ec']=tablonperfil['flag_ec'].where(tablonperfil['flag_ec']<2, 1)
# tablonperfil['flag_eo']=tablonperfil['flag_eo'].where(tablonperfil['flag_eo']<2, 1)

# #-(8)experiencia call
# tablonperfil['ec_ATC']=tablonperfil['ec_ATC'].where(tablonperfil['ec_ATC']<2, 1)
# tablonperfil['ec_BO']=tablonperfil['ec_BO'].where(tablonperfil['ec_BO']<2, 1)
# tablonperfil['ec_Cross']=tablonperfil['ec_Cross'].where(tablonperfil['ec_Cross']<2, 1)
# tablonperfil['ec_RS']=tablonperfil['ec_RS'].where(tablonperfil['ec_RS']<2, 1)
# tablonperfil['ec_Ventas']=tablonperfil['ec_Ventas'].where(tablonperfil['ec_Ventas']<2, 1)

# tablonperfil['eo_ATC']=tablonperfil['eo_ATC'].where(tablonperfil['eo_ATC']<2, 1)
# tablonperfil['eo_BO']=tablonperfil['eo_BO'].where(tablonperfil['eo_BO']<2, 1)
# tablonperfil['eo_RS']=tablonperfil['eo_RS'].where(tablonperfil['eo_RS']<2, 1)
# tablonperfil['eo_Ventas']=tablonperfil['eo_Ventas'].where(tablonperfil['eo_Ventas']<2, 1)

# #-(9)convertirmos rubro carrera en numerica
# tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Administración (Todas las afines). Ejemplo: Neg.Internacionales, bancaria,etc)',3)
# tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Administración (Todas las afines)',3)
# tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Economía, Contabilidad y Finanzas',3)
# tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Redes Sociales',1)
# tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Computación e Informática',1)
# tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Derecho y Ciencias Políticas',2)
# tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Psicología',2)
# tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Ing. Sistemas',1)
# tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Ing.Industrial, Ambiental, Estadística',1)
# tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Diseño (Gráfico, Publicitario o Web)',1)
# tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Medicina, Enfermeria, Farmacia o Fisioterapia)',2)
# tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Ciencia de la Comunicación',2)
# tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Educación',2)
# tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Secretariado',2)
# tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Turismo y Aviación Comercial',3)
# tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Idiomas',2)
# tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Gastronomía y Repostería',2)
# tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Ing.Civil, Arquitectura, Diseño de Interiores',1)
# tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Literatura, Historia, Filosofía, Sociología',2)
# tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Ing. Electrónica / Electricidad',1)
# tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Ing. Agricola o Química',1)

# #---------------------------------------------------------------------------------
# #-(10)La columna qexperiencia call convertirla a categorias
# bins2=[-1,3,6,12,100]
# names2=['[0-3]','[3-6]','[6-12]','[12-mas]']

# tablonperfil['qec_ATC']=pd.cut(tablonperfil['qec_ATC'],bins2,labels=names2)
# tablonperfil['qec_BO']=pd.cut(tablonperfil['qec_BO'],bins2,labels=names2)
# tablonperfil['qec_Cross']=pd.cut(tablonperfil['qec_Cross'],bins2,labels=names2)
# tablonperfil['qec_RS']=pd.cut(tablonperfil['qec_RS'],bins2,labels=names2)
# tablonperfil['qec_Ventas']=pd.cut(tablonperfil['qec_Ventas'],bins2,labels=names2)

# tablonperfil['qec_ATC']=tablonperfil['qec_ATC'].replace('[0-3]',1)
# tablonperfil['qec_ATC']=tablonperfil['qec_ATC'].replace('[3-6]',2)
# tablonperfil['qec_ATC']=tablonperfil['qec_ATC'].replace('[6-12]',3)
# tablonperfil['qec_ATC']=tablonperfil['qec_ATC'].replace('[12-mas]',4)

# tablonperfil['qec_BO']=tablonperfil['qec_BO'].replace('[0-3]',1)
# tablonperfil['qec_BO']=tablonperfil['qec_BO'].replace('[3-6]',2)
# tablonperfil['qec_BO']=tablonperfil['qec_BO'].replace('[6-12]',3)
# tablonperfil['qec_BO']=tablonperfil['qec_BO'].replace('[12-mas]',4)

# tablonperfil['qec_Cross']=tablonperfil['qec_Cross'].replace('[0-3]',1)
# tablonperfil['qec_Cross']=tablonperfil['qec_Cross'].replace('[3-6]',2)
# tablonperfil['qec_Cross']=tablonperfil['qec_Cross'].replace('[6-12]',3)
# tablonperfil['qec_Cross']=tablonperfil['qec_Cross'].replace('[12-mas]',4)

# tablonperfil['qec_RS']=tablonperfil['qec_RS'].replace('[0-3]',1)
# tablonperfil['qec_RS']=tablonperfil['qec_RS'].replace('[3-6]',2)
# tablonperfil['qec_RS']=tablonperfil['qec_RS'].replace('[6-12]',3)
# tablonperfil['qec_RS']=tablonperfil['qec_RS'].replace('[12-mas]',4)

# tablonperfil['qec_Ventas']=tablonperfil['qec_Ventas'].replace('[0-3]',1)
# tablonperfil['qec_Ventas']=tablonperfil['qec_Ventas'].replace('[3-6]',2)
# tablonperfil['qec_Ventas']=tablonperfil['qec_Ventas'].replace('[6-12]',3)
# tablonperfil['qec_Ventas']=tablonperfil['qec_Ventas'].replace('[12-mas]',4)

# #---------------------------------------------------------------------------------

# #-(11)La columna qexperiencia otros convertirla a categorias
# tablonperfil['qeo_ATC']=pd.cut(tablonperfil['qeo_ATC'],bins2,labels=names2)
# tablonperfil['qeo_BO']=pd.cut(tablonperfil['qeo_BO'],bins2,labels=names2)
# tablonperfil['qeo_RS']=pd.cut(tablonperfil['qeo_RS'],bins2,labels=names2)
# tablonperfil['qeo_Ventas']=pd.cut(tablonperfil['qeo_Ventas'],bins2,labels=names2)


# tablonperfil['qeo_ATC']=tablonperfil['qeo_ATC'].replace('[0-3]',1)
# tablonperfil['qeo_ATC']=tablonperfil['qeo_ATC'].replace('[3-6]',2)
# tablonperfil['qeo_ATC']=tablonperfil['qeo_ATC'].replace('[6-12]',3)
# tablonperfil['qeo_ATC']=tablonperfil['qeo_ATC'].replace('[12-mas]',4)

# tablonperfil['qeo_BO']=tablonperfil['qeo_BO'].replace('[0-3]',1)
# tablonperfil['qeo_BO']=tablonperfil['qeo_BO'].replace('[3-6]',2)
# tablonperfil['qeo_BO']=tablonperfil['qeo_BO'].replace('[6-12]',3)
# tablonperfil['qeo_BO']=tablonperfil['qeo_BO'].replace('[12-mas]',4)

# tablonperfil['qeo_RS']=tablonperfil['qeo_RS'].replace('[0-3]',1)
# tablonperfil['qeo_RS']=tablonperfil['qeo_RS'].replace('[3-6]',2)
# tablonperfil['qeo_RS']=tablonperfil['qeo_RS'].replace('[6-12]',3)
# tablonperfil['qeo_RS']=tablonperfil['qeo_RS'].replace('[12-mas]',4)

# tablonperfil['qeo_Ventas']=tablonperfil['qeo_Ventas'].replace('[0-3]',1)
# tablonperfil['qeo_Ventas']=tablonperfil['qeo_Ventas'].replace('[3-6]',2)
# tablonperfil['qeo_Ventas']=tablonperfil['qeo_Ventas'].replace('[6-12]',3)
# tablonperfil['qeo_Ventas']=tablonperfil['qeo_Ventas'].replace('[12-mas]',4)

# #---------------------------------------------------------------------------------

# tablonperfil

# """## **PASO 8**:* Generamos una base de entrenamiento  *"""

# from itertools import product

# def expand_grid(dictionary):
#    return pd.DataFrame([row for row in product(*dictionary.values())], 
#                        columns=dictionary.keys())
   
# dictionary = {'Edad': [1,2,3], 
#               'grado_formacion': [1,2,3], 
#               'estado_estudios': [1,2,3],
#               'rubro_carrera': [1,2,3,4],
#               #'flag_se':[0,1],
#               #'flag_ec':[0,1],
#               #'flag_eo':[0,1],
#               'ec_ATC':[0,1],
#               'ec_BO':[0,1],
#               'ec_Cross':[0,1],
#               'ec_RS':[0,1],
#               'ec_Ventas':[0,1],
#               'qec_ATC':[1,2,3],
#               'qec_BO':[1,2,3],
#               'qec_Cross':[1,2,3],
#               'qec_RS':[1,2,3],
#               'qec_Ventas':[1,2,3],
#                'eo_ATC':[0,1],
#                'eo_BO':[0,1],
#                'eo_RS':[0,1],
#                'eo_Ventas':[0,1],
#               'qeo_ATC':[1,2,3],
#               'qeo_BO':[1,2,3],
#               'qeo_RS':[1,2,3],
#               'qeo_Ventas':[1,2,3],
#               'se_p_ventas':[0,1],
#               'se_p_backof':[0,1],
#               'se_p_redes':[0,1],
#               'se_p_atc':[0,1]             
#               }
# data=expand_grid(dictionary)
# data.head()