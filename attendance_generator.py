import re
from datetime import date, datetime
from utilities.authenticate import authenticate
from utilities.file_management import get_file_by_name, download_bytesio
import pandas as pd
from utilities.associate_attendance import get_attendance
from tqdm import tqdm


def convert_excel_bytes_to_dataframe(file_object, sheet_name):
    excel = pd.ExcelFile(file_object, engine='openpyxl')
    return excel.parse(sheet_name=sheet_name)


if __name__ == "__main__":
    cohort = 21
    cohort_name = "FTDS Apr 2023 Cohort"
    print("Searching files!")
    attendance_files = get_file_by_name(authenticate(), name=f"{cohort_name} Attendance Report")

    print(f"Found {len(attendance_files)} files. Downloading...")
    attendance_list = []
    dates_list = []
    for file in tqdm(attendance_files):
        attendance_list.append(convert_excel_bytes_to_dataframe(download_bytesio(authenticate(), file), "Attendees"))
        dates_list.append(datetime.strptime(re.search("\d{4}-\d+-\d+", file['name']).group(0), '%Y-%m-%d'))

    sorted_indexes = sorted(list(range(len(dates_list))), key=lambda x: dates_list[x])

    student_list = convert_excel_bytes_to_dataframe(
        download_bytesio(
            authenticate(),
            get_file_by_name(
                authenticate(),
                name="student list"
            )[0]
        ),
        "FTDS"
    )
    print("Associating Attendances...")
    student_list = student_list[student_list.Cohort == cohort]
    attendance_sheet = get_attendance(student_list=student_list[['First Name', 'Last name']].copy(0),
                                      attendance_list=attendance_list,
                                      dates_list=dates_list,
                                      sort_order=sorted_indexes)
    attendance_sheet.to_csv(f"documents/Attendance_{cohort_name}_at_{date.today()}.csv")
