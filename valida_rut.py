def valida_digito_verificador(rut):
    num = []
    vec_con = [2,3,4,5,6,7]
    mul = 0
    j = 0
    for i in reversed(rut[0]):
        num.append(int(i))
    for i in num:
        if j == 6:
            j = 0
        mul+=i*vec_con[j]
        j += 1
    mod = mul%11
    dv = 11 - mod
    if dv == 11:
        dv = 0
    elif dv == 10:
        dv = "k"
    return dv

def valida_rut(rut):
    rut = rut.replace(".","")
    rut = rut.replace("-","")
    dat=[rut[:-1],rut[-1]]

    if dat[0].isdigit():
        if  dat[1].isdigit():
            dat[1] = int(dat[1])
        else:
            if dat[1] == "k" or dat[1] == "K":
                dat[1] = "k"
                pass
            else: 
                return 0 #No valido
        if dat[1] == valida_digito_verificador(dat):
            return 1 #Valido
        else:
            return 0 #No valido
    else:
        return 0 #No valido

#rut = input("Ingrese rut: ")
#print(valida_rut(rut))
