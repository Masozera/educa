import requests

username = ''
password = ''

base_url = 'http://127.0.0.1:8000/api/' 

# retrieve all courses 
r = requests.get(f'{base_url}courses/') 
courses = r.json()

available_courses = ', '.join([course['title'] for course in courses])
print(f'Available courses: {available_courses}')

# You import the Requests library and define the base URL for the API.
# 2. You use requests.get() to retrieve data from the API by sending a GET
# request to the URL http://127.0.0.1:8000/api/courses/. This API
# endpoint is publicly accessible, so it does not require any authentication.
# 3. You use the json() method of the response object to decode the JSON data
# returned by the API.
# 4. You print the title attribute of each course.

for course in courses:
    course_id = course['id']
    course_title = course['title']
    r = requests.post(f'{base_url}courses/{course_id}/enroll/', auth=(username, password))
    if r.status_code == 200:
        # successful request
        print(f'Successfully enrolled in {course_title}')

# Replace the values for the username and password variables with the credentials of
# an existing user.
# 1. You define the username and password of the student you want to enroll
# on courses.
# 2. You iterate over the available courses retrieved from the API.
# 3. You store the course ID attribute in the course_id variable and the title
# attribute in the course_title variable.
# 4. You use requests.post() to send a POST request to the URL
# http://127.0.0.1:8000/api/courses/[id]/enroll/ for each course.
# This URL corresponds to the CourseEnrollView API view, which
# allows you to enroll a user on a course. You build the URL for each
# course using the course_id variable. The CourseEnrollView view
# requires authentication. It uses the IsAuthenticated permission and the
# BasicAuthentication authentication class. The Requests library supports
# HTTP basic authentication out of the box. You use the auth parameter to
# pass a tuple with the username and password to authenticate the user using
# HTTP basic authentication.
# 5. If the status code of the response is 200 OK, you print a message to indicate
# that the user has been successfully enrolled on the course.
