import os
from yaml import dump
from glob import glob
from yaml import FullLoader
from yaml import load


class MergeYMLFiles:
    def __init__(self):
        self.current_directory = os.getcwd()
        self.resources_yml_folder = '/setup/resources/*.yml'
        self.serverless_file = 'serverless.yml'
        self.services_directory = 'services'
        self.initial_serverless = {}
        self.serverless_file_path = ''

    def __get_path_of_serverless(self, project_path: str) -> str:
        directories_in_project_path = os.listdir(project_path)
        for directory in directories_in_project_path:
            path_directory = f'{project_path}/{directory}'
            is_dir = os.path.isdir(path_directory)
            if is_dir:
                path_file = f'{path_directory}/serverless.yml'
                file_exists = os.path.exists(path_file)
                if file_exists:
                    self.serverless_file_path = f'{path_directory}/serverless.yml'

    def __get_resources(self, project_path: str) -> list:
        resources_path = f'{project_path}/setup/resources/*.yml'
        resources = glob(resources_path)
        return resources

    def __get_data_from_resources(self, resources_paths: list) -> dict:
        for resource in resources_paths:
            with open(resource) as file:
                resource_data = load(file, Loader=FullLoader)
                if resource_data and self.initial_serverless:
                    self.__compare_and_merge_dicts(resource_data)

    def __compare_and_merge_dicts(self, resources_dict: dict) -> dict:
        initial_dict_keys = list(self.initial_serverless.keys())
        resources_dict_keys = list(resources_dict.keys())

        keys_not_in_initial = [x for x in resources_dict if x not in self.initial_serverless]
        keys_in_initial_dict = [
            x for x in initial_dict_keys if x in resources_dict_keys
        ]

        for key_not_in_dict in keys_not_in_initial:
            self.initial_serverless[key_not_in_dict] = resources_dict.get(key_not_in_dict)

        for key_in_dict in keys_in_initial_dict:
            self.initial_serverless[key_in_dict].update(resources_dict.get(key_in_dict))

    def __write_new_serverless_yml_file(self):
        if self.initial_serverless:
            with open(self.serverless_file_path, 'w') as file:
                dump(self.initial_serverless, file)
            self.initial_serverless = ''

    def merge(self):
        for item in os.listdir(self.services_directory):
            path_dir = f'{self.current_directory}/{self.services_directory}/{item}'
            is_dir = os.path.isdir(path_dir)
            resources = []
            if is_dir:
                project_path = path_dir
                resources = self.__get_resources(project_path)
            if(resources):
                self.__get_path_of_serverless(project_path)
                if self.serverless_file_path:
                    with open(self.serverless_file_path) as file:
                        print('-------------------------------------->')
                        self.initial_serverless = load(file, Loader=FullLoader)
                        print(self.initial_serverless)
                        self.__get_data_from_resources(resources)
                        print('***** AFTER MERGE *****')
                        print(self.initial_serverless)
                        self.__write_new_serverless_yml_file()


if __name__ == '__main__':
    merge_yml_files = MergeYMLFiles()
    merge_yml_files.merge()
