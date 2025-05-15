from celery import shared_task , group
import time,os,json
from .models import Order
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
# from reportlab.lib import colors
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas
# from reportlab.platypus import Table,TableStyle
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

@shared_task
def generate_file_from_data(data,file_format = 'pdf' ):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_dir = Path("generated_files")
        output_dir.mkdir(parents=True, exist_ok=True)
        file_path = output_dir / f"data_output_{timestamp}.pdf"
            
        # print("data['orders'] ", data.values())
        # print("data['orders'][0]", data["orders"][0])
        # print("data['orders'][0]['quantity']", data["orders"][0]["quantity"])
        # print("data['products'][0]['name']", data["products"][0]["name"])
        # print("data['products'][0]['price']", data["products"][0]["price"])

        with PdfPages(file_path) as pdf:
            for section_name,records in data.items():
                if not isinstance(records, list) or not records:
                    df = pd.DataFrame([{"Message":"No Data Available"}])
                else:
                    df = pd.DataFrame(records)
                
                print(records, "record data")
                # # Convert to DataFrame
                # df = pd.DataFrame(data.values())

                # print("Data Frame Values: ",df)

                # plot the table using matplotlib

                fig ,ax = plt.subplots(figsize = (len(df.columns) * 2.5, len(df) * 0.6 + 1)) #Adjust size to fit content
                ax.axis('off') # hide axes
                table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center' , loc = 'center')

                # Add Section Title 
                title = f"{section_name.title()} Table" 
                ax.set_title(title,fontsize = 14,fontweight = 'bold')

                # Create Table in the Plot
                table = ax.table(cellText=df.values,colLabels=df.columns,cellLoc='center',loc = 'center')

                table.auto_set_font_size(False)
                table.set_fontsize(10)
                table.scale(1, 1.5)

                print("Table cells data : ",table.get_celld().items())
                # Highlighting the Summary Row
                for (row,col), cell in table.get_celld().items():
                    if row == 0:     #For Highlighting last row , if row == len(df)
                        cell.set_fontsize(10)
                        cell.set_text_props(weight='bold')
                        cell.set_facecolor('#d3d3d3')
                        cell.set_edgecolor('grey')
                        # linewidth , lineHeight need to be set
                    else:
                        cell.set_fontsize(10)
                        cell.set_facecolor('white')
                        cell.set_edgecolor('grey')
                        cell.set_text_props(ha='left')

                #   SAVE TO PDF
                pdf.savefig(fig, bbox_inches='tight')
                plt.close(fig)

    except Exception as e:
        print('Error Generating PDF : ',e)
        print( f" Error :{str(e)}") 
    print(f"PDF File created at : {file_path} ")

@shared_task
def subtask(name,delay):
    time.sleep(delay)
    return f"{name} completed in {delay}s "

@shared_task
def parent_task():
    tasks = group(
        subtask.s("task1",5),
        subtask.s("task2",3),
        subtask.s("task3",4),
        subtask.s("task4",2),
        subtask.s("task5",1)
    )
    result = tasks.apply_async()
    return result.join()