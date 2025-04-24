from celery import shared_task
import time,os,json
from .models import Order
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table,TableStyle
from pathlib import Path

@shared_task
def generate_file_from_data(data,file_format = 'pdf'):
    folder = 'generated_files'
    print("Folder : ",folder)
    os.makedirs(folder,exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{folder}/output_{timestamp}.{file_format}"

    c = canvas.Canvas(str(filename), pagesize=A4)
    width, height = A4

    if not isinstance(data, list) or not data:
        print("Invalid or empty data, using fallback.")
        table_data = [["Message"], ["No Data Available"]]
    elif not isinstance(data[0], dict):
        print("Data is not a list of dictionaries, converting.")
        table_data = [["Message"], ["Invalid Data Format"]]
    else:
        headers = list(data[0].keys())
        table_data = [headers] + [[str(row.get(col, "")) for col in headers] for row in data]

    table = Table(table_data, colWidths=[80] * len(table_data[0]))


    style =  TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.black),
        ('ALIGN',(0,0),(-1,-1),'LEFT'),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('BOTTOMPADDING',(0,0),(-1,0),10),
        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
    ])
    table.setStyle(style)

    #Draw Table
    table.wrapOn(c, width,height)
    table.drawOn(c,40,height- 40 - 20 * len(table_data))

    c.save()

    # if file_format == 'json':
    #     with open(filename,'w') as f:
    #         json.dump(data,f,indent=4)
    
    return f"PDF file created at: {filename}"