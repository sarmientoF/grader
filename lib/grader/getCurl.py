import os
import browser_cookie3


def getWebPage(url, outputFile):
    # url: the url you want to get info from
    # outputFile: The outputFile name
    try:
        cookies = list(browser_cookie3.firefox())
        adcloud = [x for x in cookies if x.name == "adcloud"][0].value
        mwa = [x for x in cookies if x.name == "mwa"][0].value
        mwa_profile = [x for x in cookies if x.name == "mwa_profile"][0].value
        mwa_session = [x for x in cookies if x.name == "mwa_session"][0].value

        # with open("cookies.json", "w") as text_file:
        #     text_file.write(f"{adcloud}\n{mwa}\n{mwa_profile}\n{mwa_session}")
        curl = f"""curl '{url}' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:81.0) Gecko/20100101 Firefox/81.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: https://www.mathworks.com/login?uri=https://grader.mathworks.com/' -H 'Connection: keep-alive' -H 'Cookie: _matlabgrader_session=ZGRjMzVyNzJuQU1mTmJUN3hDZXZKYTdwV3dGY1FVZjZxekoyU0gvR1ozQWRrbVFJclc5SnZwWVJ1djJ6Z0YxYmVYY3l0NGttNUJCVU1laklhaVNBd3BtcDJZRWtRVDdnZWRIaWE2V1VzMVNFc2kxSVQ3ME5MSXVrYVJoOExyT1U5enBEY240ZGZlOVhuRmtHNjBTOERhQTlXZ0hsN2owQ3hyMUZac3haWnJTZ2tTM0hUdjNNbEE3VWs1RVlkNG5YLS1abG04Ty93Zmxld3VNQllrM2tXTGJ3PT0=--aec4efb16a8e0f0000ebfa6507e318883a6aa323; _sdsat_session_count=2; _sdsat_lt_pages_viewed=71; AMCV_B1441C8B533095C00A490D4D@AdobeOrg=281789898|MCIDTS|18536|MCMID|39851645893515184602107407447943167383|MCAID|NONE|MCOPTOUT-1601545895s|NONE|MCAAMLH-1602143495|11|MCAAMB-1602143495|j8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI|MCSYNCSOP|411-18543|vVersion|4.1.0|MCCIDH|1241395866; mbox=PC#bc7f129c232540e2b511eedc6e3a0306.32_0#1664710711|session#e4d14e4ec73b43258f0d370f3730e776#1601541235; s_ecid=MCMID|39851645893515184602107407447943167383; RT="z=1&dm=grader.mathworks.com&si=3e4625f8-0eee-46ec-b9f0-f806da8e5686&ss=kfqech6g&sl=y&tt=1eh6&bcn=//684d0d3f.akstat.io/&ld=4uh35&ul=4v777"; adcloud={adcloud}; _fbp=fb.1.1601465913977.37442848; ELOQUA=GUID=8b9e1312af0c4836b9ec57a348d6cdff; _sdsat_landing_page=https://grader.mathworks.com/|1601520493270; _sdsat_pages_viewed=59; _sdsat_traffic_source=https://www.google.com/; _sdsat_Eloqua2=8b9e1312af0c4836b9ec57a348d6cdff; check=true; AMCVS_B1441C8B533095C00A490D4D@AdobeOrg=1; s_cc=true; s_sq=[[B]]; dtCookie=v_4_srv_6_sn_786D8A9361A79FD657C0162706B8D320_perc_100000_ol_0_mul_1; _uetsid=429921494131589ea1eb3ed8c9325438; _uetvid=df5fb787fff3e2a1dff00f3c135ac62a; mwa={mwa}; mwa_profile={mwa_profile}; mwa_session={mwa_session}' -H 'Upgrade-Insecure-Requests: 1' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache'"""
        os.system(f"{curl} -o {outputFile}.html")
        return {"status": 200}
    except Exception as e:
        return {"status": 404}


if __name__ == "__main__":
    url = "https://grader.mathworks.com/courses/5949-fundamental-of-mechanics-1"
    getWebPage(url, "course_01")
