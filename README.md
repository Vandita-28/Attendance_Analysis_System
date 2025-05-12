# Time Trail: Attendance Analysis System

Time Trail is a Python-based attendance analysis system designed for multi-building academic institutions. 
It processes and cross-validates punch-in/out data with academic schedules, slot timings, 
and building assignments to evaluate faculty attendance with precision.

This system identifies irregular attendance behavior such as late arrivals, early exits, absences, and unauthorized punch locations, providing actionable insights for administrators.

---
Features
- Analyze attendance for any employee over a custom date range.
- Detect and classify:
  - Early arrivals
  - Late for class / college
  - Absentees
  - Unauthorized punch-ins/outs (building mismatch)
- Validate punch location using class schedule and cabin assignments.
- Filter non-instructional days using academic calendar.
---
 Datasets Used
| File Name                  | Description |
|---------------------------|-------------|
| `Employee_Attendance_Data.csv` | Daily punch-in/out records including time and building info |
| `Class_Schedule.csv`      | Employee-wise class schedules with slot IDs |
| `Cabin_Info.csv`          | Employee cabin assignments and associated buildings |
| `Slots.csv`               | Slot-to-time and day mapping |
| `Academic_Calender.csv`   | Working and non-instructional days |

---
Technologies
- Language: Python 
- **Libraries:** `pandas`, `datetime`, `numpy`
- **Environment:** Google Colab / Jupyter Notebook
