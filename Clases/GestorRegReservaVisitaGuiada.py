class GestorRegReservaVisitaGuiada():
    cantidadVisitantes = 0
    escuelaSeleccionada = ""
    exposicionesSeleccionadas = ""
    fechaHoraReserva = ""
    guiasSeleccionados= ""
    sedeSeleccionada = ""

    def __init__(self,cantidadVisitantes,escuelaSeleccionada,exposicionesSeleccionadas,fechaHoraReserva,guiasSeleccionados,sedeSeleccionada):
        self.cantidadVisitantes = cantidadVisitantes
        self.escuelaSeleccionada = escuelaSeleccionada
        self.exposicionesSeleccionadas = exposicionesSeleccionadas
        self.fechaHoraReserva = fechaHoraReserva
        self.guiasSeleccionados = guiasSeleccionados
        self.sedeSeleccionada = sedeSeleccionada