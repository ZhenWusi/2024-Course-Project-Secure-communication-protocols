# coding:gbk
"""
@Time �� ${2024��6��} 15:57
@Auth �� ������
"""
# coding:gbk
'''
RSA�ӽ������ɣ����γ���Ƽӽ��ܺ�ǩ����֤��Կһ��
'''
from Crypto import Random
from Crypto.PublicKey import RSA
def generate_and_store_keys(identity):
    random_generator = Random.new().read
    # �����������
    # ��������RSA���ܵĹ�˽Կ��
    rsa_encryption = RSA.generate(2048, random_generator)
    private_pem_encryption = rsa_encryption.exportKey()
    public_pem_encryption = rsa_encryption.publickey().exportKey()
    with open(f'RSA_Private{identity}.pem', 'wb') as f:
        f.write(private_pem_encryption)
    with open(f'RSA_Public{identity}.pem', 'wb') as f:
        f.write(public_pem_encryption)
# ����Alice�Ĺ�˽Կ��
generate_and_store_keys('Alice')
# ����Bob�Ĺ�˽Կ��
generate_and_store_keys('Bob')
