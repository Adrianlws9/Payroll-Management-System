from database import DatabaseManager
import json

class EmployeeManager:
    def __init__(self):
        self.db = DatabaseManager()
    
    def add_employee(self, employee_data):
        try:
            # Check if employee ID already exists
            existing = self.get_employee(employee_data['employee_id'])
            if existing:
                return False, "Employee ID already exists"
            
            # Validate email format if provided
            if employee_data['email']:
                import re
                pattern = r'^1024\d{0,3}@(comp|ece|mech|civil|it|eee|ec|cs|ai|ds)\.ac\.in$'
                if not re.match(pattern, employee_data['email'].lower()):
                    return False, "Invalid email format. Must be: 1024___@dept_name.ac.in"
            
            query = '''
                INSERT INTO employees 
                (employee_id, name, email, phone, department, position, basic_salary, hire_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''
            params = (
                employee_data['employee_id'],
                employee_data['name'],
                employee_data['email'],
                employee_data['phone'],
                employee_data['department'],
                employee_data['position'],
                employee_data['basic_salary'],
                employee_data['hire_date']
            )
            success = self.db.execute_query(query, params)
            return success, "Employee added successfully" if success else "Failed to add employee"
            
        except Exception as e:
            return False, f"Error adding employee: {str(e)}"
    
    def get_employee(self, employee_id):
        try:
            query = "SELECT * FROM employees WHERE employee_id = ?"
            return self.db.fetch_one(query, (employee_id,))
        except Exception as e:
            print(f"Error getting employee: {e}")
            return None
    
    def get_all_employees(self):
        query = "SELECT * FROM employees WHERE status = 'Active' ORDER BY id"
        return self.db.fetch_all(query)
    
    def update_employee(self, employee_id, update_data):
        try:
            # Validate email format if provided
            if update_data['email']:
                import re
                pattern = r'^1024\d{0,3}@(comp|ece|mech|civil|it|eee|ec|cs|ai|ds)\.ac\.in$'
                if not re.match(pattern, update_data['email'].lower()):
                    return False, "Invalid email format. Must be: 1024___@dept_name.ac.in"
            
            query = '''
                UPDATE employees 
                SET name=?, email=?, phone=?, department=?, position=?, basic_salary=?
                WHERE employee_id=? AND status='Active'
            '''
            params = (
                update_data['name'],
                update_data['email'],
                update_data['phone'],
                update_data['department'],
                update_data['position'],
                update_data['basic_salary'],
                employee_id
            )
            success = self.db.execute_query(query, params)
            return success, "Employee updated successfully" if success else "Failed to update employee"
        except Exception as e:
            return False, f"Error updating employee: {str(e)}"
    
    def delete_employee(self, employee_id):
        query = "UPDATE employees SET status='Inactive' WHERE employee_id=?"
        self.db.execute_query(query, (employee_id,))
        return True
    
    def search_employees(self, search_term):
        query = '''
            SELECT * FROM employees 
            WHERE (name LIKE ? OR employee_id LIKE ? OR department LIKE ?) 
            AND status = 'Active'
        '''
        search_pattern = f"%{search_term}%"
        return self.db.fetch_all(query, (search_pattern, search_pattern, search_pattern))