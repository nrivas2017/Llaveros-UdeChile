def validaFecha(fecha):
    fechaValidar = fecha.split("-")
    if len(fechaValidar) !=3:
        return False,0 #"fecha incorrecta"
    else:
        diaV = fechaValidar[0]
        mesV = fechaValidar[1]
        anioV = fechaValidar[2]
        if diaV.isnumeric() and mesV.isnumeric() and anioV.isnumeric():
            dia = int(diaV)
            mes = int(mesV)
            year = int(anioV)
            diaRes = 0
            mesRes = 0
            anioRes = 0
            if((mes>0 and mes<=12)):       #Este sector valida los datos ingresados
                if((year%400==0)or(year%100!=0 and year%4==0)):      #Este sector valida si es año bisiesto
                    listames=[31,29,31,30,31,30,31,31,30,31,30,31]
                else:
                    listames=[31,28,31,30,31,30,31,31,30,31,30,31]
                if(dia<=listames[mes-1] and dia > 0):
                    diaRes = dia
                    mesRes = mes
                    anioRes = year
                else:
                    return False,0 #"El dia esta fuera de rango"
            else:
                return False,0 #"El Mes esta fuera de rango"
            return True,'{}-{}-{}'.format(diaRes, mesRes, anioRes)
        else:
            return False,0 #"fecha incorrecta"
