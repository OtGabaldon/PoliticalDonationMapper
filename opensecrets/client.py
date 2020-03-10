import os

import requests
from requests.exceptions import RequestException

from opensecrets.constants import API_FUNCTIONS, STATE_AND_CODE
from opensecrets.utils import get_base_url, get_cache


class OpenSecretsClient:
    def __init__(self, output='json'):
        self.base_url = get_base_url()
        self.output = output
        self.legislators = {'num_legislators': 0}
        self.contributions = {}
        self.spinner_states = ['|', '/', '-', '\\']

    def get_all_legislators(self):
        print('Starting to get contributers')
        print('Getting States')
        for i, (_, state_code) in enumerate(STATE_AND_CODE):
            self.get_legislators(state_code)
            os.system('clear')
            print('{} ... {}% done.'.format(
                (self.spinner_states[i % 4]), ((i/50)*100)))

        print("Done.")

        return True

    def get_all_contributions_from_state(self, state):
        self.get_legislators(state)

        num_legislators = self.legislators['num_legislators']
        for legislator in self.legislators[state]:
            self.get_candidate_contributions(
                self.legislators[state][legislator]['cid'])
            legislators_processed += 1
            os.system('clear')
            print('{} ... {}% done.'
                  .format(
                      (self.spinner_states[legislators_processed % 4]),
                      ((legislators_processed/num_legislators)*100)
                  )
                  )

        return True

    def get_legislators(self, state):
        cached_result = get_cache(self.legislators, [state])
        if cached_result:
            return cached_result

        response = self.call_open_secrets('get_legislators', [state])
        if response.get('err'):
            return response['err']

        legislators = response['response']['legislator']

        restructered = {}
        for legislator in legislators:
            data = legislator["@attributes"]
            name = data['firstlast']
            restructered[name] = data

        self.legislators[state] = restructered
        self.legislators['num_legislators'] += len(restructered)
        return restructered

    def get_candidate_contributions(self, cid, cycle=2020):
        cached_contribution = get_cache(self.contributions, [cid, cycle])
        if cached_contribution:
            return cached_contribution
        if not self.contributions.get(cid):
            self.contributions[cid] = {}

        response = self.call_open_secrets(
            'get_candidate_contributions', [cid, cycle])

        if response.get('err'):
            self.contributions[cid] = response['err']
            return response['err']

        contributions_data = {}
        contributer_list = response['response']['contributors']['contributor']
        for contributor in enumerate(contributer_list):
            contributer_data = contributor['@attributes']
            contributions_data[contributer_data['org_name']] = contributer_data

        self.contributions[cid][cycle] = contributions_data

        return contributions_data

    def build_param_string(self, function, param_values):
        '''http://www.opensecrets.org/api//?apikey=123456789 || &method=getLegislators&id=NJ'''
        function_name = function['name']
        param_names = function['params']
        param_string = '&method={}&output={}'.format(
            function_name, self.output)
        for i, param_name in enumerate(param_names):
            try:
                param_string += '&{}={}'.format(param_name, param_values[i])
            except:
                raise("passed in paramaters are incorrect\n Passed In:{}\n Required:{}".format(
                    param_values, param_names))

        return param_string

    def call_open_secrets(self, function_name, params):
        function_info = API_FUNCTIONS[function_name]
        param_values = params
        param_string = self.build_param_string(function_info, param_values)
        api_url = self.base_url.format(param_string)
        response = requests.get(api_url)
        print(response.status_code)
        if response.status_code is not requests.codes.ok: #pylint: disable=no-member
            return {'err': 'Request for {} with paramaters: {} errored with {}'.format(function_name, params, response.status_code)}
        return response.json()
