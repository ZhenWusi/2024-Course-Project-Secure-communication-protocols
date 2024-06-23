# coding:gbk
"""
@Time �� ${2024��6��} 15:56
@Auth �� ������
"""
# coding:gbk
'''
Outputs:    timeStamp() ����ʱ���
            sendTo(theSocket, message, hint=None) ��Է��׽��ַ�����Ϣ
            readFrom(theSocket, hint=None) �ӶԷ��׽��ֽ�����Ϣ
            sendLegalInfoTo(theSocket, privatePemPath, publicPemPath) ����������öԷ����кϷ���У��
            readLegalInfoFrom(theSocket, publicPemPath) У��Է���ݵĺϷ���
            RSA_SignatureTo(theSocket, RSA_DecryptText, privatePemPath) ��Է�����ʱ�����ǩ����У����Ϣ
            RSA_VerifyFrom(theSocket, publicPemPath) У��Է�������ʱ�����ǩ����У����Ϣ
            communicatePackageReceiver(theSocket, TDES_Key, publicPemPath) ����ͨ�����ݰ�
            communicatePackageReceiver(theSocket, TDES_Key, publicPemPath) ����ͨ�����ݰ�
            sendingThread(theSocket, TDES_Key, privatePemPath) ����ͨ�����ݰ����̷߳���
            receivingThread(theSocket, TDES_Key, publicPemPath) ����ͨ�����ݰ����̷߳���
'''
import random
import time
import RSA_SVED
import hashlib
# ʵ��RSA ǩ�� ��ǩ ���� ���ܵĵײ�ģ��
import TDES
# ʵ��3DES�㷨�ӽ��ܵĵײ�ģ��
# ����һ��ȫ���ֵ䣬���ڴ洢��ʹ�õ�Nonce
used_nonces = {}
def generate_nonce():
    # ����һ���������Nonce��������Ƿ��Ѵ������ֵ��У������������������
    while True:
        nonce = str(random.randint(1, 2**16))
        if nonce not in used_nonces:
            used_nonces[nonce] = True
            return nonce
def timeStamp():
    # ����ʱ���
    currentTime = time.strftime('%Y��%m��%d�� %H:%M:%S', time.localtime(time.time()))
    return currentTime
def sendTo(theSocket, message, hint=None):
    nonce = generate_nonce()
    timestamp = timeStamp()
    print(f"����ʱ���: {timestamp}")
    message_with_nonce = f"{message}-{nonce}-{timestamp}"
    hash_value = hashlib.sha256(message_with_nonce.encode()).hexdigest()
    message_to_send = f"{message_with_nonce}-{hash_value}"
    theSocket.send(message_to_send.encode('utf-8'))
    if hint is not None:
        print(hint)

def readFrom(theSocket, hint=None):
    message_received = theSocket.recv(1024).decode('utf-8')
    if hint is not None:
        print(hint)
    parts = message_received.split('-')
    if len(parts) < 4:
        print("��Ϣ��ʽ����ȷ��")
        return None
    message = '-'.join(parts[:-3])
    nonce = parts[-3]
    timestamp = parts[-2]
    received_hash = parts[-1]
    print(f"���յ�����Ϣ: {message}")
    print(f"���յ���ʱ���: {timestamp}")
    if not timestamp:
        print("ʱ��������ڻ��ʽ����")
        return None
    if nonce in used_nonces:
        print("Nonce�ѱ�ʹ�ù����������طŹ�����")
        return None
    hash_value = hashlib.sha256(f"{message}-{nonce}-{timestamp}".encode()).hexdigest()
    if hash_value != received_hash:
        print("��ϢժҪ��ƥ�䣬�����Ǳ��۸ĵ���Ϣ��")
        return None
    used_nonces[nonce] = True
    return message
def sendLegalInfoTo(theSocket, privatePemPath, publicPemPath):
    # ��Է������������У����Ϣ���кϷ�����֤
    LegalMessage = str(random.randint(2**31, 2**32))
    RSA_EncryptSignatureTo(theSocket, LegalMessage, privatePemPath, publicPemPath)
    # ���öԷ�RSA��Կ�����ɵ����������
    # Ȼ�����Լ���˽Կ��RSA���ĵ�SHA256ֵǩ��
    # ����ʱ�����ǩ����RSA���ķ���ȥ
def readLegalInfoFrom(theSocket, publicPemPath):
    # �ԶԷ������������Ϣ���кϷ���У��
    legal = RSA_VerifyFrom(theSocket, publicPemPath)
    # �յ��Է�ʱ���
    # �յ��Է�ǩ�����öԷ��Ĺ�Կ��ǩ���õ�ǩ���е�SHA256ֵ
    # ��һͬ������RSA���ģ�У����Ϣ����SHA256
    # �������SHA256ֵ�������֤�Է�Ϊ�Ϸ�
    return legal
    # �����Ƿ�Ϸ�
def RSA_EncryptSignatureTo(theSocket, RSA_DecryptText, privatePemPath, publicPemPath):
    # ����str���͵�RSA_DecryptText
    # ���öԷ���Կ���ܣ��ٶ����ĵ�SHA256ֵǩ��
    # �����ǩ������ܻᵼ�¼��ܵ�����̫�����޷����ܣ�����
    print()
    print('�����öԷ�RSA��Կ���ܣ�����ǰΪ��', RSA_DecryptText)
    RSA_EncryptText = str(RSA_SVED.rsa_encrypt(publicPemPath, RSA_DecryptText))
    # ���öԷ�RSA��Կ��������str��RSA����
    print('�����ñ���RSA˽Կ������Hashֵǩ��')
    RSA_Signature = RSA_SVED.rsa_sign(RSA_EncryptText, privatePemPath)
    # �ٶ�RSA����ǩ������bytes���͵�RSAǩ��
    sendTo(theSocket, RSA_EncryptText, '�ѷ���У����Ϣ��' + RSA_EncryptText)
    sendTo(theSocket, RSA_Signature, '�ѷ���RSAǩ����' + str(RSA_Signature))
    print()


def RSA_VerifyFrom(theSocket, publicPemPath):
    # ��ǩ
    print()
    RSA_EncryptText = readFrom(theSocket, '���յ�У����Ϣ')
    # str��У����Ϣ
    print('У����ϢΪ��', RSA_EncryptText)
    RSA_Signature = readFrom(theSocket, '���յ��Է���RSAǩ��').replace("b'", '').replace("'", '').encode('UTF-8')
    print('ǩ��Ϊ��', RSA_Signature)
    legal = RSA_SVED.rsa_verify(RSA_Signature, RSA_EncryptText, publicPemPath)
    print('�Է�����Ƿ�Ϸ���', legal)
    print()
    return legal, RSA_EncryptText
    # ����booleanֵ��ʾ�Ƿ�Ϸ���str�͵�У����Ϣ���� RSA����


def communicatePackageSender(theSocket, TDES_Key, privatePemPath, publicPemPath, TDES_DecryptText):
    # ��str�͵�ԭʼ����TDES_DecryptText����һϵ�в����󷢰�
    prpcryptObject = TDES.prpcrypt()
    # �½�TDES����
    TDES_EncryptText = TDES.DES_Encrypt(prpcryptObject, TDES_DecryptText, TDES_Key)
    # ����ԭʼ��������str�� TDES����
    RSA_EncryptSignatureTo(theSocket, TDES_EncryptText, privatePemPath, publicPemPath)
    # ��TDES�����öԷ���Կ���ܺ�ǩ������ͬУ����Ϣһ�����͸�������
    print()
    # ������һ�����ݰ�����
def communicatePackageReceiver(theSocket, TDES_Key, privatePemPath, publicPemPath):
    # ������նԷ�������ʱ�����ǩ����TDES����
    # ��ǩ������У�飬������ٽ���TDES����
    legalClient, RSA_DecryptText = RSA_VerifyFrom(theSocket, publicPemPath)
    # ����ֵΪboolean��ֵ�Ƿ�Ϸ���str��У����Ϣ
    RSA_DecryptText = RSA_DecryptText.replace("b'", '').replace("'", '')
    # ��Ϊstr�ͣ��淶������ʹ��rsa_decrypt()����
    if legalClient:
        # ����Է��Ϸ�������Ľ��н���
        TDES_EncryptText = str(RSA_SVED.rsa_decrypt(privatePemPath, RSA_DecryptText))
        # ���Լ���˽Կ����RSA���ĵõ�TDES����
        # ����bytes��TDES���ĺ�תΪstr
        TDES_EncryptText = str(TDES_EncryptText).replace("b'", '').replace("'", '')
        # str�ͣ���TDES���Ĺ淶������TDES_Decrypt()����
        prpcryptBob = TDES.prpcrypt()
        # �½�TDES����
        TDES_DecryptText = TDES.DES_Decrypt(prpcryptBob, TDES_EncryptText, TDES_Key)
        # ���ܵõ�str�͵�TDES����
        return TDES_DecryptText
        # ����str�͵�TDES����


def sendingThread(theSocket, TDES_Key, privatePemPath, publicPemPath):
    # ��ģ�����̵߳��õķ��ͺ���
    while True:
        TDES_DecryptText = input('����Ӣ�Ļ�����quit�������ͣ�')
        communicatePackageSender(theSocket, TDES_Key, privatePemPath, publicPemPath, TDES_DecryptText)
        if TDES_DecryptText == 'quit':
            # �����߳̽���
            print('�����߳̽���')
            print()
            break



def receivingThread(theSocket, TDES_Key, privatePemPath, publicPemPath):
    # ��ģ�����̵߳��õļ�������
    while True:
        TDES_DecryptText = communicatePackageReceiver(theSocket, TDES_Key, privatePemPath, publicPemPath)
        if TDES_DecryptText[0:5] == 'quit':
            # �����߳̽���
            print('�����߳̽���')
            print()
            break



