from . import study
from .. import db
from flask import render_template, request
from ..models import Student

from datetime import datetime, timedelta
from .views import pattern

students_list = [
    '王炳烨',
    '肖显扬',
    '王子钊',
    '涂人哲',
    '唐昊',
    '苏垌锟',
    '马瑞康',
    '郑宇鹏',
    '张恺隽',
    '宋昱',
    '龙泽文',
    '晋步',
    '胡尔东',
    '张亮',
    '杨振宇',
    '谷佳铭',
    '陈泽文',
    '李唯依',
    '陈丁硕',
    '梁浚洪',
    '荀天旺',
    '朱俊峰',
    '赵祉瑜',
    '赵健博',
    '张鹏程',
    '张澳',
    '曾泽铿',
    '曾繁虎',
    '苑红榜',
    '俞文浩',
    '洪玮昕',
    '谢滨键',
    '吴天琪',
    '王子翼',
    '王子都',
    '王泽禹',
    '王天',
    '韩超伟',
    '王庆宇',
    '王汉石',
    '顾浩',
    '吴昕怡',
    '唐红艳',
    '戚可盈',
    '张滢',
    '宁白杨',
    '陈璟',
    '周子琪',
    '董北北',
    '李思霏',
    '郑北辰',
    '赵士云',
    '张玮光'
]


@study.route('/console', methods=['GET'])
def student_console():
    students = db.session.query(Student).all()
    return render_template(
        'student/student_console.html',
        students=students
    )


@study.route('/console_init', methods=['GET'])
def student_init():
    return render_template('student/student_console.html')


@study.route('/init_students', methods=['GET'])
def init_students():
    db.drop_all()
    db.create_all()
    today = datetime.now()
    for student_name in students_list:
        student = Student(
            student_name=student_name,
            record_day=(today - timedelta(days=4)).strftime(pattern)
        )
        db.session.add(student)
    db.session.commit()
    return '初始化完成!'


@study.route('/change_auto', methods=['POST'])
def change_auto():
    data = request.json
    student_name = data['student_name']
    student = db.session.query(Student).filter(Student.student_name == student_name).first()
    auto_record = False
    if student is not None:
        student.auto_record = not student.auto_record
        db.session.add(student)
        db.session.commit()
        auto_record = student.auto_record
    return str(auto_record)

@study.route('/auto_record', methods=['GET'])
def auto_record():
    students = db.session.query(Student).all()
    for student in students:
        if student.auto_record:
            today = datetime.now().strftime(pattern)
            student.record_day = today
            db.session.add(student)
            db.session.commit()
    return 'auto recorded!'