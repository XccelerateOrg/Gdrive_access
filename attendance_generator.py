import re
from datetime import date, datetime
from utilities.authenticate import authenticate
from utilities.file_management import get_file_by_name, download_bytesio
import pandas as pd
from utilities.associate_attendance import get_attendance
from tqdm import tqdm


def colourcode(color):
    if isinstance(color, str):
        return 'background-color: %s' % color


def convert_excel_bytes_to_dataframe(file_object, sheet_name):
    excel = pd.ExcelFile(file_object, engine='openpyxl')
    return excel.parse(sheet_name=sheet_name)


def attendance_generate(cohort_code: int, cohort_name, sheet_name):
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
        sheet_name
    )
    print("Associating Attendances...")
    student_list = student_list[student_list.Cohort == cohort_code]
    attendance_sheet = get_attendance(student_list=student_list[['First Name', 'Last name']].copy(0),
                                      attendance_list=attendance_list,
                                      dates_list=dates_list,
                                      sort_order=sorted_indexes)
    df = pd.DataFrame(attendance_sheet)
    df.set_index(["First Name", "Last name"], inplace=True)
    week = []
    dates = df.columns
    x = len(dates) % 3
    leng = int(len(dates) / 3)
    for i in range(leng):
        week.append('Week ' + str(i + 1))
    if x == 0:
        col = pd.MultiIndex.from_product([week, [1, 2, 3]])
    else:
        week.append('Week ' + str(leng + 1))
        col1 = pd.MultiIndex.from_product([week, [1, 2, 3]])
        if x == 1:
            col = col1[0:-2]
        else:
            col = col1[0:-1]
    df = df.set_axis(col, axis='columns')
    # Fill absent as 0 mins duration
    df.fillna(0, inplace=True)
    df["% participation"] = 0 * len(df.index)
    # Determining color-code and participation rate
    for ind in df.index:
        count = 0
        for c in df.columns[0:-1]:
            if df.at[ind, c] >= 40:
                count = count + 1
                color = "limegreen"
            elif df.at[ind, c] >= 30:
                color = "gold"
            else:
                color = "red"
            df.at[ind, c] = color
        if count > 0:
            df.at[ind, "% participation"] = count/int(len(dates))
    df["% participation"] = df["% participation"].map('{:.0%}'.format)
    s = (df.style.applymap(colourcode)
         .format(formatter=" ", subset=(df.select_dtypes(object).columns[0:-1]))
         .set_caption("from " + str(dates[0]) + " to " + str(dates[-1])))
    return s

