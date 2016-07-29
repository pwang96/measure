__author__ = 'masslab'

import json
from config import software_name
import re


def generate_output_file(jsonpath):
    """

    :param jsonpath: path to the json file with all the information outputted by the new masscode
    :return: path to the output file
    """
    print "Generating output file"

    with open(jsonpath) as f:
        info = json.load(f)

    first_key = 'run 01'
    for key in info.keys():
        if 'run' in key:
            first_key = key

    filename = jsonpath.replace('.json', '_output.txt')

    restraint_accepted = [y for x, y in zip(info['restraint vec'], info['weight accepted values']) if x == 1][0]
    restraint_volume = [y for x, y in zip(info['restraint vec'], info['volumes']) if x == 1][0]
    restraint_b = [y for x, y in zip(info['restraint vec'], info['type B']) if x == 1][0]
    restraint_a = [y for x, y in zip(info['restraint vec'], info['type A']) if x == 1][0]

    check_accepted = [y for x, y in zip(info['check vec'], info['weight accepted values']) if x == 1]
    check_volume = [y for x, y in zip(info['check vec'], info['volumes']) if x == 1]
    check_b = [y for x, y in zip(info['check vec'], info['type B']) if x == 1]
    check_a = [y for x, y in zip(info['restraint vec'], info['type A']) if x == 1]
    if check_accepted:
        check_accepted = check_accepted[0]
        check_volume = check_volume[0]
        check_b = check_b[0]
        check_a = check_a[0]
    else:
        check_accepted = 0
        check_volume = 0
        check_b = 0
        check_a = 0

    standard_vec = [max(a, b) for a, b in zip(info['restraint vec'], info['check vec'])]
    report_vec = standard_vec
    for i, j in enumerate(standard_vec):
        if j == 1:
            report_vec[i] = 0
        elif j == 0:
            report_vec[i] = 1

    design_matrix = info['design matrix']
    visual_design_matrix = design_matrix
    for row_num, row in enumerate(design_matrix):
        for n, v in enumerate(row):
            if v == 1:
                visual_design_matrix[row_num][n] = '+'
            elif v == -1:
                visual_design_matrix[row_num][n] = '-'
            elif v == 0:
                visual_design_matrix[row_num][n] = ' '

    observed_check_correction = [y for x, y in zip(info['check vec'], info['corrections']) if all((x,y))][0]

    volumes = [info['volumes'][0], info['volumes'][1], info['volumes'][2], abs(info['volumes'][3])]

    standard_names = [y for x, y in zip(standard_vec, info['weight names']) if x == 1]

    report_names = [y for x, y in zip(report_vec, info['weight names']) if x == 1]
    report_corrections = [y for x, y in zip(report_vec, info['corrections']) if x == 1]
    report_exp_unc = [y for x, y in zip(report_vec, info['expanded uncertainty']) if x == 1]
    report_volumes = [y for x, y in zip(report_vec, volumes) if x == 1]
    report_coeff_exp = [y for x, y in zip(report_vec, info['weight exp coefficients']) if x == 1]

    with open(filename, 'w+') as f:
        f.write('This file was generated by "%s"\n' % software_name)
        # f.write('Series %s of %s\n' % (run number, total runs))
        f.write('Date Time: %s\n' % info['date'])
        f.write('\n\n')
        f.write('BALANCE' + '{:>6}'.format(info['balance id']) + '\n')
        # f.write('OPERATOR' )
        f.write('ACCEPTED WITHIN STANDARD DEVIATION OF THE PROCESS' +
                '{:>15.5f}'.format(info['balance std'][1]) + '{:>4}'.format('mg') + '\n')
        f.write('ACCEPTED BETWEEN STANDARD DEVIATION OF THE PROCESS' +
                '{:>14.5f}'.format(info['balance std'][0]) + '{:>4}'.format('mg') + '\n')
        f.write('\n')
        f.write('CALIBRATION DESIGN\t%s\n' % info['design id'])
        f.write('RESTRAINT VECTOR\t' + '\t'.join(str(x) for x in info['restraint vec']) + '\n')
        f.write('MASS CORRECTION OF RESTRAINT' +
                '{:>41.5f}'.format(float(restraint_accepted)) + '{:>4}'.format('mg') + '\n')
        f.write('VOLUME OF WEIGHTS BEING USED IN RESTRAINT @ ' + str(info['temperature'][0]) +
                'deg ' + 'C\t' + str(restraint_volume) + ' cm^3\n')
        f.write('TYPE B UNCERTAINTY IN THE RESTRAINT' +
                '{:>34.5f}'.format(float(restraint_b)) + '  mg\n')
        f.write('TYPE A UNCERTAINTY AFFECTING RESTRAINT' +
                '{:>34.5f}'.format(float(restraint_a)) + '  mg\n')
        # -------------------------------------------------------------------------------------------
        f.write('\n\n')
        f.write('CHECK STANDARD USED\t\n')  # TODO:THIS
        f.write('CHECK VECTOR\t' + '\t'.join(str(x) for x in info['check vec']) + '\n')
        f.write('ACCEPTED MASS CORRECTION OF CHECK' + '{:>27.5f}'.format(float(check_accepted)) + '  mg\n')
        f.write('REPORT VECTOR\t' + '\t'.join(str(x) for x in report_vec) + '\n')
        f.write('\n\n')
        f.write('SUMMARY OF WEIGHTS IN MEASUREMENT'.center(76))
        f.write('\n\n')
        f.write('WEIGHT BEING'.center(15) +
                'NOMINAL'.center(14) +
                'DENSITY'.center(15) +
                'COEFFICIENT'.center(16) +
                'ACCEPTED'.center(16) + '\n')
        f.write('TESTED'.center(15) +
                'VALUE [g]'.center(14) +
                '[g/cm^3 @ 20 C]'.center(15) +
                'OF EXPANSION'.center(16) +
                'CORRECTION [mg]'.center(16) + '\n')
        f.write('\n')
        for pos, name in enumerate(info['weight names']):
            f.write(name[:15].center(15) + str(info['nominal weights'][pos]).center(14) +
                    str(info['densities'][pos]).center(15) +
                    str(info['weight exp coefficients'][pos]).center(16) +
                    str(info['weight accepted values'][pos]).center(16) + '\n')

        # ------------------------------------------------------------------------------
        f.write('\n\n')
        f.write('DESIGN MATRIX\n')
        for row_num, row in enumerate(visual_design_matrix):
            f.write('A   ' + str(row_num + 1) + '\t' + '\t'.join(visual_design_matrix[row_num]) + '\n')
        f.write('\n')
        f.write('OBSERVATIONS IN DIVISIONS\n')
        f.write('DIRECT READINGS\n\n')
        for num, diff in enumerate(info['differences']):
            f.write('A  ' + str(num + 1) + '\t' + '{:.5f}'.format(diff) + '\n')
        f.write('\n\n')
        # ------------------------------------------------------------------------------
        f.write('SENSITIVITY WEIGHT\n')
        f.write('MASS\n')
        f.write('VOLUME\n')
        f.write('COEFFICIENT OF EXPANSION\n')
        f.write('ACCEPTED SENSITIVITY =\n')
        f.write('OBSERVED SENSITIVITY =\n')
        f.write('T-TEST =\t' + str(info['t value']))
        f.write('\n\n')
        f.write(9*' ' + 'ADJUSTED'.center(13) +
                14*' ' + 'OBSERVED'.center(13) + '\n')
        f.write(9*' ' + 'A(I)'.center(13) +
                'DELTA(I)'.center(14) + 'SENSITIVITY'.center(13) + '\n')
        f.write(9*' ' + '[mg]'.center(13) +
                '[mg]'.center(14) + '[mg/div]'.center(13) + '\n')
        f.write('\n')
        for num, val in enumerate(info['corrected differences']):
            f.write('A  ' + str(num + 1) + (6-len(str(num+1)))*' ' +
                    '{:.5f}'.format(val).center(13) +
                    '{:.5f}'.format(info['delta'][num]).center(14) + '\n')  # TODO: Observed sensitivity
        f.write('\n\n')
        f.write(29*' ' + 'VOLUME'.center(12) +
                'TYPE B'.center(11) +
                'TYPE A'.center(11) +
                'EXPANDED'.center(11) + '\n')
        f.write('ITEM'.center(15) +
                'CORRECTION'.center(14) +
                '(AT T)'.center(12) +
                'UNCERT'.center(11) +
                'UNCERT'.center(11) +
                'UNCERT'.center(11) + '\n')
        f.write('[g] or [lb]'.center(15) +
                '[mg]'.center(14) +
                '[cm^3]'.center(12) +
                '[mg]'.center(11) +
                '[mg]'.center(11) +
                '[mg]'.center(11) + '\n')
        f.write('\n')
        for weight_num, weight in enumerate(info['weight nominals']):
            f.write('{:.4f}'.format(float(weight)).center(15) +
                    '{:.5f}'.format(float(info['corrections'][weight_num])).center(14) +
                    '{:.5f}'.format(float(info['volumes'][weight_num])).center(12) +
                    '{:.5f}'.format(float(info['type B'][weight_num])).center(11) +
                    '{:.5f}'.format(float(info['type A'][weight_num])).center(11) +
                    '{:.5f}'.format(float(info['expanded uncertainty'][weight_num])).center(11) + '\n')
        f.write('\n\n')
        # --------------------------------------------------------------
        f.write('PRECISION CONTROL\n')
        f.write('OBSERVED STANDARD DEVIATION OF THE PROCESS\t' +
                '{:.5f}'.format(info['balance std'][0]) + ' [mg]\n')
        f.write('ACCEPTED STANDARD DEVIATION OF THE PROCESS\t' +
                '{:.5f}'.format(info['balance std'][1]) + ' [mg]\n')
        f.write('DEGREES OF FREEDOM\t' + '3\n')
        f.write('F RATIO\t\t' + '{:.4f}'.format(info['f ratio']) + '\n')
        f.write('\n')
        if info['f ratio'] < info['f crit']:
            f.write('F RATIO IS LESS THAN %s (CRITICAL VALUE FOR ALPHA = 0.050)\n' % '{:.4f}'.format(info['f crit']))
            f.write('THEREFORE THE STANDARD DEVIATION IS IN CONTROL\n')
        else:
            f.write('F RATIO IS GREATER THAN %s (CRITICAL VALUE FOR ALPHA = 0.050\n' % '{:.4f}'.format(info['f crit']))
            f.write('THEREFORE THE STANDARD DEVIATION IS NOT IN CONTROL\n')
        f.write('\n\n')
        f.write('CHECK VECTOR\t' + '\t'.join(str(x) for x in info['check vec']) + '\n')
        f.write('CHECK STANDARD USED\t\n')  # TODO:THIS
        f.write('ACCEPTED MASS CORRECTION OF CHECK' + '{:>14.5f}'.format(float(check_accepted)) + '  mg\n')
        f.write('OBSERVED CORECTION OF CHECK STANDARD' + '{:>19.5f}'.format(observed_check_correction) + ' mg\n')
        f.write('STANDARD DEVIATION OF THE OBSERVED CORRECTION' + '{:>11.5f}'.format(2) + ' mg\n')  # TODO: what's here
        f.write('T VALUE\t' + '{:.2f}'.format(info['t value']))
        f.write('\n\n\n')
        if abs(info['t value']) < info['t crit']:
            f.write('ABSOLUTE VALUE OF T IS LESS THAN %s (ALPHA = 0.050)\n' % info['t crit'])
            f.write('THEREFORE CHECK STANDARD IS IN CONTROL\n')
        else:
            f.write('ABSOLUTE VALUE OF T IS GREATER THAN %s (ALPHA = 0.050)\n' % info['t crit'])
            f.write('THEREFORE CHECK STANDARD IS NOT IN CONTROL\n')
        f.write('\n\n')
        # ------------------------------------------------------------------------
        f.write('TEST CONDITIONS\n')
        f.write('TEMPERATURE [C]'.center(18) + '\n')
        f.write('\t BEFORE\t\t' + '{:.4f}'.format(info['temperature'][0]) + '\n')
        f.write('\t  AFTER\t\t' + '{:.4f}'.format(info['temperature'][5]) + '\n')
        f.write('\tAVERAGE\t\t' + '{:.4f}'.format(float(sum(info['temperature']))/len(info['temperature'])) + '\n')
        f.write('\n')
        f.write('HUMIDITY [%rh]'.center(18) + '\n')
        f.write('\t BEFORE\t\t' + '{:.4f}'.format(float(info[first_key]['observation 01']['1-A1'][3])) + '\n')
        f.write('\t  AFTER\t\t' + '{:.4f}'.format(float(info[first_key]['observation 06']['4-A2'][3])) + '\n')
        try:
            # Old masscode stored average humidity as a length 1 list
            f.write('\tAVERAGE\t\t' + '{:.4f}'.format(float(info['average humidity'][0])) + '\n')
        except TypeError:
            f.write('\tAVERAGE\t\t' + '{:.4f}'.format(float(info['average humidity'])) + '\n')
        f.write('\n')
        f.write('AIR PRESSURE [Pa]'.center(18) + '\n')
        f.write('\t BEFORE\t\t' + '{:.4f}'.format(float(info[first_key]['observation 01']['1-A1'][2])) + '\n')
        f.write('\t  AFTER\t\t' + '{:.4f}'.format(float(info[first_key]['observation 06']['4-A2'][2])) + '\n')
        f.write('\tAVERAGE\t\t' + '{:.4f}'.format(float(info['average air pressure'])) + '\n')
        f.write('\n')
        f.write('AIR DENSITY [mg/cm3]\n')
        f.write('\t BEFORE\t\t' + '{:.4f}'.format(info['air density'][0]) + '\n')
        f.write('\t  AFTER\t\t' + '{:.4f}'.format(info['air density'][5]) + '\n')
        f.write('\tAVERAGE\t\t' + '{:.4f}'.format(float(sum(info['air density'])) / len(info['air density'])) + '\n')
        f.write('\n\n')
        # ---------------------------------------------------------------------------
        f.write('TABLE I'.center(76))
        f.write('\n\n')
        f.write(35*' ' + 'EXPANDED*'.center(13) + '\n')
        f.write(18*' ' + 'MASS'.center(17) +
                'UNCERTAINTY'.center(13) +
                'VOL (20 C)'.center(14) +
                'COEFF OF EXP'.center(15) + '\n')
        f.write('ITEM'.center(18) +
                '[g]'.center(17) +
                '[g]'.center(13) +
                '[cm^3]'.center(14) + '\n')
        f.write('\n')
        for number, name in enumerate(report_names):
            f.write(name.center(18) +
                    '{:.5f}'.format(info['nominal weights'][number] + float(report_corrections[number])).center(17) +
                    '{:.5f}'.format(float(report_exp_unc[number])).center(13) +
                    '{:.5f}'.format(float(report_volumes[number])).center(14) +
                    '{:.5f}'.format(float(report_coeff_exp[number])).center(15) + '\n')
        f.write('\n')
        f.write('* THE UNCERTAINTIES ARE CALCULATED ACCORDING TO NIST TECHNICAL\n')
        f.write('NOTE 1297 IMPLEMENTED JANUARY 1, 1994. SEE REFERENCE NO. 14. \n')
        f.write('THE EXPANDED UNCERTAINTY IS 2 TIMES THE ROOT SUM SQUARE OF\n')
        f.write('THE TYPE A AND TYPE B UNCERTAINTIES.\n')
        f.write('\n\n')
        # ---------------------------------------------------------------------------
        f.write('TABLE II'.center(76))
        f.write('\n\n\n')
        f.write('ITEM'.center(22) +
                'COR.A [mg]'.center(22) +
                'COR.B [mg]'.center(22) + '\n')
        f.write('\n')
        for number, name in enumerate(standard_names):
            f.write(name.center(22) + '\n')

        f.write('\n\n')
        f.write('END OF REPORT')

# generate_output_file('L:\\internal\\684.07\\Mass_Project\\Software\\PythonProjects\\measure\\testing\\peter\\20160725_41_2.json')