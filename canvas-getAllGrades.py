#!/bin/python3
# canvas-getAllGrades.py
# Enjoy!

import re
import requests
import sys
from configparser import ConfigParser

LINE = "---------------------------"
configFileExists = False

if len(sys.argv) != 1 and len(sys.argv) != 3 and len(sys.argv) != 4:
    print("Invalid # of arguments")
    print("Usage: python3 <script path> <CANVAS_URL> <CANVAS_API_TOKEN> [FILENAME_TO_SAVE_TO.txt]")
    print("OR\npython3 <script path>")
    exit(1)
else:
    print("\n" + LINE * 2)
    print("Hello! Welcome to getAllGrades.py!\n")
    print(
        "This script utilizes your canvas API token to print a \nlist of your courses and grades in a human-readable "
        "format.")
    print(LINE * 2)

if (len(sys.argv) == 3) or (len(sys.argv) == 4):
    authtoken = sys.argv[2]
    instructure_domain = sys.argv[1]
    createConfig = False
    if (len(sys.argv) == 4):
        arg3 = sys.argv[3]
        writeToFile = True
else:
    try:
        config = ConfigParser()
        config.read('config.ini')
        authtoken = config.get('canvas_auth', 'access_token')
        instructure_domain = config.get('canvas_auth', 'instance')
    except:
        print("No valid config file found")
    else:
        createConfig = False
        configFileExists = True
        print("Valid config file (config.ini) found, using to populate options")
        try:
            arg3 = config.get('canvas_auth', 'output_file')
        except:
            print("Config specified no output file")
            writeToFile = False
        else:
            writeToFile = True
        print("Making a request to the url to verify it exists...")

        try:
            testRequest = requests.get(instructure_domain)
        except:
            print("Invalid URL. Exiting")
            exit(1)
    if not configFileExists:
        print("Try using arguments instead! python3 " + sys.argv[0] + " -h for more info.")
        acceptz = input("Would you like to store your canvas URL, token, and output file settings in a config file? "
                        "\nNote that while this may make it easier to run these scripts, random users may be able to "
                        "get "
                        "your token from the config files and use it! [Y/n]: ")

        if acceptz[0].lower() == 'y':
            print("Saving entered data in config file")
            createConfig = True
            configCreator = ConfigParser()
            configCreator['canvas_auth'] = {}

        else:
            print("Not saving data in config file")
            createConfig = False
        while True:
            instructure_domain = input(
                "\nPlease type the base URL for your canvas instance:\nURL: ")

            valURL = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
            if valURL.match(instructure_domain):
                print("Making a request to the url to verify it exists...")
                try:
                    requests.get(instructure_domain)
                except:
                    print("Invalid URL. Please try again.")
                else:
                    if createConfig:
                        configCreator['canvas_auth']['instance'] = instructure_domain
                        print("Will save " + instructure_domain + " to config")
                    break
            else:
                print("Invalid URL. Please try again.")
                if instructure_domain.find("http://") == -1 and instructure_domain.find("https://") == -1:
                    print("Remember to include \"http://\" or \"https://\"")

        authtoken = input("Enter your authentication token. You can get this by going to:\n"
                          "  1) Account\n"
                          "  2) Settings\n"
                          "  3) + New Access Token\n"
                          "\nWARNING: Giving out this token to anyone will give them **FULL ACCESS** to your canvas "
                          "account\nTOKEN: ")

        while authtoken == "" or len(authtoken) < 68:
            authtoken = input("Token is too short. Try again: ")
        if createConfig:
            configCreator['canvas_auth']['access_token'] = authtoken
            print("Will save " + authtoken + " to config")

        print(LINE * 2)
        print("Canvas URL: " + instructure_domain + "/api/v1")
        print("Authtoken: " + authtoken)
        accept = input("\nProceed? [Y/n]: ")
        if accept != "" and accept[0].lower() == 'y':
            print("Continuing")
        else:
            print("Canceled")
            exit(1)

        outputsave = input("Save output to output.txt?\nThis will override any data already in this file! [Y/n]: ")
        if outputsave != "" and outputsave[0].lower() == 'y':
            print("Saving file to output.txt")
            writeToFile = True
            arg3 = "output.txt"
            if createConfig:
                configCreator['canvas_auth']['output_file'] = "output.txt"
                print("Will enable output export in config")
        else:
            print("Not saving output as file.")
            writeToFile = False
            if createConfig:
                print("Will disable output export in config")

r = requests.get(instructure_domain + "/api/v1/users/self/courses?include[]=total_scores&include["
                                      "]=current_grading_period_scores&enrollment_type=student&include["
                                      "]=concluded&per_page=1000",
                 headers={"Authorization": "Bearer " + authtoken})

courses = str(r.content)

if courses == """b'{"errors":[{"message":"Invalid access token."}]}'""":
    print("Invalid access token. Exiting")
    exit(1)
if r.status_code != 200:
    print("Unknown response. Debug info is below:\nStatus_code: "
          + r.status_code + "\nResponse: " + courses)
    exit(1)

loc = [mfindID.start() for mfindID in list(re.finditer('\"id\"\:', courses))]

getName = re.compile('(\"name\":\"[a-zA-Z0-9 -]+\")')
getID = re.compile('[0-9]+')
getLetterGrade = re.compile('\"computed_current_grade\":\"[A-Za-z+-]+\"')
getPercentGrade = re.compile('\"computed_current_score\":[0-9.]+')

if writeToFile: exportFile = open(arg3, 'w')

if createConfig:
    with open('config.ini', 'w') as configfile:
        configCreator.write(configfile)
    print("Config files saved.")

for j in range(len(loc)):
    a = loc[j]
    b = loc[j + 1] if j != (len(loc) - 1) else len(courses)

    print(LINE)
    if writeToFile: exportFile.write(LINE + "\n")

    substr = courses[int(a):b]
    courseIDreg = getID.search(substr)
    courseID = substr[courseIDreg.start(0):courseIDreg.end(0)]

    print("Course ID: " + courseID)
    if writeToFile:
        exportFile.write("Course ID: " + courseID + "\n")

    if "restricted" in substr[courseIDreg.end(0):b]:
        print("Course not available yet")
        if writeToFile:
            exportFile.write("Course not available yet\n")
    else:
        try:
            mGetName = getName.search(substr)
            substr2 = courses[mGetName.start(0) + a + 8:mGetName.end(0) + a - 1]
            print("Name: " + substr2)
            if writeToFile:
                exportFile.write("Name: " + substr2 + "\n")
        except:
            print("No Course Name found")
            if writeToFile:
                exportFile.write("No Course Name found\n")

        try:
            mGetLetterGrade = getLetterGrade.search(substr)
            substr2 = courses[mGetLetterGrade.start(0) + a + 26:mGetLetterGrade.end(0) + a - 1]
            print("Letter Grade: " + substr2)
            if writeToFile:
                exportFile.write("Letter Grade: " + substr2 + "\n")
        except:
            print("No Letter Grade found")
            if writeToFile:
                exportFile.write("No Letter Grade found\n")

        try:
            mGetPercentGrade = getPercentGrade.search(substr)
            substr2 = courses[mGetPercentGrade.start(0) + a + 25:mGetPercentGrade.end(0) + a]
            print("Percent Grade: " + substr2 + "%")
            if writeToFile:
                exportFile.write("Percent Grade: " + substr2 + "%\n")
        except:
            print("No Percent Grade found")
            if writeToFile:
                exportFile.write("No Percent Grade found\n")

print(LINE)
if writeToFile:
    exportFile.write(LINE + "\n")
    exportFile.close()
    print("Successfully exported to file " + arg3)
print("Done")
exit(0)
