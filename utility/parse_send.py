__author__ = 'masslab'

import re
from sub_ui.error_message import ErrorMessage
import datetime

def parse_output(filepath):
    """

    :param filepath: takes in an output file path to parse
    :return: dictionary with all of the data that has to be sent to the database
    """
    if 'nout' in filepath:
        try:
            dct = {'date': None,
                    'balance': None,
                    'restraint vector': None,
                    'restraint accepted': None,
                    'check vector': None,
                    'check accepted': None,
                    'report vector': None,
                    'weight names': [],
                    'densities': [],
                    'corrections': [],
                    'volumes': [],
                    'typeB': [],
                    'typeA': [],
                    'temperature': None,
                    'pressure': None,
                    'humidity': None}

            line_counter = 0
            with open(filepath) as f:
                while True:  # breaks out when STOP is read
                    line = f.readline()  # read the next line

                    # beginning of if statements and parsing
                    if line_counter < 15:  # all the one time info in headers
                        if 'DateTime' in line:
                            regex = r'(\d*-\d*-\d* \d*\:\d*)'
                            dct['date'] = re.findall(regex, line)[0]

                        if 'BALANCE' in line:
                            regex = r'(\d*)'
                            matches = re.findall(regex, line)
                            for i in matches:
                                if i != '':
                                    dct['balance'] = i

                    if 'RESTRAINT VECTOR' in line:
                        regex = r'(\d)'
                        dct['restraint vector'] = [int(i) for i in re.findall(regex, line)]

                    if 'CHECK STANDARD VECTOR' in line:
                        regex = r'(\d)'
                        dct['check vector'] = [int(i) for i in re.findall(regex, line)]

                    if 'MASS CORRECTION OF RESTRAINT' in line:
                        regex = r'(.?\d\.\d*)'
                        dct['restraint accepted'] = float(re.findall(regex, line)[0])

                    if 'ACCEPTED MASS CORRECTION OF CHECK STANDARD' in line:
                        regex = r'(.?\d\.\d*)'
                        dct['check accepted'] = float(re.findall(regex, line)[0])

                    if 'REPORT VECTOR' in line:
                        regex = r'(\d)'
                        dct['report vector'] = [int(i) for i in re.findall(regex, line)]

                    if 'EXPANSION' in line and 'CORRECTION' in line:
                        # This can only handle output files with four weights
                        f.readline()
                        for i in range(4):
                            line = f.readline()
                            dct['weight names'].append(line[0:15].strip())
                            dct['densities'].append(line[30:43].strip())

                    if '[mg]       [mg]' in line:
                        # This can only handle output files with four weights
                        f.readline()
                        for i in range(4):
                            line = f.readline()
                            regex = r'(.?\d*\.\d*)'
                            matches = re.findall(regex, line)
                            dct['corrections'].append(float(matches[1]))
                            dct['volumes'].append(float(matches[2]))
                            dct['typeB'].append(float(matches[3]))
                            dct['typeA'].append(float(matches[4]))

                    if 'AVERAGE' in line and 'DEG C' in line:
                        regex = r'(\d*\.\d*)'
                        dct['temperature'] = re.findall(regex, line)[0]

                    if 'AVERAGE' in line and 'RH' in line:
                        regex = r'(\d*\.\d*)'
                        dct['humidity'] = re.findall(regex, line)[0]

                    if 'AVERAGE' in line and 'PA' in line:
                        regex = r'(\d*)\.'
                        dct['pressure'] = re.findall(regex, line)[0]

                    if 'STOP' in line:
                        break

                    line_counter += 1
            return dct
        except:
            ErrorMessage("Not an output file")

    elif 'txt' in filepath:
        # parse the new output file
        try:
            dct = {'date': None,
                   'balance': None,
                   'restraint vector': None,
                   'restraint accepted': None,
                   'check vector': None,
                   'check accepted': None,
                   'report vector': None,
                   'weight names': [],
                   'densities': [],
                   'corrections': [],
                   'volumes': [],
                   'typeB': [],
                   'typeA': [],
                   'temperature': None,
                   'pressure': None,
                   'humidity': None}

            line_counter = 0
            with open(filepath) as f:
                while True:  # breaks out when STOP is read
                    line = f.readline()  # read the next line

                    # beginning of if statements and parsing
                    if line_counter < 15:  # all the one time info in headers
                        if 'Date Time' in line:
                            regex = r'(\d*/\d*/\d* \d*\:\d*)'
                            date_with_slash = re.findall(regex, line)[0]
                            if date_with_slash == '':
                                regex2 = r'(\d*-\d*-\d* \d*\:\d*)'
                                date_without_slash = re.findall(regex2, line)[0]
                                dct['date'] = date_without_slash
                            else:
                                dct['date'] = datetime.datetime.strftime(
                                    datetime.datetime.strptime(date_with_slash, '%m/%d/%Y %H:%M'), '%m-%d-%Y %H:%M')
                            print dct['date']

                        if 'BALANCE' in line:
                            regex = r'(\d*)'
                            matches = re.findall(regex, line)
                            for i in matches:
                                if i != '':
                                    dct['balance'] = i

                    if 'RESTRAINT VECTOR' in line:
                        regex = r'(\d)'
                        dct['restraint vector'] = [int(i) for i in re.findall(regex, line)]

                    if 'CHECK VECTOR' in line:
                        regex = r'(\d)'
                        dct['check vector'] = [int(i) for i in re.findall(regex, line)]

                    if 'MASS CORRECTION OF RESTRAINT' in line:
                        regex = r'(.?\d\.\d*)'
                        dct['restraint accepted'] = float(re.findall(regex, line)[0])

                    if 'ACCEPTED MASS CORRECTION OF CHECK' in line:
                        regex = r'(.?\d\.\d*)'
                        dct['check accepted'] = float(re.findall(regex, line)[0])

                    if 'REPORT VECTOR' in line:
                        regex = r'(\d)'
                        dct['report vector'] = [int(i) for i in re.findall(regex, line)]

                    if 'EXPANSION' in line and 'CORRECTION' in line:
                        # This can only handle output files with four weights
                        f.readline()
                        for i in range(4):
                            line = f.readline()
                            dct['weight names'].append(line[0:15].strip())
                            dct['densities'].append(line[30:43].strip())

                    if '[g] or [lb]' in line:
                        # This can only handle output files with four weights
                        f.readline()
                        for i in range(4):
                            line = f.readline()
                            regex = r'(.?\d*\.\d*)'
                            matches = re.findall(regex, line)
                            dct['corrections'].append(float(matches[1]))
                            dct['volumes'].append(float(matches[2]))
                            dct['typeB'].append(float(matches[3]))
                            dct['typeA'].append(float(matches[4]))

                    if 'TEMPERATURE [C]' in line:
                        f.readline()
                        f.readline()
                        line = f.readline()
                        regex = r'(\d*\.\d*)'
                        dct['temperature'] = re.findall(regex, line)[0]

                    if 'HUMIDITY [%rh]' in line:
                        f.readline()
                        f.readline()
                        line = f.readline()
                        regex = r'(\d*\.\d*)'
                        dct['humidity'] = re.findall(regex, line)[0]

                    if 'AIR PRESSURE [Pa]' in line:
                        f.readline()
                        f.readline()
                        line = f.readline()
                        regex = r'(\d*)\.'
                        dct['pressure'] = re.findall(regex, line)[0]

                    if 'END OF REPORT' in line:
                        break

                    line_counter += 1
            return dct
        except:
            ErrorMessage("Not an output file")


def send_output(output, db):
    # Separates data into two dictionaries, internal and external weights
    # data in the following order:
    # date, balance ID, name, weight ID (for internals only), role, correction, accepted correction,
    # type A, type B, volume, density, temperature, pressure, and humidity

    internal_dict = {'date': output['date'],
                     'balance': output['balance'],
                     'temperature': output['temperature'],
                     'pressure': output['pressure'],
                     'humidity': output['humidity'],
                     'restraint name': None,
                     'restraint ID': None,
                     'restraint accepted': output['restraint accepted'],
                     'restraint correction': None,
                     'restraint A': None,
                     'restraint B': None,
                     'restraint volume': None,
                     'restraint density': None,
                     'check name': None,
                     'check ID': None,
                     'check accepted': output['check accepted'],
                     'check correction': None,
                     'check A': None,
                     'check B': None,
                     'check volume': None,
                     'check density': None}

    external_dict = {'date': output['date'],
                     'balance': output['balance'],
                     'temperature': output['temperature'],
                     'pressure': output['pressure'],
                     'humidity': output['humidity'],
                     'unknown1 name': None,
                     'unknown1 accepted': None,
                     'unknown1 correction': None,
                     'unknown1 A': None,
                     'unknown1 B': None,
                     'unknown1 volume': None,
                     'unknown1 density': None,
                     'unknown2 name': None,
                     'unknown2 accepted': None,
                     'unknown2 correction': None,
                     'unknown2 A': None,
                     'unknown2 B': None,
                     'unknown2 volume': None,
                     'unknown2 density': None}

    for i, j in enumerate(output['restraint vector']):
        if j == 1:
            internal_dict['restraint name'] = output['weight names'][i]
            internal_dict['restraint correction'] = output['corrections'][i]
            internal_dict['restraint A'] = output['typeA'][i]
            internal_dict['restraint B'] = output['typeB'][i]
            internal_dict['restraint volume'] = output['volumes'][i]
            internal_dict['restraint density'] = output['densities'][i]

    for i, j in enumerate(output['check vector']):
        if j == 1:
            internal_dict['check name'] = output['weight names'][i]
            internal_dict['check correction'] = output['corrections'][i]
            internal_dict['check A'] = output['typeA'][i]
            internal_dict['check B'] = output['typeB'][i]
            internal_dict['check volume'] = output['volumes'][i]
            internal_dict['check density'] = output['densities'][i]

    internal_dict['restraint ID'] = db.get_weightID_by_name(internal_dict['restraint name'])[0][0]
    internal_dict['check ID'] = db.get_weightID_by_name(internal_dict['check name'])[0][0]

    count = 1
    for i, j in enumerate(output['report vector']):
        if j == 1 and count == 1:
            external_dict['unknown1 name'] = output['weight names'][i]
            external_dict['unknown1 correction'] = output['corrections'][i]
            external_dict['unknown1 A'] = output['typeA'][i]
            external_dict['unknown1 B'] = output['typeB'][i]
            external_dict['unknown1 volume'] = output['volumes'][i]
            external_dict['unknown1 density'] = output['densities'][i]
            count += 1
        if j == 1 and count == 2:
            external_dict['unknown2 name'] = output['weight names'][i]
            external_dict['unknown2 correction'] = output['corrections'][i]
            external_dict['unknown2 A'] = output['typeA'][i]
            external_dict['unknown2 B'] = output['typeB'][i]
            external_dict['unknown2 volume'] = output['volumes'][i]
            external_dict['unknown2 density'] = output['densities'][i]

    db.push_restraint_weight_data(internal_dict)
    db.push_check_weight_data(internal_dict)
    db.push_unknown1_data(external_dict)
    db.push_unknown2_data(external_dict)

    return internal_dict['restraint name'], internal_dict['check name'],\
           external_dict['unknown1 name'], external_dict['unknown2 name']


