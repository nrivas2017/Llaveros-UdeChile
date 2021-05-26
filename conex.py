#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
from sqlite3 import Error
from datetime import date
from datetime import datetime

def sql_connection():
    try:
        con = sqlite3.connect('llaveros.db')
        return con
    except Error:
        return Error

def selectLlaveros(con = sql_connection()):
    try:
        cursorObj = con.cursor()
        cursorObj.execute("""SELECT id_llavero,nombre,precio,stock FROM llaveros""")
        
        respuesta = cursorObj.fetchall()

        aData=[]
        for fila in respuesta:
            aux={"id_llavero":fila[0],"nombre":fila[1],"precio":fila[2],"cantidad":fila[3]}
            aData.append(aux)
        con.commit()
        cursorObj.close()
        return 1,aData
    except Error:
        return 0,Error

def selectDetalleWhereID(id_venta,con = sql_connection()):
    try:
        aData=[[],[]]

        cursorObj = con.cursor()
        cursorObj.execute("""SELECT fecha,nom_cliente,rut_cliente,dir_cliente,tel_cliente,tipoEntrega,total,(select sum(cantidad) from detalle  WHERE id_venta == ve.id_venta) as cantidad FROM venta as ve WHERE id_venta=%s"""%id_venta)
        respuesta = cursorObj.fetchall()
        for fila in respuesta:
            aux={"fecha":fila[0], "nom_cliente":fila[1],"rut_cliente":fila[2],"dir_cliente":fila[3],"tel_cliente":fila[4],"tipoEntrega":fila[5],"total":fila[6],"cantidad":fila[7]}
            aData[0].append(aux)

        cursorObj = con.cursor()
        cursorObj.execute("""SELECT lla.nombre,de.cantidad,lla.precio,de.subtotal FROM detalle as de INNER JOIN llaveros as lla WHERE de.id_llavero = lla.id_llavero and de.id_venta = %s"""%id_venta)
        respuesta = cursorObj.fetchall()
        for fila in respuesta:
            aux={"nombre":fila[0], "cantidad":fila[1],"precio":fila[2],"subtotal":fila[3]}
            aData[1].append(aux)

        con.commit()
        cursorObj.close()
        return 1,aData
    except Error:
        return 0,Error

def selectVentas(mes,nombre,rut,con = sql_connection()):
    try:
        cursorObj = con.cursor()
        cursorObj.execute("""SELECT id_venta,fecha,nom_cliente,rut_cliente,dir_cliente,tel_cliente,tipoEntrega,total,(select sum(cantidad) from detalle  WHERE id_venta == ve.id_venta) as cantidad from venta as ve WHERE ve.fecha LIKE '%"""+mes+"""%' AND ve.nom_cliente LIKE '"""+nombre+"""%' AND ve.rut_cliente LIKE '"""+rut+"""%' ORDER BY fecha DESC""")
        
        respuesta = cursorObj.fetchall()

        aData=[]
        for fila in respuesta:
            aux={"id_venta":fila[0], "fecha":fila[1],"nom_cliente":fila[2],"rut_cliente":fila[3],"dir_cliente":fila[4],"tel_cliente":fila[5],"tipoEntrega":fila[6],"total":fila[7],"cantidad":fila[8]}
            aData.append(aux)
        con.commit()
        cursorObj.close()
        return 1,aData
    except Error:
        return 0,Error

def selectDineroTotalMes(mes,con = sql_connection()):
    try:
        cursorObj = con.cursor()
        cursorObj.execute("""SELECT sum(total) as total_mes from venta WHERE fecha LIKE '%-"""+mes+"""-%'""")
        
        respuesta = cursorObj.fetchall()

        aData=[]
        for fila in respuesta:
            aux={"total":fila[0]}
            aData.append(aux)
        con.commit()
        cursorObj.close()
        return 1,aData
    except Error:
        return 0,Error

def selectCantidadTotalMes(mes,con = sql_connection()):
    try:
        cursorObj = con.cursor()
        cursorObj.execute("""SELECT sum(de.cantidad) as cantidad_total FROM venta as ve INNER JOIN detalle as de WHERE ve.id_venta = de.id_venta AND ve.fecha LIKE '%-"""+mes+"""-%'""")
        
        respuesta = cursorObj.fetchall()

        aData=[]
        for fila in respuesta:
            aux={"total":fila[0]}
            aData.append(aux)
        con.commit()
        cursorObj.close()
        return 1,aData
    except Error:
        return 0,Error

def selectVentasPorDia(fecha,con = sql_connection()):
    try:
        cursorObj = sql_connection().cursor()
        cursorObj.execute("""SELECT id_venta FROM venta WHERE fecha LIKE '"""+fecha+"""%'""")
        respuesta = cursorObj.fetchall()

        idVenta=[]
        data={"existe":False}

        for fila in respuesta:
            idVenta.append(fila[0])

        if len(idVenta) > 0:
            data["existe"] = True
            consulta = "(id_venta = %s"%idVenta[0]

            if len(idVenta) > 1:
                for i in range(1,len(idVenta)):
                    consulta += " or id_venta = %s"%idVenta[i]

            consulta += ")"

            for idV in idVenta:
                cursorObj.execute("""SELECT lla.nombre, de.cantidad FROM detalle AS de INNER JOIN llaveros AS lla WHERE de.id_llavero = lla.id_llavero AND %s"""%consulta)
                respuesta = cursorObj.fetchall()
                for fila in respuesta:
                    data[fila[0]]=0
                for fila in respuesta:
                    data[fila[0]]+=int(fila[1])
            
            cursorObj.execute("""SELECT sum(de.cantidad) AS cantidad_dia FROM detalle AS de INNER JOIN llaveros AS lla WHERE de.id_llavero = lla.id_llavero AND %s"""%consulta)
            respuesta = cursorObj.fetchall()
            for fila in respuesta:
                    data["cantidad"] = fila[0]

            cursorObj.execute("""SELECT sum(total) AS total FROM venta WHERE fecha like '"""+fecha+"""%'""")
            respuesta = cursorObj.fetchall()
            for fila in respuesta:
                    data["total"] = fila[0]      
        sql_connection().commit()
        cursorObj.close()
        return 1,data
    except Error:
        return 0,Error

def buscaUltimoIdVenta(con = sql_connection()):
    try:
        cursorObj = con.cursor()
        cursorObj.execute("""SELECT id_venta FROM venta WHERE id_venta = (SELECT MAX(id_venta) FROM venta) ORDER BY id_venta""")
        respuesta = cursorObj.fetchall()
        res = ""
        for fila in respuesta:
            res = fila[0]
        con.commit()
        cursorObj.close()
        return 1,res
    except Error:
        return 0,Error

def buscaIdLlavero(nombre,con = sql_connection()):
    try:
        cursorObj = con.cursor()
        cursorObj.execute("""SELECT id_llavero from llaveros WHERE nombre = '%s'"""%(nombre))
        respuesta = cursorObj.fetchall()
        res = ""
        for fila in respuesta:
            res = fila[0]
        con.commit()
        cursorObj.close()
        return 1,res
    except Error:
        return 0,Error

def buscaPrecioLlavero(llavero,con = sql_connection()):
    try:
        cursorObj = con.cursor()
        cursorObj.execute("""SELECT precio from llaveros WHERE nombre = '%s'"""%(llavero))
        respuesta = cursorObj.fetchall()
        res = ""
        for fila in respuesta:
            res = fila[0]
        con.commit()
        cursorObj.close()
        return 1,res
    except Error:
        return 0,Error

def insertarDetalle(datos,id_venta,con = sql_connection()):
    try:
        
        for i in range(len(datos["aDetalle"])):
            cursorObj = con.cursor()
            cursorObj.execute("""INSERT INTO detalle (id_venta,id_llavero,cantidad,precio,subtotal) VALUES (%s,%s,%s,%s,%s);"""%(id_venta,buscaIdLlavero(datos["aDetalle"][i]["llavero"])[1],datos["aDetalle"][i]["cantidad"],buscaPrecioLlavero(datos["aDetalle"][i]["llavero"])[1],datos["aDetalle"][i]["subtotal"]))
            con.commit()
            cursorObj.execute("""UPDATE llaveros SET stock = stock-%s WHERE id_llavero = %s"""%(datos["aDetalle"][i]["cantidad"],buscaIdLlavero(datos["aDetalle"][i]["llavero"])[1]))
            con.commit()
            cursorObj.close()
        return 1,1
    except Error:
        return 0,Error    

def insertVenta(datos,con = sql_connection()):
    try:
        cursorObj = con.cursor()
        cursorObj.execute("""INSERT INTO venta (fecha,nom_cliente,rut_cliente,dir_cliente,tel_cliente,tipoEntrega,total) VALUES ('%s','%s','%s','%s','%s','%s',%s);"""%(datos["fecha"],datos["nomCliente"],datos["rutCliente"],datos["dirCliente"],datos["telCliente"],datos["tipoEntrega"],datos["total"]))
        con.commit()
        cursorObj.close()
        insertarDetalle(datos,buscaUltimoIdVenta()[1])
        return 1,1
    except Error:
        return 0,Error

def insertarLlavero(datos,con = sql_connection()):
    try:
        cursorObj = con.cursor()
        cursorObj.execute("""INSERT INTO llaveros (nombre,precio,stock) VALUES ('%s',%s,%s);"""%(datos["nombre"],datos["precio"],datos["stock"]))
        con.commit()
        cursorObj.close()
        return 1,1
    except Error:
        return 0,Error 

def actualizarLlavero(datos,con = sql_connection()):
    try:
        cursorObj = con.cursor()
        cursorObj.execute("""UPDATE llaveros SET precio=%s,stock = stock+%s WHERE id_llavero = %s"""%(datos["precio"],datos["stock"],buscaIdLlavero(datos["nombre"])[1]))
        con.commit()
        cursorObj.close()
        return 1,1
    except Error:
        return 0,Error 


