from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, ValidationError


class AttendanceForm(FlaskForm):
    coursecode = StringField('Course:', validators=[DataRequired()])
    cohortno = StringField('Cohort:', validators=[DataRequired()])
    cohortname = StringField('Cohort Name:', validators=[DataRequired()])
    submit = SubmitField('Get Attendance')


class VideoForm(FlaskForm):
    tag = StringField('Tag', validators=[DataRequired()])
    origin = StringField('Source File link', validators=[DataRequired(), URL()])
    video = StringField('Video name', validators=[DataRequired()])
    destin = StringField('Designated File link', validators=[DataRequired(), URL()])
    user = StringField('Admin', validators=[DataRequired()])
    submit = SubmitField('ADD')


"""def validate_tag(self, tag):
    tag = VideoPath.query.filter_by(tag.data).first()
    if tag:
        raise ValidationError('This tag has been taken. Please choose a new tag.')"""
