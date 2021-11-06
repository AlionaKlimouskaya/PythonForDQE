def input_type_validation():
    raw_input_type = int(input('Select input type:\n1 - Input\n2 - Get from file\n3 - Exit\n'))
    while raw_input_type not in [1, 2, 3]:
        print("The options can be 1, 2, or 3 only.")
        raw_input_type = int(input('Select input type:\n1 - Input\n2 - Get from file\n3 - Exit\n'))
    return raw_input_type


def process_custom_folder(folder_type_choice, processor_type):
    if folder_type_choice == 2:
        user_folder = input('Enter the full path to folder like C:\\ : ')
        processor_type(default_folder=user_folder).write_from_file()
    elif folder_type_choice == 1:
        processor_type().write_from_file()
    else:
        print('Not implemented')
