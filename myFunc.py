



# 7 байт тип сообщения -> первые шесть бит: тип АДСБ, два последних: номер канала
# потом перенести в отжельную функцию
# для первого канала 0b00001100 - ADSB-112; 0b00001000 - ADSB-56; 0b00000100 - A/C
# для второго канала 0b00001101 - ADSB-112; 0b00001001 - ADSB-56; 0b00000101 - A/C
# для третьего канала 0b00001110 - ADSB-112; 0b00001010 - ADSB-56; 0b00000110 - A/C
# для четвертого канала 0b00001111 - ADSB-112; 0b00001011 - ADSB-56; 0b00000111 - A/C
def byteToTypeAndNumberOfChannel(data: bytes) -> str:
    if (data ^ 0b00001100)==0b00000000:
        return 'first channel - ADSB-112'
    elif (data ^ 0b00001000)==0b00000000:
        return 'first channel - ADSB-56'
    elif (data ^ 0b00000100)==0b00000000:
        return 'first channel - A/C'
    elif (data ^ 0b00001101)==0b00000000:
        return 'Second channel - ADSB-112'
    elif (data ^ 0b00001001)==0b00000000:
        return 'Second channel - ADSB-56'
    elif (data ^ 0b00000101)==0b00000000:
        return 'Second channel - A/C'
    elif (data ^ 0b00001110)==0b00000000:
        return 'Third channel - ADSB-112'
    elif (data ^ 0b00001010)==0b00000000:
        return 'Third channel - ADSB-56'
    elif (data ^ 0b00000110)==0b00000000:
        return 'Third channel - A/C'
    elif (data ^ 0b00001111)==0b00000000:
        return 'Forth channel - ADSB-112'
    elif (data ^ 0b00001011)==0b00000000:
        return 'Forth channel - ADSB-56'
    elif (data ^ 0b00000111)==0b00000000:
        return 'Forth channel - A/C'