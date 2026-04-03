from database import DatabaseManager
from datetime import datetime, timedelta

class AttendanceTracker:
    def __init__(self):
        self.db = DatabaseManager()
    
    def mark_attendance(self, employee_id, check_in=None, check_out=None):
        try:
            # Check if employee exists AND is active
            employee = self.db.fetch_one(
                "SELECT * FROM employees WHERE employee_id = ? AND status = 'Active'", 
                (employee_id,)
            )
            if not employee:
                return False, "Employee not found or inactive"
            
            today = datetime.now().strftime("%Y-%m-%d")
            
            # Check if attendance already exists for today
            existing = self.db.fetch_one(
                "SELECT * FROM attendance WHERE employee_id = ? AND date = ?",
                (employee_id, today)
            )
            
            if existing:
                # Update check-out time
                if check_out:
                    # Make sure check_in exists before calculating hours
                    if existing[3]:  # check_in time exists
                        check_in_time = datetime.strptime(existing[3], "%H:%M")
                        check_out_time = datetime.strptime(check_out, "%H:%M")
                        hours_worked = (check_out_time - check_in_time).seconds / 3600
                        
                        success = self.db.execute_query('''
                            UPDATE attendance 
                            SET check_out=?, hours_worked=?
                            WHERE employee_id=? AND date=?
                        ''', (check_out, hours_worked, employee_id, today))
                        if success:
                            return True, "Checked out successfully"
                        else:
                            return False, "Failed to update attendance"
                    else:
                        return False, "No check-in found for today"
                else:
                    return False, "No check-out time provided"
            else:
                # New attendance record
                if check_in:
                    success = self.db.execute_query('''
                        INSERT INTO attendance (employee_id, date, check_in, status)
                        VALUES (?, ?, ?, ?)
                    ''', (employee_id, today, check_in, "Present"))
                    if success:
                        return True, "Checked in successfully"
                    else:
                        return False, "Failed to save check-in"
                else:
                    return False, "No check-in time provided"
            
        except Exception as e:
            return False, f"Error marking attendance: {str(e)}"
    
    def get_attendance(self, employee_id, start_date, end_date):
        query = '''
            SELECT * FROM attendance 
            WHERE employee_id = ? AND date BETWEEN ? AND ?
            ORDER BY date DESC
        '''
        return self.db.fetch_all(query, (employee_id, start_date, end_date))
    
    def get_monthly_attendance(self, employee_id, month_year):
        query = '''
            SELECT * FROM attendance 
            WHERE employee_id = ? AND strftime('%Y-%m', date) = ?
            ORDER BY date
        '''
        return self.db.fetch_all(query, (employee_id, month_year))
    
    def calculate_working_hours(self, employee_id, month_year):
        attendance_records = self.get_monthly_attendance(employee_id, month_year)
        total_hours = sum(record[6] or 0 for record in attendance_records)
        return total_hours