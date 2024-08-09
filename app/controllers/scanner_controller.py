import cv2
from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import numpy as np
import base64
import os
import shutil

def process_image(image, alternativas):
    try:
        # Leer la imagen
        image_bytes = base64.b64decode(image)
        image_np = np.frombuffer(image_bytes, dtype=np.uint8)
        
        # Read the image using OpenCV
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("No se pudo decodificar la imagen.")

        # Convertir la imagen a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Aplicar desenfoque gaussiano para reducir el ruido
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Aplicar el detector de bordes Canny
        edges = cv2.Canny(blurred, 50, 150)

        # Encontrar contornos en la imagen con bordes
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Inicializar variables para el contorno más grande
        max_contour = None
        max_area = 0

        # Iterar sobre los contornos
        for contour in contours:
            # Calcular el área del contorno actual
            area = cv2.contourArea(contour)

            # Verificar si el área actual es más grande que el área máxima hasta ahora
            if area > max_area:
                max_area = area
                max_contour = contour

        if max_contour is None:
            raise ValueError("No se encontró un contorno válido.")

        # Extraer las coordenadas del rectángulo más grande
        x, y, w, h = cv2.boundingRect(max_contour)

        # Determinar las dimensiones y ubicación de la primera columna
        column_width = w // int(alternativas)
        column_height = h
        first_column_x = x
        first_column_y = y

        # Crear una copia de la imagen original para trabajar
        image_copy = image.copy()

        # Crear el directorio si no existe
        output_dir = 'static/columnas/'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Número total de columnas que deseas encontrar (incluyendo la primera columna)
        total_columnas = int(alternativas)  # Puedes ajustar esto según tus necesidades

        for i in range(0, total_columnas):
            # Calcular las coordenadas de la siguiente columna
            next_column_x = first_column_x + i * column_width

            # Recortar la región de interés (ROI) correspondiente a la siguiente columna
            roi = image_copy[first_column_y:first_column_y + column_height, next_column_x:next_column_x + column_width]
            
            cv2.rectangle(roi, (0, 0), (roi.shape[1], roi.shape[0]), (255, 255, 255), 3)

            # Guardar la ROI con el contorno de color blanco
            column_path = os.path.join(output_dir, f'columna_{i + 1}_con_contorno.png')
            cv2.imwrite(column_path, roi)

            # Verificar si la imagen se guardó correctamente
            if not os.path.exists(column_path):
                raise ValueError(f"No se pudo guardar la imagen en {column_path}")

        # Leer las imágenes generadas
        columnas = []
        for i in range(total_columnas):
            imagen_path = os.path.join(output_dir, f'columna_{i + 1}_con_contorno.png')
            columna = cv2.imread(imagen_path)
            if columna is None:
                raise ValueError(f"No se pudo leer la imagen en {imagen_path}")
            columnas.append(columna)

        # Concatenar verticalmente las imágenes
        resultado = cv2.vconcat(columnas)

        # Dibujar un rectángulo negro alrededor de la imagen resultante
        resultado_con_rectangulo = cv2.rectangle(resultado, (0, 0), (resultado.shape[1], resultado.shape[0]), (0, 0, 0), 3)

        # Guardar la imagen resultante con el rectángulo negro
        result_path = 'static/imagen_resultante.png'
        cv2.imwrite(result_path, resultado_con_rectangulo)

        # Verificar si la imagen resultante se guardó correctamente
        if not os.path.exists(result_path):
            raise ValueError(f"No se pudo guardar la imagen resultante en {result_path}")
        
        return True
    except Exception as err:
        print('Error al procesar la imagen:', err)
        return False

def solve_test(ANSWER_KEY, alternativas):
    # Clave de respuestas predefinida
    ANSWER_KEY = {int(key): int(value) for key, value in ANSWER_KEY.items()}
    # Umbral de píxeles para considerar una burbuja marcada
    UMBRAL_PIXELES = 600

    # Cargar la imagen
    image = cv2.imread('static/imagen_resultante.png')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)

    # Encontrar contornos externos
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    docCnt = None

    # Verificar si se encontraron contornos
    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            if len(approx) == 4:
                docCnt = approx
                break

    # Verificar que se haya encontrado el contorno del papel
    if docCnt is not None:
        paper = four_point_transform(image, docCnt.reshape(4, 2))
        warped = four_point_transform(gray, docCnt.reshape(4, 2))
        thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        # Encontrar contornos de las burbujas
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        questionCnts = []

        # Calcular promedios y filtrar contornos de burbujas
        suma_anchos = 0
        suma_altos = 0
        cantidad_contornos = len(cnts)
        aspect_ratios = []

        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            ar = w / float(h)
            aspect_ratios.append(ar)
            suma_anchos += w
            suma_altos += h
        
        promedio_anchos = suma_anchos / cantidad_contornos
        promedio_altos = suma_altos / cantidad_contornos
        min_ar = min(aspect_ratios)
        max_ar = max(aspect_ratios)

        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            ar = w / float(h)
            if w >= promedio_anchos and h >= promedio_altos and ar >= min_ar and ar <= max_ar:
                questionCnts.append(c)

        if questionCnts:
            # Ordenar contornos de arriba a abajo
            questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]
            correct = 0
            incorrect = 0
            score = 0.0
            total_questions = len(questionCnts) // int(alternativas)  # Total de preguntas
            respuestas_marcadas = {}

            # Evaluar cada pregunta
            for (q, i) in enumerate(np.arange(0, len(questionCnts), int(alternativas))):
                cnts = contours.sort_contours(questionCnts[i:i + int(alternativas)])[0]
                bubbled = None
                
                # Inicializar respuesta incorrecta
                answered = False

                for (j, c) in enumerate(cnts):
                    mask = np.zeros(thresh.shape, dtype="uint8")
                    cv2.drawContours(mask, [c], -1, 255, -1)
                    mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                    total = cv2.countNonZero(mask)

                    if bubbled is None and total > UMBRAL_PIXELES:
                        bubbled = (total, j)
                        answered = True
                    
                if answered:
                    respuestas_marcadas[q + 1] = bubbled[1]
                
                k = ANSWER_KEY[q]

                # Si no se marcó ninguna respuesta, marcar como incorrecta
                if not answered:
                    bubbled = (0, -1)

                # Comparar respuesta elegida con respuesta correcta
                if k == bubbled[1]:
                    color = (0, 255, 0)  # verde para respuesta correcta
                    correct += 1
                else:
                    color = (0, 0, 255)
                    incorrect += 1  # rojo para respuesta incorrecta

                # Dibujar contorno alrededor de la respuesta seleccionada en la imagen original
                cv2.drawContours(paper, [cnts[k]], -1, color, 3)

            # Calcular el puntaje final         
            score = (correct / total_questions) * 100
            nota = int(score) if score.is_integer() else round(score)

            # Mostrar el puntaje en la imagen del examen
            cv2.putText(paper, "{:.1f}%".format(nota), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)


        eliminar_contenido_directorio('static/columnas')
        eliminar_contenido_directorio('static/imagen_resultante.png')
        # Mostrar imágenes
        _, paper_encoded = cv2.imencode('.png', paper)
        paper_base64 = base64.b64encode(paper_encoded.tobytes()).decode('utf-8')
        paper_base64_with_prefix = f'data:image/png;base64,{paper_base64}'
        return {'image': paper_base64_with_prefix, 'nota': nota, 'respuestas_marcadas': respuestas_marcadas}
        
    else:
        print("No se encontró un contorno cuadrilátero para el papel del examen.")
        
def eliminar_contenido_directorio(directorio):
    # Verificar si el directorio existe
    if os.path.isdir(directorio):
        try:
            # Listar todo el contenido del directorio
            for item in os.listdir(directorio):
                item_path = os.path.join(directorio, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)  # Eliminar archivo
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)  # Eliminar subdirectorio y su contenido
            print(f"Contenido del directorio '{directorio}' ha sido eliminado.")
        except PermissionError as e:
            print(f"Error de permisos al eliminar el contenido del directorio: {e}")
        except FileNotFoundError as e:
            print(f"Archivo o directorio no encontrado: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
    else:
        os.remove("static/imagen_resultante.png")
        print(f"El archivo '{directorio}' ha sido eliminado.")