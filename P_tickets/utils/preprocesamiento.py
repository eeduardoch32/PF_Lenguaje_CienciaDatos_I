import re

# estandarizamos el texto a minúsculas y quitamos espacios extra
limpiar_texto = lambda texto: texto.strip().lower()

# limpiamos caracteres especiales
quitar_especiales = lambda texto: re.sub(r'[^\w\s]', '', texto)

def preprocesar_descripciones(lista_descripciones):
    # aplicamos map en lambdas para limpiar toda la lista en una
    descripciones_limpias = list(map(limpiar_texto, lista_descripciones))
    descripciones_finales = list(map(quitar_especiales, descripciones_limpias))
    return descripciones_finales