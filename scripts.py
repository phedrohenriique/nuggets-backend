import hashlib as hs

## test file for functions and other features
## create functions and isolate the code in them
## you can import files variables and functions in order to use them


########################################

def hash_test():
    variable_stringed = "777".encode()

    hash = hs.sha256(variable_stringed).hexdigest()
    print(hash)

    if hash == hs.sha256(variable_stringed).hexdigest():
        print("its equal")

########################################

########################################

## __main__ variable is the file being executed, if the executed file is
## the one with the file __name__ the statemns shall be done

if __name__ == "__main__":
    print('this')

########################################