import requests
import datetime
import pytz



def getDateOfQuery() :
    """
    Returns the date of query based on the current date and time.

    Return
    ------
    query_date_string - a formatted string containing the data for which query should take place
    """

    # Set the timezone
    tz = pytz.timezone('Asia/Kolkata')

    # Get the current time
    current_date_time = datetime.datetime.now()

    # Convert the current time into this timezone
    current_date_time = current_date_time.astimezone(tz)

    # If the time is already 4 pm, then we start querying for the next day
    if current_date_time.hour >= 16 :
        query_date_time = current_date_time + datetime.timedelta(days=1)
    else :
        query_date_time = current_date_time

    # Convert the query datetime into string in required format
    query_date_string = query_date_time.strftime("%d-%m-%Y")

    # Return the query date
    return query_date_string



def pingCovinForInfo() :
    """
    Sends an API call to the COVIN Web API to get bach the results from the server

    Return
    ------
    response - the HTTP response if no error occured, else None
    """

    # We try a total of 5 times
    pings_left = 5
    while pings_left > 0 :
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        }
        parameters = {
            'district_id' : "540",
            "date" : getDateOfQuery(),
        }
        response = requests.get(
            "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict", 
            headers=headers, params=parameters
        )

        if 200 <= response.status_code < 300 :
            break
    
    # If successful return the respose else return None
    if 200 <= response.status_code < 300 :
        return response.json()
    return None



def parseRawData(response_data) :
    """
    Given the raw response data, we extract only the required data factors from this.

    Parameters
    ----------
    response_data - the raw json data from the api

    Return
    ------
    candidate_centers - the list of filtered out centers
    """

    # Initialize a list to store all the filtered out centers
    candidate_centers = []

    # Parse through this json data and save the ones which have availability
    for center in response_data['sessions'] :
        if (
            (center['vaccine'] in ['COVISHIELD', 'SPUTNIK V']) and
            (center['min_age_limit'] > 44 ) and 
            (center['available_capacity_dose1'] > 0 )
        ) :
            cur_candidate = {
                'name' : center['name'],
                'num_dose_1' : center['available_capacity_dose1'],
                'fee' : center['fee'],
                'vaccine' : center['vaccine'],
                'min_age' : center['min_age_limit'],
                'slots' : center['slots']
            }
            candidate_centers.append(cur_candidate)

    # Return this list of candidates
    return candidate_centers



def logActivity(status) :
    """
    Writes the status of the current execution in the log file.

    Parameters
    ----------
    status - a message string denoting the status of the current execution
    """

    # Prepare the complete status string
    message = datetime.datetime.now().strftime() + '\t\t : \t' + status + '\n'

    # Append the message to the end of the log file
    with open('../logs/status.log', 'a') as log_file:
        log_file.write(message)



