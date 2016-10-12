import xmltodict
import sys
import csv


def xml_to_dict(file_url):
    """
    Takes an input xml file url string from Nacsport as input and transforms it to a dict.
    :param file_url: input xml string
    :return: dict containing the xml entries
    """
    with open(file_url) as fd:
        nacsport_dict = xmltodict.parse(fd.read())
    return nacsport_dict


def print_analyse(nacsport_dict, codes):
    """
    Takes an input dict as input and prints its summary.
    :param nacsport_dict: input xml string
    """
    counts = dict()
    instances = nacsport_dict["file"]["ALL_INSTANCES"]["instance"]
    for instance in instances:
        if instance["code"] in codes:
            if instance["code"] not in counts:
                counts[instance["code"]] = 0
            else:
                counts[instance["code"]] += 1
    print(counts)
    return counts


def write_dict_to_csv(stats, field_names, file_url):
    """
    This function takes the counts for each code, and writes them to a csv file
    :param stats: a dict that contains occurences of each Nacsport code
    :param field_names: a list of all code names
    :param file_url: a URL for an output file
    :return:
    """
    with open(file_url, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(field_names)
        print(stats)
        writer.writerow(stats.values())


def extract_codes(nacsport_dict):
    """
    Takes an input dict as input and prints its summary.
    :param nacsport_dict: input xml string
    """
    codes = list()
    for row in nacsport_dict["file"]["ROWS"]["row"]:
            codes.append(row["code"])
    return codes

if __name__ == '__main__':
    input_file_url = sys.argv[1]
    output_file_url = sys.argv[2]
    xml_to_dict(input_file_url)
    nacsport_dict = xml_to_dict(input_file_url)
    codes = extract_codes(nacsport_dict)
    counts = print_analyse(nacsport_dict, codes)
    write_dict_to_csv(counts, codes, output_file_url)
