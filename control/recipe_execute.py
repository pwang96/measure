__author__ = 'masslab'


def execute(methods, arguments, data_signal, progress_signal):
    """ Execute list of methods in thread separate from user interface

    Args:
        methods (list): control methods list generated by recipe maker
        arguments (list): list of arguments for each method in the "methods" argument
        data_signal (pyqtSignal): pyqtSignal object declared in "ComparatorUi"
        progress_signal (pyqtSignal): pyqtSignal object declared in "ComparatorUi"
    """
    for i in range(len(methods)):
        reading = methods[i](*arguments[i])
        if reading:
            data_signal.emit(reading)
        progress_signal.emit(None)
