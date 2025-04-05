import cv2
import numpy as np
import imutils
from imutils.perspective import four_point_transform
from imutils import contours
import base64

def procesar_y_evaluar_prueba(image_path, alumno, alternativas, ANSWER_KEY):
    try:
        print(f"Recibiendo imagen: {image_path}")
        print(f"Alternativas: {alternativas}, ANSWER_KEY: {ANSWER_KEY}")

        imagen = cv2.imread(image_path)
        if imagen is None:
            raise ValueError("La imagen no pudo cargarse correctamente.")
        
        gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 75, 200)

        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        examenCnt = None

        if len(cnts) == 0:
            raise ValueError("No se encontraron contornos.")

        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                examenCnt = approx
                break

        if examenCnt is None:
            raise ValueError("No se detectó el contorno principal del examen.")

        paper = four_point_transform(imagen, examenCnt.reshape(4, 2))
        warped = four_point_transform(gray, examenCnt.reshape(4, 2))
        thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        questionCnts = []

        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            ratio = w / float(h)
            if (w > 20 and h > 20 and 0.9 <= ratio <= 1.1):
                questionCnts.append(c)

        total_preguntas = len(ANSWER_KEY)
        if len(questionCnts) != total_preguntas * alternativas:
            raise ValueError(f"La cantidad de preguntas detectadas ({len(questionCnts)}) no coincide con la esperada ({total_preguntas * alternativas}).")

        questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]

        respuestas_marcadas = {}
        correctas = 0

        for (q, i) in enumerate(range(0, len(questionCnts), alternativas)):
            cnts_pregunta = contours.sort_contours(questionCnts[i:i+alternativas])[0]
            burbuja_marcada = None

            for (j, c) in enumerate(cnts_pregunta):
                mask = np.zeros(thresh.shape, dtype="uint8")
                cv2.drawContours(mask, [c], -1, 255, -1)
                mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                total = cv2.countNonZero(mask)

                if burbuja_marcada is None or total > burbuja_marcada[0]:
                    burbuja_marcada = (total, j)

            respuestas_marcadas[q] = burbuja_marcada[1]

            color = (0, 0, 255)
            if int(ANSWER_KEY[str(q)]) == burbuja_marcada[1]:  # <- Aquí
                color = (0, 255, 0)
                correctas += 1

            cv2.drawContours(paper, [cnts_pregunta[int(ANSWER_KEY[str(q)])]], -1, color, 3)  # <- Aquí

        nota_final = (correctas / total_preguntas) * 100

        _, paper_encoded = cv2.imencode('.png', paper)
        paper_base64 = base64.b64encode(paper_encoded).decode('utf-8')
        paper_base64_with_prefix = f'data:image/png;base64,{paper_base64}'

        resultado = {
            "nota": nota_final,
            "respuestas_marcadas": respuestas_marcadas,
            "image": paper_base64_with_prefix
        }

        return resultado

    except Exception as err:
        print(f'Error en procesar_y_evaluar_prueba: {err}')
        return None
