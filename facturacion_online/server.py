import http.server
import socketserver
import csv
import os
from datetime import datetime
from urllib.parse import parse_qs
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Configuración del puerto del servidor
PORT = 8080
DIRECTORY = os.path.dirname(os.path.realpath(__file__))

class InvoiceHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/form':
            self.path = '/templates/form.html'
        elif self.path == '/success':
            self.path = '/templates/success.html'
        else:
            self.path = '/templates/form.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/generate_invoice':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = parse_qs(post_data.decode('utf-8'))

            # Obtener datos del formulario
            client_name = data.get('client_name')[0]
            client_email = data.get('client_email')[0]
            service_description = data.get('service_description')[0]
            amount = data.get('amount')[0]

            # Generar la factura en PDF
            invoice_id = self.generate_invoice_pdf(client_name, client_email, service_description, amount)

            # Guardar los datos en un archivo CSV
            self.save_invoice_data(client_name, client_email, service_description, amount, invoice_id)

            # Redireccionar a la página de éxito
            self.send_response(301)
            self.send_header('Location', '/success')
            self.end_headers()

    def generate_invoice_pdf(self, client_name, client_email, service_description, amount):
        # Crear el nombre del archivo PDF
        invoice_id = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        pdf_file = f"{DIRECTORY}/{invoice_id}.pdf"
        
        # Crear el PDF
        pdf = canvas.Canvas(pdf_file, pagesize=letter)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 750, f"Factura: {invoice_id}")
        pdf.drawString(100, 730, f"Fecha: {datetime.now().strftime('%Y-%m-%d')}")
        pdf.drawString(100, 710, f"Cliente: {client_name}")
        pdf.drawString(100, 690, f"Email: {client_email}")
        pdf.drawString(100, 670, f"Descripción del servicio: {service_description}")
        pdf.drawString(100, 650, f"Monto: ${amount}")
        pdf.save()

        return invoice_id

    def save_invoice_data(self, client_name, client_email, service_description, amount, invoice_id):
        # Guardar los datos en el archivo CSV
        with open(f'{DIRECTORY}/data/invoices.csv', 'a', newline='') as csvfile:
            fieldnames = ['invoice_id', 'client_name', 'client_email', 'service_description', 'amount', 'date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Verificar si el archivo está vacío (escribir encabezado si es necesario)
            if os.stat(f'{DIRECTORY}/data/invoices.csv').st_size == 0:
                writer.writeheader()

            writer.writerow({
                'invoice_id': invoice_id,
                'client_name': client_name,
                'client_email': client_email,
                'service_description': service_description,
                'amount': amount,
                'date': datetime.now().strftime('%Y-%m-%d')
            })

# Iniciar el servidor
with socketserver.TCPServer(("", PORT), InvoiceHandler) as httpd:
    print(f"Sirviendo en el puerto {PORT}")
    httpd.serve_forever()
