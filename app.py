import json

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = "This is your secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


##CONFIGURE TABLE
class Student(db.Model):
    __tablename__ = "student"
    student_id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String(250), unique=True, nullable=False)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(500))
    enrollments = relationship("Enrollment", back_populates="estudent")


class Course(db.Model):
    __tablename__ = "course"
    course_id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(250), unique=True, nullable=False)
    course_name = db.Column(db.String(250), nullable=False)
    course_description = db.Column(db.String(500))
    enrollments = relationship("Enrollment", back_populates="ecourse")


class Enrollment(db.Model):
    __tablename__ = "enrollments"
    enrollment_id = db.Column(db.Integer, primary_key=True)
    estudent = relationship("Student", back_populates="enrollments")
    estudent_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False)
    ecourse = relationship("Course", back_populates="enrollments")
    ecourse_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable=False)


# db.create_all()
parser = reqparse.RequestParser()


def abort_error(error_code, error_message):
    if True:
        abort(404, error_code=error_code, error_message=error_message)


course_fields = {
    'course_id': fields.Integer,
    'course_name': fields.String,
    'course_code': fields.String,
    'course_description': fields.String,
}

student_fields = {
    'student_id': fields.Integer,
    'roll_number': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
}


class CourseAPI(Resource):
    @marshal_with(course_fields)
    def get(self, course_id):
        course = Course.query.get(course_id)
        if not course:
            abort_error(error_code="COURSE005", error_message="Course not found")
        return course, 200

    @marshal_with(course_fields)
    def delete(self, course_id):
        course = Course.query.get(course_id)
        if not course:
            abort_error(error_code="COURSE005", error_message="Course not found")
        db.session.delete(course)
        db.session.commit()
        return 'Successfully Deleted', 204

    @marshal_with(course_fields)
    def put(self, course_id):
        course = Course.query.get(course_id)
        if not course:
            abort_error(error_code="COURSE005", error_message="Course not found")
        data = request.get_json(force=True)
        if "course_name" not in data or type(data["course_name"]) != str:
            abort_error(error_code="COURSE001", error_message="Course Name is required and should be string.")
        if "course_code" not in data or type(data["course_code"]) != str:
            abort_error(error_code="COURSE002", error_message="Course Code is required and should be string.")
        if "course_description" not in data or type(data["course_description"]) != str:
            abort_error(error_code="COURSE003", error_message="Course Description should be string.")
        if course.course_code != data["course_code"] and Course.query.filter_by(
                course_code=data["course_code"]).first():
            abort_error(error_code="COURSE004",
                        error_message="The Course code should be unique. This code is already available in database")
        course.course_name = data["course_name"]
        course.course_code = data["course_code"]
        course.course_description = data["course_description"]
        db.session.commit()
        return course, 201


class CoursePostAPI(Resource):
    @marshal_with(course_fields)
    def post(self):
        data = request.get_json(force=True)
        if "course_name" not in data or type(data["course_name"]) != str:
            abort_error(error_code="COURSE001", error_message="Course Name is required and should be string.")
        if "course_code" not in data or type(data["course_code"]) != str:
            abort_error(error_code="COURSE002", error_message="Course Code is required and should be string.")
        if "course_description" not in data or type(data["course_description"]) != str:
            abort_error(error_code="COURSE003", error_message="Course Description should be string.")
        if Course.query.filter_by(course_code=data["course_code"]).first():
            abort_error(error_code="COURSE004",
                        error_message="The Course code should be unique. This code is already available in database")
        new_course = Course(
            course_name=data["course_name"],
            course_code=data["course_code"],
            course_description=data["course_description"]
        )
        db.session.add(new_course)
        db.session.commit()
        return new_course, 201


class StudentAPI(Resource):
    @marshal_with(student_fields)
    def get(self, student_id):
        student = Student.query.get(student_id)
        if not student:
            abort_error(error_code="STUDENT005", error_message="Student not found")
        return student, 200

    @marshal_with(student_fields)
    def delete(self, student_id):
        student = Student.query.get(student_id)
        if not student:
            abort_error(error_code="STUDENT005", error_message="Student not found")
        db.session.delete(student)
        db.session.commit()
        return 'Successfully Deleted', 204

    @marshal_with(student_fields)
    def put(self, student_id):
        student = Student.query.get(student_id)
        if not student:
            abort_error(error_code="STUDENT005", error_message="Student not found")
        data = request.get_json(force=True)
        if "roll_number" in data and (type(data["roll_number"]) != str or len(data["roll_number"]) <= 0):
            abort_error(error_code="STUDENT001", error_message="Roll Number required and should be String ")
        if "first_name" in data and (type(data["first_name"]) != str or len(data["first_name"]) <= 0):
            abort_error(error_code="STUDENT002", error_message="First Name is required and should be String ")
        if "last_name" in data and type(data["last_name"]) != str:
            abort_error(error_code="STUDENT003", error_message="Last Name is String")
        if "roll_number" in data and student.roll_number != data["roll_number"] and Student.query.filter_by(
                roll_number=data["roll_number"]).first():
            abort_error(error_code="STUDENT004",
                        error_message="The roll number should be unique. This roll number is already available in database")
        if "roll_number" in data:
            student.roll_number = data["roll_number"]
        if "first_name" in data:
            student.first_name = data["first_name"]
        if "last_name" in data:
            student.last_name = data["last_name"]
        db.session.commit()
        return student, 201


class StudentPostAPI(Resource):
    @marshal_with(student_fields)
    def post(self):
        data = request.get_json(force=True)
        if "roll_number" not in data or type(data["roll_number"]) != str:
            abort_error(error_code="STUDENT001", error_message="Roll Number required and should be String ")
        if "first_name" not in data or type(data["first_name"]) != str:
            abort_error(error_code="STUDENT002", error_message="First Name is required and should be String ")
        if "last_name" in data and type(data["last_name"]) != str:
            abort_error(error_code="STUDENT003", error_message="Last Name is String")
        if Student.query.filter_by(roll_number=data["roll_number"]).first():
            abort_error(error_code="STUDENT004",
                        error_message="The roll number should be unique. This roll number is already available in database")
        new_student = Student(
            roll_number=data["roll_number"],
            first_name=data["first_name"],
        )
        if "last_name" in data:
            new_student.last_name = data["last_name"]
        db.session.add(new_student)
        db.session.commit()
        return new_student, 201


class EnrollmentPostAPI(Resource):
    @marshal_with(student_fields)
    def post(self, student_id):
        student = Student.query.get(student_id)
        if not student:
            abort_error(error_code="ENROLLMENT002", error_message="Student does not exist.")
        data = request.get_json(force=True)
        course = Course.query.get(data["course_id"])
        if not course:
            abort_error(error_code="ENROLLMENT001", error_message="Course does not exist.")

        if "course_id" not in data or type(data["roll_number"]) != str:
            abort_error(error_code="STUDENT001", error_message="Roll Number required and should be String ")
        course = Course.query.get(data["course_id"])
        if not course:
            abort_error(error_code="ENROLLMENT001", error_message="Course does not exist.")
        new_student = Student(
            roll_number=data["roll_number"],
            first_name=data["first_name"],
        )
        if "last_name" in data:
            new_student.last_name = data["last_name"]
        db.session.add(new_student)
        db.session.commit()
        return new_student, 201


api.add_resource(CourseAPI, '/api/course/<course_id>')
api.add_resource(CoursePostAPI, '/api/course')
api.add_resource(StudentAPI, '/api/student/<student_id>')
api.add_resource(StudentPostAPI, '/api/student')
api.add_resource(EnrollmentPostAPI, '/api/student/<student_id>/course')

if __name__ == "__main__":
    app.run(debug=True)
