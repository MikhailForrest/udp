import socket
import math
import myFunc
from crc import Calculator, Crc16
from time import strftime, gmtime
import copy

UDP_IP = "10.1.1.16"
UDP_PORT = 49002

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP,UDP_PORT))

print(myFunc.TC11Message(bytes([0x58,0x1B,0x66,0xE9,0xBD,0x8C,0xEE]))['n_lat_cpr']) #odd; CPR latitude  : 95454; CPR longitude : 101614; 
                                                                                    #ICAO 7C1BE8; tc = 11
print(myFunc.pairOfMessages(bytes([0x58,0xb9,0x71,0xa3,0x6c,0x12,0xa6]),1.2,bytes([0x58,0xb9,0x75,0x02,0x8b,0xd3,0xb8]),1.21))
# 1 - 58 b9 71 a3 6c 12 a6 2 - 58 b9 75 02 8b d3 b8

numOf112 = 0 # счетчик для количества 112 битных пакетов
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print(data.hex())
    airData = hex(data[0])
    if airData=='0x81':
        print('=======================================================')
        line_str = ''
        line_str += 'CountOfMess  '+str(int(hex(data[1]),16))+'; '
        line_str += 'number of receiver  '+str(int(data[2:4].hex(),16))+'; '
        line_str += 'NumOfPack  '+str(int(data[4:6].hex(),16))+'; '
        count_of_mess = int(hex(data[1]),16)
        print(line_str)
        #calc = Calculator(Crc16.CCITT)
        #chckSm = calc.checksum(data[0:len(data)-2])
        #print((chckSm))
        init_mess = 6
        for i_mess in range(0,count_of_mess):
            info_of_ch = myFunc.byteToTypeAndNumberOfChannel(data[init_mess])
            print(info_of_ch)
            myByte = copy.copy(data[init_mess])
            myByte = myByte>>2
            if (myByte ^ 0b000001) == 0b000000: #A/C сообщение
                time_in_nanosec = int(data[(init_mess+1):(init_mess+7)].hex(),16)
                line_str = ''
                line_str+=strftime("%H:%M:%S",gmtime(time_in_nanosec/1000000000))+";  "
                line_str += 'level  '+str(40-int(data[(init_mess+7):(init_mess+8)].hex(),16))+'; ' 
                line_str += 'SNR  '+str(2+20*math.log10(int(data[(init_mess+8):(init_mess+9)].hex(),16)))+';'
                print(line_str)
                init_mess+=11 #11 - длина A/C сообщения
            elif (myByte ^ 0b000010) == 0b000000:
                time_in_nanosec = int(data[(init_mess+1):(init_mess+7)].hex(),16)
                line_str = ''
                line_str+=strftime("%H:%M:%S",gmtime(time_in_nanosec/1000000000))+";  "
                line_str += 'level  '+str(40-int(data[(init_mess+9):(init_mess+10)].hex(),16))+'; ' 
                line_str += 'SNR  '+str(2+20*math.log10(int(data[(init_mess+10):(init_mess+11)].hex(),16)))+';'
                print(line_str)
                init_mess+=18 #18 - длина ADSB-56 сообщения
            elif (myByte ^ 0b000011) == 0b000000:
                time_in_nanosec = int(data[(init_mess+1):(init_mess+7)].hex(),16)
                line_str = ''
                line_str+=strftime("%H:%M:%S",gmtime(time_in_nanosec/1000000000))+";  "
                line_str += 'level  '+str(40-int(data[(init_mess+9):(init_mess+10)].hex(),16))+'; ' 
                line_str += 'SNR  '+str(2+20*math.log10(int(data[(init_mess+10):(init_mess+11)].hex(),16)))+';'
                print(line_str)
                if (data[init_mess] ^ 0b00001100)==0b00000000: # здесь уже заложено номер 1 канала
                    adsb_112_Data = data[(init_mess+11):(init_mess+25)]         
                    if ((adsb_112_Data[0]>>2) ^ 0b100011)==0b00000: # проверка df17 - первые шесть бит первого байта
                        print(adsb_112_Data.hex())
                        ME_in_bytes = adsb_112_Data[4:11]
                        #print(ME_in_bytes.hex())
                        mB1 =  copy.copy(ME_in_bytes[0])
                        print ('tc=  '+str(int(hex((mB1>>3)),16)))
                        if ((ME_in_bytes[2] | 0b11111011) ^ 0b11111111) == 0b00000000: #смотрим 6-ой бит в третьем байте MESSAGE
                            print ("CPR odd (1)")
                        else:
                            print ("CPR even (0)") 
                        print('ICAOaddress   '+adsb_112_Data[1:4].hex())
                        numOf112 +=1
                    else:
                        print('not df17')
                # adsb_112_Data = data[(init_mess+11):(init_mess+25)]
                # print(adsb_112_Data.hex())
                init_mess+=25 #25 - длина ADSB-112 сообщения

        # line_str = ''
        # line_str += 'level  '+str(40-int(data[15:16].hex(),16))+'; ' 
        # line_str += 'SNR  '+str(2+20*math.log10(int(data[16:17].hex(),16)))+';'
        # print(line_str)
        # print(myFunc.byteToTypeAndNumberOfChannel(data[6]))
        

        # if (data[6] ^ 0b00001100)==0b00000000: # здесь уже заложено номер 1 канала
        #     adsb_112_Data = data[17:31]         
        #     if ((adsb_112_Data[0]>>2) ^ 0b100011)==0b00000: # проверка df17 - первые шесть бит первого байта
        #         print(adsb_112_Data.hex())
        #         ME_in_bytes = adsb_112_Data[4:11]
        #         #print(ME_in_bytes.hex())
        #         print ('tc=  '+str(int(hex((ME_in_bytes[0]>>3)),16)))
        #         if ((ME_in_bytes[2] | 0b11111011) ^ 0b11111111) == 0b00000000: #смотрим 6-ой бит в третьем байте MESSAGE
        #             print ("CPR odd (1)")
        #         else:
        #             print ("CPR even (0)") 
        #         print('ICAOaddress   '+adsb_112_Data[1:4].hex())
        #         numOf112 +=1
        #     else:
        #         print('not df17')
        
        if numOf112 >100:
            break