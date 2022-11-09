from genericpath import exists
from sonarqube import SonarQubeClient
import git
import os
import json
import time
import GetDetails
import CreateDirectory

url = 'http://localhost:9000'
username = "admin" #http://localhost:9000 kullanıcı adı
password = "cuneyt" #http://localhost:9000  giriş şifresi
sonar = SonarQubeClient(sonarqube_url=url, username=username, password=password)

projeVar = False
result = sonar.auth.check_credentials()
repos = os.getcwd() + "\\repos"

with open('repos.txt', 'r') as f:
    myNames = f.readlines()


def nameOfProject(baglanti):
    gitrep = baglanti.strip()
    source = gitrep.split("/")
    boyut = len(source)
    sourcePath = source[boyut - 1]
    baseSource = os.getcwd() #+ "\\" + sourcePath[0]
    baseSource = baseSource.replace("\\", "/")
    sourcePath = sourcePath[: len(sourcePath) - 4]
    return sourcePath

metrikler = {"bugs,vulnerabilities,security_hotspots_reviewed,code_smells,coverage,duplicated_lines_density,ncloc,security_hotspots"}

projectList = list(sonar.projects.search_projects())
for c in range(len(myNames)):
    projeVar = False
    CreateDirectory.create(repos)
    if not os.path.exists(nameOfProject(myNames[c])):
        print(myNames[c].strip() + " klonlanıyor...")
        git.Git(repos).clone(myNames[c].strip())
        for proj in projectList:
            if proj["key"] == nameOfProject(myNames[c]):
                print(nameOfProject(myNames[c]) + " isimli project key daha önce kullanılmış")
                projeVar = True
                break
        if not projeVar:
            sonar.user_tokens.revoke_user_token(name=nameOfProject(myNames[c]))
            sonar.projects.create_project(project=nameOfProject(myNames[c]), name=nameOfProject(myNames[c]), visibility="public")
            print(nameOfProject(myNames[c]) + " oluşturuldu.")
            user_token = sonar.user_tokens.generate_user_token(name=nameOfProject(myNames[c]))
            print(user_token["token"])
            proper = open(repos + "\\sonar-project.properties", "w")
            proper.write("sonar.projectKey=" + nameOfProject(myNames[c]) + "\nsonar.projectName=" + nameOfProject(myNames[c]) + 
                "\nsonar.projectVersion=1.0\nsonar.host.url=" + url + "\nsonar.login=" + user_token["token"] + 
                    "\nsonar.sourceEncoding=UTF-8" +
                        "\nsonar.java.binaries=.\nsonar.login=" + username + "\nsonar.password=" + password + "\nsonar.sources=./" + nameOfProject(myNames[c]))
            proper.close()
            os.system(f'cmd /c "cd {repos} && sonar-scanner"')
resultDir = os.getcwd() + "\\rapor"
raporDetay = resultDir + "\\rapor detay"
CreateDirectory.create(resultDir)
CreateDirectory.create(raporDetay)
timesec = 30
while timesec > 0:
    print("Verilerin yüklenmesi için son %d" %timesec )
    time.sleep(1)
    timesec-=1

projectList = list(sonar.projects.search_projects())

for proj in projectList:
    component = sonar.measures.get_component_with_specified_measures(component=proj["key"],branch="master",metricKeys=metrikler)
    qualitygates_status = sonar.qualitygates.get_project_qualitygates_status(projectKey=proj["key"], branch="master")
    json_str = json.dumps(component)
    resp = json.loads(json_str)
    boy = len(resp["component"]["measures"])
    satirSayisi = sonar.measures.get_component_with_specified_measures(component=proj["key"],branch="master",metricKeys="ncloc")

    res = open(resultDir + "\\" + proj["name"] + ".txt", "w")
    # detay = open(raporDetay + "\\" + proj["name"] + ".txt", "w")
    if qualitygates_status["projectStatus"]["status"] == "OK":
        res.write("\n           Proje adı: " + proj["name"] + " - Status: Passed\n")
    else:
        res.write("\n           Proje adı: " + proj["name"] + " - Status: Failed\n")
    satir = 0
    for i in range(boy):
        if  satirSayisi["component"]["measures"]:
            if resp["component"]["measures"][i]["metric"] == "bugs":
                reliability = sonar.measures.get_component_with_specified_measures(component=proj["key"],branch="master",metricKeys="reliability_rating")
                res.write("Bugs: " + ": " + resp["component"]["measures"][i]["value"] + "             Reliability: %" + reliability["component"]["measures"][0]["value"] + "\n")
                GetDetails.listAllDetails(proj["key"], "BUG", raporDetay)
            elif resp["component"]["measures"][i]["metric"] == "ncloc":
                res.write("Code Lines: " + resp["component"]["measures"][i]["value"] + "\n")
                satir = resp["component"]["measures"][i]["value"]
            elif resp["component"]["measures"][i]["metric"] == "code_smells":
                maintainability = sonar.measures.get_component_with_specified_measures(component=proj["key"],branch="master",metricKeys="sqale_rating")
                debt = sonar.measures.get_component_with_specified_measures(component=proj["key"],branch="master",metricKeys="sqale_index")
                res.write("Debt: " + debt["component"]["measures"][0]["value"] + "minute(s)     " + "Code Smells: " + resp["component"]["measures"][i]["value"] + "    " + 
                      "Maintainability: %" + maintainability["component"]["measures"][0]["value"] + "\n")
                GetDetails.listAllDetails(proj["key"], "CODE_SMELL", raporDetay)
            elif resp["component"]["measures"][i]["metric"] == "security_hotspots":
                security_hotspots_reviewed = sonar.measures.get_component_with_specified_measures(component=proj["key"],branch="master",metricKeys="security_hotspots_reviewed")
                security_review_rating = sonar.measures.get_component_with_specified_measures(component=proj["key"],branch="master",metricKeys="security_review_rating")
                if  security_hotspots_reviewed["component"]["measures"] :
                    res.write("Security Hotspots: " + resp["component"]["measures"][i]["value"] +  "    Reviewed %" + security_hotspots_reviewed["component"]["measures"][0]["value"] +
                          "            Security Review: %" + security_review_rating["component"]["measures"][0]["value"] + "\n")
                else:
                    res.write("Security Hotspots: " +   resp["component"]["measures"][i]["value"] + "       Reviewed: --"  +
                          "            Security Review: %" + security_review_rating["component"]["measures"][0]["value"] + "\n")
            elif resp["component"]["measures"][i]["metric"] == "vulnerabilities":
                security_rating = sonar.measures.get_component_with_specified_measures(component=proj["key"],branch="master",metricKeys="security_rating")
                res.write("Vulnerabilities: " + resp["component"]["measures"][i]["value"] + "             Security: %" + security_rating["component"]["measures"][0]["value"] + "\n")
                GetDetails.listAllDetails(proj["key"], "VULNERABILITY", raporDetay)
            elif resp["component"]["measures"][i]["metric"] == "coverage":
                lines_to_cover = sonar.measures.get_component_with_specified_measures(component=proj["key"],branch="master",metricKeys="lines_to_cover")
                duplicated_lines_density = sonar.measures.get_component_with_specified_measures(component=proj["key"],branch="master",metricKeys="duplicated_lines_density")
                duplicated_blocks = sonar.measures.get_component_with_specified_measures(component=proj["key"],branch="master",metricKeys="duplicated_blocks")
                res.write("Coverage: %" + resp["component"]["measures"][i]["value"]  + " Duplications: " + duplicated_lines_density["component"]["measures"][0]["value"] + 
                            "   Duplicated Blocks: " + duplicated_blocks["component"]["measures"][0]["value"] + "\n")
                v1 = str(lines_to_cover["component"]["measures"][0]["value"])
                res.write("Coverage on %s Lines to cover     Duplications on %s Lines\n" % (v1, satir))
        else:
            res.write(proj["name"] + " projesinin dosyaları bulunamadı.\n")
    res.close()