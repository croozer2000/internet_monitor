import os
import subprocess
import re
import datetime


def pingTest(hostName):
    # response = os.system("ping " + hostName)
    # if you want stdout to be piped to variable

    response = subprocess.Popen("ping -c 3 -w 5 " + hostName, shell=True, stdout=subprocess.PIPE).stdout
    response = response.read()
    match = r"(\d*)% packet loss"
    match2 = r"unreachable"
    
    # print(response.decode())
    m = int(re.search(match,response.decode()).group(1))
    # print(m)
    if m > 0:
        return False, datetime.datetime.now()
    else:
        return True, datetime.datetime.now()

def pingTestandLog(hostName, logfile, additionalMessage = ""):
    results, time = pingTest(hostName)
    if not results:
        if not os.path.isdir("log"):
            os.mkdir("log")
        
        logFile.write(str(time) + ": Ping failed to "+hostName+  " "+ additionalMessage +"\n")

    return results

if __name__ == "__main__":
    logFile = open("log/outage.log",'a')
    test_hosts = ["192.168.0.0","192.168.0.0"]

    failureCount = 0
    internet_recovered = False
    while failureCount <= 5:
        log_results = 0
        for host in test_hosts:
            if not pingTestandLog(host, logFile):
                log_results += 1
        

        if log_results == len(test_hosts):
            logFile.write(str(datetime.datetime.now()) + ": Detected internet failure. "+"\n")
            failureCount += 2
        # elif log_results < len(test_hosts):
        #     logFile.write(str(time) + ": Possible issues with test internet servers "+"\n")
        #     failureCount += 1
        else:
            break

        # reset the router
        if failureCount >= 4:
            logFile.write(str(datetime.datetime.now()) + ": Resting internet. "+"\n")
            # if router Reset function:
                # internet_recovered = True
            pass
        
    if failureCount > 0 and internet_recovered:
        logFile.write(str(datetime.datetime.now()) + ": Internet was restored. "+"\n")
    elif failureCount > 0:
        logFile.write(str(datetime.datetime.now()) + ": Internet is still down. "+"\n")
        
    logFile.close()