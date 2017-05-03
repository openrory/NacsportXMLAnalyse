import xmltodict
import sys
import csv
from matplotlib import pyplot as plt
from bokeh.plotting import figure, output_file, show, gridplot
from bokeh.charts import Histogram
from bokeh.models import Range1d
from bokeh.models.widgets import Panel, Tabs


def xml_to_dict(file_url: str)->dict:
    """
    Takes an input xml file url string from Nacsport as input and transforms it to a dict.
    :rtype: dict
    :param file_url: input xml string
    :return: dict containing the xml entries
    """
    with open(file_url) as fd:
        nacsport_dict = xmltodict.parse(fd.read())
    return nacsport_dict


def player_analyse(nacsport_dict: dict, codes: dict):
    """
    Takes an input dict as input and prints its summary.
    :param nacsport_dict: input dict
    :param codes: input dict containing labels like codes['Zija']['Pass niet goed']
    """
    counts = dict()
    actions_sec = dict()
    actions_min = dict()
    instances = nacsport_dict["file"]["ALL_INSTANCES"]["instance"]
    # print(instances)
    for instance in instances:
        if instance["code"] in codes:
            if instance["code"] not in counts:
                counts[instance["code"]] = 1

            else:
                counts[instance["code"]] += 1
            if instance["code"] not in actions_sec:
                actions_sec[instance["code"]] = []
            if instance["code"] not in actions_min:
                actions_min[instance["code"]] = []
            actions_sec[instance["code"]].append(float(instance["start"]))
            actions_min[instance["code"]].append(float(instance["start"])/60)
    return counts, actions_sec, actions_min


def team_analyse(nacsport_dict: dict, codes: list):
    """
    Takes an input dict as input and prints its summary.
    :param codes: a list containing all codes in the xml file
    :param nacsport_dict: input xml string
    """
    counts = dict()
    actions_sec = dict()
    actions_min = dict()
    instances = nacsport_dict["file"]["ALL_INSTANCES"]["instance"]
    for instance in instances:
        if instance["code"] in codes:
            if instance["code"] not in counts:
                counts[instance["code"]] = 1
            else:
                counts[instance["code"]] += 1
            if instance["code"] not in actions_sec:
                actions_sec[instance["code"]] = []
            if instance["code"] not in actions_min:
                actions_min[instance["code"]] = []
            actions_sec[instance["code"]].append(float(instance["start"]))
            actions_min[instance["code"]].append(float(instance["start"])/60)
    return counts, actions_sec, actions_min


def write_actions_to_csv(actions:dict, field_names: list, file_url: str)->None:
    """
        This function takes the action and their time of occurrence, and writes them to a csv file
        :param actions: a dict that contains actions as keys and occurences as time for each Nacsport code
        :param field_names: a list [type, code]
        :param file_url: a URL for an output file
        :return:
        """
    with open(file_url, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(field_names)
        for action in actions:
            for time in actions[action]:
                writer.writerow([action, time])


def write_dict_to_csv(stats: dict, field_names: list, file_url: str)->None:
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
        # writer.writerow(stats.values())


def extract_player_codes(nacsport_dict: dict):
    names = list()
    codes_per_player = dict()
    actions_sec = dict()
    actions_min = dict()
    codes = list()
    # TODO: concatenate labels like "Ben Niet goed" to codes
    for instance in nacsport_dict["file"]["ALL_INSTANCES"]["instance"]:
        name = instance["code"]
        if name not in names:  # if the name does not exist yet
            names.append(name)
            codes_per_player[name] = list()
        if type(instance["label"]) is list:  # if there is only one label
            for label in instance["label"]:
                code = label["text"]
                name_code = name + " " + code
        elif instance["label"]:
            code = instance["label"]["text"]
            name_code = name + " " + code
        else:
            return
        if code not in codes_per_player[name]:  # if the code does not exist yet
            codes_per_player[name].append(code)
            codes.append(name_code)
            actions_sec[name_code] = []  # make a list for the actions per second
            actions_min[name_code] = []  # make a list for the actions per minute
        actions_sec[name_code].append(float(instance["start"]))  # add to the actions per second
        actions_min[name_code].append(float(instance["start"]) / 60)  # add to the actions per minute
    return names, codes_per_player, actions_sec, actions_min


def extract_team_codes(nacsport_dict: dict)->list:
    """
    Takes an input dict as input and prints its summary.
    :param nacsport_dict: input xml string
    """
    codes = list()
    for row in nacsport_dict["file"]["ROWS"]["row"]:
            codes.append(row["code"])
    return codes


def plot_actions_team_min(actions: dict, output_file_url: str)->None:
    """
    Plots all actions in a line diagrams and outputs them to an html file.
    :param actions: a list of all actions and their timestamp.
    :param output_file_url: string containing the directory and filename
    :return: None
    """
    # output to static HTML file
    output_file(output_file_url)
    tabs = []
    for action in actions:
        # create a new plot with a title and axis labels
        p = Histogram(actions[action], title=action, bins=[0, 15, 30, 45, 60, 75, 90, 105])
        p.xaxis.axis_label = 'Tijd (min.)'
        p.yaxis.axis_label = 'Frequentie'
        p.x_range = Range1d(0, 105)

        # create a tab
        tab = Panel(child=p, title=action)
        # add to existing tabs
        tabs.append(tab)

    tabs = Tabs(tabs=tabs)

    # show the results
    show(tabs)
    # TODO: add to gridplot, and then show


def plot_actions_players_min(actions: dict, output_file_url: str)->None:
    """
    Plots all actions in a line diagrams and outputs them to an html file.
    :param actions: a list of all actions and their timestamp.
    :param output_file_url: string containing the directory and filename
    :return: None
    """
    # output to static HTML file
    output_file(output_file_url)
    tabs = []
    for action in actions:
        # create a new plot with a title and axis labels
        p = Histogram(actions[action], title=action, bins=[0, 15, 30, 45, 60, 75, 90, 105])
        p.xaxis.axis_label = 'Tijd (min.)'
        p.yaxis.axis_label = 'Frequentie'
        p.x_range = Range1d(0, 105)

        # create a tab
        tab = Panel(child=p, title=action)
        # add to existing tabs
        tabs.append(tab)

    tabs = Tabs(tabs=tabs)

    # show the results
    show(tabs)
    # TODO: group by player
    # TODO: add to gridplot, and then show


def plot_actions_sec(actions: dict) -> None:
    """
    Plots all actions in a line diagrams and outputs them to an image file.
    :param actions: a list of all actions and their timestamp.
    :return: None
    """
    plt.interactive(False)
    bin_names = ['0', '15', '30', '45', '60', '75', '90', '105']

    counter = 1
    for action in actions:

        plt.figure(counter)
        plt.hist(actions[action], bins=[0, 900, 1800, 2700, 3600, 4500, 5400, 6300])
        plt.title(action)
        plt.ylabel('Aantal')
        plt.xlabel('Tijd (min.)')
        plt.xticks(range(0, 6300, 900), bin_names)
    plt.show()


if __name__ == '__main__':
    input_file_url = sys.argv[2]
    file_name = input_file_url.split('/')[-1].split('.')[0]  # get the file name without extension
    directory = '/'.join(input_file_url.split('/')[:-1])
    outfile_html = directory + "/" + file_name + '.html'
    outfile_csv = directory + "/" + file_name + '.csv'
    # print(outfile_html)

    command = sys.argv[1]

    # xml_to_dict(input_file_url)
    nacsport_dict = xml_to_dict(input_file_url)
    actions_fieldnames = ['type', 'time']

    if command == '-i':  # individual
        names, codes, actions_sec, actions_min = extract_player_codes(nacsport_dict)
        plot_actions_players_min(actions_min, outfile_html)
        write_actions_to_csv(actions_min, actions_fieldnames, outfile_csv)
    elif command == '-t':  # team
        codes = extract_team_codes(nacsport_dict)
        counts, actions_sec, actions_min = team_analyse(nacsport_dict, codes)
        plot_actions_team_min(actions_min, outfile_html)
        write_actions_to_csv(actions_min, actions_fieldnames, outfile_csv)
