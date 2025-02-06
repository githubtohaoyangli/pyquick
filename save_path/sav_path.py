import os
def save_path(path,filename,write_mode,writein):
    try:
        with open(os.path.join(path,filename),write_mode) as f:
            if write_mode == 'w' or write_mode == 'a' or write_mode == 'w+' or write_mode == 'a+':
                f.write(str(writein))
            else:
                return 0
    except FileNotFoundError:
        raise FileNotFoundError
    except Exception:
        raise Exception
def read_path(path,filename,read_mode):
    try:
        with open(os.path.join(path,filename),"r") as r:
            if read_mode == 'read':
                return r.read()
            elif read_mode == 'readlines':
                return r.readlines()
            elif read_mode=='readline':
                return r.readline()
            else:
                return 0
    except FileNotFoundError:
        raise FileNotFoundError
    except Exception:
        raise Exception
        