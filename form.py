from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, ValidationError

class AttendanceForm(FlaskForm):
    coursecode = StringField('Course Sheet Name in Student List (Example: FTDS, FTUX)', validators=[DataRequired()])
    cohortno = StringField('Cohort Number (in Student List):', validators=[DataRequired()])
    cohortname = StringField('Course Meeting Name (Example: FTDS Apr 2023 Cohort)', validators=[DataRequired()])
    submit = SubmitField('Get Attendance')

def validate_tag(self, tag):
    tag = VideoPath.query.filter_by(tag.data).first()
    if tag:
        raise ValidationError('This tag has been taken. Please choose a new tag.')
    
def validate_video_name(self, video_name):
    video_name = VideoPath.query.filter_by(video_name.data).first()
    if video_name:
        raise ValidationError('This video name has been taken. Please choose a new video name.')
    
class VideoForm(FlaskForm):
    tag = StringField('Tag', validators=[DataRequired(message = "Data Required for Tag")])
    origin = StringField('Source File link', validators=[DataRequired(message = "Data Required for Source File Link"), URL(message="URL must be valid")])
    video = StringField('Video name', validators=[DataRequired(message = "Data Required for Video Title")])
    destin = StringField('Designated File link', validators=[DataRequired(message = "Data Required for Destination File Link"), URL(message="URL must be valid")])
    user = StringField('Admin', validators=[DataRequired(message = "Data Required for User")])
    submit = SubmitField('ADD')

