from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


DBHOST = os.environ.get("DBHOST") or "localhost"
DBUSER = os.environ.get("DBUSER") or "root"
DBPWD = os.environ.get("DBPWD") or "passwors"
DATABASE = os.environ.get("DATABASE") or "employees"
DBPORT = int(os.environ.get("DBPORT"))
BUCKET = os.environ.get("BUCKET")
IMAGENAME = os.environ.get("IMAGENAME")
HEADER_NAME = os.environ.get("HEADER_NAME",)


db_conn = connections.Connection(
    host=DBHOST,
    port=DBPORT,
    user=DBUSER,
    password=DBPWD,
    db=DATABASE
)


def download_s3_image(bucket, image_name):
    try:
        s3 = boto3.client('s3')
        os.makedirs("app/static", exist_ok=True)
        image_path = os.path.join("app/static", "bg.jpg")
        s3.download_file(bucket, image_name, image_path)
        logging.info(f"Downloaded {image_name} from S3 bucket {bucket}")
    except Exception as e:
        logging.error(f"Error downloading image from S3: {e}")


if BUCKET and IMAGENAME:
    download_s3_image(BUCKET, IMAGENAME)
else:
    logging.warning("S3 BUCKET or IMAGENAME not provided. Background image won't be set.")

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', header=HEADER_NAME)

@app.route("/about", methods=['GET','POST'])
def about():
    return render_template('about.html', header=HEADER_NAME)

@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        cursor.execute(insert_sql, (emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = f"{first_name} {last_name}"
    finally:
        cursor.close()

    return render_template('addempoutput.html', name=emp_name, header=HEADER_NAME)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html", header=HEADER_NAME)

@app.route("/fetchdata", methods=['GET', 'POST'])
def FetchData():
    emp_id = request.form['emp_id']
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location FROM employee WHERE emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql, (emp_id,))
        result = cursor.fetchone()

        if not result:
            return "Employee not found", 404

        output = {
            "emp_id": result[0],
            "first_name": result[1],
            "last_name": result[2],
            "primary_skills": result[3],
            "location": result[4]
        }

    except Exception as e:
        logging.error(f"Error fetching employee data: {e}")
        return "Error occurred", 500
    finally:
        cursor.close()

    return render_template("getempoutput.html", **output, header=HEADER_NAME)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
