from flask import Flask, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from form import VideoForm, AttendanceForm
from attendance_generator import attendance_generate


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config['SECRET_KEY'] = '962da5a46aa2aadd65d7bcaba821997ace8679jjj'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/attendance", methods=['GET', 'POST'])
def attendance():
    form = AttendanceForm()
    if request.method == 'POST':
        sheet_name = form.coursecode.data
        cohort = int(form.cohortno.data)
        cohort_name = form.cohortname.data
        try:
            attendance = attendance_generate(cohort_code=cohort, cohort_name=cohort_name, sheet_name=sheet_name)
        except (ValueError):
            print("Something is wrong.")
            return render_template("attend1.html", form=form)
        else:
             attendance.set_table_styles([
                        {"selector": "table",
                         "props": [("border", "2px solid black"), ("border-collapse", "collapse"), ("width", "120%")]},
                        {"selector": "th",
                         "props": [("border", "2px solid black"),
                                   ("border-collapse", "collapse"),
                                   ("text-align", "left")]},
                        {"selector": "td",
                         "props": [("color", "black"),
                                   ("border", "2px groove black"), ("border-collapse", "collapse"),
                                   ("text-align", "center")]}])
        #attendance.to_csv(f"documents/Attendance_{cohort_name}_at_{date.today()}.csv")
        return render_template("attendance_list.html",
                               course_template=sheet_name,
                               tables=[attendance.to_html(header=True)])
    return render_template("attend1.html", form=form)


@app.route("/classvideos", methods=['GET', 'POST'])
def classvideos():
    form = VideoForm()
    """if form.validate_on_submit():
        video = VideoPath(tag=form.tag.data, origin=form.origin.data, video=form.video.data, user=form.user.data)
        db.session.add(video)"""

    return render_template("class_video.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
