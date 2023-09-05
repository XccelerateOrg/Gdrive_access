from utilities.authenticate import authenticate
from utilities.file_management import get_file_by_name, download_bytesio
import pandas as pd


if __name__ == "__main__":
    attendance_files = get_file_by_name(authenticate(), name="FTDS Apr 2023 Cohort Attendance Report")
    student_list = get_file_by_name(authenticate(), name="student list")
    file = download_bytesio(authenticate(), student_list[0], 'student_list.xlsx')
    # file = download_file_from_google_drive(student_list[0]['id'], 'student_list.csv')
    excel = pd.ExcelFile(file, engine='openpyxl')
    df_ftds = excel.parse(sheet_name='FTDS')
    print(len(attendance_files))
