import copy
from math import floor, fmod 
import math

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

    if ((message[2] | 0b11110111) ^ 0b11111111) == 0b00000000: #смотрим 5-ый бит в третьем байте MESSAGE
        timeT = 1
    else:
        timeT = 0
    
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
    return {'n_lat_cpr': n_lat_cpr, 'n_lon_cpr': n_lon_cpr, 'lat_cpr':lat_cpr,'lon_cpr':lon_cpr,'dlat':dlat,'format':f_cpr, 'time': timeT}

def pairOfMessages(message1,time1, message2, time2): # для вычисления координат # https://mode-s.org/decode/content/ads-b/3-airborne-position.html
    msg1 = TC11Message(message1)
    msg2 = TC11Message(message2)
    latitude = -91
    if (msg1['format'] == 0) and (msg2['format'] == 1): #здесь только если первое четное - >  надо написать обратное!!!!
        index_j = floor(59*msg1['lat_cpr']-60*msg2['lat_cpr']+0.5)
        lat_even = msg1['dlat']*(fmod(index_j,60)+msg1['lat_cpr']) # в градусах
        lat_odd =  msg2['dlat']*(fmod(index_j,59)+msg2['lat_cpr']) # в градусах
        if lat_even>=270:
            lat_even-=360
        if lat_odd>=270:
            lat_odd-=360
        # далее номер зоны по долготе
        NL_even = floor(2*math.pi/(math.acos(1-(1-math.cos(math.pi/(2*NZ)))/((math.cos(math.pi*lat_even/180))**2))))
        NL_odd = floor(2*math.pi/(math.acos(1-(1-math.cos(math.pi/(2*NZ)))/((math.cos(math.pi*lat_odd/180))**2))))
        longitude = -361
        if NL_even==NL_odd: #находятся в одинаковых долготных зонах -> можно дальше вычислять
            if time1>time2:
                latitude = lat_even
            else:
                latitude = lat_odd
            #вычисляем индекс долготы
            index_m = floor(msg1['lon_cpr']*(NL_even-1)-msg2['lon_cpr']*NL_even+0.5)
            n_even = max(NL_even , 1)
            n_odd = max(NL_odd-1 , 1)
            dlon_even = 360/n_even
            dlon_odd = 360/n_odd
            lon_even = dlon_even*((index_m % n_even) +msg1['lon_cpr'])
            lon_odd = dlon_odd*((index_m % n_odd) +msg2['lon_cpr'])
            if time1>=time2:
                longitude = lon_even
            else: 
                longitude = lon_odd
            if longitude>180:
                longitude -=360

    return (round(latitude,5), round(longitude,5)) 