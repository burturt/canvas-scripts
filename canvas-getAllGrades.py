import re
import requests
import json
from pip._vendor.distlib.compat import raw_input

loop = True

while (loop):

    instructure_domain = str(raw_input("Please type the base URL for your canvas instance."))

    valURL = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    m = valURL.match(instructure_domain)
    if m:
        print('Valid url')
        loop = False
    else:
        print('Invalid url. Please try again.')
        if (instructure_domain.find("http://") == -1):
            print('Remember to include http:// or https:// at the beginning of the URL!')

loop = True

while (loop):
    authtoken = str(raw_input("Please paste your authentication token. You can get this by going to account --> "
                              "settings and creating a new access token.\nWord of warning: giving out this token to "
                              "anyone will give them **FULL ACCESS** to your canvas account, so be careful where you "
                              "put "
                              "this!"))
    if authtoken != '':
        loop = False
    else:
        print("No token provided.")

authhead = {"Authorization": "Bearer " + authtoken}

accept = str(raw_input(
    "Making a request to the url " +
    instructure_domain + "/api/v1 using the authentication token " +
    authtoken + ". Proceed? [Y/n]"))

if accept[0].lower() == 'y':
    print("Continuing")
else:
    print("Canceled")
    exit(1)

r = requests.get(instructure_domain + "/api/v1/users/self/courses?include[]=total_scores&include["
                                      "]=current_grading_period_scores&enrollment_type=student&include["
                                      "]=concluded&per_page=1000",
                 headers=authhead)

courses = str(r.content)
if courses == """b'{"errors":[{"message":"Invalid access token."}]}'""":
    print("Invalid access token. Exiting")
    exit(1)

loc = [mfindID.start() for mfindID in list(re.finditer('\"id\"\:', courses))]

getName = re.compile('(\"name\":\"[a-zA-Z0-9 -]+\")')
getID = re.compile('[0-9]+')
getLetterGrade = re.compile('\"computed_current_grade\":\"[A-Za-z+-]+\"')
getPercentGrade = re.compile('\"computed_current_score\":[0-9.]+')

for a in loc:
    substr = courses[int(a):]

    courseIDreg = getID.search(substr)
    courseID = substr[courseIDreg.start(0):courseIDreg.end(0)]
    print("Course ID: " + courseID)

    if "restricted" in substr[courseIDreg.end(0):50]:
        print("Course not available yet")
    else:

        try:

            mGetName = getName.search(substr)
            substr2 = courses[mGetName.start(0) + a + 8:mGetName.end(0) + a - 1]
            print("Name: " + substr2)
        except:
            print("No Course Name found")

        try:

            mGetLetterGrade = getLetterGrade.search(substr)
            substr2 = courses[mGetLetterGrade.start(0) + a + 26:mGetLetterGrade.end(0) + a - 1]
            print("Letter Grade: " + substr2)
        except:
            print("No Letter Grade found")
        try:

            mGetPercentGrade = getPercentGrade.search(substr)
            substr2 = courses[mGetPercentGrade.start(0) + a + 25:mGetPercentGrade.end(0) + a]
            print("Percent Grade: " + substr2 + "%")
        except:
            print("No Percent Grade found")
print("Done")
exit(0)
