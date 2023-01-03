from . import study
from .. import db
from flask import render_template, request
from ..models import Student
from collections import defaultdict

from datetime import datetime

pattern = '%Y/%m/%d'

@study.route('/show_records', methods=['GET'])
def show_records():
    all_students = db.session.query(Student).all()
    student_days = defaultdict(list)
    today = datetime.now()
    overdue_students = []
    for student in all_students:
        record_day = student.record_day
        past_day = (today-datetime.strptime(record_day, pattern)).days
        student_days[student.student_name] = [record_day, past_day]

        if past_day > 2:
            overdue_students.append(student.student_name)

    return render_template(
        'student/student_all.html',
        student_days=student_days,
        overdue_students=overdue_students
    )


@study.route('/record', methods=['GET'])
def record():
    return render_template('student/student_record.html')

@study.route('/record_one', methods=['POST'])
def record_one():
    data = request.json
    student_name = data['student_name']
    student = db.session.query(Student).filter(Student.student_name==student_name).first()
    response = '打卡失败...'
    if student is not None:
        today = datetime.now().strftime(pattern)
        student.record_day = today
        db.session.add(student)
        db.session.commit()
        response = '打卡成功!'
    return response