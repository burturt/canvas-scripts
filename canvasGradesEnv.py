#!/bin/python3
# canvasGradesTest.py
# Enjoy!
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

from dotenv import load_dotenv
from canvasGrades import getGrades
import os

load_dotenv()

print("Canvas-getAllGradesV2  Copyright (C) 2020 burturt")
print("This program comes with ABSOLUTELY NO WARRANTY; for details see https://git.io/Jv9Hg.")
print("This is free software, and you are welcome to redistribute it")
print("under certain conditions; see https://git.io/Jv9Hg details.")
print("Should the above links not work, please refer to the GNU General Public License as published by the Free "
      "Software Foundation, either version 3 of the License, or any later version. A copy of that license should have "
      "been included with this program.")

LINE = "---------------------------"
print(LINE)
if os.getenv("CANVAS_URL") and os.getenv("CANVAS_TOKEN"):
    print("Using .env values")
    if os.getenv("CANVAS_SEARCH_YEAR") and os.getenv("CANVAS_SEARCH_MONTH"):
        getGrades(os.getenv("CANVAS_URL"), os.getenv("CANVAS_TOKEN"), os.getenv("CANVAS_SEARCH_YEAR"),
                  os.getenv("CANVAS_SEARCH_MONTH"))
    else:
        getGrades(os.getenv("CANVAS_URL"), os.getenv("CANVAS_TOKEN"))
    exit(0)
CANVAS_URL = input("Enter the canvas url (looks like https://canvas.instructure.com): ")
CANVAS_API_KEY = input("Enter your authentication token. You can get this by going to:\n"
                       "  1) Account\n"
                       "  2) Settings\n"
                       "  3) + New Access Token\n"
                       "\nWARNING: Giving out this token to anyone will give them **FULL ACCESS** to your canvas "
                       "account\nTOKEN: ")
filter = input("Do you want to only show one semester's classes? [y/n]: ")
if filter[0] == "y" or filter[0] == "Y":
    CANVAS_SEARCH_YEAR = input("What year would you like to search for? Enter the year that the first day of school is in. ")
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
