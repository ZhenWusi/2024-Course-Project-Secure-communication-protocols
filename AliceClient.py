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
def connectToServer(host, port):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ����socket�����������ӷ����
    print("���ڳ����������", host, ":", port, "��������...")
    serverSocket.connect((host, port))
    print("���ӳɹ�")
    print()
    return serverSocket


if __name__ == "__main__":
    print("�ͻ���")
    host = input("�����������IP��ַ��")
    port = int(input("������ͨ�Ŷ˿ںţ�"))
    # host = "127.0.0.1"
    # port = 9999
    serverSocket = connectToServer(host, port)
    # ���ӵ��������׽���
    global privatePemPath
    # �Լ���RSA˽Կ�ļ�
    global publicPemPath
    # �Է���RSA��Կ�ļ�
    privatePemPath = 'RSA_PrivateAlice.pem'
    publicPemPath = 'RSA_PublicBob.pem'
    Fc.sendLegalInfoTo(serverSocket, privatePemPath, publicPemPath)
    # ������������Լ��ĺϷ���У����Ϣ
    legalServer = Fc.readLegalInfoFrom(serverSocket, publicPemPath)
    # У��������ĺϷ���
    if (legalServer):
        # У��Է���ݺϷ�ʱ��ʼЭ��DH��Կ�Լ�����ͨ��
        DH_Group = 15
        # ����DH�㷨��˽Կ�ԵĲ���
        DH_AliceClient, DH_PrivateAlice, DH_PublicAlice = DH.DH_Original(DH_Group)
        # ����DHE����DH��˽Կ
        Fc.sendTo(serverSocket, DH_Group)
        # 1.����DH_Group��������
        Fc.sendTo(serverSocket, DH_PublicAlice, "������������Ϳͻ���DH��Կ")
        # 2.���Ϳͻ���DH��Կ��������
        DH_PublicBob = Fc.readFrom(serverSocket, '�ѽ��յ�������DH��Կ')
        # 3.���շ�����DH��Կ
        print('������DH��Կ', str(DH_PublicBob)[0:20])
        # DH��Կ����Э��õ�����Կ
        DH_FinalKey = DH.DH_FinalKeyGenerator(DH_AliceClient, int(DH_PublicBob))
        # ���ɹ���DH��Կ
        print('��ʼͨ��...')
        print()
        TDES_Key = str(DH_FinalKey)[0:24]
        # ʹ��Э�̳��Ĺ���DH��Կ��ǰ24λ��TDES��Կ
        # ���߳�ʵ�ֱ߼����߷���
        clientSending = threading.Thread(target=Fc.sendingThread,
                                         args=(serverSocket, TDES_Key, privatePemPath, publicPemPath),
                                         name='clientSendingThread')
        clientReceiving = threading.Thread(target=Fc.receivingThread,
                                           args=(serverSocket, TDES_Key, privatePemPath, publicPemPath),
                                           name='clientReceivingThread')
        clientSending.start()
        clientReceiving.start()
        clientSending.join()
        clientReceiving.join()
        print('ͨ���ѽ���...')
    else:
        print("���������Ϸ����ѹر�����")
    print('�Ự�������ѹر�����')
