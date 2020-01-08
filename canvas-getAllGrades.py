import re
import requests
import sys
from configparser import ConfigParser

loop = True
loop2 = True
loop3 = True
writeToFile = False
createConfig = False

print("This script will use a canvas API token to get a list of courses with grades and parse the output into "
      "human-readable text.")

if (len(sys.argv) != 1) & (len(sys.argv) != 3) & (len(sys.argv) != 4):
    print("Usage: python3 " + sys.argv[0] + "CANVAS_URL CANVAS_API_TOKEN (optional)FILENAME_TO_SAVE_TO.txt)\nThe "
                                            "canvas url should be of format https://example.com, filename export is "
                                            "optional. Config file will be used by default if no extra arguments are "
                                            "given")
    exit(1)
elif (len(sys.argv) == 3) | (len(sys.argv) == 4):
    authtoken = sys.argv[2]
    instructure_domain = sys.argv[1]
    loop = False
    loop2 = False
    loop3 = False
    if (len(sys.argv) == 4):
        arg3 = sys.argv[3]
        writeToFile = True

elif (len(sys.argv) == 1):
    try:
        config = ConfigParser()
        config.read('config.ini')
        authtoken = config.get('canvas_auth', 'access_token')
        instructure_domain = config.get('canvas_auth', 'instance')
    except:
        print("No valid config file found")
        configFileExists = False
    else:
        loop = False
        loop2 = False
        loop3 = False
        configFileExists = True
        print("Valid config file (config.ini) found, using to populate options")
        try:
            arg3 = config.get('canvas_auth', 'output_file')
        except:
            print("Config specified no output file")
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

if loop3:
    acceptz = input("Would you like to store your canvas URL, token, and output file settings in a config file? "
                    "\nNote that while this may make it easier to run these scripts, random users may be able to get "
                    "your token from the config files and use it! [Y/n]: ")

    if acceptz[0].lower() == 'y':
        print("Saving entered data in config file")
        createConfig = True
        configCreator = ConfigParser()
        configCreator['canvas_auth'] = {}

    else:
        print("Not saving data in config file")
        createConfig = False
        exit(1)

while (loop):

    instructure_domain = input("Please type the base URL for your canvas instance:\n")

    valURL = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    m = valURL.match(instructure_domain)
    if m:
        print("Making a request to the url to verify it exists...")

        try:
            testRequest = requests.get(instructure_domain)
        except:
            print("Invalid URL. Please try again.")
        else:
            loop = False
            if createConfig:
                configCreator['canvas_auth']['instance'] = instructure_domain
                print("Will save " + instructure_domain + " to config")
    else:
        print('Invalid URL. Please try again')
        if (instructure_domain.find("http://") == -1 & instructure_domain.find("https://") == -1):
            print('Remember to include http:// or https:// at the beginning of the URL!')

while (loop2):
    authtoken = input("Please paste your authentication token. You can get this by going to account --> "
                      "settings and creating a new access token.\nWord of warning: giving out this token to "
                      "anyone will give them **FULL ACCESS** to your canvas account, so be careful where you "
                      "put "
                      "this!\n")
    if authtoken != '':
        loop2 = False
        if createConfig:
            configCreator['canvas_auth']['access_token'] = authtoken
            print("Will save " + authtoken + " to config")
    else:
        print("No token provided.")

authhead = {"Authorization": "Bearer " + authtoken}

if loop3:

    accept = input(
        "Making a request to the url " +
        instructure_domain + "/api/v1 using the authentication token " +
        authtoken + ". Proceed? [Y/n]: ")

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
if r.status_code != 200:
    print("Unknown response. Debug info is below:")
    print("Status_code: " + str(r.status_code) + "\nResponse: " + courses)
    exit(1)

if loop3:

    outputsave = input("Save output to output.txt? This will override any data already in this file! [Y/n]\n")

    if outputsave[0].lower() == 'y':
        print("Saving file to output.txt")
        writeToFile = True
        arg3 = "output.txt"
        if createConfig:
            configCreator['canvas_auth']['output_file'] = "output.txt"
            print("Will enable output export in config")

    else:
        print("Not saving output as file.")
        if createConfig:
            print("Will disable output export in config")

loc = [mfindID.start() for mfindID in list(re.finditer('\"id\"\:', courses))]

if createConfig:
    with open('config.ini', 'w') as configfile:
        configCreator.write(configfile)
    print("Config files saved.")

getName = re.compile('(\"name\":\"[a-zA-Z0-9 -]+\")')
getID = re.compile('[0-9]+')
getLetterGrade = re.compile('\"computed_current_grade\":\"[A-Za-z+-]+\"')
getPercentGrade = re.compile('\"computed_current_score\":[0-9.]+')

if writeToFile:
    exportFile = open(arg3, 'w')

for j in range(len(loc)):
    a = loc[j]
    if j != (len(loc) - 1):
        b = loc[j + 1]
    else:
        b = len(courses)
    print("---------------------------")
    if writeToFile:
        exportFile.write("---------------------------\n")

    substr = courses[int(a):b]

    courseIDreg = getID.search(substr)
    courseID = substr[courseIDreg.start(0):courseIDreg.end(0)]
    if writeToFile:
        exportFile.write("Course ID: " + courseID + "\n")
    print("Course ID: " + courseID)

    if "restricted" in substr[courseIDreg.end(0):b]:
        print("Course not available yet")
        if writeToFile:
            exportFile.write("Course not available yet" + "\n")
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
                exportFile.write("No Course Name found" + "\n")

        try:

            mGetLetterGrade = getLetterGrade.search(substr)
            substr2 = courses[mGetLetterGrade.start(0) + a + 26:mGetLetterGrade.end(0) + a - 1]
            print("Letter Grade: " + substr2)
            if writeToFile:
                exportFile.write("Letter Grade: " + substr2 + "\n")
        except:
            print("No Letter Grade found")
            if writeToFile:
                exportFile.write("No Letter Grade found" + "\n")
        try:

            mGetPercentGrade = getPercentGrade.search(substr)
            substr2 = courses[mGetPercentGrade.start(0) + a + 25:mGetPercentGrade.end(0) + a]
            print("Percent Grade: " + substr2 + "%")
            if writeToFile:
                exportFile.write("Percent Grade: " + substr2 + "%" + "\n")
        except:
            print("No Percent Grade found")
            if writeToFile:
                exportFile.write("No Percent Grade found" + "\n")

print("---------------------------")
if writeToFile:
    exportFile.write("---------------------------" + "\n")
    exportFile.close()
    print("Successfully exported to file " + arg3)
print("Done")
exit(0)
