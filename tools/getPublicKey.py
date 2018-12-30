#!/usr/bin/env python3

from ledgerblue.comm import getDongle
from ledgerblue.commException import CommException
import argparse
import struct

def apduPrefix():
    # https://en.wikipedia.org/wiki/Smart_card_application_protocol_data_unit
    CLA = bytes.fromhex("E0")
    INS = b"\x02"
    P1 = b"\x00"
    P2 = b"\x01"
    return CLA + INS + P1 + P2

def exchange(apdu):
    dongle = getDongle(True)
    return dongle.exchange(apdu)

def main(args):
    payload = struct.pack("<I", args.index)
    L_c = bytes([len(payload)])
    apdu = apduPrefix() + L_c + payload
    response = exchange(apdu)
    print(response.hex())

    offset = 1 + response[0]
    address = response[offset + 1 : offset + 1 + response[offset]]
    print("Public key " + response[1 : 1 + response[0]].hex())
    print(str(len(address)) + ": " + address.hex())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', '-i', type=int, required=True)
    args = parser.parse_args()
    main(args)
