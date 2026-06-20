from transformers import pipeline

class ClasificadorIA:
    def __init__(self):
        print("Cargando modelo de Hugging Face...")
        self.clasificador = pipeline(
            "zero-shot-classification", 
            model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli" 
        )
        # cargamos las categorias
        self.categorias = ["red", "hardware", "software", "acceso", "seguridad", "otras"] 

    def clasificar_ticket(self, texto):
        try:
            resultado = self.clasificador(texto, self.categorias)
            # retorna la categoría
            return resultado['labels'][0]
        except Exception as e:
            print(f"Error al clasificar: {e}")
            return "otras"