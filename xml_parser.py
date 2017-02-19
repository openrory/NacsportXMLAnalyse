import xmltodict


class XMLParser:
    def __init__(self, input_file_URL):
        self.input_file_URL = input_file_URL

    def xml_to_dict(self, file_url:str)->dict:
        """
        Takes an input xml file url string from Nacsport as input and transforms it to a dict.
        :param file_url: input xml string
        :return: dict containing the xml entries
        """
        with open(file_url) as fd:
            self.nacsport_dict = xmltodict.parse(fd.read())
        return self.nacsport_dict

    def extract_codes(self, nacsport_dict: dict)->list:
        """
        Takes an input dict as input and prints its summary.
        :param nacsport_dict: input xml string
        """
        self.codes = list()
        for row in nacsport_dict["file"]["ROWS"]["row"]:
            self.codes.append(row["code"])
        return self.codes


