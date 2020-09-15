"""

@FileName: yaml.py
@Author: chenxiaodong
@CreatTime: 2020/9/14 16:43
@Descriptions:
This class is for yaml-file deal

"""
import yaml


class yaml_tools:
    def __init__(self, file_path: None) -> None:
        """
        you should provide the file_path to use this tool.
        if file_path not found, will raise FileNotFoundError

        * yaml_to_json()  change yaml to json
        * get_config_by_name(config_name: None)

        :param: file_path

        """
        if self.path is None:
            raise FileNotFoundError(" The file is not exist!")
        self.path = file_path

    def yaml_to_dict(self) -> dict:
        """
        change yaml-file to dict

        """
        with open(self.path, "r") as f:
            yaml_file = yaml.safe_load(f)
        return yaml_file

    def get_config_by_name(self, config_name: None) -> str:
        """
        use get method to get the string words

        :param:config_name
        :return:String
        """
        return self.yaml_to_dict().get(config_name)
