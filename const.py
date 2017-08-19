#!/usr/bin/python
# -*-coding:utf-8-*-
__author__ = "ihciah"


class BtCommandByte(object):
    @staticmethod
    def findCommand(c):
        keys = filter(lambda x: not x.startswith("__") and BtCommandByte.__getattribute__(BtCommandByte, x) == c,
                      dir(BtCommandByte))
        return keys[0] if keys else "NO_MATCH_COMMAND"

    __fmversion__ = "1.2.7"
    PRT_PRINT_DATA = 0
    PRT_PRINT_DATA_COMPRESS = 1
    PRT_FIRMWARE_DATA = 2
    PRT_USB_UPDATE_FIRMWARE = 3
    PRT_GET_VERSION = 4
    PRT_SENT_VERSION = 5
    PRT_GET_MODEL = 6
    PRT_SENT_MODEL = 7
    PRT_GET_BT_MAC = 8
    PRT_SENT_BT_MAC = 9
    PRT_GET_SN = 10
    PRT_SENT_SN = 11
    PRT_GET_STATUS = 12
    PRT_SENT_STATUS = 13
    PRT_GET_VOLTAGE = 14
    PRT_SENT_VOLTAGE = 15
    PRT_GET_BAT_STATUS = 16
    PRT_SENT_BAT_STATUS = 17
    PRT_GET_TEMP = 18
    PRT_SENT_TEMP = 19
    PRT_SET_FACTORY_STATUS = 20
    PRT_GET_FACTORY_STATUS = 21
    PRT_SENT_FACTORY_STATUS = 22
    PRT_SENT_BT_STATUS = 23
    PRT_SET_CRC_KEY = 24
    PRT_SET_HEAT_DENSITY = 25
    PRT_FEED_LINE = 26
    PRT_PRINT_TEST_PAGE = 27
    PRT_GET_HEAT_DENSITY = 28
    PRT_SENT_HEAT_DENSITY = 29
    PRT_SET_POWER_DOWN_TIME = 30
    PRT_GET_POWER_DOWN_TIME = 31
    PRT_SENT_POWER_DOWN_TIME = 32
    PRT_FEED_TO_HEAD_LINE = 33
    PRT_PRINT_DEFAULT_PARA = 34
    PRT_GET_BOARD_VERSION = 35
    PRT_SENT_BOARD_VERSION = 36
    PRT_GET_HW_INFO = 37
    PRT_SENT_HW_INFO = 38
    PRT_SET_MAX_GAP_LENGTH = 39
    PRT_GET_MAX_GAP_LENGTH = 40
    PRT_SENT_MAX_GAP_LENGTH = 41
    PRT_GET_PAPER_TYPE = 42
    PRT_SENT_PAPER_TYPE = 43
    PRT_SET_PAPER_TYPE = 44
    PRT_GET_COUNTRY_NAME = 45
    PRT_SENT_COUNTRY_NAME = 46
    PRT_DISCONNECT_BT_CMD = 47
    PRT_MAX_CMD = 48

