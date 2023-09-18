from flask import Flask, render_template, request
from datetime import date
import attendance_generator

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/attendance", methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        sheet_name = request.form["course"]
        cohort = request.form.get('cohortno', type=int)
        cohort_name = request.form["cohortname"]
        try:
         attendance = attendance_generator.attendance_generate(cohort_code=cohort,
                                                              cohort_name=cohort_name,
                                                              sheet_name=sheet_name)
        except (ValueError, TypeError, IndexError):
            print("Something is wrong.")
            return render_template("attend.html")
        else:
         attendance.set_table_styles([
                    {"selector": "table",
                     "props": [("border", "2px solid black"), ("border-collapse", "collapse")]},
                    {"selector": "th",
                     "props": [("border", "2px solid black"),
                               ("border-collapse", "collapse"),
                               ("text-align", "left"), ("width", "400px")]},
                    {"selector": "td",
                     "props": [("color", "black"),
                               ("border", "2px groove black"), ("border-collapse", "collapse"), ("text-align", "center"),
                               ("width", "50px")]}])
        #attendance.to_csv(f"documents/Attendance_{cohort_name}_at_{date.today()}.csv")
        return render_template("attendance_list.html",
                               course_template=sheet_name,
                               tables=[attendance.to_html(header=True)])
    return render_template("attend.html")


if __name__ == '__main__':
    app.run(debug=True)
