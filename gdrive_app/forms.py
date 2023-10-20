from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, ValidationError
from gdrive_app.models import VideoPath


def validate_tag(self, tag):
    tag = VideoPath.query.filter_by(tag=tag.data).first()
    if tag:
        raise ValidationError('This tag has been taken. Please choose a new tag.')


class VideoForm(FlaskForm):
    tag = StringField('Tag (A name to identify the operation)', validators=[DataRequired(message="Data Required for Tag"), validate_tag])
    origin = StringField('Gdrive link to Source folder (Typically Meet Recordings)', validators=[DataRequired(message="Data Required for Source File Link"),
                                                         URL(message="URL must be valid")])
    video = StringField('Partial name of video files (Files are usually saved as the meeting name)',
                        validators=[DataRequired(message="Data Required for Video Title"),
                                    # validate_video_name
                                    ])
    destin = StringField('GDrive link to Destination folder (This is where the videos will be moved to)',
                         validators=[DataRequired(message="Data Required for Destination File Link"),
                                     URL(message="URL must be valid")])
    user = StringField('Authorizing Person', validators=[DataRequired(message="Data Required for User")])
    submit = SubmitField('ADD TO DB')


class AttendanceForm(FlaskForm):
    coursecode = StringField('Course Sheet Name in Student List (Example: FTDS, FTUX)', validators=[DataRequired()])
    cohortno = StringField('Cohort Number (in Student List):', validators=[DataRequired()])
    cohortname = StringField('Course Meeting Name (Example: FTDS Apr 2023 Cohort)', validators=[DataRequired()])
    submit = SubmitField('Get Attendance')
