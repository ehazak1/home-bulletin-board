from bs4 import BeautifulSoup
import requests
from datetime import date
import logging


class statsCollector():
    ''' This class will handle collecting stats from the leaders page on cfjc'''
    def __init__(self, day=None):
        self.base_url = 'https://crossfitjohnscreek.sites.zenplanner.com/workout-leaderboard-daily-results.cfm?'
        if not day:
            today = date.today()
            self.day = today.strftime('%Y-%m-%d')
        else:
            self.day = day


    def __repr__(self):
        print("base_url: {}date={}".format(self.base_url, self.day))


    def open_stats_page(self, session=None):
        url = "{}date={}".format(self.base_url, self.day)
        if session:
            url = "{}&{}={}".format(url, session['type'], session['value']) 
        r = requests.get(url)
        if r.status_code != 200:
            logging.warning("Failed to access: {}".format(url))
            return None

        soup = BeautifulSoup(r.content, 'html.parser')
        html  = list(soup.children)[1]  
        return html.find('td', attrs={'id': 'idPage'})


    def get_sessions(self):
        page = self.open_stats_page()
        sessions = []
        for type in ['appointmentid', 'programid']:
            try:
                option = page.find_all('option', attrs={'type': type})[0]
            except IndexError:
                continue
            sessions.append({
                'name': option.contents[0].strip(),
                'type': option.attrs.get('type'), 
                'value': option.attrs.get('value')})
        return sessions


    def get_daily_results(self):
        daily_results = []
        sessions = self.get_sessions()
        for session in sessions:
            page = self.open_stats_page(session)
            skillboxes = page.find_all('div', attrs={'class': 'skillBox'})
            for skillbox in skillboxes:
                skill = {}
                skill['skill_name'] = skillbox.find_next('h2').find('a').contents[0]
                skills_list = ['squat', 'deadlift', 'snatch', 'clean', 'jerk', 'press']
                if any(skill_element in skill['skill_name'].lower() for skill_element in skills_list):
                    skill['type'] = 'Strength/Skill'
                else:
                    skill['type'] = 'Conditioning'
                results = skillbox.find_all('div', attrs={'class': 'personResult'})
                results_data = []
                for result in results:
                    parsed_res = {}
                    data = result.get_text(separator=',',strip=True).split(',')
                    temp_data = data[0].split('\xa0\n')
                    parsed_res['standing'] = temp_data[0]
                    parsed_res['Name'] = temp_data[1]
                    parsed_res['result'] = data[1]
                    try:
                        data[2]
                        parsed_res['rx'] = True
                        results_data.append(parsed_res)
                    except IndexError:
                        parsed_res['rx'] = False
                        results_data.append(parsed_res)
                skill['results'] = results_data
                daily_results.append(skill)
        return daily_results

        
