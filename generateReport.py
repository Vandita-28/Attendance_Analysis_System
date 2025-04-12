# Imports
import pandas as pd
from datetime import datetime, timedelta

# Variables
cabin = pd.read_csv("Cabin_Info.csv")
schedule = pd.read_csv("Class_Schedule.csv")
attendance = pd.read_csv("Employee_Attendance_Data.csv")
leave = pd.read_csv("Leave_Info.csv")
slots = pd.read_csv("Slots.csv")
calender = pd.read_csv("Academic_Calender.csv")

# Functions
def get_schedule(emp_id, schedule_df):
    result = schedule_df[schedule_df['Employee ID'] == emp_id][['Class Building', 'Slot ID']]
    return list(result.itertuples(index=False, name=None))

def get_class(schedule_list, slots_df):
    result = []
    for _, slot_id in schedule_list:
        matches = slots_df[slots_df['Slot_ID'] == slot_id]
        result.extend(matches[['Start_Time', 'End_Time', 'Day']].itertuples(index=False, name=None))
    return result

def filter_classes(class_schedule, calender_df):
    instructional_df = calender_df[calender_df['Status'] == 'Instructional']
    day_to_date = {}
    for _, row in instructional_df.iterrows():
        day = row['Day']
        date = row['Date']
        if day not in day_to_date:
            day_to_date[day] = date
    filtered_schedule = []
    for start, end, day in class_schedule:
        if day in day_to_date:
            filtered_schedule.append((start, end, day, day_to_date[day]))
    return filtered_schedule

def build_first_class_times(schedule_list, slots_df):
    class_times = {}
    for _, slot_id in schedule_list:
        matches = slots_df[slots_df['Slot_ID'] == slot_id]
        for _, row in matches.iterrows():
            start_time = datetime.strptime(row['Start_Time'], "%H:%M").time()
            day = row['Day']
            if day not in class_times or start_time < class_times[day]:
                class_times[day] = start_time
    return class_times

def full_attendance_report(emp_id, date_df, attendance_df, class_slots_df):
    results = []

    # Create a dict of class days and their corresponding start times
    emp_schedule = get_schedule(emp_id, schedule)
    first_class_time = build_first_class_times(emp_schedule, slots)

    for _, row in date_df.iterrows():
        date = row['Date']
        day = row['Day']
        work_start_str = row['From Time']

        if work_start_str == 'NA':
            continue

        work_start = datetime.strptime(work_start_str, "%H:%M").time()

        emp_attendance = attendance_df[
            (attendance_df['Employee ID'] == emp_id) & 
            (attendance_df['Date'] == date)
        ]

        if emp_attendance.empty:
            status = "Absent"
        else:
            punch_in_str = emp_attendance.iloc[0]['Punch In Time']
            punch_in_time = datetime.strptime(punch_in_str, "%H:%M").time()

            if punch_in_time <= work_start:
                status = "Arrived In Time"
            else:
                if day in first_class_time:
                    if punch_in_time <= first_class_time[day]:
                        status = "Late entry"
                    else:
                        status = "Late to class"
                else:
                    status = "Late entry"
        results.append((date.strftime("%d-%m-%Y"), day, str(work_start), status))
    return results

# Processing
empID = int(input("Enter Employee ID: "))
classes = get_schedule(empID, schedule)
classes = get_class(classes, slots)
classes = filter_classes(classes, calender)

attendance['Date'] = pd.to_datetime(attendance['Date'], format="%d-%m-%Y")
calender['Date'] = pd.to_datetime(calender['Date'], format="%d-%m-%Y")

start_date_str = input("Enter start date (DD-MM-YYYY): ")
end_date_str = input("Enter end date (DD-MM-YYYY): ")
start_date = pd.to_datetime(start_date_str, format="%d-%m-%Y")
end_date = pd.to_datetime(end_date_str, format="%d-%m-%Y")

date_range_df = calender[
    (calender['Date'] >= start_date) &
    (calender['Date'] <= end_date) &
    (calender['Status'] == 'Instructional')
]

emp_schedule = get_schedule(empID, schedule)
class_slots = get_class(emp_schedule, slots)
filtered_classes = filter_classes(class_slots, calender)

timetable = pd.DataFrame(filtered_classes, columns=['Start_Time', 'End_Time', 'Day', 'Date'])
timetable['Employee ID'] = empID
timetable['Date'] = pd.to_datetime(timetable['Date'], dayfirst=True)

attendance_report = full_attendance_report(empID, date_range_df, attendance, timetable)
print("\nAttendance Report (Instructional Days):")
for date, day, work_start, status in attendance_report:
    print(f"{date} ({day}) - Work starts at {work_start} - {status}")
