from lxml import html
from getCurl import getWebPage
import json
import os


def createDirectory(dirName):
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory ", dirName,  " Created ")
    else:
        print("Directory ", dirName,  " already exists")


def saveFile(name, data):
    with open(name, "w") as text_file:
        text_file.write(data)


def getTree(url, name):
    fileName = f'htmls/{name.replace(" ", "_")}'
    print(fileName)
    getWebPage(url, fileName)
    with open(f'{fileName}.html', 'r') as file:
        page = file.read()
    tree = html.fromstring(page)
    return tree


def getPageLine(url, name, startWith):
    fileName = f'htmls/{name.replace(" ", "_")}'
    print(fileName)
    getWebPage(url, fileName)
    with open(f'{fileName}.html', 'r') as file:
        id = []
        for ln in file:
            if ln.startswith(startWith):
                id.append(ln[2:])
    return id


def getPage(url, name):
    fileName = f'htmls/{name.replace(" ", "_")}'
    print(fileName)
    getWebPage(url, fileName)
    with open(f'{fileName}.html', 'r') as file:
        page = file.read()
    return page


def getCodes(fileName):
    with open('jsons/{fileName}.json') as json_file:
        rawCodeJson = json.load(json_file)
    starterCode = rawCodeJson['problem']['starterCode']['code']
    referenceCode = rawCodeJson['problem']['referenceSolution']
    return starterCode, referenceCode


def createStorage():
    createDirectory("htlms")
    createDirectory("jsons")


def getGraderJson():
    createStorage()

    graderUrl = "https://grader.mathworks.com"
    grader = "grader"
    graderTree = getTree(graderUrl, grader)

    activeCoursesXpath = "/html/body/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div/div[1]/article"
    assignmentXpath = "/html/body/div[2]/div[1]/nav/div/div/div/div/ul/li/ul[2]/li"
    problemXpath = "/html/body/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div/table/tbody/tr"
    codeXpath = "/html/body/div[2]/div[2]/div/div/div/div[2]/div/div[6]/div/div[2]/section/div/div/div[5]/div/div[6]/div[4]/div[2]/div/div[3]/div"
    startWith = "    var authoringApp = new AuthoringApp("
    endWith = ");\n"

    rawCourses = graderTree.xpath(activeCoursesXpath)

    CoursesJson = []
    for rawCourse in rawCourses:
        course = rawCourse.xpath(".//div/div/header/div/div/p/strong/a")[0]
        courseTitle = course.text
        courseUrl = graderUrl + course.attrib.get('href')

        courseTree = getTree(courseUrl, courseTitle)
        rawAssignments = courseTree.xpath(assignmentXpath)
        AssignmentsJson = []
        for rawAssignment in rawAssignments[0: -1]:
            assignment = rawAssignment.xpath(".//div/div[1]/a")[0]
            assignmentTitle = assignment.text
            assignmentTitle = assignmentTitle.replace(" ", "_")
            assignmentUrl = graderUrl + assignment.attrib.get('href')

            assignmentTree = getTree(assignmentUrl, assignmentTitle)

            rawProblems = assignmentTree.xpath(problemXpath)
            ProblemsJson = []
            for rawProblem in rawProblems:
                problem = rawProblem.xpath(".//td/div/div[1]/a")[0]
                problemTitle = problem.text + " Edit"
                problemTitle = problemTitle.replace(" ", "_")
                problemUrl = graderUrl + problem.attrib.get('href') + "/edit"

                problemTree = getTree(problemUrl, problemTitle)

                codeLine = getPageLine(problemUrl, problemTitle, startWith)[0]
                codeLine = codeLine[codeLine.find('{'): - len(endWith)]
                saveFile(f'jsons/{problemTitle}.json', codeLine)
                starterCode, referenceCode = getCodes(problemTitle)

                problemJson = {"title": problemTitle, "link": problemUrl,
                               "starterCode": starterCode, "referenceCode": referenceCode}
                ProblemsJson.append(problemJson)

            assignmentJson = {"title": assignmentTitle,
                              "link": assignmentUrl, "problems": ProblemsJson}
            AssignmentsJson.append(assignmentJson)

        courseJson = {"title": courseTitle,
                      "link": courseUrl, "assignments": AssignmentsJson}
        CoursesJson.append(courseJson)

    data = {"grader": {"courses": CoursesJson}}
    saveFile("myGrader.json", json.dumps(data))


if __name__ == "__main__":
    createStorage()
