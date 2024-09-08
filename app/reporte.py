class Reporte:
    def __init__(self, id_reporte: int, tipo_reporte: str):
        self.id_reporte = id_reporte
        self.tipo_reporte = tipo_reporte

    def generar_reporte(self, mensaje: str):
        return f"Reporte generado: {mensaje}"

    def exportar_excel(self):
        print("Exportando reporte a Excel...")
