def user_input(prompt:str, default:str="", required:bool=True):
    full_promt = f"{prompt}: "
    if default:
        full_promt = f"{prompt} (Default: {default}): "
    while True:
        value = input(full_promt) or default
        if value != "" or required is False:
            return value
        print(f"{prompt} is required and cannot be empty.")

manufacturer = user_input(prompt="Manufacturer", default="Orics", required=True)
owner = user_input(prompt="Owner", default="", required=True)
serial = user_input(prompt="Serial Number", default="", required=True)
machine = user_input(prompt="Machine", default="", required=True)
location = user_input(prompt="Location", default="", required=False)


policy = {
   "machine": {
       "owner": owner,
       "manufacturer": manufacturer,
       "machine": machine,
       "serial_number": serial
    }
}

print(policy)