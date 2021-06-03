from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QTableWidgetItem,QComboBox,QSpinBox,QMessageBox,QTableView
from PyQt5.QtCore import QPropertyAnimation, Qt
from mainWindows import Ui_MainWindow
from PyQt5.QtGui import QIcon, QPixmap,QMouseEvent,QFont,QStandardItemModel
from datetime import date
from datetime import datetime
import os,sys
from conex import *
from valida_rut import *
from valida_fecha import *

#os.system("pyuic5 -x main_windows.ui -o mainWindows.py")
# pyinstaller --onefile --windowed --ico=logo.ico app.py

WINDOW_SIZE = 0

class mywindow(QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowTitle("UNIVERSIDAD DE CHILE")
        self.setWindowIcon(QIcon("images/logo.png"))
        self.ui.btn_menu.setIcon(QIcon("images/menu.png"))
        self.ui.btn_restore.setIcon(QIcon("images/restore.png"))
        self.ui.btn_minimize.setIcon(QIcon("images/minimize.png"))
        self.ui.btn_close.setIcon(QIcon("images/close.png"))
        self.ui.btn_home.setStyleSheet("QPushButton{background-image: url(images/home_2.png); background-repeat:none;padding-left: 30px;background-position: center left;border-left: 2px solid rgb(0,136,255);border-bottom: 2px solid rgb(0,136,255);}")
        self.ui.btn_venta.setStyleSheet("QPushButton{background-image: url(images/venta_2.png); background-repeat:none;padding-left: 30px;background-position: center left;}")
        self.ui.btn_historial.setStyleSheet("QPushButton{background-image: url(images/historial_2.png); background-repeat:none;padding-left: 35px;background-position: center left;}")
        self.ui.btn_stock.setStyleSheet("QPushButton{background-image: url(images/stock_2.png); background-repeat:none;padding-left: 30px;background-position: center left;}")
        
        ##################################################################################################################
        ################################### Eventos + Funcion ############################################################
        ##################################################################################################################
        self.ui.btn_menu.clicked.connect(self.slideLeftMenu)                 #btn Menu
        self.ui.btn_restore.clicked.connect(self.restore_or_maximize_window) #btn restore
        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())   #btn minimize
        self.ui.btn_close.clicked.connect(lambda: self.close())              #btn close
        self.ui.main_header.mouseMoveEvent = self.moveWindow                 #Movimiento de la ventana

        self.ui.stackedWidget.setCurrentWidget(self.ui.home_page)             #Carga Home como pagina inicial
        self.ui.btn_home.clicked.connect(self.cambioHome)                     #btn home
        self.ui.btn_venta.clicked.connect(self.cambioVenta)                   #btn venta
        self.ui.btn_historial.clicked.connect(self.cambioHistorial)           #btn historial
        self.ui.btn_stock.clicked.connect(self.cambioStock)                   #btn stock

        ################### Pagina Home #######################
        self.ui.tableVentasDiarias.setSelectionBehavior(QTableView.SelectRows)
        self.ui.tableStockHome.setSelectionBehavior(QTableView.SelectRows)

        #################### Pagina Venta #########################
        self.ui.btn_addItem.clicked.connect(self.addItem)
        self.ui.btn_aceptar.clicked.connect(self.aceptarDatos)
        self.ui.checkBox_confirmar.stateChanged.connect(lambda: self.checkBoxChange(self.ui.checkBox_confirmar,self.ui.btn_aceptar))
        self.ui.btn_eliminar.clicked.connect(self.eliminarFila)  

        ################### Pagina Historial #######################
        self.ui.comboBoxFiltroMes.addItem("Todos")
        for i in range(1,13):
            self.ui.comboBoxFiltroMes.addItem(str(i))
        self.ui.comboBoxFiltroMes.currentIndexChanged.connect(self.filtroMesHistorial)
        self.ui.lineEditFiltroNombreHistorial.textChanged.connect(self.filtroNombreHistorial)
        self.ui.lineEditFiltroRutHistorial.textChanged.connect(self.filtroRutHistorial)    

        self.ui.tableHistorial.setSelectionBehavior(QTableView.SelectRows)
        self.ui.tableHistorial.doubleClicked.connect(self.clickRowHistorial) 

        self.ui.btnEliminarVenta.clicked.connect(self.eliminarVenta)
        self.ui.checkBoxConfirmarEliminarVenta.stateChanged.connect(lambda: self.checkBoxChange(self.ui.checkBoxConfirmarEliminarVenta,self.ui.btnEliminarVenta))
        #################### Pagina Stock #########################
        self.ui.btn_aceptarActualizaStock.clicked.connect(self.aceptarActualizaLlavero)
        self.ui.checkBox_confirmarActualizaStock.stateChanged.connect(lambda: self.checkBoxChange(self.ui.checkBox_confirmarActualizaStock,self.ui.btn_aceptarActualizaStock))
        
        self.ui.btn_aceptarStock.clicked.connect(self.aceptarNuevoLlavero)
        self.ui.checkBox_confirmarStock.stateChanged.connect(lambda: self.checkBoxChange(self.ui.checkBox_confirmarStock,self.ui.btn_aceptarStock))

        self.ui.tableStock.setSelectionBehavior(QTableView.SelectRows)        
        
        # Exportar/Importar DB
        self.ui.btnSeleccionarDestinoDB.clicked.connect(self.seleccionaDirectorio)
        self.ui.btnExportarDB.clicked.connect(self.exportarDB)
        self.ui.checkBoxConfirmarNuevaDB.stateChanged.connect(lambda: self.checkBoxChange(self.ui.checkBoxConfirmarNuevaDB,self.ui.btnImportarDB))
        self.ui.btnSeleccionarArchivoDB.clicked.connect(self.seleccionaArchivo)
        self.ui.btnImportarDB.clicked.connect(self.importarDB)
        
        ##################################################################################################################
        #########################################  Ajustes ###############################################################  
        ##################################################################################################################

        ####### Tabla Stock Home
        self.ui.tableStockHome.setColumnWidth(0,420)
        self.ui.tableStockHome.setColumnWidth(1,170)
        ####### Tabla Cantidad Mensual Home
        self.ui.tableCantidadMensual.setColumnWidth(0,250)
        ####### Tabla Total Mensual Home
        self.ui.tableTotalMensual.setColumnWidth(0,250)
        
        ####### Tabla Venta datos Cliente
        self.ui.tableCliente.setColumnWidth(0,150)
        self.ui.tableCliente.setColumnWidth(1,200)
        self.ui.tableCliente.setColumnWidth(2,150)
        self.ui.tableCliente.setColumnWidth(3,250)
        self.ui.tableCliente.setColumnWidth(4,150)
        self.ui.tableCliente.setColumnWidth(5,150)
        self.ui.comboBox_Cliente = QComboBox()
        self.ui.comboBox_Cliente.addItem("Presencial")
        self.ui.comboBox_Cliente.addItem("Envío")
        self.ui.tableCliente.setCellWidget(0, 5, self.ui.comboBox_Cliente)
        ####### Tabla Venta Detalle
        self.ui.tableDetalle.setColumnWidth(0,220)
        self.ui.tableDetalle.setColumnWidth(1,120)
        self.ui.tableDetalle.setColumnWidth(2,160)       

        ####### Tabla Historial ventas historico
        self.ui.tableHistorial.setColumnWidth(0,130)
        self.ui.tableHistorial.setColumnWidth(1,160)
        self.ui.tableHistorial.setColumnWidth(2,85)
        self.ui.tableHistorial.setColumnWidth(3,80)
        self.ui.tableHistorial.setColumnWidth(4,70)
        ####### Tabla Cantidad Mensual Historial
        self.ui.tableCantidadMensual_Historial.setColumnWidth(0,250)
        ####### Tabla Total Mensual Historial
        self.ui.tableTotalMensual_Historial.setColumnWidth(0,250)
        ####### Tabla Historial datos venta
        self.ui.tableHistorialVentaSeleccionada.setColumnWidth(0,150)
        self.ui.tableHistorialVentaSeleccionada.setColumnWidth(1,200)
        self.ui.tableHistorialVentaSeleccionada.setColumnWidth(2,150)
        self.ui.tableHistorialVentaSeleccionada.setColumnWidth(3,250)
        self.ui.tableHistorialVentaSeleccionada.setColumnWidth(4,150)
        self.ui.tableHistorialVentaSeleccionada.setColumnWidth(5,150)
        ####### Tabla Historial detalle venta
        self.ui.tableHistorialDetalleVentaSeleccionada.setColumnWidth(0,220)
        self.ui.tableHistorialDetalleVentaSeleccionada.setColumnWidth(1,200)
        self.ui.tableHistorialDetalleVentaSeleccionada.setColumnWidth(2,150)
        self.ui.tableHistorialDetalleVentaSeleccionada.setColumnWidth(3,250)

        ######### Tabla Stock select
        self.ui.tableStock.setColumnWidth(0,200)
        self.ui.tableStock.setColumnWidth(1,150)
        self.ui.tableStock.setColumnWidth(2,250)
        ####### Tabla Stock Actualiza llavero
        self.ui.tableActualizaStock.setColumnWidth(0,200)
        self.ui.tableActualizaStock.setColumnWidth(1,150)
        self.ui.tableActualizaStock.setColumnWidth(2,250)
        ####### Tabla Stock nuevo llavero
        self.ui.tableLlavero.setColumnWidth(0,200)
        self.ui.tableLlavero.setColumnWidth(1,150)
        self.ui.tableLlavero.setColumnWidth(2,250)
        
        ####################### Cambio borde boton menú seleccionado ####################
        for w in self.ui.left_side_menu.findChildren(QPushButton):
            w.clicked.connect(self.applyButtonStyle)

        ##################################################################################################################
        self.ui.comboBoxLlavero = []
        self.ui.comboBoxLlaveroStock = []
        self.ui.spinBoxCantidad = []
        self.ui.btnDetalle = []  
        self.ui.idVentaEliminar = ""

        self.selectHome()
       

    def filtroMesHistorial(self):
        nombre = str(self.ui.lineEditFiltroNombreHistorial.text())
        rut = str(self.ui.lineEditFiltroRutHistorial.text())
        mes = str(self.ui.comboBoxFiltroMes.currentText())
        if mes == "Todos":
            mes = ""
        else:
            mes = "-"+mes+"-"
        self.selectHistorial(mes,nombre,rut)

    def filtroNombreHistorial(self):
        nombre = str(self.ui.lineEditFiltroNombreHistorial.text())
        rut = str(self.ui.lineEditFiltroRutHistorial.text())
        mes = str(self.ui.comboBoxFiltroMes.currentText())
        if mes == "Todos":
            mes = ""
        else:
            mes = "-"+mes+"-"
        self.selectHistorial(mes,nombre,rut)
    def filtroRutHistorial(self):
        nombre = str(self.ui.lineEditFiltroNombreHistorial.text())
        rut = str(self.ui.lineEditFiltroRutHistorial.text())
        mes = str(self.ui.comboBoxFiltroMes.currentText())
        if mes == "Todos":
            mes = ""
        else:
            mes = "-"+mes+"-"
        self.selectHistorial(mes,nombre,rut)

    def cambioHome(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.home_page) #Carga pagina
        self.selectHome() #Carga Tabla
    def cambioVenta(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.venta_page)  #Carga pagina

        self.eliminarFila() #Limpia filas para despues actualizar contenido
        self.addItem()  #carga un item inicial

        today = date.today()#Día actual
        fecha = str(today.day)+"-"+str(today.month)+"-"+str(today.year)
        self.ui.tableCliente.setItem(0 , 0, QTableWidgetItem(fecha))
    def cambioHistorial(self):

        
        today = date.today()
        mesActual = str(today.month)
        self.ui.comboBoxFiltroMes.setCurrentIndex(int(mesActual))

        self.ui.stackedWidget.setCurrentWidget(self.ui.historial_page) #Carga pagina
        nombre = str(self.ui.lineEditFiltroNombreHistorial.text())
        rut = str(self.ui.lineEditFiltroRutHistorial.text())
        mes = str(self.ui.comboBoxFiltroMes.currentText())

        if mes == "Todos":
            mes = ""
        else:
            mes = "-"+mes+"-"
        self.selectHistorial(mes,nombre,rut) #Carga tabla historial
    def cambioStock(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.stock_page)  #carga pagina
        self.selectStock()  #carga tabla stock

    def checkBoxChange(self,checkbox,btn):
        if checkbox.isChecked(): #Si el checkbox esta marcado
            btn.setEnabled(True)    #habilita btn
        else:
            btn.setEnabled(False)   #deshabilita btn

    def addItem(self):

        data = selectLlaveros()
        
        if data[0] == 0:
            self.dbError("Ha ocurrido un error al hacer una peticion en la BD")
            return
        else:
            data = data[1]

        rowPosition = self.ui.tableDetalle.rowCount()
        self.ui.tableDetalle.insertRow(rowPosition)
        self.ui.comboBoxLlavero.append(QComboBox())
        for i in range(len(data)):
            self.ui.comboBoxLlavero[rowPosition].addItem(data[i]["nombre"])
        self.ui.comboBoxLlavero[rowPosition].currentIndexChanged.connect(lambda: self.llaveroCambiado(rowPosition))
        self.ui.tableDetalle.setCellWidget(rowPosition, 0, self.ui.comboBoxLlavero[rowPosition])

        self.ui.spinBoxCantidad.append(QSpinBox())
        self.ui.spinBoxCantidad[rowPosition].setMinimum(1)

        self.ui.tableDetalle.setCellWidget(rowPosition, 1, self.ui.spinBoxCantidad[rowPosition])
        self.ui.spinBoxCantidad[rowPosition].valueChanged.connect(lambda: self.cantidadCambiada(rowPosition))

        if len(data) == 0:
            self.ui.tableDetalle.setItem(rowPosition , 2, QTableWidgetItem("0")) #SubTotal
            self.ui.output_total.setText("0")

        else:
            self.ui.tableDetalle.setItem(rowPosition , 2, QTableWidgetItem(str(data[0]["precio"]))) #SubTotal

            total = 0
            for i in range(rowPosition + 1):
                total += int(self.ui.tableDetalle.item(i, 2).text())
            if rowPosition == 0:
                self.ui.output_total.setText(str(data[0]["precio"]))
            else:
                self.ui.output_total.setText(str(total))
                   
    def eliminarFila(self):
        if self.ui.tableDetalle.rowCount() > 0:
            rowTotalAntes = self.ui.tableDetalle.rowCount() - 1 #Posicion de la ultima fila antes de borrar
            self.ui.tableDetalle.removeRow(rowTotalAntes) #Elimina la ultima
            self.ui.comboBoxLlavero.pop(rowTotalAntes) #Elimina el ultimo objetio llavero de la lista
            self.ui.spinBoxCantidad.pop(rowTotalAntes) #Elimina el ultimo objetio cantidad de la lista

            rowPosition = self.ui.tableDetalle.rowCount()
            total = 0
            if rowPosition == 0:
                self.ui.output_total.setText("0")
                return
            if rowPosition == 1:
                total = int(self.ui.tableDetalle.item(0, 2).text())
                self.ui.output_total.setText(str(total))
                return
            else:
                for i in range(rowPosition):
                    total += int(self.ui.tableDetalle.item(i, 2).text())
                self.ui.output_total.setText(str(total))  
                return 
        else: 
            return

    def llaveroCambiado(self,row):
        data = selectLlaveros()
        if data[0] == 0:
            self.dbError("Ha ocurrido un error al hacer una peticion en la BD")
            return
        else:
            data = data[1]

        i = self.ui.comboBoxLlavero[row].currentIndex()
        self.ui.spinBoxCantidad[row].setValue(1)
        self.ui.tableDetalle.setItem(row , 2, QTableWidgetItem(str(data[i]["precio"])))

        rowPosition = self.ui.tableDetalle.rowCount()
        total = 0
        if rowPosition == 1:
            total = int(self.ui.tableDetalle.item(0, 2).text())
            self.ui.output_total.setText(str(total))
        else:
            for i in range(rowPosition):
                total += int(self.ui.tableDetalle.item(i, 2).text())
            self.ui.output_total.setText(str(total))
        
    def cantidadCambiada(self,row):
        data = selectLlaveros()
        if data[0] == 0:
            self.dbError("Ha ocurrido un error al hacer una peticion en la BD")
            return
        else:
            data = data[1]

        i = self.ui.comboBoxLlavero[row].currentIndex()
        self.ui.tableDetalle.setItem(row , 2, QTableWidgetItem(str(data[i]["precio"] * self.ui.spinBoxCantidad[row].value())))

        rowPosition = self.ui.tableDetalle.rowCount()
        total = 0
        if rowPosition == 1:
            total = int(self.ui.tableDetalle.item(0, 2).text())
            self.ui.output_total.setText(str(total))
        else:
            for i in range(rowPosition):
                total += int(self.ui.tableDetalle.item(i, 2).text())
            self.ui.output_total.setText(str(total))

    def aceptarDatos(self): 
        
        fecha = str(self.ui.tableCliente.item(0, 0).text())
        nomCliente = str(self.ui.tableCliente.item(0, 1).text())
        rutCliente = str(self.ui.tableCliente.item(0, 2).text())
        dirCliente = str(self.ui.tableCliente.item(0, 3).text())
        telCliente = str(self.ui.tableCliente.item(0, 4).text())
        tipoEntrega = str(self.ui.comboBox_Cliente.currentText())
        
        rutCliente = rutCliente.replace(".","")
        rutCliente = rutCliente.replace("-","")
        if validaFecha(fecha)[0] == False:
            QMessageBox.information(self, 'Error', 'Fecha inválida. Usar formato dd-mm-aaaa')
            return
        else:
            fecha = validaFecha(fecha)[1]
        if nomCliente == "" or nomCliente.replace(" ","") == "":
            QMessageBox.information(self, 'Error', 'Nombre Cliente vacío')
            return
        if tipoEntrega == "Envío":
            if rutCliente == "" or rutCliente.replace(" ","") == "":
                QMessageBox.information(self, 'Error', 'Rut Cliente vacío')
                return
            elif valida_rut(rutCliente) == 0:
                QMessageBox.information(self, 'Error', 'Rut Cliente inválido')
                return
            elif dirCliente == "" or dirCliente.replace(" ","") == "": 
                QMessageBox.information(self, 'Error', 'Dirección Cliente vacío')
                return
            elif telCliente == "" or telCliente.replace(" ","") == "": 
                QMessageBox.information(self, 'Error', 'Teléfono Cliente vacío')
                return
        if tipoEntrega == "Presencial":
            if rutCliente == "" or rutCliente.replace(" ","") == "":
                pass
            elif valida_rut(rutCliente) == 0:
                QMessageBox.information(self, 'Error', 'Rut Cliente inválido')
                return

        if self.ui.tableDetalle.rowCount() == 0:
            QMessageBox.information(self, 'Error', 'Detalle vacío')
            return
        
        aDetalle = []
        total = 0
        for row in range(self.ui.tableDetalle.rowCount()):
            if self.ui.comboBoxLlavero[row].currentText() == "" or self.ui.comboBoxLlavero[row].currentText().replace(" ","") == "":
                QMessageBox.information(self, 'Error', 'Llavero vacío')
                return
            aDetalle.append({"llavero":self.ui.comboBoxLlavero[row].currentText(),"cantidad":self.ui.spinBoxCantidad[row].value(),"subtotal":self.ui.tableDetalle.item(row, 2).text()})
            total += int(self.ui.tableDetalle.item(row, 2).text())

        for i in range(len(aDetalle)):
            for j in range(len(aDetalle)):
                if i!=j and aDetalle[j]["llavero"] == aDetalle[i]["llavero"]:
                    QMessageBox.information(self, 'Error', 'Llavero repetido')
                    return

        Datos = {"nomCliente":nomCliente,"rutCliente":rutCliente,"dirCliente":dirCliente,"telCliente":telCliente,"tipoEntrega":tipoEntrega,"fecha":fecha,"aDetalle":aDetalle,"total":str(total)}

        respuesta = insertVenta(Datos)
        if respuesta[0] == 0:
            self.dbError("Ha ocurrido un error al ingresar la venta en la BD")
        else:
            QMessageBox.information(self, 'Venta Ingresada', 'Venta Ingresada')

        while self.ui.tableDetalle.rowCount() > 0:
            self.eliminarFila()
        
        self.ui.tableCliente.setItem(0, 1, QTableWidgetItem(""))
        self.ui.tableCliente.setItem(0, 2, QTableWidgetItem(""))
        self.ui.tableCliente.setItem(0, 3, QTableWidgetItem(""))
        self.ui.tableCliente.setItem(0, 4, QTableWidgetItem(""))
        self.addItem()
        self.ui.checkBox_confirmar.setChecked(False)
        return

    def aceptarActualizaLlavero(self):
           
        nombre = self.ui.comboBoxLlaveroStock[0].currentText()
        precio = self.ui.tableActualizaStock.item(0, 1).text()
        stock = self.ui.tableActualizaStock.item(0, 2).text()

        if nombre == "" or nombre.replace(" ","") == "":
            QMessageBox.information(self, 'Error', 'Llavero vacío')
            return
        elif precio == "" or precio.replace(" ","") == "":
            QMessageBox.information(self, 'Error', 'Precio vacío')
            return
        elif not precio.isnumeric():
            QMessageBox.information(self, 'Error', 'El precio ingresado no escorrecto')
            return
        if stock == "" or stock.replace(" ","") == "":
            QMessageBox.information(self, 'Error', 'Stock vacío')
            return
        elif not stock.isnumeric():
            QMessageBox.information(self, 'Error', 'El stock ingresado no es correcto')
            return

        Datos = {"nombre":nombre,"precio":precio,"stock":stock}

        respuesta = actualizarLlavero(Datos)
        if respuesta[0] == 0:
            self.dbError("Ha ocurrido un error al ingresar la venta en la BD")
        else:
            QMessageBox.information(self, 'Llavero actualizado', 'Llavero actualizado')

        self.ui.tableActualizaStock.setItem(0, 2, QTableWidgetItem(""))
        self.ui.checkBox_confirmarActualizaStock.setChecked(False)
        self.selectStock()

    def aceptarNuevoLlavero(self):
        data = selectLlaveros()
        
        if data[0] == 0:
            self.dbError("Ha ocurrido un error al hacer una peticion en la BD")
            return
        else:
            data = data[1]

        nombre = self.ui.tableLlavero.item(0, 0).text()
        precio = self.ui.tableLlavero.item(0, 1).text()
        stock = self.ui.tableLlavero.item(0, 2).text()

        for i in range(len(data)):
            if data[i]["nombre"] == nombre:
                QMessageBox.information(self, 'Error', 'Ya existe un llavero con ese nombre')
                return

        if nombre == "" or nombre.replace(" ","") == "":
            QMessageBox.information(self, 'Error', 'Nombre del llavero vacío')
            return
        if precio == "" or precio.replace(" ","") == "":
            QMessageBox.information(self, 'Error', 'Precio vacío')
            return
        elif not precio.isnumeric():
            QMessageBox.information(self, 'Error', 'El precio ingresado no escorrecto')
            return
        if stock == "" or stock.replace(" ","") == "":
            QMessageBox.information(self, 'Error', 'Stock vacío')
            return
        elif not stock.isnumeric():
            QMessageBox.information(self, 'Error', 'El stock ingresado no es correcto')
            return

        Datos = {"nombre":nombre,"precio":precio,"stock":stock}

        respuesta = insertarLlavero(Datos)
        if respuesta[0] == 0:
            self.dbError("Ha ocurrido un error al ingresar la venta en la BD")
        else:
            QMessageBox.information(self, 'Llavero ingresado', 'Llavero ingresado')

        self.ui.tableLlavero.setItem(0, 0, QTableWidgetItem(""))
        self.ui.tableLlavero.setItem(0, 1, QTableWidgetItem(""))
        self.ui.tableLlavero.setItem(0, 2, QTableWidgetItem(""))
        self.ui.checkBox_confirmarStock.setChecked(False)
        self.selectStock()
            
    def dbError(self,error):
        QMessageBox.information(self, 'Error', error)
        return
    
    def selectHome(self):
        today = date.today()
        mesActual = str(today.month)
        yearActual = str(today.year)

        data = selectLlaveros()
        dineroMes = selectDineroTotalMes("-" + mesActual + "-")
        cantidadMes = selectCantidadTotalMes("-" + mesActual + "-")

        if data[0] == 0 or dineroMes[0] == 0 or cantidadMes[0] == 0:
            self.dbError("Ha ocurrido un error al hacer una peticion en la BD")
            return
        else:
            data = data[1]
            dineroMes = dineroMes[1]
            cantidadMes = cantidadMes[1]

        while self.ui.tableStockHome.rowCount() > 0:
            rowTotalAntes = self.ui.tableStockHome.rowCount() - 1 
            self.ui.tableStockHome.removeRow(rowTotalAntes) #Limpia filas para despues actualizar contenido

        while self.ui.tableVentasDiarias.rowCount() > 0:
            rowTotalAntes = self.ui.tableVentasDiarias.rowCount() - 1 
            self.ui.tableVentasDiarias.removeRow(rowTotalAntes) #Limpia filas para despues actualizar contenido

        while self.ui.tableVentasDiarias.columnCount() > 0:
            columnTotalAntes = self.ui.tableVentasDiarias.columnCount() - 1
            self.ui.tableVentasDiarias.removeColumn(columnTotalAntes) #Limpia columnas para despues actualizar contenido

        for i in range(len(data)):
            rowPosition = self.ui.tableStockHome.rowCount()
            self.ui.tableStockHome.insertRow(rowPosition)
            
            item_1 = QTableWidgetItem(str(data[i]["nombre"]))
            item_2 = QTableWidgetItem(str(data[i]["cantidad"]))
            font = QFont()
            font.setFamily("MS Shell Dlg 2")
            font.setPointSize(12)
            item_1.setFont(font)
            item_2.setFont(font)
            item_2.setTextAlignment(Qt.AlignCenter)

            self.ui.tableStockHome.setItem(rowPosition , 0, item_1)
            self.ui.tableStockHome.setItem(rowPosition , 1, item_2)

            column_index = self.ui.tableVentasDiarias.columnCount() #Agrega cantidad de columas = cantidad de llaveros
            self.ui.tableVentasDiarias.setColumnCount(column_index + 1)

            header_item = QTableWidgetItem(str(data[i]["nombre"]))
            font = QFont("MS Shell Dlg 2", 11)
            header_item.setFont(font)
            self.ui.tableVentasDiarias.setHorizontalHeaderItem(column_index, header_item)
            self.ui.tableVentasDiarias.setColumnWidth(rowPosition,150)

        column_index = self.ui.tableVentasDiarias.columnCount() #Ultima columna para la cantidad de ventas 
        self.ui.tableVentasDiarias.setColumnCount(column_index + 1)
        header_item = QTableWidgetItem("Cantidad de llaveros")
        font = QFont("MS Shell Dlg 2", 11)
        font.setBold(True)
        header_item.setFont(font)
        self.ui.tableVentasDiarias.setHorizontalHeaderItem(column_index, header_item)
        self.ui.tableVentasDiarias.setColumnWidth(column_index,150)

        column_index = self.ui.tableVentasDiarias.columnCount() #Ultima columna para la cantidad de ventas 
        self.ui.tableVentasDiarias.setColumnCount(column_index + 1)
        header_item = QTableWidgetItem("Total ventas diarias")
        font = QFont("MS Shell Dlg 2", 11)
        font.setBold(True)
        header_item.setFont(font)
        self.ui.tableVentasDiarias.setHorizontalHeaderItem(column_index, header_item)
        self.ui.tableVentasDiarias.setColumnWidth(column_index,160)

        if dineroMes[0]["total"] == None:
            item_1 = QTableWidgetItem("$ 0")
            item_2 = QTableWidgetItem("0")
        else:
            item_1 = QTableWidgetItem("$ "+str(dineroMes[0]["total"]))
            item_2 = QTableWidgetItem(str(cantidadMes[0]["total"]))
        item_1.setFont(font)
        item_2.setFont(font)
        item_1.setTextAlignment(Qt.AlignCenter)
        item_2.setTextAlignment(Qt.AlignCenter)
        self.ui.tableTotalMensual.setItem(0 , 0, item_1)
        self.ui.tableCantidadMensual.setItem(0 , 0, item_2)

        if( (int(yearActual) % 400 == 0) or ( int(yearActual) % 100 != 0 and int(yearActual) % 4 == 0)): #Este sector valida si es año bisiesto
            listames=[31,29,31,30,31,30,31,31,30,31,30,31]
        else:
            listames=[31,28,31,30,31,30,31,31,30,31,30,31]

        cantidadDeDias = listames[int(mesActual)-1] # Cantidad de dias que tiene el mes actual

        for i in range(1,cantidadDeDias+1):
            rowPosition = self.ui.tableVentasDiarias.rowCount() #Agrega filas = cantidad de dias del mes
            self.ui.tableVentasDiarias.insertRow(rowPosition)
            header_item = QTableWidgetItem(str(i)+"-"+str(mesActual)+"-"+str(yearActual))
            font = QFont("MS Shell Dlg 2", 11)
            header_item.setFont(font)
            self.ui.tableVentasDiarias.setVerticalHeaderItem(rowPosition, header_item)

            dataPorDia = selectVentasPorDia(str(i)+"-"+str(mesActual)+"-"+str(yearActual))
            if dataPorDia[0] == 0:
                self.dbError("Ha ocurrido un error al hacer una peticion en la BD")
                return
            else:
                dataPorDia = dataPorDia[1]

            if dataPorDia["existe"]:
                for i in range(len(data)):
                    if str(data[i]["nombre"]) in dataPorDia:
                        font = QFont("MS Shell Dlg 2", 11)
                        item_1 = QTableWidgetItem(str(dataPorDia[str(data[i]["nombre"])]))
                        item_1.setFont(font)
                        item_1.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableVentasDiarias.setItem(rowPosition , i, item_1)
                item_2 = QTableWidgetItem(QTableWidgetItem(str(dataPorDia["cantidad"])))
                item_2.setFont(font)
                item_2.setTextAlignment(Qt.AlignCenter)
                self.ui.tableVentasDiarias.setItem(rowPosition , i+1, item_2)
                item_3 = QTableWidgetItem("$ "+str(dataPorDia["total"]))
                item_3.setFont(font)
                self.ui.tableVentasDiarias.setItem(rowPosition , i+2, item_3)
       
    def selectStock(self):
        data = selectLlaveros()
        if data[0] == 0:
            self.dbError("Ha ocurrido un error al hacer una peticion en la BD")
            return
        else:
            data = data[1]

        while self.ui.tableStock.rowCount() > 0:
            rowTotalAntes = self.ui.tableStock.rowCount() - 1
            self.ui.tableStock.removeRow(rowTotalAntes)
        for i in range(len(data)):
            rowPosition = self.ui.tableStock.rowCount()
            self.ui.tableStock.insertRow(rowPosition)
            self.ui.tableStock.setItem(rowPosition , 0, QTableWidgetItem(str(data[i]["nombre"])))
            self.ui.tableStock.setItem(rowPosition , 1, QTableWidgetItem(str(data[i]["precio"])))
            self.ui.tableStock.setItem(rowPosition , 2, QTableWidgetItem(str(data[i]["cantidad"])))

        if len(self.ui.comboBoxLlaveroStock) > 0:
            self.ui.comboBoxLlaveroStock.pop(0)
        self.ui.comboBoxLlaveroStock.append(QComboBox())

        for i in range(len(data)):
            self.ui.comboBoxLlaveroStock[0].addItem(data[i]["nombre"])
        self.ui.comboBoxLlaveroStock[0].currentIndexChanged.connect(lambda: self.llaveroCambiadoStock(0))
        self.ui.tableActualizaStock.setCellWidget(0, 0, self.ui.comboBoxLlaveroStock[0])

        if len(data) == 0:
            self.ui.tableActualizaStock.setItem(0 , 1, QTableWidgetItem("0"))
        else:
            self.ui.tableActualizaStock.setItem(0 , 1, QTableWidgetItem(str(data[0]["precio"])))

    def llaveroCambiadoStock(self,row):
        data = selectLlaveros()
        if data[0] == 0:
            self.dbError("Ha ocurrido un error al hacer una peticion en la BD")
            return
        else:
            data = data[1]

        i = self.ui.comboBoxLlaveroStock[row].currentIndex()
        self.ui.tableActualizaStock.setItem(row , 1, QTableWidgetItem(str(data[i]["precio"])))

    def selectHistorial(self,mes,nombre,rut):

        dineroMes = selectDineroTotalMes(mes)
        cantidadMes = selectCantidadTotalMes(mes)            
        
        data = selectVentas(mes,nombre,rut)
        if data[0] == 0 or dineroMes[0] == 0 or cantidadMes[0] == 0:
            self.dbError("Ha ocurrido un error al hacer una peticion en la BD")
            return
        else:
            data = data[1]
            dineroMes = dineroMes[1]
            cantidadMes = cantidadMes[1]

        while self.ui.tableHistorial.rowCount() > 0:
            rowTotalAntes = self.ui.tableHistorial.rowCount() - 1
            self.ui.tableHistorial.removeRow(rowTotalAntes)
        for i in range(len(data)):
            rowPosition = self.ui.tableHistorial.rowCount()
            self.ui.tableHistorial.insertRow(rowPosition)
            self.ui.tableHistorial.setItem(rowPosition , 0, QTableWidgetItem(str(data[i]["fecha"])))
            self.ui.tableHistorial.setItem(rowPosition , 1, QTableWidgetItem(str(data[i]["nom_cliente"])))
            self.ui.tableHistorial.setItem(rowPosition , 2, QTableWidgetItem(str(data[i]["tipoEntrega"])))
            self.ui.tableHistorial.setItem(rowPosition , 3, QTableWidgetItem(str(data[i]["cantidad"])))
            self.ui.tableHistorial.setItem(rowPosition , 4, QTableWidgetItem(str(data[i]["total"])))

            header_item = QTableWidgetItem(str(data[i]["id_venta"]))
            self.ui.tableHistorial.setVerticalHeaderItem(rowPosition, header_item)

        font = QFont("MS Shell Dlg 2", 11)
        font.setBold(True)

        if dineroMes[0]["total"] == None:
            item_1 = QTableWidgetItem("$ 0")
            item_2 = QTableWidgetItem("0")
        else:
            item_1 = QTableWidgetItem("$ "+str(dineroMes[0]["total"]))
            item_2 = QTableWidgetItem(str(cantidadMes[0]["total"]))
        item_1.setFont(font)
        item_2.setFont(font)
        item_1.setTextAlignment(Qt.AlignCenter)
        item_2.setTextAlignment(Qt.AlignCenter)
        self.ui.tableTotalMensual_Historial.setItem(0 , 0, item_1)
        self.ui.tableCantidadMensual_Historial.setItem(0 , 0, item_2)

    def eliminarVenta(self):
        if self.ui.idVentaEliminar == "":
            QMessageBox.information(self, 'Error', 'Ninguna venta seleccionada')
            return
        else:
            res = eliminaVenta(self.ui.idVentaEliminar)
            if res[0] == 0:
                self.dbError("Ha ocurrido un error al hacer una peticion en la BD")
                return
            else:
                res = res[1]   
            QMessageBox.information(self, 'Venta Eliminada', 'Se ha eliminado la venta')
            self.ui.idVentaEliminar = ""            
            self.ui.checkBoxConfirmarEliminarVenta.setChecked(False)
            while self.ui.tableHistorialVentaSeleccionada.rowCount() > 0:
                rowTotalAntes = self.ui.tableHistorialVentaSeleccionada.rowCount() - 1
                self.ui.tableHistorialVentaSeleccionada.removeRow(rowTotalAntes)
            while self.ui.tableHistorialDetalleVentaSeleccionada.rowCount() > 0:
                rowTotalAntes = self.ui.tableHistorialDetalleVentaSeleccionada.rowCount() - 1
                self.ui.tableHistorialDetalleVentaSeleccionada.removeRow(rowTotalAntes)
            self.cambioHistorial()

    def clickRowHistorial(self, index):
        row = index.row()
        id_venta = self.ui.tableHistorial.verticalHeaderItem(row).text()

        self.ui.idVentaEliminar = id_venta

        data = selectDetalleWhereID(id_venta)
        if data[0] == 0:
            self.dbError("Ha ocurrido un error al hacer una peticion en la BD")
            return
        else:
            dataCliente = data[1][0]
            dataLlaveros = data[1][1]

        while self.ui.tableHistorialVentaSeleccionada.rowCount() > 0:
            rowTotalAntes = self.ui.tableHistorialVentaSeleccionada.rowCount() - 1
            self.ui.tableHistorialVentaSeleccionada.removeRow(rowTotalAntes)
        for i in range(len(dataCliente)):
            rowPosition = self.ui.tableHistorialVentaSeleccionada.rowCount()
            self.ui.tableHistorialVentaSeleccionada.insertRow(rowPosition)
            self.ui.tableHistorialVentaSeleccionada.setItem(rowPosition , 0, QTableWidgetItem(str(dataCliente[i]["fecha"])))
            self.ui.tableHistorialVentaSeleccionada.setItem(rowPosition , 1, QTableWidgetItem(str(dataCliente[i]["nom_cliente"])))
            self.ui.tableHistorialVentaSeleccionada.setItem(rowPosition , 2, QTableWidgetItem(str(dataCliente[i]["rut_cliente"])))
            self.ui.tableHistorialVentaSeleccionada.setItem(rowPosition , 3, QTableWidgetItem(str(dataCliente[i]["dir_cliente"])))
            self.ui.tableHistorialVentaSeleccionada.setItem(rowPosition , 4, QTableWidgetItem(str(dataCliente[i]["tel_cliente"])))
            self.ui.tableHistorialVentaSeleccionada.setItem(rowPosition , 5, QTableWidgetItem(str(dataCliente[i]["tipoEntrega"])))
            self.ui.tableHistorialVentaSeleccionada.setItem(rowPosition , 6, QTableWidgetItem(str(dataCliente[i]["cantidad"])))
            self.ui.tableHistorialVentaSeleccionada.setItem(rowPosition , 7, QTableWidgetItem(str(dataCliente[i]["total"])))

        while self.ui.tableHistorialDetalleVentaSeleccionada.rowCount() > 0:
            rowTotalAntes = self.ui.tableHistorialDetalleVentaSeleccionada.rowCount() - 1
            self.ui.tableHistorialDetalleVentaSeleccionada.removeRow(rowTotalAntes)
        for i in range(len(dataLlaveros)):
            rowPosition = self.ui.tableHistorialDetalleVentaSeleccionada.rowCount()
            self.ui.tableHistorialDetalleVentaSeleccionada.insertRow(rowPosition)
            self.ui.tableHistorialDetalleVentaSeleccionada.setItem(rowPosition , 0, QTableWidgetItem(str(dataLlaveros[i]["nombre"])))
            self.ui.tableHistorialDetalleVentaSeleccionada.setItem(rowPosition , 1, QTableWidgetItem(str(dataLlaveros[i]["cantidad"])))
            self.ui.tableHistorialDetalleVentaSeleccionada.setItem(rowPosition , 2, QTableWidgetItem(str(dataLlaveros[i]["precio"])))
            self.ui.tableHistorialDetalleVentaSeleccionada.setItem(rowPosition , 3, QTableWidgetItem(str(dataLlaveros[i]["subtotal"])))
            
    def slideLeftMenu(self):
        width = self.ui.left_side_menu.width()
        if width == 50:
            newWidth = 127
        else:
            newWidth = 50
        self.animation = QPropertyAnimation(self.ui.left_side_menu, b'minimumWidth')
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InQuart)
        self.animation.start()

    def restore_or_maximize_window(self):
        global WINDOW_SIZE
        win_status = WINDOW_SIZE

        if win_status == 0:
            WINDOW_SIZE = 1
            self.showMaximized()
        else:
            WINDOW_SIZE = 0
            self.showNormal()

    def moveWindow(self,e):
        if self.isMaximized() == False:
            if e.buttons() == Qt.LeftButton:
                self.move(self.pos() + e.globalPos() - self.clickPosition)
                self.clickPosition = e.globalPos()
                e.accept()
                
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def applyButtonStyle(self):
        borderStyle = "background-position: center left;border-left: 2px solid rgb(0,136,255);border-bottom: 2px solid rgb(0,136,255);"
        for w in self.ui.left_side_menu.findChildren(QPushButton):
            if w.objectName() != self.sender().objectName():
                defaultStyle = w.styleSheet().replace(borderStyle,"background-position: center left;")
                w.setStyleSheet(defaultStyle)
        
        if borderStyle in self.sender().styleSheet():
            pass
        else:
            newStyle = self.sender().styleSheet().replace("background-position: center left;",borderStyle)
            self.sender().setStyleSheet(newStyle)
        return
    
    def seleccionaDirectorio(self):
        fileName = QFileDialog.getExistingDirectory(self, 'Select directory')
        if fileName:
            self.ui.btnExportarDB.setEnabled(True)
            self.ui.labelRutaDestinoDB.setText(fileName)

    def seleccionaArchivo(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()","","All Files (*)",options=options)
        if fileName:
            self.ui.labelRutaArchivoDB.setText(fileName)

    def importarDB(self):
        rutaArchivo = str(self.ui.labelRutaArchivoDB.text())
        if rutaArchivo.replace(rutaArchivo[:-3],"") != ".db":
            QMessageBox.information(self, 'Error', 'Archivo seleccionado no corresponde a una DB')
            return
        else:
            fDB = open(rutaArchivo,"rb")
            fDestino = open("llaveros.db","wb")
            fDestino.write(fDB.read())
            self.ui.checkBoxConfirmarNuevaDB.setChecked(False)
            self.ui.labelRutaArchivoDB.setText("")
            self.selectStock()
            QMessageBox.information(self, 'DB importada', 'DB importada')
    def exportarDB(self):
        rutaDestino = str(self.ui.labelRutaDestinoDB.text())
        fDB = open("llaveros.db","rb")
        fDestino = open(rutaDestino + "/llaveros.db","wb")
        fDestino.write(fDB.read())
        self.ui.btnExportarDB.setEnabled(False)
        self.ui.labelRutaDestinoDB.setText("")
        QMessageBox.information(self, 'DB exportada', 'DB exportada')
def window():
    app = QApplication(sys.argv)
    win = mywindow()
    win.show()
    sys.exit(app.exec())
window()