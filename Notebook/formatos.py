import pandas as pd

### 1. Funcion para Ubicar los archivos de cada quincena para un mes en particular.
def Quincenas(carp1, arch1, arch2):
    df1 = pd.read_csv(f'{carp1}{arch1}.csv', sep=';',
                      usecols=['CEDULA','APELLIDO Y NOMBRE', 'Unnamed: 2', 'CARGO',
                               'UBICACIÓN GEOGRAFICA', 'AÑO', 'MES', 'DIA', 'NETO A PAGAR'])
    df2 = pd.read_csv(f'{carp1}{arch2}.csv', sep=';',
                      usecols=['CEDULA','APELLIDO Y NOMBRE', 'Unnamed: 2', 'CARGO', 'NETO A PAGAR'])
    return df1, df2

### 2. Funcion para Renombrar y Seleccionar las Columnas de la tabla.
# Partimos de la primera quincena para generar la mayoria de la información necesaria.
def Renom_Selecc1(df1):
    df1.rename(columns={"CEDULA":"Cedula", "APELLIDO Y NOMBRE":"Apellido", "Unnamed: 2":"Nombre",
                       "CARGO":"Cargo", "UBICACIÓN GEOGRAFICA":"Ubicación", "AÑO":"Año", "MES":"Mes",
                       "DIA":"Dia", "NETO A PAGAR":"1era Quincena",}, inplace=True)
    df1 = df1.loc[:, ['Cedula', 'Apellido', 'Nombre', 'Cargo', 'Ubicación',
                      'Año', 'Mes', 'Dia', '1era Quincena']]
    return df1

### 3. Funcion para Reorganizar la fecha en la tabla.
def Organiz_Fechas(df1):
    dfA = df1.loc[:, ['Año', 'Mes', 'Dia']]
    dfA['Año'] = dfA['Año'].astype('string')
    dfA['Mes'] = dfA['Mes'].astype('string')
    dfA['Dia'] = dfA['Dia'].astype('string')
    df1['Fecha de Ingreso'] = dfA['Año'] + '-' + dfA['Mes'] + '-' + dfA['Dia']
    df1['Fecha de Ingreso'] = pd.to_datetime(df1['Fecha de Ingreso'], format='%Y/%m/%d')
    del dfA
    df1 = df1.loc[:, ['Cedula', 'Apellido', 'Nombre', 'Cargo', 'Ubicación',
                      'Fecha de Ingreso', '1era Quincena']]
    df1['1era Quincena'] = df1['1era Quincena'].str.replace(',', '.').astype(float)
    return df1

### 4. Funcion para Renombrar y Seleccionar las columnas de la segunda quincena.
def Renom_Selecc2(df2):
    df2.rename(columns={"CEDULA":"Cedula", "APELLIDO Y NOMBRE":"Apellido", "Unnamed: 2":"Nombre",
                       "CARGO":"Cargo", "UBICACIÓN GEOGRAFICA":"Ubicación", "AÑO":"Año", "MES":"Mes",
                       "DIA":"Dia", "NETO A PAGAR":"2da Quincena",}, inplace=True)
    df2 = df2.loc[:, ['Cedula', 'Apellido', 'Nombre', 'Cargo', '2da Quincena']]
    df2['2da Quincena'] = df2['2da Quincena'].str.replace(',', '.').astype(float)
    return df2

### 5. Funcion para Comprobar transcripcion de datos previo union de ambas tablas.
def Comp_transcrip(df1, df2):
    diff_cedula = df1['Cedula'].equals(df2['Cedula'])
    diff_Apellido = df1['Apellido'].equals(df2['Apellido'])
    diff_Nombre = df1['Nombre'].equals(df2['Nombre'])
    diff_Cargo = df1['Cargo'].equals(df2['Cargo'])
    diferencia = {'diff_cedula':diff_cedula, 'diff_Apellido':diff_Apellido,
              'diff_Nombre':diff_Nombre, 'diff_Cargo':diff_Cargo}
    for i in range(0,len(diferencia)):
        if list(diferencia.values())[i] == True:
            print(f'Sin problemas en la Columna {df1.columns[i]}')
        else:
            print(f'Se observaron diferencias en las celdas de la Columna {df1.columns[i]}')

### 6. Funcion para Unir tablas y Generar monto total.
def Monto_total(df1, df2):
    df1 = df1.reset_index()
    df2 = df2.reset_index()
    df1 = df1.loc[:, ['Cedula', 'Apellido', 'Nombre', 'Cargo', 'Ubicación',
                      'Fecha de Ingreso', '1era Quincena']]
    df1 = df1.set_index('Cedula')
    df2 = df2.loc[:, ['Cedula', '2da Quincena']]
    df2 = df2.set_index('Cedula')
    df1['2da Quincena'] = df2['2da Quincena']
    df1['total'] = df1['1era Quincena'] + df1['2da Quincena']
    del df2
    return df1

### 7. Funcion para generacion de archivo con la informacion solicitada.
def Resultados_Docentes(carp1, arch1, arch2, arch3):
    tabla1, tabla2 = Quincenas(carp1, arch1, arch2)
    print('Primero creamos las dos tablas con los datos de los archivos con las quincenas.')
    tabla1 = Renom_Selecc1(tabla1)
    print('Renombranos las columnas tabla 1.')
    tabla1 = Organiz_Fechas(tabla1)
    print('Reorganizamos la fecha en la tabla 1.')
    tabla2 = Renom_Selecc2(tabla2)
    print('Renombranos y seleccionamos las columnas tabla 2.')
    Comp_transcrip(tabla1, tabla2)
    print('Comprobacion de transcripcion antes de unir ambas tablas.')
    tabla = Monto_total(tabla1, tabla2)
    print('Generacion de tabla final con la información deseada.')
    tabla.to_csv(f'{carp1}{arch3}.csv', sep=';')
    print(f'Generado archivo {arch3}.csv en la carpeta {carp1}')
    del tabla, tabla1, tabla2

carp1 = 'Datos/'
arch1 = 'Informacion RRHH 1era quincena'
arch2 = 'Informacion RRHH 2da quincena'
arch3 = 'Resultados Docentes'
Resultados_Docentes(carp1, arch1, arch2, arch3)
