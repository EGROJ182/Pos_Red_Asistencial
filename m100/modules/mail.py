import re
import os
import base64
import pickle
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from ..models.models_proveedores import proveedores
from .alert import alert
import locale
# Configurar localización en español
# locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')

# Alcances necesarios para enviar correos con la API de Gmail
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def get_credentials():
    """
    Obtiene credenciales OAuth 2.0 de Google.
    Si no existen o son inválidas, abre el navegador para autenticarse.
    Guarda/lee el token en 'token.json'.
    """
    # Obtiene la ruta absoluta del directorio donde está este script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    
    # Construye la ruta absoluta para 'credentials.json' y 'token.json'
    client_secret_file = os.path.join(script_dir, "credentials.json")
    token_path = os.path.join(script_dir, "token.json")
    
    creds = None
    
    # Si ya existe un token (el archivo token.json) lo cargamos
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # Si no hay credenciales o son inválidas, solicitamos autorización
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Si el token expiró, lo refrescamos
            creds.refresh(Request())
        else:
            # Autenticación con OAuth 2.0 (abrirá el navegador)
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Guardamos las credenciales para futuras ejecuciones
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    
    return creds

def send_email():
    """
    Envía un correo a la lista de destinatarios usando la Gmail API con OAuth 2.0.
    Utiliza formato HTML y <pre> para respetar saltos de línea y espacios.
    """
    # Obtenemos las credenciales y construimos el servicio de Gmail
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    # Lista de destinatarios
    destinatarios = [
        "ricaurte.rojas@gestarinnovacion.com",
        "omar.vanegas@positiva.gov.co",
        "seguimiento.redasistencial@positiva.gov.co",
        "esperanza.castillo@positiva.gov.co",
        "yudybarrera@gestarinnovacion.com",
        "yudy.barrera@positiva.gov.co",
        "analistaprocesosgs@gestarinnovacion.com",
        "anagonzalez@gestarinnovacion.com",
        "jorgetorres@gestarinnovacion.com",
        "milena.galindo@gestarinnovacion.com",
        "alejandra.rondon@gestarinnovacion.com",
        "analistadeprocesos@positiva.gov.co",
        "analistared1@positiva.gov.co",
        "analistared2@positiva.gov.co",
        "analistared3@positiva.gov.co",
        "analistared4@positiva.gov.co",
        "analistared5@positiva.gov.co",
        "analistared6@positiva.gov.co",
        "analistared7@positiva.gov.co",
        "analistared16@positiva.gov.co",
        "analistared14@positiva.gov.co",
        "analistared12@positiva.gov.co",
        "daniel.romero@gestarinnovacion.com",
        "analistared11@positiva.gov.co"
    ]

    # Alistar mensaje por consulta a la tabla de proveedores
    message = message2 = message3 = message4 = message5 = message6 = message7 = ""
    query_get = alert(proveedores)
    counter = counter2 = counter3 = counter4 = counter5 = counter6 = counter7 = 1

    for proveedor in query_get:
        if proveedor.dias_restantes > 15:
            message6 += (
                f"<tr>"
                f"<td style='text-align:center;'>{counter6}</td>"
                f"<td>{proveedor.nombre}</td>"
                f"<td>{proveedor.nit}</td>"
                f"<td style='text-align:center;'>{proveedor.numero_contrato}-{proveedor.year_contrato}</td>"
                f"<td style='text-align:center;'>{proveedor.message}</td>"
                f"</tr>\n"
            )
            counter6 += 1
        elif proveedor.dias_restantes > 7 and proveedor.dias_restantes < 16:
            message5 += (
                f"<tr>"
                f"<td style='text-align:center;'>{counter5}</td>"
                f"<td>{proveedor.nombre}</td>"
                f"<td>{proveedor.nit}</td>"
                f"<td style='text-align:center;'>{proveedor.numero_contrato}-{proveedor.year_contrato}</td>"
                f"<td style='text-align:center;'>{proveedor.message}</td>"
                f"</tr>\n"
            )
            counter5 += 1
        elif proveedor.dias_restantes > 2 and proveedor.dias_restantes < 8:
            message4 += (
                f"<tr>"
                f"<td style='text-align:center;'>{counter4}</td>"
                f"<td>{proveedor.nombre}</td>"
                f"<td>{proveedor.nit}</td>"
                f"<td style='text-align:center;'>{proveedor.numero_contrato}-{proveedor.year_contrato}</td>"
                f"<td style='text-align:center;'>{proveedor.message}</td>"
                f"</tr>\n"
            )
            counter4 += 1
        elif proveedor.dias_restantes == 2:
            message3 += (
                f"<tr>"
                f"<td style='text-align:center;'>{counter3}</td>"
                f"<td>{proveedor.nombre}</td>"
                f"<td>{proveedor.nit}</td>"
                f"<td style='text-align:center;'>{proveedor.numero_contrato}-{proveedor.year_contrato}</td>"
                f"<td style='text-align:center;'>{proveedor.message}</td>"
                f"</tr>\n"
            )
            counter3 += 1
        elif proveedor.dias_restantes == 1:
            message2 += (
                f"<tr>"
                f"<td style='text-align:center;'>{counter2}</td>"
                f"<td>{proveedor.nombre}</td>"
                f"<td>{proveedor.nit}</td>"
                f"<td style='text-align:center;'>{proveedor.numero_contrato}-{proveedor.year_contrato}</td>"
                f"<td style='text-align:center;'>{proveedor.message}</td>"
                f"</tr>\n"
            )
            counter2 += 1
        elif proveedor.dias_restantes == 0:
            message += (
                f"<tr>"
                f"<td style='text-align:center;'>{counter}</td>"
                f"<td>{proveedor.nombre}</td>"
                f"<td>{proveedor.nit}</td>"
                f"<td style='text-align:center;'>{proveedor.numero_contrato}-{proveedor.year_contrato}</td>"
                f"<td style='text-align:center;'>{proveedor.message}</td>"
                f"</tr>\n"
            )
            counter += 1
        else:
            message7 += (
                f"<tr>"
                f"<td style='text-align:center;'>{counter7}</td>"
                f"<td>{proveedor.nombre}</td>"
                f"<td>{proveedor.nit}</td>"
                f"<td style='text-align:center;'>{proveedor.numero_contrato}-{proveedor.year_contrato}</td>"
                f"<td style='text-align:center;'>{proveedor.message}</td>"
                f"</tr>\n"
            )
            counter7 += 1

    # 4) Crear el contenido HTML con <pre> para conservar el formato
    html_content = f"""
        <html>
        <head>
            <meta charset="utf-8"/>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.4;
                    background: white;
                    color: #fff;
                    margin: 0;
                    padding: 20px;
                }}
                p {{
                    margin: 10px 0;
                    font-weight: lighter;
                }}
                h1 {{
                    text-align: center;
                    color: red;
                }}
                .hoy {{
                    color: #d9534f;
                }}
                .manana {{
                    color: darkred;
                }}
                .pasado {{
                    color: orange;
                }}
                .semana {{
                    color: yellow;
                }}
                .otra {{
                    color: lightgreen;
                }}
                .mes {{
                    color: lightblue;
                }}

                /* Estilos de la tabla */
                table {{
                    width: 100%;
                    max-width: 900px;
                    border-collapse: collapse;
                    margin: 0 auto 20px auto;
                }}
                th, td {{
                    border: 1px solid #ccc;
                    padding: 8px;
                    text-align: center;
                }}
                th {{
                    background-color: #ff7c01;
                    color: white;
                }}
                tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
                tr:hover {{
                    background: #123249c2;
                    color: white;
                }}

                /* Contenedor para centrar y darle un aspecto "card" */
                .table-container {{
                    background-color: #f9f9f9;
                    color: #000;
                    padding: 10px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    overflow-x: auto;
                    margin: 0 auto 20px auto;
                }}
                section {{
                    width: 100%;
                    color: #000;
                    padding: 10px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    overflow-x: auto;
                    margin: 0 auto 20px auto;
                }}
                div {{
                    width: 90%;
                    color: #000;
                    padding: 10px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    overflow-x: auto;
                    margin: 0 auto 20px auto;
                }}
                /* Responsividad */
                @media only screen and (max-width: 600px) {{
                    table {{
                        font-size: 12px;
                    }}
                    th, td {{
                        padding: 4px;
                    }}
                    .table-container {{
                        padding: 5px;
                    }}
                    section {{
                        padding: 5px;
                    }}
                    div {{
                        padding: 5px;
                    }}
                 }}
                @media screen and (min-width: 600px) {{
                    .desktop-footer {{
                        display: table !important;
                    }}
                    .mobile-footer {{
                        display: none !important;
                    }}
                }}
            
                @media screen and (max-width: 599px) {{
                    .desktop-footer {{
                        display: none !important;
                    }}
                    .mobile-footer {{
                        display: table !important;
                    }}
                }}
        </style>
        </head>
        <body>
            <p>Buen día,</p>
            <p>Cordial saludo</p>
            <h1>Alertas de Contratos</h1>
            <section>
            <div id="message7" class="table-container">
            <h2> ❌ Contratos Vencidos en la Maestra hoja (Contratos Vigentes)</h2>
            <table>
                <thead>
                    <tr>
                    <th>Item</th>
                    <th>Razón Social</th>
                    <th>NIT</th>
                    <th>Número Contrato</th>
                    <th>Fecha Vencimiento</th>
                    </tr>
                </thead>
                <tbody>
                    {message7}
                </tbody>
            </table>
            </div>
            <div id="message" class="table-container">
            <h2 class="hoy"> ☢ Contratos que finalizan Hoy</h2>
            <table>
                <thead>
                    <tr>
                    <th>Item</th>
                    <th>Razón Social</th>
                    <th>NIT</th>
                    <th>Número Contrato</th>
                    <th>Fecha Vencimiento</th>
                    </tr>
                </thead>
                <tbody>
                    {message}
                </tbody>
            </table>
            </div>
            <div id="message2" class="table-container">
            <h2 class="manana"> ⚠ Contratos que finalizan mañana</h2>
            <table>
                <thead>
                    <tr>
                    <th>Item</th>
                    <th>Razón Social</th>
                    <th>NIT</th>
                    <th>Número Contrato</th>
                    <th>Fecha Vencimiento</th>
                    </tr>
                </thead>
                <tbody>
                    {message2}
                </tbody>
            </table>
            </div>
            <div id="message3" class="table-container">
            <h2 class="pasado"> 🚧 Contratos que finalizan pasado mañana</h2>
            <table>
                <thead>
                    <tr>
                    <th>Item</th>
                    <th>Razón Social</th>
                    <th>NIT</th>
                    <th>Número Contrato</th>
                    <th>Fecha Vencimiento</th>
                    </tr>
                </thead>
                <tbody>
                    {message3}
                </tbody>
            </table>
            </div>
            <div id="message4" class="table-container">
            <h2 class="semana"> 🌋 Contratos que finalizan esta semana 4 a 7 días</h2>
            <table>
                <thead>
                    <tr>
                    <th>Item</th>
                    <th>Razón Social</th>
                    <th>NIT</th>
                    <th>Número Contrato</th>
                    <th>Fecha Vencimiento</th>
                    </tr>
                </thead>
                <tbody>
                    {message4}
                </tbody>
            </table>
            </div>
            <div id="message5" class="table-container">
            <h2 class="otra"> 🔥 Contratos que finalizan la otra semana 8 a 15 días</h2>
            <table>
                <thead>
                    <tr>
                    <th>Item</th>
                    <th>Razón Social</th>
                    <th>NIT</th>
                    <th>Número Contrato</th>
                    <th>Fecha Vencimiento</th>
                    </tr>
                </thead>
                <tbody>
                    {message5}
                </tbody>
            </table>
            </div>
            <div id="message6" class="table-container">
            <h2 class="mes"> 🆗 Contratos que finalizan de 16 a 30 días</h2>
            <table>
                <thead>
                    <tr>
                    <th>Item</th>
                    <th>Razón Social</th>
                    <th>NIT</th>
                    <th>Número Contrato</th>
                    <th>Fecha Vencimiento</th>
                    </tr>
                </thead>
                <tbody>
                    {message6}
                </tbody>
            </table>
            </div>
            </section>
            <section>
                <p>Página Red Asistencial - Módulo Proveedores Contratados</p>
                <p>Link: <a href="https://jdjrq144-8000.use.devtunnels.ms/proveedores-contratados/red-asistencial/" target="_blank">Clic para ir a la página</a></p>
                <br><br><br>
                <p style="text-align: center; font: 900;">Jorge Vega - Python Gmail API</p>
            </section>
        </body>
        </html>
    """
    if not message7:  # Si message6 está vacío o no cumple la condición
        html_content = re.sub(r'<div id="message7" class="table-container">.*?</div>', '', html_content, flags=re.DOTALL)
    if not message:  # Si message6 está vacío o no cumple la condición
        html_content = re.sub(r'<div id="message" class="table-container">.*?</div>', '', html_content, flags=re.DOTALL)
    if not message2:  # Si message6 está vacío o no cumple la condición
        html_content = re.sub(r'<div id="message2" class="table-container">.*?</div>', '', html_content, flags=re.DOTALL)
    if not message3:  # Si message6 está vacío o no cumple la condición
        html_content = re.sub(r'<div id="message3" class="table-container">.*?</div>', '', html_content, flags=re.DOTALL)
    if not message4:  # Si message6 está vacío o no cumple la condición
        html_content = re.sub(r'<div id="message4" class="table-container">.*?</div>', '', html_content, flags=re.DOTALL)
    if not message5:  # Si message6 está vacío o no cumple la condición
        html_content = re.sub(r'<div id="message5" class="table-container">.*?</div>', '', html_content, flags=re.DOTALL)
    if not message6:  # Si message6 está vacío o no cumple la condición
        html_content = re.sub(r'<div id="message6" class="table-container">.*?</div>', '', html_content, flags=re.DOTALL)

    # 5) Crear el mensaje MIMEText con formato "html"
    mensaje = MIMEText(html_content, "html", "utf-8")
    mensaje["to"] = ", ".join(destinatarios)
    # Asunto con fecha en español
    mensaje["subject"] = (
        f"⚠ - Alertas Automáticas de finalización de Contratos Maestra (Red Asistencial) "
        f"{datetime.now().strftime('%A %d de %B de %Y')}"
    )

    # 6) Convertir a base64 y enviar
    raw = base64.urlsafe_b64encode(mensaje.as_bytes()).decode("utf-8")
    body = {"raw": raw}

    try:
        response = service.users().messages().send(userId="me", body=body).execute()
        print(f"Correo enviado con ID: {response['id']}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

if __name__ == "__main__":
    send_email()