import mysql.connector

class DBManager:
    def __init__(self, host="localhost", user="root", password="", database="db_soporte_cibertec"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.inicializar_sistema()

    def inicializar_sistema(self):
        """Conecta al servidor local de XAMPP, crea la BD si no existe y luego la tabla."""
        try:
            conexion_servidor = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = conexion_servidor.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            conexion_servidor.commit()
            cursor.close()
            conexion_servidor.close()

            conexion_bd = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cursor_bd = conexion_bd.cursor()
            cursor_bd.execute('''
                CREATE TABLE IF NOT EXISTS tickets (
                    id_ticket VARCHAR(50) PRIMARY KEY,
                    descripcion TEXT,
                    fecha VARCHAR(50),
                    categoria VARCHAR(50)
                )
            ''')
            conexion_bd.commit()
            cursor_bd.close()
            conexion_bd.close()
            print(f"Instancia MySQL Activa: Base de datos '{self.database}' y tabla 'tickets' listas.")
            
        except Exception as e:
            print(f"Error crítico al inicializar MySQL: {e}")

    def insertar_ticket(self, ticket):
        """Operación DML: Inserta o actualiza un ticket con su categoría de IA."""
        try:
            conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cursor = conexion.cursor()
            
            query = '''
                REPLACE INTO tickets (id_ticket, descripcion, fecha, categoria)
                VALUES (%s, %s, %s, %s)
            '''
            valores = (ticket.id_ticket, ticket.descripcion, ticket.fecha, ticket.categoria)
            
            cursor.execute(query, valores)
            conexion.commit()
            
            cursor.close()
            conexion.close()
        except Exception as e:
            print(f"Error DML al insertar ticket {ticket.id_ticket}: {e}")

    def obtener_todos_los_tickets(self):
        """Operación DML: SELECT para recuperar registros (Útil para auditorías o reportes)."""
        try:
            conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cursor = conexion.cursor(dictionary=True) # Devuelve filas como diccionarios
            cursor.execute("SELECT * FROM tickets")
            resultados = cursor.fetchall()
            cursor.close()
            conexion.close()
            return resultados
        except Exception as e:
            print(f"Error DML al seleccionar tickets: {e}")
            return []