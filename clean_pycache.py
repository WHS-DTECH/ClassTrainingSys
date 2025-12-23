import os

for root, dirs, files in os.walk('.'):
    for d in dirs:
        if d == '__pycache__':
            pycache_path = os.path.join(root, d)
            print(f'Removing {pycache_path}')
            try:
                import shutil
                shutil.rmtree(pycache_path)
            except Exception as e:
                print(f'Error removing {pycache_path}: {e}')
    for f in files:
        if f.endswith('.pyc'):
            pyc_path = os.path.join(root, f)
            print(f'Removing {pyc_path}')
            try:
                os.remove(pyc_path)
            except Exception as e:
                print(f'Error removing {pyc_path}: {e}')
