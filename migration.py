if __name__ == '__main__':
    import os

    try:
        os.system('python3 manage.py makemigrations')
        print('==================== MAKE MIGRATIONS done ====================')
    except OSError:
        f'{OSError=}'

    try:
        os.system('python3 manage.py migrate')
        print('======================== MIGRATE done ========================')
    except OSError:
        f'{OSError=}'
