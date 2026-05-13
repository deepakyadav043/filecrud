### project -->> CURD OPERATION

from pathlib import Path 
import os

def readfileandfolder():
    try:
        p = Path('')
        items = list(p.rglob('*'))
        for index ,file in enumerate(items):
            print(f'{index+1} - {file}')
    except Exception as e:
        print(e)


def create_file():
    try:

        readfileandfolder()
    # C:\Users\HP\Desktop\file handling\hello.txt
        file_name = input('enter name of your file:')
        p = Path(file_name)
        if p.exists():
            print('FILE ALREADY EXISTS')
        else:
            with open(file_name,'w') as file:
                content = input('enter your file content:')
                file.write(content)
                print('FILE ADDED !')
    except Exception as e:
            print(e)
            pass

def read_file():
    try:

        readfileandfolder()
        file_name = input('enter your name of your file:')
        p = Path(file_name)
        if p.exists():
            with open(file_name,'r') as file:
                print(file.read())
        else:
            print('FILE NOT FOUND!')
    except Exception as e:
        print(e)

def update_file():
    try:

        readfileandfolder()
        file_name = input('enter your name of file to update')
        p = Path(file_name)
        if p.exists():
            print('press 1 to overwrite the content')
            print('press 2 to append the content')
            option = int(input('enter your choice for updating a file:'))
            if option == 1:
                  with open(file_name,'w') as file:
                    content = input('enter content to update')
                    file.write(content)
                    print('CONTENT CHANGED')
                    pass
            elif option == 2:
                with open(file_name,'a') as file:
                    content = input('enter content to update')
                    file.write(content)
                    print('FILE UPDATED SUCCECCFULLY')

            else:
                print('invalid input')
        else:
             with open(file_name,'w') as file:
                content = input('enter your file content:')
                file.write(content)
                print('FILE ADDED !')
            #print('FILE NOT EXISTS!')

        #     with open(file_name,'a') as file:
        #         content = input('enter content to update')
        #         file.write(content)
        #         print('FILE UPDATED SUCCECCFULLY')
        # else:
        #     print('file not found!')
    except Exception as e:
        print(e)

def delete_file():
    try:
         
    #import OS ## OPERATING SYSTEM
        readfileandfolder()
        file_name = input('enter your name of file :')
        p = Path(file_name)
        if p.exists():
            os.remove(p) ## os is removing path of that file completely from that system
            print('FILE DELETED')
        else:
            print("FILE DOES NOT EXIST")
    except Exception as e:
        print(e)

def rename_file():
    try:

        readfileandfolder()
        file_name = input('enter name of your file:')
        p = Path(file_name)
        if p.exists():
            new_file = input('enter the name of your file:')
            p.rename(new_file)
            print('FILE RENAMED!')
        else:
            print('FILE NOT FOUND!')
    except Exception as e:
        print(e)

def create_folder():
    try:

        readfileandfolder()
        folder_name = input('Enter name of your folder:')
        p = Path(folder_name)
        if p.exists():
            print('FOLDER ALREADY EXIST')
        else:
            p.mkdir()
            print('FOLDER CREATED!')
    except Exception as e:
        print(e)

def delete_folder():
    try:

        readfileandfolder()
        folder_name = input  ("enter the name of your folder:")
        p = Path(folder_name)
        if p.exists():
            p.rmdir()
            print("FOLDER DELETED!")
        else:
            print("folder not found")
    except Exception as e:
        print(e)

def create_file_in_folder():
    try:
        readfileandfolder()
        folder_name = input("enter name of your folder")
        file_name = input('enter the name of your file')
        p = Path(folder_name) / file_name
        if p.exists():
            print("File already existed")
        else:
            p.mkdir()
            print("created successfully")
            with open(file_name,'w') as file:
                content = input('enter your file content:')
                file.write(content)
            print("created successfully")
    except Exception as e:
        print(e)
        



while True:
    print("press 1 for creating a file")
    print("press 2 for reading a file ")
    print("press 3 for updating a file")
    print("press 4 for deleting a file")
    print('press 5 for renaming a file')
    print("press 6 for creating a folder")
    print("press 7 for deleting a folder")
    print("press 8 for creating file and folder")
    print('press 0 for exiting........')



    option = int (input("enter your choice:"))
    if option == 1:
        create_file()
    elif option == 2:
        read_file()
    elif option == 3:
        update_file()

    elif option == 4:
        delete_file()
    
    elif option == 5:
        rename_file()
    elif option == 6:
        create_folder()

    elif option == 7:        
        delete_folder()

    elif option == 8:
        create_file_in_folder()


    elif option == 0:
        break
    
#### important note :-- if two or more if , else condition come in our code then it is said to be ladder
