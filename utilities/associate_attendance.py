from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import datetime
format = '%I:%M %p'


def get_attendance(student_list: pd.DataFrame, attendance_list: list, dates_list: list, sort_order: list = None):

    if len(student_list) == 0 or len(attendance_list) == 0:
        return student_list
   
    # nlp = SentenceTransformer('paraphrase-albert-small-v2', cache_folder="./models")
    nlp = SentenceTransformer('thenlper/gte-base', cache_folder="./models")
    student_list["First Name"] = student_list["First Name"].astype(str)
    student_list["Last name"] = student_list["Last name"].astype(str)
    student_list['FullName'] = student_list[["First Name", "Last name"]].agg(" ".join, axis=1)
    student_list['NameVector'] = student_list["FullName"].apply(nlp.encode)
    student_list_dicts = student_list.to_dict('records')
    if not sort_order:
        sort_order = list(range(len(attendance_list)))
    for idx in tqdm(sort_order):
        attendance, attendance_date = attendance_list[idx], dates_list[idx]
        # attendance.dropna(how='all', inplace=True)
        attendance["First name"] = attendance["First name"].astype(str)
        attendance["Last name"] = attendance["Last name"].astype(str)
        attendance["FullName"] = attendance[["First name", "Last name"]].agg(" ".join, axis=1)
        attendance["Time joined"] = attendance["Time joined"].astype(str)
        attendance["Time exited"] = attendance["Time exited"].astype(str)
        attendance["Time Duration"] = " "
        for i in range(len(attendance)):
            start = attendance["Time joined"][i]
            end = attendance["Time exited"][i]
            attendance["Time Duration"][i] = (datetime.strptime(end, format) -
                                              datetime.strptime(start, format))
            attendance["Time Duration"][i] = attendance["Time Duration"][i]/pd.Timedelta(1, 'm')
        attendance["Time Duration"] = attendance["Time Duration"].astype(int)
        attendance = attendance[["FullName", "Time Duration"]].copy()
        attendance["NameVector"] = attendance["FullName"].apply(nlp.encode)

        for student in student_list_dicts:
            # cur_score = 0
            for attendant in attendance.index:
                # score = util.dot_score(student['NameVector'],
                #                        attendance.loc[attendant, ['NameVector']].values[0]).numpy()[0, 0]
                score = util.cos_sim(student['NameVector'],
                                     attendance.loc[attendant, ['NameVector']].values[0]).numpy()[0, 0]
                # print(f"{student['FullName']} x {attendance.loc[attendant, 'FullName']} = {score}")
                if score > 0.85:
                    student[attendance_date.strftime('%d-%m-%Y')] = attendance.loc[attendant, 'Time Duration']
                    # cur_score = score
                    # pass
    new_list = pd.DataFrame.from_records(student_list_dicts)
    new_list = new_list.drop(columns=['FullName', 'NameVector'])
    sorted_date_list = [dt.strftime('%d-%m-%Y') for dt in np.asarray(dates_list)[sort_order]]
    return new_list.reindex(['First Name', 'Last name'] + sorted_date_list, axis=1)
