import mechanicalsoup
import json

class MyGCI():
    def __init__(self):
        self.gci = {}
        self.browser = mechanicalsoup.StatefulBrowser()

    def signIn(self, username, password):
        self.browser.open("https://login.gci.com/")

        self.browser.select_form()

        self.browser["pf.username"] = username
        self.browser["pf.pass"] = password

        self.browser.submit_selected()

    def getUsage(self, username, password):
        self.signIn(username, password) # Sign in before proceeding

        date_options = self.browser.open("https://my.gci.com/web/guest/exportusage?p_p_id=exportusage_WAR_gciportalwar_INSTANCE_B1MC3ECJxwvW&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1&p_p_resource_id=getInitData")
        dateObj = json.loads(date_options.text)

        date = dateObj['portletData']['periods'][0]['value']
        usage_report = self.browser.open("https://my.gci.com/web/guest/exportusage?p_p_id=exportusage_WAR_gciportalwar_INSTANCE_B1MC3ECJxwvW&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=exportData&p_p_cacheability=cacheLevelPage&reportId=INTERNET_MONTHLY&periodName=" + date)
        parsed_report = usage_report.text.split(',')

        self.gci['days_remaining'] = parsed_report[11].split('\n')[1]
        self.gci['included_usage'] = parsed_report[12]
        self.gci['used_usage'] = parsed_report[13]
        self.gci['buckets_added'] = parsed_report[14]
        self.gci['download_usage'] = parsed_report[18]
        self.gci['upload_usage'] = parsed_report[19]

        resp = ''
        for key, value in self.gci.items():
            resp = resp + ("gci_%s %s \n" % (key, value))

        return resp