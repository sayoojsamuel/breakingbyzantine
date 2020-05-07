#!/usr/bin/env python3

import random
import time
from collections import Counter
from Crypto.Hash import HMAC, SHA256

SHARED_SECRET = b"AllHailByzantine"
ROUND_TIME = 10  # 10 Seconds
OPTIONS = [
    b"Attack",
    b"Retreat"
]


def decide() -> bytes:
    """
    Function to decide a binary choice in OPTIONS
    OUTPUT:
    @decision: str, from @OPTIONS
    """
    decision = random.choice(OPTIONS)
    return decision


def encodeMessage(message: bytes, time: float) -> bytes:
    """
    Function to encode message

    Add the @header, @footer, and merge message+time
    """
    header = b"beginbyzantine|"
    footer = b"|endbyzantine"

    encoded_message = header \
        + time.hex().encode() \
        + b"|" \
        + message \
        + footer

    return encoded_message

def decodeMessage(encoded_message: bytes) -> (bytes, float):
    """
    Function to decode message

    Remove the @header, @footer, and merge message+time
    """
    header = b"beginbyzantine|"
    footer = b"|endbyzantine"
    raw_data = encoded_message.split(b"|")
    timeHex, message = raw_data[1].decode(), raw_data[2]
    t = time.time().fromhex(timeHex)

    return message, t


def generateHMAC(encoded_message: bytes) -> str:
    """
    Function to generate HMAC for given message
    INPUT:
    @encoded_message: bytes
    OUTPUT:
    @mac: str, the HMAC for the current message
    """

    macObject = HMAC.new(
        key = SHARED_SECRET,
        msg = encoded_message,
        digestmod = SHA256
    )
    mac = macObject.hexdigest()
    return mac

   
def verifyHMAC(mac: str, encoded_message: bytes) -> bool:
    """
    Function to verify HMAC for encoded_message

    Performs hmac and time validity

    INPUT:
    @mac: str, the hmac generated
    @encoded_message: bytes
    OUTPUT:
    @validity: bool, True if Valid, False otherwise
    """
    validity = None

    macObject = HMAC.new(
        key = SHARED_SECRET,
        msg = encoded_message,
        digestmod = SHA256
    )

    # Check hmac validity
    mac_validity = (macObject.hexdigest() == mac)

    # Check time validity
    curr_time = time.time()
    message, _time = decodeMessage(encoded_message)
    time_validity = ((_time - curr_time) < ROUND_TIME)

    """
    # NOTE: Check foro HMAC.hexverify.   Now defaulted to basic check
    try:
        macObject.hexverify(mac)
        validity = True
    except ValueError:
        validity = False
    """
    return mac_validity and time_validity


def announceDecision():
    """
    The Main function to decide and announce the decision

    Used parameters
    @message = decision
    @_time = time of message generation

    OUTPUT:
    A tuple consisting of
    @encoded_message
    @_time
    @mac
    """
    message = decide()
    _time = time.time()
    encoded_message = encodeMessage(message, _time)
    mac = generateHMAC(encoded_message)
    # FIXME: Complete according to the need

    return (
        message,
        encoded_message,
        _time,
        mac
    )


def collectiveDecision(message: bytes, others: (bytes, bytes)) -> bytes:
    """
    Function to finalize the attack plan

    INPUT:
    @message: bytes, the self.decision of the plan of attack
    @others: (bytes, bytes), general2 and general3's plan of attack

    OUTPUT:
    @collective_decision: bytes, the majority decision
    """
    plans = [message] + list(others)
    final_decision, vote_count = Counter(plans).most_common(1)[0]

    return final_decision

    return max()
