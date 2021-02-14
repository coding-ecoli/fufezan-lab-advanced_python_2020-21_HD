def find_peaks(list_of_intensities):
    """Find peaks

    Find local maxima for a given list of intensities or tuples
    Intensities are defined as local maxima if the 
    intensities of the elements in the list before and after 
    are smaller than the peak we want to determine.

    Args:
        list_of_intensities (list of floats, ints or tuple of ints): a list of
            numeric values

    Returns:
        list of floats or tuples: list of the identified local maxima

    Note:
        This is just a place holder for the TDD part :)
        
    1 5 [6] 4 1 2 [3] 2 
    """
    peaks = []
    for pos, current_peak in enumerate(list_of_intensities[:-1]):
        if pos == 0:
            continue
        if list_of_intensities[pos - 1] < current_peak > list_of_intensities[pos + 1]:
            peaks.append(current_peak)
    return peaks