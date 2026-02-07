import os
import base64

class SetEnvironment():
    def __init__(self, config_filepath, env, env_specific_variables, common_variables, secret_values) -> None:
        self.config_filepath = config_filepath
        self.env = env
        self.update_variable(env_specific_variables, common_variables, secret_values)
        
    def base64_encode(self, variable):
        value = os.getenv(variable + "_" + self.env, '')
        return base64.b64encode(value.encode('utf-8'))
    
    def update_variable(self, env_specific_variables, common_variables, secret_values):      
        with open(self.config_filepath, 'r') as file:
            content = file.read()
        env = self.env
        
        variable_list = env_specific_variables + common_variables
        for variable in variable_list:
            if variable in env_specific_variables:
                value = os.getenv(variable + "_" + env, '')
            else:
                value = os.getenv(variable, '')
            if variable in secret_values:
                value = base64.b64encode(value.encode('utf-8')).decode('utf-8')
            content = content.replace(variable + '_VALUE', "" + value)
            
        # content = content.replace('TAG_VALUE', ""+os.getenv("TAG_" + env, ''))
        # content = content.replace('PASSWORD_VALUE', ""+os.getenv("PASSWORD_" + env, ''))
        # content = content.replace('REGISTRY_DOMAIN_VALUE', ""+os.getenv("REGISTRY_DOMAIN_" + env, ''))
        # content = content.replace('PAT_TOKEN_VALUE', ""+os.getenv("PAT_TOKEN"))
        # content = content.replace('GIT_USER_VALUE', ""+os.getenv("GIT_USER_" + env, ''))
        # content = content.replace('CLIENT_SECRET_VALUE', ""+os.getenv("CLIENT_SECRET_" + env, ''))
        # content = content.replace('CONTAINER_REGISTRY_VALUE', ""+os.getenv("CONTAINER_REGISTRY_" + env, ''))
        # content = content.replace('REPO_NAME', os.getenv("REPO_NAME", ''))
        # content = content.replace('BUILD_ID', os.getenv("BUILD_ID", ''))   
        # content = content.replace('NIFI_REGISTRY_REPO_VALUE', ""+os.getenv("NIFI_REGISTRY_REPO_" + env, ''))     

        with open(self.config_filepath, 'w') as file:
            file.write(content)
    
if __name__ == "__main__":
    env = os.getenv("ENV", '')
    component = os.getenv('COMPONENT', '')
    env_specific_variables = []
    common_variables = []
    secret_values = []
    if component == 'nifi_cluster':
        env_specific_variables = ['NIFI_DOMAIN', 'TAG', 'CLIENT_SECRET', 'CONTAINER_REGISTRY', 'STORAGE_CLASS_NAME']
        common_variables = ['REPO_NAME', 'PASSWORD', 'BUILD_ID']
    if component == 'nifi_registry':
        env_specific_variables = ['REGISTRY_DOMAIN', 'TAG', 'GIT_USER', 'NIFI_REGISTRY_REPO', 'STORAGE_CLASS_NAME']
        common_variables = ['PAT_TOKEN']
    if component == 'nifi_storage_secret':
        env_specific_variables = ['STORAGE_ACCOUNT_NAME']
        common_variables = ['STORAGE_ACCESS_KEY']
        secret_values = ['STORAGE_ACCOUNT_NAME', 'STORAGE_ACCESS_KEY']
    if component == 'nifi_storage_class':
        env_specific_variables = ['STORAGE_ACCOUNT_NAME', 'STORAGE_ACCOUNT_RG_NAME', 'STORAGE_CLASS_NAME']
        
    if component == 'nifi_zookeeper':
        env_specific_variables = ['STORAGE_CLASS_NAME']
       
    KUBECONFIG_FILEPATH = os.getenv("KUBECONFIG_FILEPATH", '')
    print(f"updating file {KUBECONFIG_FILEPATH}")
    SetEnvironment(KUBECONFIG_FILEPATH, env, env_specific_variables, common_variables, secret_values)


