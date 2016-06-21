__author__ = 'masslab'

import time
from config import software_name
import re


def generate_input_file(path, main_dict, data_dict, run_number, runs_total):
    """ Create a masscode input file with metadata from main_dict and data from data_dict

    Args:
        path (str):  Path specified by user
        main_dict (dictionary):  Calibration metadata
        data_dict (dictionary):  Measurement data
        run_number (int):  Number of current run
        runs_total (int):  Number of runs to be executed

    Returns:
        filename (str): path to input file
    """
    print "Generating input file"

    observation = []
    environment = []

    # Reorganize data in data dictionary
    for key1 in sorted(data_dict.keys()):
        reading = []
        for key2 in sorted(data_dict[key1].keys()):
            reading.append(data_dict[key1][key2][0])
            environment.append(data_dict[key1][key2][1:])
        # calculate average of differences in readings
        try:
            observation.append(str((float(reading[0])+float(reading[3]))/2 - (float(reading[1])+float(reading[2]))/2))
        except ValueError:
            pattern = r'.?(\d*\.\d*)'
            matches = [re.findall(pattern, reading[i]) for i in range(4)]
            observation.append(str((float(matches[0][0])+float(matches[3][0]))/2 - (float(matches[1][0])+float(matches[2][0]))/2))

    # Cut out extension of the self.path variable (*.settings)
    filename = path + "_" + str(run_number) + ".ntxt"

    # Open new input file!
    with open(filename, "w+") as input_file:
        input_file.write("NEW FORMAT\n")
        input_file.write("READ HEADER\n")
        input_file.write('This file was been generated by "%s"\n' % software_name)
        input_file.write('Series %s of %s \n' % (run_number, runs_total))
        input_file.write("DateTime: %s\n" % time.strftime("%Y-%m-%d %H:%M"))
        input_file.write("Weight History Ids: %s\n" % str(main_dict['weight history id']))
        input_file.write("Internal Weights: %s\n" % str(main_dict['weight internal']))
        input_file.write("Addon History Ids: %s\n" % str(main_dict['addon history id']))
        input_file.write("\n")
        input_file.write("\n")
        input_file.write("\n")
        input_file.write("END HEADER\n")
        input_file.write("\n")
        # input_file.write("DATE\t%s\n" % time.strftime("%m %d %Y"))
        input_file.write('%s UNITS\n' % main_dict['units'])
        input_file.write("TYPE B UNCERTAINTY\t%s\n" % main_dict['restraint type b'])
        # input_file.write("RESTRAINT IDENTIFICATION\t%s\n" %cls.settings_dict["RESTRAINT IDENTIFICATION"])
        input_file.write("\n")
        input_file.write("BALANCE CODE\t%s\n" % main_dict['balance id'])
        # input_file.write("CHECK STANDARD\t%s\n" %cls.settings_dict["CHECK STANDARD"])
        input_file.write("READ TEMPERATURE PRESSURE HUMIDITY\n")
        for row in environment:
            input_file.write('\t'.join(row) + '\n')
        input_file.write("END OF ENVIRONMENT\n")
        input_file.write("!Environmental data is corrected before database entry.\n")
        input_file.write("\n")
        input_file.write("BALANCE WITHIN STANDARD DEVIATION\t%s\n" % main_dict['balance std dev'])
        input_file.write("BALANCE BETWEEN STANDARD DEVIATION\t%s\n" % main_dict['check between'])
        input_file.write('! "Balance between standard deviation" corresponds to between uncertainty in the reference.\n')
        input_file.write("\n")
        input_file.write("NUMBER OF OBSERVATIONS\t%s\n" % len(main_dict['design matrix']))
        input_file.write("NUMBER OF UNKNOWN\t%s\n" % len(main_dict['design matrix'][0]))
        input_file.write("READ WEIGHT\n")
        for weight in main_dict['weight info']:
            input_file.write(weight[0]+"\n")
        input_file.write("END\n")
        input_file.write("\n")
        input_file.write("GRAVITY GRADIENT 0.000000002665\n")
        for i in range(len(main_dict['cg differences'])):
            input_file.write("CENTER OF GRAVITY HEIGHT DIFFERENCE %s %s\n" % (str(i+1), main_dict['cg differences'][i]))
        input_file.write("\n")
        for i in range(len(main_dict['addon info'])):
            if main_dict['addon info'][i]:
                input_file.write("READ ADDON WEIGHT %s\n" % str(i+1))
                for addon in main_dict['addon info'][i]:
                    input_file.write(addon[0] + "\n")
                input_file.write("END\n\n")
        input_file.write("WEIGHT RESTRAINT\t%s\n" % ' '.join([str(i) for i in main_dict['restraint vec']]))
        input_file.write("WEIGHT CHECK STANDARD\t%s\n" % ' '.join([str(i) for i in main_dict['check vec']]))
        # input_file.write("WEIGHT RESTRAINT NEW SERIES\t%s\n" % cls.settings_dict["WEIGHT RESTRAINT NEW SERIES"])
        input_file.write("WEIGHT PRINT\t%s\n" % ' '.join([str(i) for i in main_dict['report vec']]))
        input_file.write("\n")
        input_file.write("READ DESIGN MATRIX\n")
        input_file.write('\n'.join([' '.join([str(i) for i in x]) for x in main_dict['design matrix']]))
        input_file.write('\nEND\n')
        input_file.write("\n")
        input_file.write("TEMPERATURE UNCERTAINTY\t%s\n" % main_dict['temperature uncert'])
        input_file.write("PRESSURE UNCERTAINTY\t%s\n" % main_dict['pressure uncert'])
        input_file.write("HUMIDITY UNCERTAINTY\t%s\n" % main_dict['humidity uncert'])
        input_file.write("\n")
        input_file.write("READ OBSERVATIONS\n")
        for i in observation:
            input_file.write(str(i).format(".6f")+"\n")
        input_file.write("END\n")
        input_file.write("\n")
        fn = filename[:]
        input_file.write('PYTHON FILE %s\n' % (fn.replace('.ntxt', '') + '.python_file'))
        input_file.write("\n")
        input_file.write("END OF SERIES\n")
        input_file.write("STOP\n")
        input_file.write("\n")
        input_file.write("!---------- All Weighing Data ----------!\n")
        for key1 in sorted(data_dict.keys()):
            for key2 in sorted(data_dict[key1].keys()):
                input_file.write(key2 + ':\t' + str(data_dict[key1][key2]) + '\n')

    return filename
