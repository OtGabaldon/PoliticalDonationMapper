import requests
from wrapper.constants import API_FUNCTIONS
from wrapper.utils import get_base_url

class OpenSecretsClient:
    def __init__(self,output='json'):
        self.base_url = get_base_url()
        self.output = output

    def get_legislators(self,state):
        legislator_function = API_FUNCTIONS['get_legislators']
        param_values = [state]
        param_string = self.build_param_string(legislator_function,param_values)
        api_url = self.base_url.format(param_string)
        response = requests.get(api_url)
        return response
        
    def build_param_string(self,function,param_values):
        '''http://www.opensecrets.org/api//?apikey=123456789 || &method=getLegislators&id=NJ'''
        function_name = function['name']
        param_names = function['params']
        param_string = '&method={}&output={}'.format(function_name,self.output)
        for i,param_name in enumerate(param_names):
            try:
                param_string += '&{}={}'.format(param_name,param_values[i])
            except:
                raise("passed in paramaters are incorrect\n Passed In:{}\n Required:{}".format(param_values,param_names))

        return param_string
