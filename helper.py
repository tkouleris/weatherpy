import datetime


def page_data():
    return {
        'year': datetime.date.today().year
    }


def day_of_the_week(day_number):
    match day_number:
        case 0:
            return 'Monday'
        case 1:
            return 'Tuesday'
        case 2:
            return 'Wednesday'
        case 3:
            return 'Thursday'
        case 4:
            return 'Friday'
        case 5:
            return 'Saturday'
    return 'Sunday'
