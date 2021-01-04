#!/bin/python3
# canvasGrades.py
# Enjoy!
#    Canvas-Get Grades
#    Copyright (C) 2020 burturt
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import datetime
import sys
import json
import requests


def getGrades(API_URL, API_KEY, year_filter = None, month_filter = None):
    LINE = "---------------------------\n"
    if not (sys.version_info.major == 3):
        print(
            "It appears you are not using python 3. Python 3 is the only supported version and no support will be given "
            "for other versions of python. You have been warned.")
    grades = ""
    try:
        r = requests.get(API_URL + "/api/v1/users/self/courses?include[]=total_scores&include["
                                              "]=current_grading_period_scores&enrollment_type=student&include["
                                              "]=concluded&per_page=1000",
                         headers={"Authorization": "Bearer " + API_KEY})

        courses = json.loads(r.content.decode("utf-8"))
    except:
        print("An error occurred while trying to get the grades. Make sure the URL and token is correct!")
        raise

    grades += LINE

    if year_filter and month_filter:
        search_string = year_filter + "-" + month_filter + "-01"
        search_date = datetime.datetime.strptime(search_string, "%Y-%m-%d")
        grades += "Searching all courses around the date " + str(search_date.date()) + ":\n"
    else:
        grades += "Searching all courses:\n"
        search_date = None


    for i in courses:
        # Some courses don't have a start_date b/c they are closed
        if "access_restricted_by_date" in i:
            continue
        start_date = datetime.datetime.strptime(i["start_at"], '%Y-%m-%dT%H:%M:%SZ')
        if search_date:
            date_difference = abs((start_date - search_date).days)
            if not (date_difference < 60):
                continue
        grades += LINE
        grades += "Course name: " + i["name"] + "\n"
        grades += "Course ID: " + str(i["id"]) + "\n"
        grades += "Start date: " + str(start_date.date()) + "\n"
        grades += "Letter Grade: " + str(i["enrollments"][0]["computed_current_grade"]) + "\n"

        grades += "Percent Grade: " + str(i["enrollments"][0]["computed_current_score"]) + ("%" if i["enrollments"][0]["computed_current_score"] else "") + "\n"

    grades += LINE

    print(grades)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) != 5 and len(sys.argv) != 3:
        pass
    elif len(sys.argv) == 3:
        getGrades(sys.argv[1], sys.argv[2])
        exit(0)
    else:
        getGrades(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        exit(0)

    # If called directly w/o arguments

    print("Canvas-getAllGradesV2  Copyright (C) 2020 burturt")
    print("This program comes with ABSOLUTELY NO WARRANTY; for details see https://git.io/Jv9Hg.")
    print("This is free software, and you are welcome to redistribute it")
    print("under certain conditions; see https://git.io/Jv9Hg details.")
    print("Should the above links not work, please refer to the GNU General Public License as published by the Free "
          "Software Foundation, either version 3 of the License, or any later version. A copy of that license should have "
          "been included with this program.")

    LINE = "---------------------------"
    print(LINE)
    CANVAS_URL = input("Enter the canvas url (looks like https://canvas.instructure.com): ")
    CANVAS_API_KEY = input("Enter your authentication token. You can get this by going to:\n"
                           "  1) Account\n"
                           "  2) Settings\n"
                           "  3) + New Access Token\n"
                           "\nWARNING: Giving out this token to anyone will give them **FULL ACCESS** to your canvas "
                           "account\nTOKEN: ")
    filter = input("Do you want to only show one semester's classes? [y/n]: ")
    if filter[0] == "y" or filter[0] == "Y":
        CANVAS_SEARCH_YEAR = input(
            "What year would you like to search for? Enter the year that the first day of school is in. ")
        CANVAS_SEARCH_SEMESTER = input("Fall or Spring semester [F/S]? ")
        if (CANVAS_SEARCH_SEMESTER[0] == "F" or CANVAS_SEARCH_SEMESTER == "f"):
            CANVAS_SEARCH_MONTH = "08"
        elif (CANVAS_SEARCH_SEMESTER[0] == "S" or CANVAS_SEARCH_SEMESTER == "s"):
            CANVAS_SEARCH_MONTH = "01"
        else:
            print("I'm not sure what you mean. Quitting")
            exit(1)
        getGrades(CANVAS_URL, CANVAS_API_KEY, CANVAS_SEARCH_YEAR, CANVAS_SEARCH_MONTH)
    else:
        getGrades(CANVAS_URL, CANVAS_API_KEY)
    dontclose = input("Finished! Hit enter to close.")

