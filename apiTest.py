import virustotal_python
from virustotal_python import Virustotal
import time
from base64 import urlsafe_b64encode


def checkLink(url):
    with open("key.txt", 'r', encoding="utf-8") as fp:
        APIKey = (f"{fp.read()}")

    with Virustotal(API_KEY=APIKey, API_VERSION="v3") as vtotal:
        try:
            # Send URL to VirusTotal for analysis
            vtotal.request("urls", data={"url": url}, method="POST")
            time.sleep(2.5)
            # URL safe encode URL in base64 format
            url_id = urlsafe_b64encode(url.encode()).decode().strip("=")
            # Obtain the analysis results for the URL using the url_id
            analysis_resp = vtotal.request(f"urls/{url_id}")
            x = []
            for name in analysis_resp.data["attributes"]["last_analysis_results"]:
                y = (analysis_resp.data["attributes"]["last_analysis_results"][f"{name}"]["result"])
                x.append(f"{y}")

            numberOfClean = 0
            numberOfMalicious = 0
            numberOfSuspicious = 0
            numberOfPhishing = 0
        
            for i in range(len(x)):
                if x[i] == 'clean':
                    numberOfClean += 1
                elif x[i] == 'malicious':
                    numberOfMalicious += 1
                elif x[i] == 'suspicious':
                    numberOfSuspicious += 1
                elif x[i] == 'phishing':
                    numberOfPhishing += 1
        
            #print(f"Number of clean reports: {numberOfClean}")
            #print(f"Number of malicious reports: {numberOfMalicious}")
            #print(f"Number of suspicious reports: {numberOfSuspicious}")
            #print(f"Number of phishing reports: {numberOfPhishing}")
            x = [f"{numberOfClean}", f"{numberOfMalicious}", f"{numberOfSuspicious}", f"{numberOfPhishing}"]
            return x
        except virustotal_python.virustotal.VirustotalError as err:
            print(f"An error occurred: {err}\nCatching and continuing with program.")
    #Source https://pypi.org/project/virustotal-python/