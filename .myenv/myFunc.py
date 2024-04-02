import copy
from math import floor, fmod 

NZ = 15 #represents the number of latitude zones between the equator and a pole. In Mode S, is defined to be 15.

# 7 байт тип сообщения -> первые шесть бит: тип АДСБ, два последних: номер канала
# потом перенести в отжельную функцию
# для первого канала 0b00001100 - ADSB-112; 0b00001000 - ADSB-56; 0b00000100 - A/C
# для второго канала 0b00001101 - ADSB-112; 0b00001001 - ADSB-56; 0b00000101 - A/C
# для третьего канала 0b00001110 - ADSB-112; 0b00001010 - ADSB-56; 0b00000110 - A/C
# для четвертого канала 0b00001111 - ADSB-112; 0b00001011 - ADSB-56; 0b00000111 - A/C
def byteToTypeAndNumberOfChannel(data: bytes) -> str:
    dt = copy.deepcopy(data)
    if (dt ^ 0b00001100)==0b00000000:
        return 'first channel - ADSB-112'
    elif (dt ^ 0b00001000)==0b00000000:
        return 'first channel - ADSB-56'
    elif (dt ^ 0b00000100)==0b00000000:
        return 'first channel - A/C'
    elif (dt ^ 0b00001101)==0b00000000:
        return 'Second channel - ADSB-112'
    elif (dt ^ 0b00001001)==0b00000000:
        return 'Second channel - ADSB-56'
    elif (dt ^ 0b00000101)==0b00000000:
        return 'Second channel - A/C'
    elif (dt ^ 0b00001110)==0b00000000:
        return 'Third channel - ADSB-112'
    elif (dt ^ 0b00001010)==0b00000000:
        return 'Third channel - ADSB-56'
    elif (dt ^ 0b00000110)==0b00000000:
        return 'Third channel - A/C'
    elif (data ^ 0b00001111)==0b00000000:
        return 'Forth channel - ADSB-112'
    elif (dt ^ 0b00001011)==0b00000000:
        return 'Forth channel - ADSB-56'
    elif (dt ^ 0b00000111)==0b00000000:
        return 'Forth channel - A/C'
    

def TC11Message(message):  # для кода типа 11 (и других кодов местоположения) Doc 9871 (page A.2.3.1) TC- type code in DF17,18
    if ((message[2] | 0b11111011) ^ 0b11111111) == 0b00000000: #смотрим 6-ой бит в третьем байте MESSAGE
        f_cpr = 1
    else:
        f_cpr = 0
    
    n_lat_cpr_Bytes = bytearray(3)
    n_lat_cpr_Bytes[0] = (message[2]&0b00000011)
    n_lat_cpr_Bytes[1:2] = message[3:4]
    n_lat_cpr_Bytes[2:3] = message[4:5]
    n_lat_cpr = int.from_bytes(n_lat_cpr_Bytes,'big')>>1

    n_lon_cpr_Bytes = bytearray(3)
    n_lon_cpr_Bytes[0] = (message[4]&0b00000001)
    n_lon_cpr_Bytes[1:2] = message[5:6]
    n_lon_cpr_Bytes[2:3] = message[6:7]
    n_lon_cpr = int.from_bytes(n_lon_cpr_Bytes,'big')

    lat_cpr = n_lat_cpr/(2**17)
    lon_cpr = n_lon_cpr/(2**17)
    if  f_cpr == 0:
        dlat = 360/(4*NZ)
    else: 
        dlat = 360/(4*NZ-1)
    #floor() 
    return {'n_lat_cpr': n_lat_cpr, 'n_lon_cpr': n_lon_cpr, 'lat_cpr':lat_cpr,'lon_cpr':lon_cpr,'dlat':dlat,'format':f_cpr}

def pairOfMessages(message1,message2): # для вычисления координат # https://mode-s.org/decode/content/ads-b/3-airborne-position.html
    msg1 = TC11Message(message1)
    msg2 = TC11Message(message2)
    if (msg1['format'] == 0) and (msg2['format'] == 1):
        index_j = floor(59*msg1['lat_cpr']-60*msg2['lat_cpr']+0.5)
        lat_even = msg1['dlat']*(fmod(index_j,60)+msg1['lat_cpr'])
        lat_odd =  msg2['dlat']*(fmod(index_j,59)+msg2['lat_cpr'])
        if lat_even>=270:
            lat_even-=360
        if lat_odd>=270:
            lat_odd-=360

            
        print (lat_even)
        print (lat_odd)

    return (msg1['n_lat_cpr'],msg1['n_lon_cpr'],msg2['n_lat_cpr'],msg2['n_lon_cpr']) 