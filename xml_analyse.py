import xmltodict
import sys


def xml_to_dict(file_url):
    """
    Takes an input xml file url string from Nacsport as input and transforms it to a dict.
    :param file_url: input xml string
    :return: dict containing the xml entries
    """
    with open(file_url) as fd:
        nacsport_dict = xmltodict.parse(fd.read())
    return nacsport_dict


def print_analyse(nacsport_dict):
    """
    Takes an input dict as input and prints its summary.
    :param nacsport_dict: input xml string
    """
    codes = analyse_codes(nacsport_dict)
    counts = dict()
    for instance in nacsport_dict["file"]["ALL_INSTANCES"]["instance"]:
        if instance["code"] in codes:
            if instance["code"] not in counts:
                counts[instance["code"]] = 0
            else:
                counts[instance["code"]] += 1
    print(counts)
    print(codes)


def analyse_codes(nacsport_dict):
    codes = list()
    for row in nacsport_dict["file"]["ROWS"]["row"]:
            codes.append(row["code"])
    return codes

if __name__ == '__main__':
    input_file_url = sys.argv[1]
    output_file_url = sys.argv[2]
    xml_to_dict(input_file_url)
    nacsport_dict = xml_to_dict(input_file_url)
    print_analyse(nacsport_dict)
