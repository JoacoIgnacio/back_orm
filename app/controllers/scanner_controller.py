import cv2
import numpy as np
import base64
from PIL import Image
import io

def ordenar_contornos(contornos):
    return sorted(contornos, key=lambda c: (cv2.boundingRect(c)[1], cv2.boundingRect(c)[0]))

def mejorar_brillo(imagen_gray):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(imagen_gray)

def aumentar_brillo(imagen_gray, alpha=1.2, beta=30):
    return cv2.convertScaleAbs(imagen_gray, alpha=alpha, beta=beta)

def encontrar_marco(imagen):
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    _, umbral = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contornos = sorted(contornos, key=cv2.contourArea, reverse=True)
    for c in contornos:
        peri = cv2.arcLength(c, True)
        aprox = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(aprox) == 4:
            return aprox.reshape(4, 2)
    return None

def ordenar_puntos(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    d = np.diff(pts, axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    rect[1] = pts[np.argmin(d)]
    rect[3] = pts[np.argmax(d)]
    return rect

def recortar_area(imagen, puntos):
    rect = ordenar_puntos(puntos)
    (tl, tr, br, bl) = rect
    ancho = max(int(np.linalg.norm(br - bl)), int(np.linalg.norm(tr - tl)))
    alto = max(int(np.linalg.norm(tr - br)), int(np.linalg.norm(tl - bl)))
    dst = np.array([[0, 0], [ancho - 1, 0], [ancho - 1, alto - 1], [0, alto - 1]], dtype="float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    return cv2.warpPerspective(imagen, M, (ancho, alto))

def agrupar_por_filas(contornos, tolerancia=25):
    filas = []
    contornos = sorted(contornos, key=lambda c: cv2.boundingRect(c)[1])
    for contorno in contornos:
        x, y, w, h = cv2.boundingRect(contorno)
        agregado = False
        for fila in filas:
            _, fy, _, fh = cv2.boundingRect(fila[0])
            if abs(y - fy) < tolerancia:
                fila.append(contorno)
                agregado = True
                break
        if not agregado:
            filas.append([contorno])
    return filas

def extraer_respuestas(imagen_recortada, max_alternativas,answer_key):
    gris = cv2.cvtColor(imagen_recortada, cv2.COLOR_BGR2GRAY)
    gris = aumentar_brillo(gris, alpha=1.2, beta=20)

    umbral = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 57, 5)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    umbral = cv2.dilate(umbral, kernel, iterations=1)

    h, w = umbral.shape
    margen = 5
    umbral = umbral[margen:h - margen, margen:w - margen]
    imagen_recortada = imagen_recortada[margen:h - margen, margen:w - margen]

    contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    burbujas = []
    for c in contornos:
        area = cv2.contourArea(c)
        _, _, w, h = cv2.boundingRect(c)
        aspect_ratio = float(w) / h if h != 0 else 0
        if 250 < area < 2500 and 0.7 < aspect_ratio < 1.3:
            burbujas.append(c)

    burbujas = ordenar_contornos(burbujas)

    # Número estimado de columnas según cantidad esperada de preguntas
    # cada columna puede contener hasta 24 preguntas (filas)
    num_preguntas_esperadas = len(answer_key)
    columnas_detectadas = min(3, max(1, (num_preguntas_esperadas + 23) // 24))


    columnas = [[] for _ in range(columnas_detectadas)]
    total_w = imagen_recortada.shape[1]

    for c in burbujas:
        x, _, _, _ = cv2.boundingRect(c)
        col_width = total_w // columnas_detectadas
        col_idx = min(x // col_width, columnas_detectadas - 1)

        columnas[col_idx].append(c)

    respuestas_columnas = []
    burbujas_columnas = []
    for col in columnas:
        filas = agrupar_por_filas(col, tolerancia=30)
        col_respuestas = []
        col_burbujas = []
        for fila in filas:
            fila = sorted(fila, key=lambda c: cv2.boundingRect(c)[0])
            if len(fila) < 3 or len(fila) > max_alternativas:
                continue
            valores = []
            for contorno in fila:
                mascara = np.zeros(umbral.shape, dtype="uint8")
                cv2.drawContours(mascara, [contorno], -1, 255, -1)
                total = cv2.countNonZero(cv2.bitwise_and(umbral, umbral, mask=mascara))
                valores.append(total)

            max_valor = max(valores)
            seleccionada = -1
            for i, val in enumerate(valores):
                if val >= 0.75 * max_valor:
                    if seleccionada == -1:
                        seleccionada = i
                    else:
                        seleccionada = -1
                        break
            col_respuestas.append(seleccionada)
            col_burbujas.append(fila)
        respuestas_columnas.append(col_respuestas)
        burbujas_columnas.append(col_burbujas)

    # Recorrer por columnas primero (de arriba hacia abajo, izquierda a derecha)
    respuestas_lineal = []
    burbujas_lineal = []
    num_columnas = len(respuestas_columnas)
    for col_idx in range(num_columnas):
        col_r = respuestas_columnas[col_idx]
        col_b = burbujas_columnas[col_idx]
        for fila_idx in range(len(col_r)):
            respuestas_lineal.append(col_r[fila_idx])
            burbujas_lineal.append(col_b[fila_idx])

    """print(f"Total burbujas detectadas: {len(burbujas)}")
    print(f"Total preguntas detectadas: {len(respuestas_lineal)}")"""

    return respuestas_lineal, burbujas_lineal, imagen_recortada

def corregir_respuestas(respuestas, answer_key):
    correctas = 0
    for i, r in enumerate(respuestas):
        if i in answer_key and r == answer_key[i]:
            correctas += 1
    return correctas, len(answer_key)

def procesar_y_evaluar_prueba(imagen, formato, alumno, alternativas, answer_key, total_columnas):
    if imagen is None or formato is None:
        return {"error": "No se pudo cargar la imagen o el formato."}

    answer_key = {int(k): int(v) for k, v in answer_key.items()}

    marco = encontrar_marco(imagen)
    if marco is None:
        return {"error": "No se detectó el marco en la imagen."}

    recortada = recortar_area(imagen, marco)
    respuestas, burbujas_pregunta, imagen_eval = extraer_respuestas(recortada, alternativas,answer_key)

    for i, fila in enumerate(burbujas_pregunta):
        if i >= len(respuestas):
            continue
        seleccionada = respuestas[i]
        correcta = answer_key.get(i, -1)
        for j, contorno in enumerate(fila):
            if seleccionada == -1:
                color = (0, 255, 255)  # Amarillo: no respondida
            elif j == seleccionada and j == correcta:
                color = (0, 255, 0)    # Verde: correcta
            elif j == seleccionada and j != correcta:
                color = (0, 0, 255)    # Rojo: incorrecta
            elif j == correcta:
                color = (255, 0, 0)    # Azul: correcta no marcada
            else:
                color = (200, 200, 200)
            cv2.drawContours(imagen_eval, [contorno], -1, color, 2)


    _, imagen_codificada = cv2.imencode('.png', imagen_eval)
    imagen_base64 = base64.b64encode(imagen_codificada).decode('utf-8')
    imagen_base64_con_prefijo = f'data:image/png;base64,{imagen_base64}'

    aciertos, total = corregir_respuestas(respuestas, answer_key)

    resultado = {
        "alumno": alumno,
        "respuestas_detectadas": respuestas,
        "total_preguntas": total,
        "respuestas_correctas": aciertos,
        "imagen": imagen_base64_con_prefijo
    }
    return resultado
