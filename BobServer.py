# coding:gbk
"""
@Time �� ${2024��6��} 15:54
@Auth �� ������
"""
import socket
import threading
import Function as Fc
# ��ߴ��븴�öȵ��в�ģ�飬�ڲ���װ�˴��������
import DiffieHellman as DH
# DH�㷨���ɹ�˽Կ�Լ�Э�̹�����Կ
import RSA_SVED
def serverStart(host, port):
    # ���������������׽���
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ����socket�������ڶ����ṩ����
    mySocket.bind((host, port))
    # ���׽���

    print("������", host, ":", port, "������")

    mySocket.listen(5)
    # ����������������������Ŷ�

    return mySocket


def serverListening(mySocket):
    clientSocket, clientAddress = mySocket.accept()
    # �����ͻ������ӣ���ClientSocket����ͻ����׽��ֶ���addrΪ�ͻ����׽��ֵ�ַ
    print("�ͻ���: %s" % str(clientAddress), "�����ӵ�������")
    return clientSocket, clientAddress
def clientClose(clientSocket, clientAddress):
    clientSocket.close()
    print("�ͻ���: %s" % str(clientAddress), "�ѶϿ�����")
if __name__ == "__main__":
    print("��������")
    host = input("�����������IP��ַ��")
    port = int(input("������ͨ�Ŷ˿ںţ�"))
    #host = "127.0.0.1"
    #port = 9999
    mySocket = serverStart(host, port)
    global privatePemPath
    # �Լ���RSA˽Կ�ļ�
    global publicPemPath
    # �Է���RSA��Կ�ļ�
    privatePemPath = 'RSA_PrivateBob.pem'
    publicPemPath = 'RSA_PublicAlice.pem'
    clientSocket, clientAddress = serverListening(mySocket)
    # �ȴ��ͻ�������
    legalClient = Fc.readLegalInfoFrom(clientSocket, publicPemPath)
    # У��ͻ��˵ĺϷ���
    Fc.sendLegalInfoTo(clientSocket, privatePemPath, publicPemPath)
    # ��ͻ��˷����Լ��ĺϷ���У����Ϣ
    if(legalClient):
        # ��ʼЭ��DH��Կ�Լ�����ͨ��
        DH_Group = Fc.readFrom(clientSocket)
        # 1.�յ�DH_Group
        print('�ͻ���ʹ�õ�DH_GroupΪ��', DH_Group)
        DH_PublicAlice = Fc.readFrom(clientSocket, "�ѽ��յ��ͻ���DH��Կ")
        # �������ӿͻ����׽��ֽ����乫Կ DH_PublicAlice
        print("�ͻ���DH��Կ��", DH_PublicAlice[0:20])
        DH_BobServer, DH_PrivateBob, DH_PublicBob = DH.DH_Original(int(DH_Group))
        # ������ʹ����ͬ��int��DH_Group����DHE����DH��˽Կ
        Fc.sendTo(clientSocket, DH_PublicBob, "����ͻ��˷��ͷ�����DH��Կ")
        # ���Ϸ�ʱ��ʼͨ��
        DH_FinalKey = DH.DH_FinalKeyGenerator(DH_BobServer, int(DH_PublicAlice))
        # ���������ɹ���DH��Կ
        TDES_Key = str(DH_FinalKey)[0:24]
        # ʹ��Э�̳��Ĺ���DH��Կ��ǰ24λ��TDES��Կ
        print('��ʼͨ��...')
        print()
        # ���߳�ʵ�ֱ߼����߷���
        serverSending = threading.Thread(target=Fc.sendingThread, args=(clientSocket, TDES_Key, privatePemPath, publicPemPath), name='serverSendingThread')
        serverReceiving = threading.Thread(target=Fc.receivingThread, args=(clientSocket, TDES_Key, privatePemPath, publicPemPath), name='serverSendingThread')
        serverSending.start()
        serverReceiving.start()
        serverSending.join()
        serverReceiving.join()
        print('ͨ���ѽ���...')
    else:
        print("�Ƿ��ͻ��ˣ��ѹر�����")
        clientSocket.close()
clientClose(clientSocket, clientAddress)
