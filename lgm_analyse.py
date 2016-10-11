#import xmltodict
import sys
import json


def to_dict(file_url):
    '''
    Takes an input xml file url string from Nacsport as input and transforms it to a dict.
    :param file_url: input xml string
    :return: dict containing the xml entries
    '''
    lgm_dict = dict()
    with open(file_url, encoding='utf-8-sig') as fd:
        file_string = fd.read()
        parse(file_string)

        #nacsport_dict = xmltodict.parse(fd.read())
        #print(nacsport_dict)
    return lgm_dict


def parse(file_string):
    parsed_json = json.loads(file_string)
    print(parsed_json)


def analyse(lgm_dict):
    codes = analyse_codes(lgm_dict)
    counts = dict()
    for instance in lgm_dict["file"]["ALL_INSTANCES"]["instance"]:
        if instance["code"] in codes:
            if instance["code"] not in counts:
                counts[instance["code"]] = 0
            else:
                counts[instance["code"]] += 1
    print(counts)
    print(codes)


def analyse_codes(lgm_dict):
    codes = list()
    for row in lgm_dict["file"]["ROWS"]["row"]:
            codes.append(row["code"])
    return codes

if __name__ == '__main__':
    input_file_url = sys.argv[1]
    output_file_url = sys.argv[2]
    lgm_dict = to_dict(input_file_url)
    analyse(lgm_dict)
