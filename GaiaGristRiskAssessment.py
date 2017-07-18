"""
This implementation of the Lex Code Hook Interfaceis used to 
in order to serve a prototype bot which allows users to assess their mental 
health risk

"""
import math
import dateutil.parser
import datetime
import time
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


""" --- Helpers to build responses which match the structure of the necessary dialog actions --- """


def get_slots(intent_request):
    return intent_request['currentIntent']['slots']


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


""" --- Helper Functions --- """


def parse_int(n):
    try:
        return int(n)
    except ValueError:
        return float('nan')


def build_validation_result(is_valid, violated_slot, message_content):
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot,
        }

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }


def isvalid_date(date):
    try:
        dateutil.parser.parse(date)
        return True
    except ValueError:
        return False


def validate_risk_assessment(validation, suic, suic_past_att, suic_most_rec, suic_patt_att, suic_first_occ, suic_how_many, suic_note_prev, suic_discovery, suic_lethality, suic_ser_succd, suic_regret, suic_curr_int, suic_plans, suic_plan_real, suic_steps_takn, suic_prosp_leth, suic_int_inform, suic_eol_prep, suic_s_h_behv, suic_int_p_trig, suic_pot_trig, suic_p_trig_mtch, suic_fam_hist, suic_ideation, suic_id_control, suic_id_hi_risk):
    #if date is not None:
    #    if not isvalid_date(date):
    #        return build_validation_result(False, 'PickupDate', 'I did not understand that, what date would you like to pick the flowers up?')
    #    elif datetime.datetime.strptime(date, '%Y-%m-%d').date() <= datetime.date.today():
    #        return build_validation_result(False, 'PickupDate', 'You can pick up the flowers from tomorrow onwards.  What day would you like to pick them up?')


    return build_validation_result(True, None, None)


""" --- Functions that control the bot's behavior --- """


def risk_assessment(intent_request):
    """
    Performs dialog management and fulfillment for mental health risk assessment
    Beyond fulfillment, the implementation of this intent demonstrates the use 
    of the elicitSlot dialog action in slot validation and re-prompting.
    """

#    logger.debug('dispatch userId={}, intentName={}, slots={}'.format(intent_request['userId'], intent_request['currentIntent']['name'], slots))

    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt for the first violation detected.
        slots = get_slots(intent_request)

        validation = slots["validation"]
        suic = slots["suic"]
        suic_past_att = slots["suic_past_att"]
        suic_most_rec = slots["suic_most_rec"]
        suic_patt_att = slots["suic_patt_att"]
        suic_first_occ = slots["suic_first_occ"]
        suic_how_many = slots["suic_how_many"]
        suic_note_prev = slots["suic_note_prev"]
        suic_discovery = slots["suic_discovery"]
        suic_lethality = slots["suic_lethality"]
        suic_ser_succd = slots["suic_ser_succd"]
        suic_regret = slots["suic_regret"]
        suic_curr_int = slots["suic_curr_int"]
        suic_plans = slots["suic_plans"]
        suic_plan_real =  slots["suic_plan_real"]
        suic_steps_takn = slots["suic_steps_takn"]
        suic_prosp_leth = slots["suic_prosp_leth"]
        suic_int_inform = slots["suic_int_inform"]
        suic_eol_prep =  slots["suic_eol_prep"]
        suic_s_h_behv = slots["suic_s_h_behv"]
        suic_int_p_trig = slots["suic_int_p_trig"]
        suic_pot_trig = slots["suic_pot_trig"]
        suic_p_trig_mtch = slots["suic_p_trig_mtch"]
        suic_fam_hist = slots["suic_fam_hist"]
        suic_ideation = slots["suic_ideation"]
        suic_id_control = slots["suic_id_control"]
        suic_id_hi_risk = slots["suic_id_hi_risk"]

        validation_result = validate_risk_assessment(validation, suic, suic_past_att, suic_most_rec, suic_patt_att, suic_first_occ, suic_how_many, suic_note_prev, suic_discovery, suic_lethality, suic_ser_succd, suic_regret, suic_curr_int, suic_plans, suic_plan_real, suic_steps_takn, suic_prosp_leth, suic_int_inform, suic_eol_prep, suic_s_h_behv, suic_int_p_trig, suic_pot_trig, suic_p_trig_mtch, suic_fam_hist, suic_ideation, suic_id_control, suic_id_hi_risk)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        # Pass the price of the flowers back through session attributes to be used in various prompts defined
        # on the bot model.
        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

        return delegate(output_session_attributes, get_slots(intent_request))

    # Order the flowers, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    response = 'You are not at risk. Please do re-assess if there are any changes in your situation.'
    slots = get_slots(intent_request)
    if slots["suic_past_att"] == 'yes' or slots["suic_curr_int"] == 'yes':
        response = 'You are at risk but there is hope. Please get support from PAPYRUS HOPELineUK. Here are their details and they are open now for you to contact them. Contact PAPYRUS HOPELineUK Call: 0800 068 41 41 Text: 07786 209697 Email: pat@papyrus-uk.org'
    
    logger.debug('dispatch userId={}, intentName={}, response={}'.format(intent_request['userId'], intent_request['currentIntent']['name'], response))
    
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': response})
#                  'content': 'Thanks, your order for {} has been placed and will be ready for pickup by {} on {}'.format(flower_type, pickup_time, date)})


""" --- Intents --- """


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'GaiaSuicideIntent':
        return risk_assessment(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
