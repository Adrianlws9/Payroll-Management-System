from database import DatabaseManager
from datetime import datetime

class PayrollCalculator:
    def __init__(self):
        self.db = DatabaseManager()
    
    def calculate_salary(self, employee_id, month_year, overtime_hours=0):
        try:
            # Validate inputs
            if not employee_id or not month_year:
                return None, "Employee ID and month/year are required"
                
            if overtime_hours < 0:
                return None, "Overtime hours cannot be negative"
                
            employee = self.db.fetch_one("SELECT * FROM employees WHERE employee_id = ?", (employee_id,))
            if not employee:
                return None, "Employee not found"
                
            basic_salary = employee[7]  # basic_salary column
            overtime_rate = basic_salary / (22 * 8) * 1.5  # 1.5x hourly rate
            overtime_pay = overtime_hours * overtime_rate
            
            # Simple deduction calculation
            deductions = self.calculate_deductions(basic_salary)
            
            net_salary = basic_salary + overtime_pay - deductions
            
            # CREATE THE salary_data DICTIONARY
            salary_data = {
                'basic_salary': basic_salary,
                'overtime_hours': overtime_hours,
                'overtime_pay': overtime_pay,
                'deductions': deductions,
                'net_salary': net_salary
            }
            
            return salary_data, "Salary calculated successfully"  # ← MUST RETURN 2 VALUES
            
        except Exception as e:
            return None, f"Error calculating salary: {str(e)}"  # ← MUST RETURN 2 VALUES
    
    def calculate_deductions(self, basic_salary):
        # Simple tax calculation (you can make this more complex)
        if basic_salary <= 250000:
            tax = 0
        elif basic_salary <= 500000:
            tax = (basic_salary - 250000) * 0.05
        elif basic_salary <= 1000000:
            tax = 12500 + (basic_salary - 500000) * 0.2
        else:
            tax = 112500 + (basic_salary - 1000000) * 0.3
        
        # Provident fund (12% of basic)
        pf = basic_salary * 0.12
        
        return tax + pf
    
    def save_salary_record(self, employee_id, month_year, salary_data):
        query = '''
            INSERT INTO salary_records 
            (employee_id, month_year, basic_salary, overtime_hours, overtime_pay, deductions, net_salary, payment_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            employee_id,
            month_year,
            salary_data['basic_salary'],
            salary_data['overtime_hours'],
            salary_data['overtime_pay'],
            salary_data['deductions'],
            salary_data['net_salary'],
            datetime.now().strftime("%Y-%m-%d")
        )
        self.db.execute_query(query, params)
        return True
    
    def get_salary_history(self, employee_id):
        query = '''
            SELECT * FROM salary_records 
            WHERE employee_id = ? 
            ORDER BY month_year DESC
        '''
        return self.db.fetch_all(query, (employee_id,))