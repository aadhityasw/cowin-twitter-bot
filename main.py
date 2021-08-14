import requests
import datetime
import pytz
import tweepy
#import config
import os
#from user_agent import generate_user_agent



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
            #"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
            #"User-Agent": generate_user_agent()
        }
        parameters = {
            'district_id' : os.environ['DISTRICT_ID'],#config.DISTRICT_ID,
            "date" : getDateOfQuery(),
        }
        response = requests.get(
            "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict", 
            headers=headers, params=parameters
        )

        if 200 <= response.status_code < 300 :
            break

        pings_left -= 1
    
    # If successful return the respose else return None
    if 200 <= response.status_code < 300 :
        return response.json()
    else :
        print(response.status_code)
        print(response.json())
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
            (center['vaccine'] in ['COVISHIELD']) and
            (center['min_age_limit'] >= 18 ) and 
            (center['available_capacity'] > 0 )
        ) :
            cur_candidate = {
                'name' : center['name'],
                'num_dose_1' : center['available_capacity_dose1'],
                'num_dose_2' : center['available_capacity_dose2'],
                'fee' : center['fee'],
                'vaccine' : center['vaccine'],
                'date' : center['date'],
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

    # Trim the log file such that it contains only the last 1000 records

    # Read in all the lines of logs
    with open('logs/status.log', 'r') as log_file:
        past_records = log_file.readlines()
    # Trim the logs such that it will now contain only the last 1000 lines
    past_records = past_records[-1000:]
    # Write only these last 1000 records back into the log file
    with open('logs/status.log', 'w') as log_file:
        log_file.writelines(past_records)

    # Proceed with appending the current log record

    # Appends the time with this status message
    status_message = str(datetime.datetime.now()) + '\t\t : \t' + status + '\n'

    # Append the message to the end of the log file
    with open('logs/status.log', 'a') as log_file:
        log_file.write(status_message)



def prepareAvailableCentersMessage(candidate_centers) :
    """
    Given the candidate centers, parses through this data and prepares a string message.

    Parameters
    ----------
    candidate-centers - the list of centers which matches with our conditions

    Return
    ------
    message - the center's details in a formatted manner for display or any other purpose
    """

    # Initialize an empty string which will hold the final message
    message = ""

    # Load in the center details in a formatted manner
    for i, center in enumerate(candidate_centers) :
        message += f"{i+1}. {center['name']} :\n"
        message += f"\tDoses Available (Dose 1) : {center['num_dose_1']}\n"
        message += f"\tDoses Available (Dose 2) : {center['num_dose_2']}\n"
        message += f"\tFee : {center['fee']}\n"
        message += f"\tVaccine : {center['vaccine']}\n"
        message += f"\tAge group : {center['min_age']}+ years\n"
        message += f"\tDate : {center['date']}\n"
        message += f"\tSlots : {center['slots'][0]}\n"
        for j in range(1, len(center['slots'])) :
            message += f"\t\t\t{center['slots'][j]}\n"
        message += "---------------------------------\n\n\n"
    
    # Return this formatted message
    return message



def storeCurrentCandidateCenters(message) :
    """
    Given the formatted message containing the center details, prints it in a status file.

    Parameters
    ----------
    message - the formatted message with the center details
    """

    # Adds the current time above the message
    message = str(datetime.datetime.now()) + '\n\n\n' + message + '\n'

    # Write the message to the output file
    with open('logs/vaccine_centers.txt', 'w') as output_file:
        output_file.write(message)



def sendTwitterDM(message) :
    """
    Given a message, use the tweepy library to send a twitter DM to the user

    Parameters
    ----------
    message - the formatted message with the center details
    """

    # Establish a connection using the Authorization tokens
    #auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
    #auth.set_access_token(config.TWITTER_ACCESS_KEY, config.TWITTER_ACCESS_SECRET)
    auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['TWITTER_ACCESS_KEY'], os.environ['TWITTER_ACCESS_SECRET'])

    # Create API handler
    api = tweepy.API(auth)

    # Get the user-id of the reciever using their twitter username
    user = api.get_user(os.environ['TWITTER_RECIPIENT_USER_NAME'])
    recipient_id = user.id_str

    # Send a DM
    api.send_direct_message(recipient_id, message)



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Parent Code ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# Ping the COVIN API requesting a list of all vaccination centers available
covin_response = pingCovinForInfo()

# Use this to store the log messages
log_message = ""

# If the response is not None, then proceed
if covin_response is not None :
    # log the current status
    log_message += "COVIN data extracted; "

    # Extract the candidate centers after scutiny of the returned centers
    candidate_centers = parseRawData(covin_response)

    # Log the number of centers left
    log_message += f"{len(candidate_centers)} Candidate centers found; "

    # Proceed based on whether any candidates are left after scrutiny
    if len(candidate_centers) > 0 :
        # Prepare the message using these candidate centers
        message = prepareAvailableCentersMessage(candidate_centers)

        # Store these candidate centres in a file
        storeCurrentCandidateCenters(message)

        # Send Message to the twitter user using tweepy
        sendTwitterDM(message)

        # Log the sending of message (Twitter DM)
        log_message += "Message sent through twitter DM"

else :
    log_message += "Pings to COVIN failed;"

# Log this message into the log file
logActivity(log_message)
