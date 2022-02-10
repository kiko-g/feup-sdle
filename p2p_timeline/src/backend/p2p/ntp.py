import time, ntplib

def ntp_time():
    try: 
        ntp_server = "pt.pool.ntp.org"
        ntp = ntplib.NTPClient()
        ntp_response = ntp.request(ntp_server)
 
    except:
        print('\n Error While Accessing The NTP Server pt.pool.ntp.org \n') 
        return 0
    
    print('\n NTP Request... \n')
    diff = 0

    if ntp_response:
        now = time.time()
        diff = now - ntp_response.tx_time

    return diff
