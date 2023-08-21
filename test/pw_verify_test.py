from rubatochat.api.v1.auth import encrypt_password, verify_password

_password = "abcd"
print(verify_password(_password,encrypt_password(_password)))