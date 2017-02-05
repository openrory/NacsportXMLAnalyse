import xmltodict
import sys
import csv
from matplotlib import pyplot as plt
from bokeh.plotting import figure, output_file, show, gridplot
from bokeh.charts import Histogram
from bokeh.models import Range1d
from bokeh.models.widgets import Panel, Tabs


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
        writer.writerow(stats.values())


def extract_codes(nacsport_dict: dict)->list:
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
        tab = Panel(child=p, title=action)
        tabs.append(tab)

    tabs = Tabs(tabs=tabs)

    # show the results
    show(tabs)


def plot_actions_players_min(actions: dict)->None:
    """
    Plots all actions in a line diagrams and outputs them to an html file.
    :param actions: a list of all actions and their timestamp.
    :return: None
    """
    # output to static HTML file
    output_file(outfile_url)
    histograms = []
    for action in actions:
        # create a new plot with a title and axis labels
        p = Histogram(actions[action], title=action, bins=[0, 15, 30, 45, 60, 75, 90, 105])
        p.xaxis.axis_label = 'Tijd (min.)'
        p.yaxis.axis_label = 'Frequentie'
        p.x_range = Range1d(0, 105)
        histograms.append(p)

    s = gridplot(histograms, ncols=2)

    # show the results
    show(s)


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
    input_file_url = sys.argv[1]
    file_name = input_file_url.split('/')[-1].split('.')[0]  # get the file name without extension
    directory = '/'.join(input_file_url.split('/')[:-1])
    outfile_url = directory + file_name + '.html'
    print(outfile_url)

    command = sys.argv[2]

    xml_to_dict(input_file_url)
    nacsport_dict = xml_to_dict(input_file_url)
    codes = extract_codes(nacsport_dict)
    counts, actions_sec, actions_min = print_analyse(nacsport_dict, codes)

    # write_dict_to_csv(counts, codes, output_file_url)
    if command == '-i':  # individual
        plot_actions_players_min(actions_min, outfile_url)
    elif command == '-t':  # team
        plot_actions_team_min(actions_min, outfile_url)

