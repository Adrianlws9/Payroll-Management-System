from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

class PayslipGenerator:
    def __init__(self):
        self.output_dir = "payslips"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
def generate_payslip(self, employee_data, salary_data, month_year):
    try:
        # Validate inputs
        if not employee_data or not salary_data or not month_year:
            return None, "Missing required data for payslip"
            
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        filename = f"{self.output_dir}/payslip_{employee_data[1]}_{month_year}.pdf"
        
        # Create PDF
        c = canvas.Canvas(filename, pagesize=letter)
        
        # Company Header
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 750, "ABC Company Pvt. Ltd.")
        c.setFont("Helvetica", 12)
        c.drawString(100, 730, "Pay Slip for " + month_year)
        
        # Employee Information
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, 700, "Employee Information:")
        c.setFont("Helvetica", 10)
        
        info_y = 680
        c.drawString(120, info_y, f"Employee ID: {employee_data[1]}")
        c.drawString(120, info_y-20, f"Name: {employee_data[2]}")
        c.drawString(120, info_y-40, f"Department: {employee_data[5]}")
        c.drawString(120, info_y-60, f"Position: {employee_data[6]}")
        
        # Salary Details
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, 580, "Salary Details:")
        c.setFont("Helvetica", 10)
        
        salary_y = 560
        c.drawString(120, salary_y, f"Basic Salary: ₹{salary_data['basic_salary']:,.2f}")
        c.drawString(120, salary_y-20, f"Overtime Hours: {salary_data['overtime_hours']}")
        c.drawString(120, salary_y-40, f"Overtime Pay: ₹{salary_data['overtime_pay']:,.2f}")
        c.drawString(120, salary_y-60, f"Deductions: ₹{salary_data['deductions']:,.2f}")
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(120, salary_y-90, f"Net Salary: ₹{salary_data['net_salary']:,.2f}")
        
        # Footer
        c.setFont("Helvetica", 8)
        c.drawString(100, 100, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(100, 85, "This is a computer-generated document")
        
        c.save()
        
        # Verify file was created
        if os.path.exists(filename):
            return filename, "Payslip generated successfully"
        else:
            return None, "Failed to create payslip file"
            
    except PermissionError:
        return None, "No permission to create payslip file"
    except Exception as e:
        return None, f"Error generating payslip: {str(e)}"