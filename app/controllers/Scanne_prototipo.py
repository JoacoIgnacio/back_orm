import cv2
import numpy as np

# Simulación de clave de respuestas para 36 preguntas
ANSWER_KEY = {i: np.random.randint(0, 5) for i in range(36)}

def ordenar_contornos(contornos):
    return sorted(contornos, key=lambda c: (cv2.boundingRect(c)[1], cv2.boundingRect(c)[0]))

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
    rect[0] = pts[np.argmin(s)]  # top-left
    rect[2] = pts[np.argmax(s)]  # bottom-right
    rect[1] = pts[np.argmin(d)]  # top-right
    rect[3] = pts[np.argmax(d)]  # bottom-left
    return rect

def recortar_area(imagen, puntos):
    rect = ordenar_puntos(puntos)
    (tl, tr, br, bl) = rect
    ancho = max(int(np.linalg.norm(br - bl)), int(np.linalg.norm(tr - tl)))
    alto = max(int(np.linalg.norm(tr - br)), int(np.linalg.norm(tl - bl)))

    dst = np.array([
        [0, 0],
        [ancho - 1, 0],
        [ancho - 1, alto - 1],
        [0, alto - 1]
    ], dtype="float32")

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

def extraer_respuestas(imagen_recortada):
    gris = cv2.cvtColor(imagen_recortada, cv2.COLOR_BGR2GRAY)
    umbral = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 57, 5)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    umbral = cv2.dilate(umbral, kernel, iterations=1)

    h, w = umbral.shape
    margen = 5
    umbral = umbral[margen:h - margen, margen:w - margen]
    imagen_recortada = imagen_recortada[margen:h - margen, margen:w - margen]

    cv2.imshow("Debug - Umbral aplicado", umbral)

    contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    debug = imagen_recortada.copy()
    burbujas = []
    for c in contornos:
        area = cv2.contourArea(c)
        _, _, w, h = cv2.boundingRect(c)
        aspect_ratio = float(w) / h if h != 0 else 0
        if 250 < area < 2500 and 0.7 < aspect_ratio < 1.3:
            burbujas.append(c)
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(debug, (x, y), (x + w, y + h), (0, 255, 0), 1)

    print(f"Burbujas válidas detectadas: {len(burbujas)}")
    cv2.imshow("Resultado final (burbujas detectadas)", debug)

    burbujas = ordenar_contornos(burbujas)

    if len(burbujas) > 180:
        print("⚠️ Se detectaron más de 180 burbujas. Usando solo las 180 primeras ordenadas.")
        burbujas = burbujas[:180]

    columnas = [[] for _ in range(3)]
    total_w = imagen_recortada.shape[1]

    for c in burbujas:
        x, y, w, h = cv2.boundingRect(c)
        if x < total_w / 3:
            columnas[0].append(c)
        elif x < 2 * total_w / 3:
            columnas[1].append(c)
        else:
            columnas[2].append(c)

    respuestas = []
    burbujas_por_pregunta = []

    for col in columnas:
        filas = agrupar_por_filas(col, tolerancia=30)

        for fila in filas:
            if len(fila) != 5:
                print("❗ Advertencia: una fila no tiene 5 burbujas. Se ignora.")
                respuestas.append(-1)
                burbujas_por_pregunta.append(fila)
                continue

            fila = sorted(fila, key=lambda c: cv2.boundingRect(c)[0])
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

            respuestas.append(seleccionada)
            burbujas_por_pregunta.append(fila)

    return respuestas, burbujas_por_pregunta, imagen_recortada

def corregir(respuestas):
    correctas = 0
    for i, r in enumerate(respuestas):
        if i in ANSWER_KEY and r == ANSWER_KEY[i]:
            correctas += 1
    return correctas, len(ANSWER_KEY)

def visualizar_resultado(imagen, respuestas, burbujas_por_pregunta):
    for i, fila in enumerate(burbujas_por_pregunta):
        correcta = ANSWER_KEY.get(i, -1)
        marcada = respuestas[i]

        for j, contorno in enumerate(fila):
            x, y, w, h = cv2.boundingRect(contorno)
            if marcada == -1:
                color = (0, 255, 255)
            elif j == marcada and j == correcta:
                color = (0, 255, 0)
            elif j == marcada and j != correcta:
                color = (0, 0, 255)
            elif j == correcta:
                color = (255, 0, 0)
            else:
                color = (200, 200, 200)
            cv2.rectangle(imagen, (x, y), (x + w, y + h), color, 2)

    cv2.imshow("Corrección visual", imagen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

imagen = cv2.imread("f.jpeg")
marco = encontrar_marco(imagen)

if marco is None:
    print("❌ No se detectó el marco.")
else:
    recortada = recortar_area(imagen, marco)
    respuestas, burbujas_pregunta, imagen_eval = extraer_respuestas(recortada)
    aciertos, total = corregir(respuestas)

    print("📋 Respuestas detectadas:", respuestas)
    print(f"✅ Resultado: {aciertos}/{total}")
    visualizar_resultado(imagen_eval, respuestas, burbujas_pregunta)
