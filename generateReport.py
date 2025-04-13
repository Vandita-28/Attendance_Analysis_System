#Imports
import pandas as pd
from datetime import datetime

#Variables
cabin = pd.read_csv("Cabin_Info.csv")
schedule = pd.read_csv("Class_Schedule.csv")
attendance = pd.read_csv("Employee_Attendance_Data.csv")
leave = pd.read_csv("Leave_Info.csv")
slots = pd.read_csv("Slots.csv")
calender = pd.read_csv("Academic_Calender.csv")

attendance['Date'] = pd.to_datetime(attendance['Date'], format="%d-%m-%Y")
calender['Date'] = pd.to_datetime(calender['Date'], format="%d-%m-%Y")

#Input
empID = int(input("Enter Employee ID: "))
start_date = pd.to_datetime(input("Enter start date (DD-MM-YYYY): "), format="%d-%m-%Y")
end_date = pd.to_datetime(input("Enter end date (DD-MM-YYYY): "), format="%d-%m-%Y")

#Functions
def get_schedule(emp_id, schedule_df):
    return schedule_df[schedule_df['Employee ID'] == emp_id][['Class Building', 'Slot ID']].values.tolist()

def build_class_times_by_date(emp_schedule, slots_df, calender_df):
    date_to_times = {}
    instructional = calender_df[calender_df['Status'] == 'Instructional']
    for _, slot_id in emp_schedule:
        slot_rows = slots_df[slots_df['Slot_ID'] == slot_id]
        for _, slot in slot_rows.iterrows():
            day = slot['Day']
            start_time = datetime.strptime(slot['Start_Time'], "%H:%M").time()
            end_time = datetime.strptime(slot['End_Time'], "%H:%M").time()
            matching_dates = instructional[instructional['Day'] == day]
            for _, date_row in matching_dates.iterrows():
                date = date_row['Date']
                if date not in date_to_times:
                    date_to_times[date] = (start_time, end_time)
                else:
                    existing_start, existing_end = date_to_times[date]
                    date_to_times[date] = (min(existing_start, start_time), max(existing_end, end_time))
    return date_to_times

#Processing
date_range_df = calender[
    (calender['Date'] >= start_date) &
    (calender['Date'] <= end_date)
]

emp_schedule = get_schedule(empID, schedule)
class_times_by_date = build_class_times_by_date(emp_schedule, slots, calender)

# Attendance Report
print("\nAttendance Report:")
for _, row in date_range_df.iterrows():
    date = row['Date']
    day = row['Day']
    status = row['Status']
    date_str = date.strftime('%d-%m-%Y')
    label = f"{date_str} ({day})"
    if status != 'Instructional':
        print(f"{label} - Non Instructional Day")
        continue
    class_start, class_end = class_times_by_date.get(date, (None, None))
    emp_attendance = attendance[
        (attendance['Employee ID'] == empID) &
        (attendance['Date'] == date)
    ]
    if emp_attendance.empty:
        entry_status = "Absent"
        exit_status = "Absent"
    else:
        punch_in = datetime.strptime(emp_attendance.iloc[0]['Punch In Time'], "%H:%M").time()
        punch_out = datetime.strptime(emp_attendance.iloc[0]['Punch Out Time'], "%H:%M").time()
        if class_start:
            entry_status = "Arrived In Time" if punch_in <= class_start else "Late Entry"
        else:
            entry_status = "Arrived (No Class)"
        if class_end:
            exit_status = "Left On Time" if punch_out >= class_end else "Left Early"
        else:
            exit_status = "Left (No Class)"
    print(f"{label} - Entry: {entry_status} | Exit: {exit_status}")