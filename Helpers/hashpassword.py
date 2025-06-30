import bcrypt

def hash_password(plain_password):
    # bcrypt expects bytes, so encode the string first
    password_bytes = plain_password.encode('utf-8')
    # Generate salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Return hashed password as a utf-8 string
    return hashed.decode('utf-8')

# Example usage:
host_password = hash_password('hostpassword123')
performer_password = hash_password('performerpassword123')

print("Host hashed password:", host_password)
print("Performer hashed password:", performer_password)
