from multiprocessing import Pool
import json
import os
import http.client
import re
import requests
from lxml import html
from git import Repo


baseFolder = "codes"

startWith = "    var authoringApp = new AuthoringApp("
endWith = ");\n"
pools = 35


def saveFile(name, data):
    with open(name, "w") as text_file:
        text_file.write(data)

def login():
    conn = http.client.HTTPSConnection("login.mathworks.com")

    payload = "identifier=sarmiento.f.aa%40m.titech.ac.jp&credentials=fegasadi11J&type=MWAR&profileTier=dotcom&release=1.1&platform=web&entitlementId=&mfaTokenString=&sourceId=&userAgent=Mozilla%2F5.0+(Macintosh%3B+Intel+Mac+OS+X+10.15%3B+rv%3A91.0)+Gecko%2F20100101+Firefox%2F91.0"

    headers = {
        'Accept': "application/json",
        'X_MW_WS_callerId': "WEB-login",
        'X-Requested-With': "XMLHttpRequest",
        'Origin': "https://login.mathworks.com"
        }

    conn.request("POST", "/authenticationws/service/v4/login", payload, headers)

    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))
    tokenString = data["tokenString"]
   

    ###########################################################################################################################

    url = "https://login.mathworks.com/embedded-login/v2/cookies"

    payload = f"token={tokenString}&sourceId=&session=false"

    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:92.0) Gecko/20100101 Firefox/92.0",
        'Accept': "text/plain, */*; q=0.01",
        'Accept-Language': "en-US,en;q=0.5",
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'X_MW_WS_requestId': "22539b52-c508-4ebf-af17-22dcb7daa082",
        'X-Requested-With': "XMLHttpRequest",
        'Origin': "https://login.mathworks.com",
        'Connection': "keep-alive",
        'Referer': "https://login.mathworks.com/embedded-login/v2/login.html?locale=en",
        'Sec-Fetch-Dest': "empty",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Site': "same-origin",
        'TE': "trailers"
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    mwa = response.cookies["mwa"]
    mwa_session = response.cookies["mwa_session"]

    ###########################################################################################################################
    url = "https://grader.mathworks.com/"

    payload = ""

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:92.0) Gecko/20100101 Firefox/92.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.mathworks.com/",
        "Connection": "keep-alive",
        "Cookie": """mwa=%s; mwa_session=%s"""%(mwa, mwa_session),
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0"
    }

    response = requests.request("GET", url, data=payload, headers=headers)
    tree = html.fromstring(response.text)

    saveFile("main.html", response.text)
    X_CSRF_Token = "/html/head/meta[5]"

    csrf_token_ref = tree.xpath(X_CSRF_Token)

    csrf_token = csrf_token_ref[0].attrib.get("content")

    _matlabgrader_session = response.cookies["_matlabgrader_session"]

    saveFile(".credentials.json", json.dumps({"mwa": mwa, "mwa_session": mwa_session, "_matlabgrader_session": _matlabgrader_session, "csrf_token": csrf_token}))

    print("🚀 Successfully logged in")
    return mwa, mwa_session, _matlabgrader_session

def loadCredentials():
    try:
        with open(".credentials.json", "r") as file:
            creds = json.loads(file.read())
        global mwa
        global mwa_session
        global _matlabgrader_session
        global csrf_token

        mwa = creds["mwa"]
        mwa_session =  creds["mwa_session"]
        _matlabgrader_session =  creds["_matlabgrader_session"]
        csrf_token =  creds["csrf_token"]
        print("🚀 Credentials Loaded")
    except:
        print("🚨 Log in first")

def get_page(url, outputFile):
    payload = ""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:92.0) Gecko/20100101 Firefox/92.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.mathworks.com/",
        "Connection": "keep-alive",
        "Cookie": """mwa=%s; mwa_session=%s"""%(mwa, mwa_session),
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0"
    }

    response = requests.request("GET", url, data=payload, headers=headers)

    saveFile(outputFile, response.text)
    return {"status": response.status_code}


def createDirectory(dirName):
    if not os.path.exists(dirName):
        os.makedirs(f"{dirName}")


def getTree(url, name):
    fileName = f'.htmls/{name}.html'
    print(fileName)
    get_page(url, fileName)
    with open(fileName, 'r') as file:
        page = file.read()
    tree = html.fromstring(page)
    return tree


def getPageLine(dir, startWith):
    fileName = f'{dir}/.page.html'
    # print(get_page(url, fileName), os.getpid())
    with open(fileName, 'r') as file:
        id = []
        for ln in file:
            if ln.startswith(startWith):
                id.append(ln[2:])
    return id


def getCodes(dir):
    with open(f'{dir}/.problem.json') as json_file:
        rawCodeJson = json.load(json_file)
    starterCode = rawCodeJson['problem']['starterCode']['code']
    referenceCode = rawCodeJson['problem']['referenceSolution']
    return starterCode, referenceCode




def getGraderJson():
    createDirectory(".htmls")

    graderUrl = "https://grader.mathworks.com"
    grader = "grader"
    graderTree = getTree(graderUrl, grader)

    activeCoursesXpath = "/html/body/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div/div[1]/article"
    assignmentXpath = "/html/body/div[2]/div[1]/nav/div/div/div/div/ul/li/ul[2]/li"
    problemXpath = "/html/body/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div/table/tbody/tr"
    codeXpath = "/html/body/div[2]/div[2]/div/div/div/div[2]/div/div[6]/div/div[2]/section/div/div/div[5]/div/div[6]/div[4]/div[2]/div/div[3]/div"


    rawCourses = graderTree.xpath(activeCoursesXpath)

    CoursesJson = []
    for rawCourse in rawCourses:
        course = rawCourse.xpath(".//div/div/header/div/div/p/strong/a")[0]
        courseTitle = course.text
        courseTitle = re.sub(r"[^a-zA-Z0-9]+", '', courseTitle)
        courseUrl = graderUrl + course.attrib.get('href')

        courseTree = getTree(courseUrl, courseTitle)
        rawAssignments = courseTree.xpath(assignmentXpath)
        AssignmentsJson = []
        for rawAssignment in rawAssignments[0: -1]:
            assignment = rawAssignment.xpath(".//div/div[1]/a")[0]
            assignmentTitle = assignment.text
            assignmentTitle = re.sub(r"[^a-zA-Z0-9]+", '', assignmentTitle)
            assignmentUrl = graderUrl + assignment.attrib.get('href')

            assignmentTree = getTree(assignmentUrl, assignmentTitle)

            rawProblems = assignmentTree.xpath(problemXpath)
            ProblemsJson = []
            for rawProblem in rawProblems:
                problem = rawProblem.xpath(".//td/div/div[1]/a")[0]
                problemTitle = problem.text + " Edit"
                problemTitle = re.sub(r"[^a-zA-Z0-9]+", '', problemTitle)
                problemUrl = graderUrl + problem.attrib.get('href')

                problemJson = {"title": problemTitle, "link": problemUrl}
                ProblemsJson.append(problemJson)

            assignmentJson = {"title": assignmentTitle,
                              "link": assignmentUrl, "problems": ProblemsJson}
            AssignmentsJson.append(assignmentJson)

        courseJson = {"title": courseTitle,
                      "link": courseUrl, "assignments": AssignmentsJson}
        CoursesJson.append(courseJson)

    data = {"grader": {"courses": CoursesJson}}
    saveFile("myGrader.json", json.dumps(data))


def saveProblem(courseName, assignmentName, problem):
    name = problem["title"]
    link = problem["link"] + "/edit"
    dirName = f"{baseFolder}/{courseName}/{assignmentName}/{name}"
    # print(f'start file: {name} ({os.getpid()}) ...')

    createDirectory(dirName)
    get_page(link, f"{dirName}/.page.html")

    codeLine = getPageLine(dirName, startWith)[0]
    codeLine = codeLine[codeLine.find('{'): - len(endWith)]
    saveFile(f'{dirName}/.problem.json', codeLine)

    starterCode, referenceCode = getCodes(dirName)
    saveFile(f'{dirName}/reference.m', referenceCode)
    saveFile(f'{dirName}/starter.m', starterCode)
    saveFile(f'{dirName}/.link.txt', problem["link"])


def saveProblems():

    jsonFile = "myGrader.json"
    with open(jsonFile, "r") as f:
        graderJson = json.load(f)


    print('Parent process {}.'.format(os.getpid()))
    p = Pool(pools)

    for course in graderJson["grader"]["courses"]:
        courseName = course["title"]
        for assignment in course["assignments"]:
            assignmentName = assignment["title"]
            for problem in assignment["problems"]:
                p.apply_async(saveProblem, args=(courseName, assignmentName,problem,))

    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')

#######################################################
##################    Get  Changes   ##################
#######################################################


def modifiedFiles():
    repo = Repo()

    changed_files = [file.b_path for file in repo.index.diff(None).iter_change_type("M") ]

    changed_files += repo.untracked_files

    changed_files = [file for file in changed_files if file.startswith("codes/") and file.endswith(".m")]

    changed_files = ["/".join(file.split("/")[:-1]) for file in changed_files]

    changed_files = list(dict.fromkeys(changed_files))
    return changed_files


def UploadModified():
    print("🚨 Updating Modified files")
    changed_files = modifiedFiles()
    p = Pool(pools)

    for file in changed_files:
        p.apply_async(UploadChange, args=(file,))
    print('🏁 Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('⌛️ All subprocesses done.')
#######################################################
##################  Upload Changes   ##################
#######################################################

def UploadChange(path):
    print(f"✍️ Updating {path}")
    with open(f"{path}/.link.txt", 'r') as file:
        url = file.read()

    with open(f"{path}/.problem.json", 'r') as file:
        problem = file.read()

    with open(f"{path}/starter.m", 'r') as file:
        starter = file.read()

    with open(f"{path}/reference.m", 'r') as file:
        reference = file.read()

    problemJson = json.loads(problem)

    problemJson["problem"]["starterCode"]["code"] = starter
    problemJson["problem"]["referenceSolution"] = reference
    
    data_raw = json.dumps({"session": problemJson["session"], "problem": problemJson["problem"]}, separators=(',',':'))

    data_raw = repr(data_raw)
   
    curlText = """curl -s '%s/instructor/save' -X POST \
    -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:92.0) Gecko/20100101 Firefox/92.0' \
    -H 'Accept: */*' \
    -H 'Accept-Language: en-US,en;q=0.5' --compressed \
    -H 'X-CSRF-Token: %s'\
    -H 'Content-Type: application/json' \
    -H 'X-Requested-With: XMLHttpRequest' \
    -H 'Origin: https://grader.mathworks.com' \
    -H 'Connection: keep-alive' \
    -H 'Cookie: _matlabgrader_session=%s; mwa=%s; mwa_session=%s' \
    -H 'Sec-Fetch-Dest: empty' \
    -H 'Sec-Fetch-Mode: cors' \
    -H 'Sec-Fetch-Site: same-origin' \
    --data-raw $%s   > /dev/null"""%(url,csrf_token,_matlabgrader_session, mwa, mwa_session, data_raw)
    # saveFile("curlRaw.sh", curlText)
    os.system(curlText)
    print(f"✅ Udated {path}")
