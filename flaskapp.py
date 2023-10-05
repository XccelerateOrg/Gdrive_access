from flask import Flask, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from form import VideoForm, AttendanceForm
from attendance_generator import attendance_generate
from file_migrate import move_file_to_folder, get_id, get_videos
from utilities.authenticate import authenticate

# imports from form.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, ValidationError

# imports from model.py to avoid circular import
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
    pass

# declare SQLite DB and App
db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config['SECRET_KEY'] = '962da5a46aa2aadd65d7bcaba821997ace8679jjj'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)

# including model to avoid circular import
class VideoPath(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tag: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    origin: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    video: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    destin: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    user: Mapped[str] = mapped_column(String, unique=False, nullable=False)

    def __repr__(self):
        return f"VideoPath('{self.tag}','{self.video}','{self.destin}', '{self.user})"


with app.app_context():
    db.create_all()
    
# declerations from form.py
def validate_tag(self, tag):
    tag = VideoPath.query.filter_by(tag = tag.data).first()
    if tag:
        raise ValidationError('This tag has been taken. Please choose a new tag.')
    
def validate_video_name(self, video_name):
    video_name = VideoPath.query.filter_by(video = video_name.data).first()
    if video_name:
        raise ValidationError('This video name has been taken. Please choose a new video name.')
    
class VideoForm(FlaskForm):
    tag = StringField('Tag', validators=[DataRequired(message = "Data Required for Tag"), validate_tag])
    origin = StringField('Source File link', validators=[DataRequired(message = "Data Required for Source File Link"), URL(message="URL must be valid")])
    video = StringField('Video name', validators=[DataRequired(message = "Data Required for Video Title"), validate_video_name])
    destin = StringField('Designated File link', validators=[DataRequired(message = "Data Required for Destination File Link"), URL(message="URL must be valid")])
    user = StringField('Admin', validators=[DataRequired(message = "Data Required for User")])
    submit = SubmitField('ADD')


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

    # if deleting entry
    if request.method == 'POST' and 'delete_entry_button' in request.form:
        print("Deleting Entry: " + request.form["path_id"])
        to_delete = VideoPath.query.filter_by(tag=request.form["path_id"]).first()
        db.session.delete(to_delete)
        db.session.commit()
    # if adding entry
    elif request.method == 'POST' and form.validate_on_submit():
        video = VideoPath(tag=form.tag.data, origin=form.origin.data, video=form.video.data, destin=form.destin.data, user=form.user.data)
        db.session.add(video)
        db.session.commit()
        print("Form video added to db")
        
        #inital transfer for new entry
        print("Transfering files...")
        origin = get_id(form.origin.data)
        video = form.video.data
        destin = get_id(form.destin.data)
        vid_lst = get_videos(authenticate(), origin, video)
        print("Transfering Pathname: " + video)
        print("Origin Folder ID: " + origin )
        print("Destination Folder ID: " + destin)
        print("Transfered Videos: ")

        for items in vid_lst:
            print("Transfering: " + items["name"])
            #move_file_to_folder(service=authenticate(),
                                #file_id=items['id'],
                                #folder_id=destin)
    
    videos = VideoPath.query.all()
    return render_template("class_video.html", form=form, videos=videos)


if __name__ == '__main__':
    app.run(debug=True)
