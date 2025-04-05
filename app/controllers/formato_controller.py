from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime
import qrcode
import json

def crear_opciones(alternativas):
    todas_opciones = ['A', 'B', 'C', 'D', 'E']
    opciones = todas_opciones[:alternativas]
    return opciones

def crear_formato(curso, alternativas, asignatura, num_preguntas):
    try:
        # Configuración inicial
        opciones = crear_opciones(int(alternativas))
        ancho_imagen = 1272 * 4  # 8.5 pulgadas a 300 DPI (resolución aumentada 4 veces)
        alto_imagen = 1647 * 4   # 11 pulgadas a 300 DPI (resolución aumentada 4 veces)
        color_fondo = "white"
        color_texto = "black"
        color_circulo = "black"
        color_rectangulo = "black"
        radio_circulo = 15 * 4  # Radio aumentado para la resolución más alta
        espacio_entre_circulos = 40 * 4
        espacio_entre_preguntas = 40 * 4
        margen_superior = 500 * 4
        margen_izquierdo = 50 * 4
        espacio_entre_columnas = 300 * 4  # Ajustado a la nueva resolución
        preguntas_por_columna = 10

        # Calcular la cantidad de preguntas por columna
        if num_preguntas > 60:
            preguntas_por_columna = 25

        if num_preguntas == 50:
            preguntas_por_columna = 20

        if num_preguntas == 10:
            preguntas_por_columna = 10

        # Crear una imagen nueva en formato carta con fondo blanco
        imagen = Image.new("RGBA", (ancho_imagen, alto_imagen), color_fondo)
        dibujar = ImageDraw.Draw(imagen)
        
        font_path = os.path.join(os.getcwd(), "fonts", "Lato-Regular.ttf")

        fuente = ImageFont.truetype(font_path, 60)
        fuente_labels = ImageFont.truetype(font_path, 80)

        # Dibujar etiquetas de nombre y apellido
        dibujar.text((margen_izquierdo, 400), "Nombre:", fill=color_texto, font=fuente_labels)
        dibujar.text((margen_izquierdo, 720), "Apellido:", fill=color_texto, font=fuente_labels)

        # Dibujar las respuestas en la imagen
        for i in range(1, num_preguntas + 1):
            columna = (i - 1) // preguntas_por_columna  # Determinar la columna actual
            fila = (i - 1) % preguntas_por_columna  # Determinar la fila dentro de la columna
            total_columnas = columna + 1
            
            # Ajustar la posición según la columna
            posicion_x_pregunta = margen_izquierdo + columna * espacio_entre_columnas
            posicion_y_pregunta = margen_superior + (fila * espacio_entre_preguntas)
            
            # Dibujar círculos con opciones
            for j, opcion in enumerate(opciones):
                x_circulo = posicion_x_pregunta + 400 + (j * espacio_entre_circulos)
                y_circulo = posicion_y_pregunta
                coordenadas = [
                    (x_circulo - radio_circulo, y_circulo - radio_circulo),
                    (x_circulo + radio_circulo, y_circulo + radio_circulo),
                ]
                dibujar.ellipse(coordenadas, outline=color_circulo, width=8) # Dibuja el círculo
                
                # Obtener el tamaño de la letra usando textbbox
                bbox = dibujar.textbbox((0, 0), opcion, font=fuente)
                ancho_letra = bbox[2] - bbox[0]
                alto_letra = bbox[3] - bbox[1]
                
                # Calcular posición para centrar la letra dentro del círculo
                x_texto = x_circulo - ancho_letra / 2
                y_texto = y_circulo - alto_letra / 1.5
                
                dibujar.text((x_texto, y_texto), opcion, fill=color_texto, font=fuente)  # Escribe la opción dentro del círculo

            # Ajustar la posición del número de pregunta para que quede centrado verticalmente con las opciones
            bbox_pregunta = dibujar.textbbox((0, 0), f'{i} ', font=fuente)
            ancho_pregunta = bbox_pregunta[2] - bbox_pregunta[0]
            alto_pregunta = bbox_pregunta[3] - bbox_pregunta[1]
            x_pregunta = posicion_x_pregunta + 200
            y_pregunta_centrada = posicion_y_pregunta - (alto_pregunta / 0.5 - radio_circulo)  # Ajuste para centrar verticalmente

            dibujar.text((x_pregunta, y_pregunta_centrada), f'{i} ', fill=color_texto, font=fuente)

        # Calcular dimensiones del rectángulo que cubre todas las preguntas
        num_columnas = (num_preguntas - 1) // preguntas_por_columna + 1
        ancho_rectangulo = (num_columnas * espacio_entre_columnas)
        alto_rectangulo = (preguntas_por_columna * espacio_entre_preguntas)

               # Coordenadas del área de preguntas
        x0 = margen_izquierdo - 30
        y0 = margen_superior - 100
        x1 = margen_izquierdo + ancho_rectangulo
        y1 = margen_superior + alto_rectangulo

        # Dibujar contorno más grueso
        #dibujar.rectangle([(x0, y0), (x1, y1)], outline="black", width=16)

        # Tamaño del marcador
        marcador = 60

        # Dibujar marcadores guía en cada esquina del área de preguntas
        esquinas = [
            (x0 - marcador // 2, y0 - marcador // 2),  # superior izquierda
            (x1 - marcador // 2, y0 - marcador // 2),  # superior derecha
            (x0 - marcador // 2, y1 - marcador // 2),  # inferior izquierda
            (x1 - marcador // 2, y1 - marcador // 2),  # inferior derecha
        ]
        for esquina in esquinas:
            dibujar.rectangle(
                [esquina, (esquina[0] + marcador, esquina[1] + marcador)],
                fill="black"
            )


        # Obtener la fecha actual y formatearla
        fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Guardar la imagen en formato carta usando nombre_formato y fecha actual
        nombre_archivo = f"{asignatura}_{fecha_actual}.png"
        output_directory = os.path.join(os.getcwd(), f'static/formato/{curso}/{asignatura}')
        os.makedirs(output_directory, exist_ok=True)
        
        output_path = os.path.join(output_directory, nombre_archivo)
        imagen = imagen.resize((1272, 1647), Image.LANCZOS)
        imagen.save(output_path)
        return {'ruta': nombre_archivo, 'columnas':total_columnas }
    except Exception as err:
        print('Error al crear el formato:', err)
        return None


def agregar_qr_alumno(alumnos, curso, asignatura_id, asignatura, ruta_formato):
    try:
        image_directory = os.path.join(os.getcwd(), f'static/formato/{curso}/{asignatura}')
        output_directory = os.path.join(os.getcwd(), f'static/alumnos/{curso}/{asignatura}')
        
        # Asegúrate de que el directorio de salida existe
        os.makedirs(output_directory, exist_ok=True)

        # Verifica si el archivo existe en el directorio
        formato_path = os.path.join(image_directory, ruta_formato)
        if not os.path.exists(formato_path):
            raise FileNotFoundError(f"El archivo de formato '{ruta_formato}' no se encontró en la ruta '{image_directory}'.")

        # Procesar cada alumno
        for alumno in alumnos:
            nombre_imagen = f"{alumno['nombre']}_{alumno['apellido']}_{curso}_{asignatura}.png"
            output_path = os.path.join(output_directory, nombre_imagen)

            if not os.path.exists(output_path):
                # Abrir la imagen principal (formato)
                imagen = Image.open(formato_path)
                ancho_imagen, alto_imagen = imagen.size
                dibujar = ImageDraw.Draw(imagen)
                
                # Generar el código QR con la información del alumno
                qr_data = {
                    "id": alumno["id"],
                    "nombre": alumno["nombre"],
                    "apellido": alumno["apellido"],
                    "curso_id": alumno["curso_id"],
                    "asignatura_id": asignatura_id
                }
                qr_info = json.dumps(qr_data)
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(qr_info)
                qr.make(fit=True)
                qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')
                
                # Redimensionar el código QR para que se ajuste al lado derecho de la imagen
                qr_size = 250
                qr_img = qr_img.resize((qr_size, qr_size), Image.LANCZOS)

                # Calcular la posición del código QR (al lado derecho de la hoja)
                qr_x = ancho_imagen - qr_size - 50
                qr_y = 50  # Posición vertical en la parte superior derecha

                # Pegar el código QR en la imagen principal
                imagen.paste(qr_img, (qr_x, qr_y))
                
                font_path = os.path.join(os.getcwd(), "fonts", "Lato-Regular.ttf")
                fuente_labels = ImageFont.truetype(font_path, 20)
                
                # Escribir el nombre y apellido del alumno en la imagen
                dibujar.text((200, 100), alumno['nombre'], fill="black", font=fuente_labels)
                dibujar.text((200, 180), alumno['apellido'], fill="black", font=fuente_labels)
                
                # Guardar la imagen con el código QR en el directorio de salida
                imagen = imagen.convert("RGBA")
                imagen = imagen.resize((1272, 1647))
                imagen.save(output_path)
                print(f"Formato guardado para {alumno['nombre']} {alumno['apellido']} en {output_path}")
            else:
                print(f"La imagen ya existe: {output_path}")
        return True
    except Exception as err:
        print(f'Error al crear el formato: {err}')
        return False