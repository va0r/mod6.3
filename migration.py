if __name__ == '__main__':
    import os

    try:
        print('==================== MAKE MIGRATIONS ====================')
        os.system('python3 manage.py makemigrations')
    except OSError:
        f'{OSError=}'

    try:
        print('======================== MIGRATE ========================')
        os.system('python3 manage.py migrate')
    except OSError:
        f'{OSError=}'
