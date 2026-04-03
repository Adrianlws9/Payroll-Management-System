import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from employee_manager import EmployeeManager
from attendance_tracker import AttendanceTracker
from payroll_calculator import PayrollCalculator
from payslip_generator import PayslipGenerator
from datetime import datetime

class PayrollSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Payroll Management System")
        self.root.geometry("1000x700")
        
        # Initialize managers
        self.emp_manager = EmployeeManager()
        self.attendance_tracker = AttendanceTracker()
        self.payroll_calculator = PayrollCalculator()
        self.payslip_generator = PayslipGenerator()
        
        self.setup_gui()
    
    def setup_gui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create frames for different sections
        self.employee_frame = ttk.Frame(self.notebook)
        self.attendance_frame = ttk.Frame(self.notebook)
        self.payroll_frame = ttk.Frame(self.notebook)
        self.reports_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.employee_frame, text="Employee Management")
        self.notebook.add(self.attendance_frame, text="Attendance")
        self.notebook.add(self.payroll_frame, text="Payroll")
        self.notebook.add(self.reports_frame, text="Reports")
        
        self.setup_employee_management()
        self.setup_attendance_management()
        self.setup_payroll_management()
        self.setup_reports()

         # BIND TAB CHANGE EVENT
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
    
    def setup_employee_management(self):
        # Employee form
        form_frame = ttk.LabelFrame(self.employee_frame, text="Employee Details")
        form_frame.pack(fill='x', padx=10, pady=5)
        
        labels = ['Employee ID', 'Name', 'Email', 'Phone', 'Department', 'Position', 'Basic Salary']
        self.employee_entries = {}
        
        departments = ['comp', 'ece', 'mech', 'civil', 'it', 'eee', 'ec', 'cs', 'ai', 'ds']
        
        for i, label in enumerate(labels):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='w')
            
            if label == 'Department':
                # Use Combobox for department selection
                department_var = tk.StringVar()
                entry = ttk.Combobox(form_frame, textvariable=department_var, values=departments)
                entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
                self.employee_entries[label] = entry
            else:
                entry = ttk.Entry(form_frame)
                entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
                self.employee_entries[label] = entry
            
            # Add real-time validation for email field
            if label == 'Email':
                entry.bind('<KeyRelease>', self.validate_email_real_time)
        
        # Add email format hint
        email_hint = ttk.Label(form_frame, text="Format: 1024___@dept_name.ac.in", 
                            font=('Arial', 8), foreground='gray')
        email_hint.grid(row=2, column=2, padx=5, sticky='w')
        
        # Add department hint
        dept_hint = ttk.Label(form_frame, text="Departments: comp, ece, mech, civil, it, eee, ec, cs, ai, ds", 
                            font=('Arial', 8), foreground='gray')
        dept_hint.grid(row=4, column=2, padx=5, sticky='w')
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=len(labels), column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Add Employee", command=self.add_employee).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Update Employee", command=self.update_employee).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete Employee", command=self.delete_employee).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_employee_form).pack(side='left', padx=5)
        
        # Search
        search_frame = ttk.Frame(self.employee_frame)
        search_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side='left')
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side='left', padx=5, fill='x', expand=True)
        ttk.Button(search_frame, text="Search", command=self.search_employees).pack(side='left', padx=5)
        ttk.Button(search_frame, text="Show All", command=self.load_employees).pack(side='left', padx=5)
        
        # Employee list
        list_frame = ttk.LabelFrame(self.employee_frame, text="Employees")
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        columns = ('Sr No', 'Employee ID', 'Name', 'Department', 'Position', 'Salary')
        self.employee_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Set column headings and widths
        self.employee_tree.heading('Sr No', text='Sr No')
        self.employee_tree.heading('Employee ID', text='Employee ID')
        self.employee_tree.heading('Name', text='Name')
        self.employee_tree.heading('Department', text='Department')
        self.employee_tree.heading('Position', text='Position')
        self.employee_tree.heading('Salary', text='Salary')
        
        self.employee_tree.column('Sr No', width=60)
        self.employee_tree.column('Employee ID', width=100)
        self.employee_tree.column('Name', width=150)
        self.employee_tree.column('Department', width=120)
        self.employee_tree.column('Position', width=120)
        self.employee_tree.column('Salary', width=100)
        
        self.employee_tree.pack(fill='both', expand=True)
        self.employee_tree.bind('<<TreeviewSelect>>', self.on_employee_select)
        
        # Load employees with sequential numbering
        self.load_employees()
    def validate_email_format(self, email):
        """
        Validate email format: 1024___@dept_name.ac.in
        Pattern: 4 digits + optional 3 digits + @ + department name + .ac.in
        Example: 1024@comp.ac.in, 1024123@ece.ac.in
        """
        import re
        
        # Strip whitespace and convert to lowercase
        email = email.strip().lower()
        
        # Regular expression pattern for validation
        pattern = r'^1024\d{0,3}@(comp|ece|mech|civil|it|eee|ec|cs|ai|ds)\.ac\.in$'
        
        # Check if email matches the pattern
        if re.match(pattern, email):
            return True, "Valid email format"
        else:
            return False, "Email must be in format: 1024___@dept_name.ac.in\nExample: 1024@comp.ac.in or 1024123@ece.ac.in"
          
    def load_attendance_records(self):
        # Clear existing records
        for item in self.attendance_tree.get_children():
            self.attendance_tree.delete(item)
        
        # Load only attendance records for active employees
        query = """
            SELECT a.* 
            FROM attendance a 
            JOIN employees e ON a.employee_id = e.employee_id 
            WHERE e.status = 'Active'
            ORDER BY a.date DESC, a.employee_id
        """
        records = self.attendance_tracker.db.fetch_all(query)
        
        for record in records:
            self.attendance_tree.insert('', 'end', values=(
                record[0],  # ID
                record[1],  # Employee ID
                record[2],  # Date
                record[3] or '-',  # Check In
                record[4] or '-',  # Check Out
                f"{record[5]:.2f}" if record[5] else '0.00'  # Hours Worked
            ))

    def setup_attendance_management(self):
        # Attendance form
        form_frame = ttk.LabelFrame(self.attendance_frame, text="Mark Attendance")
        form_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(form_frame, text="Employee ID:").grid(row=0, column=0, padx=5, pady=5)
        self.attendance_emp_id = ttk.Entry(form_frame)
        self.attendance_emp_id.grid(row=0, column=1, padx=5, pady=5)
        
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Check In", 
                  command=lambda: self.mark_attendance('check_in')).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Check Out", 
                  command=lambda: self.mark_attendance('check_out')).pack(side='left', padx=5)
        
       # Attendance list
        list_frame = ttk.LabelFrame(self.attendance_frame, text="Attendance Records")
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        columns = ('ID', 'Employee ID', 'Date', 'Check In', 'Check Out', 'Hours')
        self.attendance_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.attendance_tree.heading(col, text=col)
            self.attendance_tree.column(col, width=100)
        
        self.attendance_tree.pack(fill='both', expand=True)
        
        # LOAD ATTENDANCE RECORDS WHEN TAB OPENS
        self.load_attendance_records()
    
    def setup_payroll_management(self):
        # Payroll form
        form_frame = ttk.LabelFrame(self.payroll_frame, text="Process Payroll")
        form_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(form_frame, text="Employee ID:").grid(row=0, column=0, padx=5, pady=5)
        self.payroll_emp_id = ttk.Entry(form_frame)
        self.payroll_emp_id.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Month-Year (YYYY-MM):").grid(row=1, column=0, padx=5, pady=5)
        self.payroll_month = ttk.Entry(form_frame)
        self.payroll_month.grid(row=1, column=1, padx=5, pady=5)
        self.payroll_month.insert(0, datetime.now().strftime("%Y-%m"))
        
        ttk.Label(form_frame, text="Overtime Hours:").grid(row=2, column=0, padx=5, pady=5)
        self.overtime_hours = ttk.Entry(form_frame)
        self.overtime_hours.grid(row=2, column=1, padx=5, pady=5)
        self.overtime_hours.insert(0, "0")
        
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Calculate Salary", 
                  command=self.calculate_salary).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Generate Payslip", 
                  command=self.generate_payslip).pack(side='left', padx=5)
        
        # Salary details
        details_frame = ttk.LabelFrame(self.payroll_frame, text="Salary Details")
        details_frame.pack(fill='x', padx=10, pady=5)
        
        self.salary_text = tk.Text(details_frame, height=8, width=80)
        self.salary_text.pack(fill='both', padx=5, pady=5)
    
    def setup_reports(self):
        # Reports frame
        reports_frame = ttk.Frame(self.reports_frame)
        reports_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        ttk.Button(reports_frame, text="Generate Monthly Report", 
                  command=self.generate_monthly_report).pack(pady=5)
        ttk.Button(reports_frame, text="View Salary History", 
                  command=self.view_salary_history).pack(pady=5)
        
        # Report display
        self.report_text = tk.Text(reports_frame, height=20, width=80)
        self.report_text.pack(fill='both', expand=True, pady=5)
    
    def validate_employee_input(self):
        try:
            # Check required fields
            employee_id = self.employee_entries['Employee ID'].get().strip()
            name = self.employee_entries['Name'].get().strip()
            salary_text = self.employee_entries['Basic Salary'].get().strip()
            
            if not employee_id:
                return False, "Employee ID is required"
            if not name:
                return False, "Employee Name is required"
            if not salary_text:
                return False, "Basic Salary is required"
                
            # Validate salary
            salary = float(salary_text)
            if salary <= 0:
                return False, "Salary must be positive"
                
            # Validate email format if provided
            email = self.employee_entries['Email'].get().strip()
            if email:
                is_valid, email_message = self.validate_email_format(email)
                if not is_valid:
                    return False, email_message
            
            return True, "Valid"
            
        except ValueError:
            return False, "Please enter a valid number for salary"
    # Employee Management Methods
    def add_employee(self):
        # First validate all inputs
        is_valid, message = self.validate_employee_input()
        if not is_valid:
            messagebox.showerror("Input Error", message)
            return
        
        try:
            employee_data = {
                'employee_id': self.employee_entries['Employee ID'].get().strip(),
                'name': self.employee_entries['Name'].get().strip(),
                'email': self.employee_entries['Email'].get().strip(),
                'phone': self.employee_entries['Phone'].get().strip(),
                'department': self.employee_entries['Department'].get().strip(),
                'position': self.employee_entries['Position'].get().strip(),
                'basic_salary': float(self.employee_entries['Basic Salary'].get().strip()),
                'hire_date': datetime.now().strftime("%Y-%m-%d")
            }
            
            # Validate required fields again
            if not employee_data['employee_id']:
                messagebox.showerror("Input Error", "Employee ID is required")
                return
            if not employee_data['name']:
                messagebox.showerror("Input Error", "Employee Name is required")
                return
            
            success, message = self.emp_manager.add_employee(employee_data)
            if success:
                messagebox.showinfo("Success", message)
                self.clear_employee_form()
                self.load_employees()
            else:
                messagebox.showerror("Error", message)

        except ValueError as e:
            messagebox.showerror("Input Error", "Please enter a valid number for salary")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add employee: {str(e)}")
    def validate_email_real_time(self, *args):
        """Real-time email validation as user types"""
        email = self.employee_entries['Email'].get().strip()
        
        if email:  # Only validate if email is not empty
            is_valid, message = self.validate_email_format(email)
            
            # Change background color based on validation
            if is_valid:
                self.employee_entries['Email'].config(background='#e8f5e8')  # Light green
            else:
                self.employee_entries['Email'].config(background='#ffe6e6')  # Light red
        else:
            self.employee_entries['Email'].config(background='white')  # Default
    def update_employee(self):
        try:
            employee_id = self.employee_entries['Employee ID'].get().strip()
            if not employee_id:
                messagebox.showwarning("Warning", "Please select an employee to update")
                return
            
            # Validate inputs first
            is_valid, message = self.validate_employee_input()
            if not is_valid:
                messagebox.showerror("Input Error", message)
                return
            
            update_data = {
                'name': self.employee_entries['Name'].get().strip(),
                'email': self.employee_entries['Email'].get().strip(),
                'phone': self.employee_entries['Phone'].get().strip(),
                'department': self.employee_entries['Department'].get().strip(),
                'position': self.employee_entries['Position'].get().strip(),
                'basic_salary': float(self.employee_entries['Basic Salary'].get().strip())
            }
            
            success, message = self.emp_manager.update_employee(employee_id, update_data)
            if success:
                messagebox.showinfo("Success", message)
                self.load_employees()
            else:
                messagebox.showerror("Error", message)
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for salary")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update employee: {str(e)}")
    
    def delete_employee(self):
        employee_id = self.employee_entries['Employee ID'].get()
        if not employee_id:
            messagebox.showwarning("Warning", "Please select an employee to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this employee?"):
            if self.emp_manager.delete_employee(employee_id):
                messagebox.showinfo("Success", "Employee deleted successfully!")
                self.clear_employee_form()
                self.load_employees()
    
    def clear_employee_form(self):
        for entry in self.employee_entries.values():
            entry.delete(0, tk.END)
    
    def load_employees(self):
        # Clear existing records
        for item in self.employee_tree.get_children():
            self.employee_tree.delete(item)
        
        employees = self.emp_manager.get_all_employees()
        
        # Use sequential numbering starting from 1
        serial_number = 1
        for emp in employees:
            self.employee_tree.insert('', 'end', values=(
                serial_number,           # Sequential number (1, 2, 3...)
                emp[1],                  # Employee ID (EMP001, EMP002, etc.)
                emp[2],                  # Name
                emp[5],                  # Department
                emp[6],                  # Position
                f"₹{emp[7]:,.2f}"       # Salary
            ))
            serial_number += 1
    
    def search_employees(self):
        search_term = self.search_entry.get().strip()
        if not search_term:
            self.load_employees()  # Show all with sequential numbering
            return
        
        # Clear existing records
        for item in self.employee_tree.get_children():
            self.employee_tree.delete(item)
        
        employees = self.emp_manager.search_employees(search_term)
        
        # Use sequential numbering for search results too
        serial_number = 1
        for emp in employees:
            self.employee_tree.insert('', 'end', values=(
                serial_number,           # Sequential number
                emp[1],                  # Employee ID
                emp[2],                  # Name
                emp[5],                  # Department
                emp[6],                  # Position
                f"₹{emp[7]:,.2f}"       # Salary
            ))
            serial_number += 1
    
    def on_employee_select(self, event):
        selection = self.employee_tree.selection()
        if selection:
            item = selection[0]
            values = self.employee_tree.item(item, 'values')
            
            # Clear all fields first
            self.clear_employee_form()
            
            # values[0] = Sequential number (1, 2, 3...)
            # values[1] = Employee ID (EMP001, EMP002, etc.)
            employee_id = values[1]  # This is the actual Employee ID
            
            # Fill the form with selected employee data
            self.employee_entries['Employee ID'].insert(0, employee_id)
            self.employee_entries['Name'].insert(0, values[2])         # Name
            self.employee_entries['Department'].insert(0, values[3])   # Department
            self.employee_entries['Position'].insert(0, values[4])     # Position
            
            # Get email and phone from database (not shown in table)
            employee_details = self.emp_manager.get_employee(employee_id)
            if employee_details:
                self.employee_entries['Email'].insert(0, employee_details[3] or '')
                self.employee_entries['Phone'].insert(0, employee_details[4] or '')
                self.employee_entries['Basic Salary'].insert(0, str(employee_details[7] or ''))
    
    # Attendance Methods
    def mark_attendance(self, action_type):
        employee_id = self.attendance_emp_id.get().strip()
        if not employee_id:
            messagebox.showwarning("Warning", "Please enter Employee ID")
            return
        
        current_time = datetime.now().strftime("%H:%M")
        
        try:
            # Call the attendance tracker
            if action_type == 'check_in':
                success, message = self.attendance_tracker.mark_attendance(employee_id, check_in=current_time)
            else:
                success, message = self.attendance_tracker.mark_attendance(employee_id, check_out=current_time)
            
            # Show message and refresh attendance records
            if success:
                messagebox.showinfo("Success", f"{message} at {current_time}")
                self.load_attendance_records()  # Refresh the table
                self.attendance_emp_id.delete(0, tk.END)  # Clear the input field
            else:
                messagebox.showerror("Error", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to mark attendance: {str(e)}")
    def on_tab_changed(self, event):
        selected_tab = self.notebook.index(self.notebook.select())
        if selected_tab == 1:  # Attendance tab is index 1
            self.load_attendance_records()
    # Payroll Methods
    def calculate_salary(self):
        employee_id = self.payroll_emp_id.get()
        month_year = self.payroll_month.get()
        overtime_hours = float(self.overtime_hours.get() or 0)
        
        if not employee_id or not month_year:
            messagebox.showwarning("Warning", "Please fill all fields")
            return
        
        salary_data = self.payroll_calculator.calculate_salary(
            employee_id, month_year, overtime_hours
        )
        
        if salary_data:
            self.salary_text.delete(1.0, tk.END)
            self.salary_text.insert(tk.END, f"Salary Calculation for {month_year}\n")
            self.salary_text.insert(tk.END, f"Basic Salary: ₹{salary_data['basic_salary']:,.2f}\n")
            self.salary_text.insert(tk.END, f"Overtime Pay: ₹{salary_data['overtime_pay']:,.2f}\n")
            self.salary_text.insert(tk.END, f"Deductions: ₹{salary_data['deductions']:,.2f}\n")
            self.salary_text.insert(tk.END, f"Net Salary: ₹{salary_data['net_salary']:,.2f}\n")
            
            # Save to database
            self.payroll_calculator.save_salary_record(employee_id, month_year, salary_data)
        else:
            messagebox.showerror("Error", "Employee not found")
    
    def generate_payslip(self):
        try:
            employee_id = self.payroll_emp_id.get().strip()
            month_year = self.payroll_month.get().strip()
            
            if not employee_id or not month_year:
                messagebox.showwarning("Warning", "Please enter Employee ID and Month-Year")
                return
            
            # Get employee data
            employee = self.emp_manager.get_employee(employee_id)
            if not employee:
                messagebox.showerror("Error", "Employee not found")
                return
            
            # Calculate salary data first
            overtime_text = self.overtime_hours.get().strip()
            overtime_hours = float(overtime_text) if overtime_text else 0.0
            
            # This should return TWO values: (salary_data, message)
            result = self.payroll_calculator.calculate_salary(
                employee_id, month_year, overtime_hours
            )
            print(f"DEBUG: calculate_salary returned: {type(result)} - {result}")
        
            if isinstance(result, tuple):
                print(f"DEBUG: Tuple length: {len(result)}")
                salary_data, calc_message = result
            else:
                salary_data = result
                calc_message = "Calculation completed"
            # Check if result has two values
            if isinstance(result, tuple) and len(result) == 2:
                salary_data, calc_message = result
            else:
                # Handle case where only one value is returned
                salary_data = result
                calc_message = "Calculation completed"
            
            if not salary_data:
                messagebox.showerror("Error", calc_message)
                return
            
            # Generate payslip - this should also return TWO values
            result2 = self.payslip_generator.generate_payslip(
                employee, salary_data, month_year
            )
            
            # Check if result has two values
            if isinstance(result2, tuple) and len(result2) == 2:
                filename, message = result2
            else:
                # Handle case where only one value is returned
                filename = result2
                message = "Payslip generation completed"
            
            if filename:
                messagebox.showinfo("Success", f"{message}\nFile saved as: {filename}")
            else:
                messagebox.showerror("Error", message)
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid overtime hours")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate payslip: {str(e)}")
    
    # Report Methods
    def generate_monthly_report(self):
        # Simple report generation
        employees = self.emp_manager.get_all_employees()
        
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(tk.END, "Monthly Payroll Report\n")
        self.report_text.insert(tk.END, "="*50 + "\n")
        
        total_salary = 0
        for emp in employees:
            salary_data = self.payroll_calculator.calculate_salary(emp[1], datetime.now().strftime("%Y-%m"))
            if salary_data:
                self.report_text.insert(tk.END, f"{emp[2]}: ₹{salary_data['net_salary']:,.2f}\n")
                total_salary += salary_data['net_salary']
        
        self.report_text.insert(tk.END, f"\nTotal Monthly Salary: ₹{total_salary:,.2f}\n")
    
    def view_salary_history(self):
        employee_id = simpledialog.askstring("Input", "Enter Employee ID:")
        if employee_id:
            history = self.payroll_calculator.get_salary_history(employee_id)
            
            self.report_text.delete(1.0, tk.END)
            self.report_text.insert(tk.END, f"Salary History for {employee_id}\n")
            self.report_text.insert(tk.END, "="*50 + "\n")
            
            for record in history:
                self.report_text.insert(tk.END, 
                    f"{record[2]}: ₹{record[7]:,.2f} (Paid on: {record[8]})\n")