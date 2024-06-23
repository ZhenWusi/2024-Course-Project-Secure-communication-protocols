# coding:gbk
"""
@Time �� ${2024��6��} 15:57
@Auth �� ������
"""
# coding:gbk
# ��������Ŀ�
from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Cipher import PKCS1_v1_5 as ED_PKCS1_v1_5
from Crypto.Hash import SHA256
import base64

# RSASSA-PSS ǩ������
# PSS (Probabilistic Signature Scheme) ��һ�ֻ��� RSA ��ǩ��������ͨ������Ϊ�ȴ�ͳ�� PKCS#1 v1.5 ǩ���������Ӱ�ȫ��
# ��������һ��������ķ�ʽ������ǩ����������ǩ���Ĳ���Ԥ���ԺͰ�ȫ�ԡ�
# ����ԣ�PSS ������ǩ��ʱ���������ֵ��ʹ�ü�ʹͬһ��Ϣ���ǩ�������ɵ�ǩ��Ҳ��ͬ���������������˰�ȫ�ԣ���ֹ��һЩ����������
# ��Ϣ��չ��PSS ʹ����һ����ϣ�������� SHA-256������Ϣ������չ��Ȼ�����չ�����Ϣ����ǩ����
def rsa_sign(data, privatePemPath):
    """
    ʹ�� RSA ˽Կ�����ݽ���ǩ��
    :param data: ��Ҫǩ��������
    :param privatePemPath: RSA ˽Կ���ļ�·��
    :return: base64 �����ǩ��
    """
    try:
        # ��ȡ˽Կ�ļ�
        with open(privatePemPath, 'rb') as private_key_file:
            pri_key = RSA.import_key(private_key_file.read())  # ����˽Կ
            signer = pss.new(pri_key)  # ���� PSS ǩ������
            hash_obj = SHA256.new(data.encode('utf-8'))  # �������ݵ� SHA256 ��ϣֵ
            signature = base64.b64encode(signer.sign(hash_obj))  # ʹ��˽Կ�Թ�ϣֵ����ǩ�������� base64 ����
            return signature
    except Exception as e:
        print('ǩ��ʧ��:', e)
        return None

def rsa_verify(signature, data, publicPemPath):
    """
    ʹ�� RSA ��Կ��֤ǩ��
    :param signature: base64 �����ǩ��
    :param data: ԭʼ����
    :param publicPemPath: RSA ��Կ���ļ�·��
    :return: ǩ����֤�����True ��ʾ��֤ͨ����False ��ʾ��֤ʧ��
    """
    try:
        # ��ȡ��Կ�ļ�
        with open(publicPemPath, 'rb') as public_key_file:
            pub_key = RSA.import_key(public_key_file.read())  # ���빫Կ
            hash_obj = SHA256.new(data.encode('utf-8'))  # �������ݵ� SHA256 ��ϣֵ
            verifier = pss.new(pub_key)  # ���� PSS ��֤����
            verifier.verify(hash_obj, base64.b64decode(signature))  # ʹ�ù�Կ��֤ǩ��
            return True
    except (ValueError, TypeError) as e:
        print('��ǩʧ��:', e)
        return False
# PKCS#1 v1.5��һ�־���� RSA ���ܺ�ǩ����䷽��,�������ô�ʵ�ּӽ���
def rsa_encrypt(publicPemPath, RSA_DecryptText):
    """
    ʹ�� RSA ��Կ�����ݽ��м���
    :param publicPemPath: RSA ��Կ���ļ�·��
    :param RSA_DecryptText: ��Ҫ���ܵ�����
    :return: base64 ����ļ�������
    """
    with open(publicPemPath, 'r') as f:
        key = f.read()  # ��ȡ��Կ�ļ�����
        rsakey = RSA.import_key(key)  # ���빫Կ
        cipher = ED_PKCS1_v1_5.new(rsakey)  # ���� PKCS1_v1_5 ���ܶ���
        RSA_EncrptText = base64.b64encode(cipher.encrypt(RSA_DecryptText.encode('utf-8')))  # ʹ�ù�Կ�������ݲ����� base64 ����
    return RSA_EncrptText

def rsa_decrypt(privatePemPath, RSA_EncrptText):
    """
    ʹ�� RSA ˽Կ�����ݽ��н���
    :param privatePemPath: RSA ˽Կ���ļ�·��
    :param RSA_EncrptText: base64 ����ļ�������
    :return: ���ܺ��ԭʼ����
    """
    with open(privatePemPath, 'r') as f:
        key = f.read()  # ��ȡ˽Կ�ļ�����
        rsakey = RSA.import_key(key)  # ����˽Կ
        cipher = ED_PKCS1_v1_5.new(rsakey)  # ���� PKCS1_v1_5 ���ܶ���
        RSA_DecryptText = cipher.decrypt(base64.b64decode(RSA_EncrptText), "ERROR")  # ʹ��˽Կ��������
    return RSA_DecryptText
