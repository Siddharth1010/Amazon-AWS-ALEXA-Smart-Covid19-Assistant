from __future__ import print_function
import random
import boto3

# Functions that build all of the responses


def get_test_response(label):
    session_attributes = {}
    card_title = "Test"
    op=str(label)
    if op=="b'odyMask'":
        speech_output="Person is wearing a mask"
    else:
        speech_output="Person is not wearing a mask. " "Please do so before going outside. "
    
    reprompt_text = "You never responded to the first test message. Sending another one."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
card_title, speech_output, reprompt_text, should_end_session))


def get_SD_response(label):
    session_attributes = {}
    card_title = "Test"
    op=str(label)
    if op=="b'OK'":
        speech_output="Social Distancing Protocols are being maintained"
    else:
        speech_output="Social Distancing Protocols are not being maintained"
    
    reprompt_text = "You never responded to the first test message. Sending another one."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
card_title, speech_output, reprompt_text, should_end_session))
    

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# Functions that control the skill's behavior
def get_compliment_response():

    session_attributes = {}
    card_title = "Compliment"
    speech_output = "This is test by siddharth"
    reprompt_text = "I said," + "This is test by siddharth"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_welcome_response():

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Your application has started!"
    reprompt_text = "I don't know if you heard me, welcome to our alexa application!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying our application. " "Have a nice day! "
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# Events

def on_session_started(session_started_request, session):
    """ Called when the session starts.
        One possible use of this function is to initialize specific 
        variables from a previous state stored in an external database
    """
    pass

    

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Get test response
    if intent_name == "HelloWorldIntent":
        return get_compliment_response()
    # Face Mask Intent and result storage into S3
    elif intent_name == "MaskIntent":
        session = boto3.Session(aws_access_key_id="""  Enter AWS Access Key ID  """,aws_secret_access_key="""  Enter AWS Secret Access Key   """,)
        s1 = session.resource('s3')
        bucket = s1.Bucket('face-mask-status1')
        obj = bucket.Object(key='status.txt') 
        response = obj.get()
        text = response["Body"].read()
        label=text
        return get_test_response(label)
    # Social Distancing Intent and result storage into S3  
    elif intent_name == "SDistancingIntent":
        session = boto3.Session(aws_access_key_id="""  Enter AWS Access Key ID  """,aws_secret_access_key="""  Enter AWS Secret Access Key   """,)
        s1 = session.resource('s3')
        bucket = s1.Bucket('social-distance-status1')
        obj = bucket.Object(key='SDstatus.txt') 
        response = obj.get()
        text = response["Body"].read()
        label=text
        return get_SD_response(label)
        
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])


# Main handler

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])