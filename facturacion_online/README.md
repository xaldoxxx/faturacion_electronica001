# sistema de facturación simple y funcional, construido usando solo librerías internas de Python y un servidor básico de http.server

# Sistema de Facturación Electrónica

Este sistema permite a los autónomos y freelancers generar facturas personalizadas en formato PDF. Las facturas se pueden descargar y los datos se almacenan para su gestión futura.

## Requisitos

- Python 3.x
- Librerías estándar de Python (`http.server`, `csv`, `datetime`)
- Librería `reportlab` para la generación de PDFs

## Instalación

1. Clona este repositorio en tu máquina local.
2. Asegúrate de tener instalada la librería `reportlab`:


 Sistema de Facturación Electrónica para Autónomos y Freelancers usando solo librerías internas de Python
/facturacion_online/
├── server.py              # Archivo principal que ejecuta el servidor web
├── data/
│   ├── __init__.py        # Archivo vacío para indicar que 'data' es un paquete
│   ├── clients.csv        # Archivo CSV para almacenar datos de los clientes
│   ├── invoices.csv       # Archivo CSV para almacenar las facturas generadas
├── templates/
│   ├── form.html          # Formulario HTML para introducir datos de facturación
│   ├── success.html       # Página de éxito después de generar una factura
├── static/
│   ├── style.css          # Archivo CSS con estilo básico para el sitio web
└── README.md              # Archivo de instrucciones para el uso del sistema

