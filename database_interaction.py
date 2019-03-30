import subprocess

def get_database_connection():
    import mysql.connector as mariadb

    db_connection = mariadb.connect(user='kbhffdk', password='localpass', \
            database='kbhff_dk', port="54321")
    return db_connection

def get_php_password_hash(plaintext_password):
    '''Generate hash of plaintext password in php, return the hash.
    Make sure "password_hash.php" contains the hashing algorithm used in the application.'''
    result = subprocess.run(
            ["php", "password_hash.php", plaintext_password],
            stdout = subprocess.PIPE,
            check = True
            )
    return result.stdout.decode("UTF-8")

def get_password_reset_token_by_userid(user_id, cursor):
    cursor.execute("SELECT token FROM user_password_reset_tokens WHERE user_id=%s", (user_id,))
    reset_token = cursor.fetchone()
    if reset_token is not None:
        reset_token = reset_token[0]
    return reset_token

def get_password_hash_by_userid(user_id, cursor):
    cursor.execute("SELECT password FROM user_passwords WHERE user_id=%s", (user_id,))
    password_hash =  cursor.fetchone()
    if password_hash is not None:
        password_hash = password_hash[0]
    return password_hash

