# generador_qr.py
import os
from flask import Blueprint
import qrcode


generador_qr_bp = Blueprint('generador_qr', __name__)

# ...

@generador_qr_bp.route('/generarqr', methods=['POST'])
def generar_qr_imagen(nombre, apellido, info_string):

    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(info_string)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        ruta_absoluta = os.path.abspath(f"static/qr_images/qr_{nombre}_{apellido}.png")

        carpeta_qr_images = os.path.dirname(ruta_absoluta)
        if not os.path.exists(carpeta_qr_images):
            os.makedirs(carpeta_qr_images)

        img.save(ruta_absoluta)

        return {'ruta_qr': ruta_absoluta}
    except Exception as e:
        print("Error:", e)
        raise e
