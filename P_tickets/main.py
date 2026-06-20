import os
import csv
from models.ticket import Ticket
from nlp.clasificador import ClasificadorIA
from database.db_manager import DBManager
from utils.preprocesamiento import limpiar_texto


def obtener_prioridad(texto):
    texto = texto.lower()

    if any(palabra in texto for palabra in [
        'servidor', 'caido', 'caída', 'hackeo',
        'virus', 'malware', 'ataque'
    ]):
        return 'CRITICA'

    elif any(palabra in texto for palabra in [
        'internet', 'red', 'wifi', 'conexion'
    ]):
        return 'ALTA'

    elif any(palabra in texto for palabra in [
        'correo', 'acceso', 'contraseña', 'password'
    ]):
        return 'MEDIA'

    return 'BAJA'


def main():
    print("=== SISTEMA CLASIFICADOR DE TICKETS CIBERTEC ===")
    
    # incicializamos
    db = DBManager()
    ia = ClasificadorIA()
    tickets_procesados = []
    directorio_base = os.path.dirname(os.path.abspath(__file__))
    ruta_entrada = os.path.join(directorio_base, 'data', 'tickets_entrada.csv')
    ruta_salida = os.path.join(directorio_base, 'data', 'reporte_salida.csv')

    # leemos CSV
    try:
        with open(ruta_entrada, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                # preprocesamiento funcional
                desc_limpia = limpiar_texto(fila['descripcion'])
                
                nuevo_ticket = Ticket(fila['id'], desc_limpia, fila['fecha'])
                
                # clasificación por la IA
                print(f"Clasificando ticket {nuevo_ticket.id_ticket}...")
                categoria_asignada = ia.clasificar_ticket(nuevo_ticket.descripcion)
                nuevo_ticket.asignar_categoria(categoria_asignada)

                prioridad = obtener_prioridad(nuevo_ticket.descripcion)
                nuevo_ticket.prioridad = prioridad


                # Base de Datos
                db.insertar_ticket(nuevo_ticket)
                tickets_procesados.append(nuevo_ticket)

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta:\n{ruta_entrada}")
    
    # resultados
    if tickets_procesados:
        try:
            with open(ruta_salida, mode='w', newline='', encoding='utf-8') as archivo_salida:
                campos = ['id_ticket', 'descripcion', 'fecha', 'categoria', 'prioridad']
                escritor = csv.DictWriter(archivo_salida, fieldnames=campos)
                escritor.writeheader()
                for t in tickets_procesados:
                    escritor.writerow({
                        'id_ticket': t.id_ticket,
                        'descripcion': t.descripcion,
                        'fecha': t.fecha,
                        'categoria': t.categoria,
                        'prioridad': t.prioridad
                    })
            print("===================================================")
            print("¡Proceso Finalizado! Reporte generado exitosamente.")
            print("INTEGRANTES:")
            print("Valerin Romero")
            print("Javier Peralta")
            print("Raul Chavez")
            print("===================================================")
        except Exception as e:
             print(f"Error al exportar: {e}")

if __name__ == "__main__":
    main()