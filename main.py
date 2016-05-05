from decryptor import Decryptor

options = {
    'MAXLENGTH': 7,
    'UPPERCASE': True,
    'LOWERCASE': True,
    'SPACE': True,
    'NUMBERS': True,
    'SPECIALCHARS': True
}
machine = Decryptor('28aa2fd1fa0e2e87549a81f8196c4919869e8c7c', options) # hash of password: A7B§

machine.decrypt()
