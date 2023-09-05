from sentence_transformers import SentenceTransformer, util
import pandas as pd
from tqdm import tqdm


def get_attendance(student_list: pd.DataFrame, attendance_list: list, dates_list: list, sort_order: list = None):
    nlp = SentenceTransformer('paraphrase-albert-small-v2', cache_folder="./models")
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
        attendance = attendance[["FullName", "Duration"]].copy()
        attendance["NameVector"] = attendance["FullName"].apply(nlp.encode)

        for student in student_list_dicts:
            # cur_score = 0
            for attendant in attendance.index:
                score = util.dot_score(student['NameVector'],
                                       attendance.loc[attendant, ['NameVector']].values[0]).numpy()[0, 0]
                if score > 110:
                    student[attendance_date.strftime('%d-%m-%Y')] = attendance.loc[attendant, 'Duration']
                    # cur_score = score
                    # pass
    new_list = pd.DataFrame.from_records(student_list_dicts)
    new_list = new_list.drop(columns=['FullName', 'NameVector'])
    return new_list
