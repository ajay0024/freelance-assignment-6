from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_restful import reqparse, abort, Api, Resource

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
        abort(404, code=error_code, message=error_message)


class CourseAPI(Resource):
    def get(self, course_id):
        course = Course.query.get(course_id)
        return course

    def delete(self, todo_id):
        abort_error(todo_id)
        # del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        print(args)
        return "course", 201



class CoursePostAPI(Resource):

    def post(self):
        args = parser.parse_args()
        print("Help")
        print(args)
        return "TODOS[todo_id]", 201


api.add_resource(CourseAPI, '/api/course/<course_id>')
api.add_resource(CoursePostAPI, '/api/course')




if __name__ == "__main__":
    app.run(debug=True)
