from fpdf import FPDF
from datetime import datetime

def generate_health_report(name, email, prediction_result, disease_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="MediScan AI - Health Report", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {email}", ln=True)
    pdf.cell(200, 10, txt=f"Disease Checked: {disease_name}", ln=True)
    pdf.cell(200, 10, txt=f"Prediction Result: {prediction_result}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

    filename = f"{disease_name}_report.pdf"
    pdf.output(filename)
    return filename
