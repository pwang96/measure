__author__ = 'masslab'


def data_structure_addon_weights(cls):
    """ Populate main_dict with add on weights detected in user interface"""
    n = len(cls.main_dict['design matrix'][0])
    cls.main_dict['addon info'] = [[] for i in range(n)]
    cls.main_dict['addon history id'] = [[] for i in range(n)]
    for i in range(n):
        for i2 in range(4, cls.ui.weightTable.columnCount()):
            addon_str = str(cls.ui.weightTable.item(i, i2).text())
            if addon_str:
                if addon_str.split("|")[0] == 'EXT':
                    addon_id = addon_str.split("|")[1].strip()
                    addon_name = addon_str.split("|")[2].lstrip()
                    result = cls.db.external_addon_weight_data(int(addon_id))

                    # Unpack query result
                    addon_coeff_exp = str(format(result[1], ".6f"))
                    addon_nominal = float(result[2])
                    addon_accepted = float(result[2])
                    addon_value = str(format(addon_nominal+addon_accepted/1000, ".8f"))
                    addon_density = str(format(result[3], ".6f"))
                    
                    # Store in settings dictionary for input file
                    cls.main_dict['addon history id'][i].append(result[0])

                    cls.main_dict['addon info'][i].append(['{:<16}'.format(addon_name) + '{:>10}'.format(addon_coeff_exp) +
                                                           '{:>12}'.format(addon_value) + '{:>6}'.format(0) +
                                                           '{:>10}'.format(addon_density)])
                else:
                    addon_id = addon_str.split("|")[0]
                    addon_name = addon_str.split("|")[1].lstrip()
                    result = cls.db.addon_weight_data(int(addon_id))

                    # Unpack query result
                    addon_coeff_exp = str(format(result[1], ".6f"))
                    addon_nominal = float(result[2])
                    addon_accepted = float(result[3])
                    addon_value = str(format(addon_nominal+addon_accepted/1000, ".8f"))
                    addon_density = str(format(result[4], ".6f"))

                    # Store in settings dictionary for input file
                    cls.main_dict['addon history id'][i].append(result[0])

                    cls.main_dict['addon info'][i].append(['{:<16}'.format(addon_name) + '{:>10}'.format(addon_coeff_exp) +
                                                           '{:>12}'.format(addon_value) + '{:>6}'.format(0) +
                                                           '{:>10}'.format(addon_density)])

