from flask import render_template, request, url_for, flash
from gdrive_app import app, db
from gdrive_app.utilities.attendance_generator import attendance_generate
from gdrive_app.utilities.authenticate import authenticate
from gdrive_app.models import VideoPath
from gdrive_app.forms import VideoForm, AttendanceForm
from gdrive_app.file_migrate import get_id, get_videos, move_file_to_folder


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
        except Exception as e:
            print("Something is wrong.")
            return render_template("attend.html", form=form)
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
        # attendance.to_csv(f"documents/Attendance_{cohort_name}_at_{date.today()}.csv")
        return render_template("attendance_list.html",
                               course_template=sheet_name,
                               tables=[attendance.to_html(header=True)])
    return render_template("attend.html", form=form)


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
        video = VideoPath(tag=form.tag.data, origin=form.origin.data, video=form.video.data, destin=form.destin.data,
                          user=form.user.data)
        db.session.add(video)
        db.session.commit()
        print("Form video added to db")

        # inital transfer for new entry
        print("Transfering files...")
        origin = get_id(form.origin.data)
        video = form.video.data
        destin = get_id(form.destin.data)
        vid_lst = get_videos(authenticate(), origin, video)
        print("Transfering Pathname: " + video)
        print("Origin Folder ID: " + origin)
        print("Destination Folder ID: " + destin)
        print("Transfered Videos: ")

        for items in vid_lst:
            print("Transfering: " + items["name"])
            move_file_to_folder(service=authenticate(),
                                file_id=items['id'],
                                folder_id=destin)

    videos = VideoPath.query.all()
    return render_template("class_video.html", form=form, videos=videos)
