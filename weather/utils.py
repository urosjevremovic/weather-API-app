def get_wind_direction(degree):
    """Convert wind degree to direction."""

    DEGREES = [-11.25, 11.25, 33.75, 56.25,
               78.75, 101.25, 123.75, 146.25,
               168.75, 191.25, 213.75, 236.25,
               258.75, 281.25, 303.75, 326.25, 348.75]

    DIRECTIONS = ['N', 'NNE', 'NE', 'ENE',
                  'E', 'ESE', 'SE', 'SSE',
                  'S', 'SSW', 'SW', 'WSW',
                  'W', 'WNW', 'NW', 'NNW']

    # North wind correction.
    if degree > 348.75:
        degree -= 360

    for i in range(len(DIRECTIONS)):
        left_border = DEGREES[i]
        right_border = DEGREES[i + 1]

        if left_border < degree <= right_border:
            return DIRECTIONS[i]