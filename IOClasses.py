#------------------------------------------#
# Title: IO Classes
# Desc: A Module for IO Classes
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# DBiesinger, 2030-Jan-02, Extended functionality to add tracks
# jstevens, 2020-Mar-21, added additional functionality and methods
#------------------------------------------#

if __name__ == '__main__':
    raise Exception('This file is not meant to run by itself')

import DataClasses as DC
import ProcessingClasses as PC

class FileIO:
    """Processes data to and from file:

    properties:

    methods:
        save_inventory(file_name, lst_Inventory): -> None
        load_inventory(file_name): -> (a list of CD objects)

    """
    @staticmethod
    def save_inventory(file_name: list, lst_Inventory: list) -> None:
        """Saves list of CD Objects to a file and saves list of tracks to a file


        Args:
            file_name (list): list of file names [CD Inventory, Track Inventory] that hold the data.
            lst_Inventory (list): list of CD objects.

        Returns:
            None.

        """
        file_name_CD = file_name[0] 
        file_name_track = file_name[1]
        try:
            with open(file_name_CD, 'w') as file:
                for disc in lst_Inventory:
                    file.write(disc.get_record())
            with open(file_name_track, 'w') as file:
                for disc in lst_Inventory: 
                    tracks = disc.cd_tracks
                    disc_id = disc.cd_id
                    for track in tracks:
                        if track is not None:
                            record = '{},{}'.format(disc_id, track.get_record()) 
                            file.write(record)
        except Exception as e:
            print('There was a general error!', e, e.__doc__, type(e), sep='\n')

    @staticmethod
    def load_inventory(file_name: list) -> list:
        """Loads CD information into a list of CD Objects and loads track information into a list of tracks


        Args:
            file_name (list): list of file names [CD Inventory, Track Inventory] that hold the data.

        Returns:
            list: list of CD objects.

        """
        lst_Inventory = []
        file_name_CD = file_name[0] 
        file_name_track = file_name[1]
        while True:
            try:
                open(file_name_CD, 'r')
                open(file_name_track, 'r') 
            except OSError as e:
                print('The file AlbumInventory.txt or TrackInventory.txt was not found, Please make sure the files are in the correct path.', e)
                userexit = (input ("If you want to load the files, please put them in the correct path and press enter, type 'continue' to start without loading files or to start a new file, type 'exit' to not load anything\n"))
                if userexit.lower() == 'exit':
                    print('Goodbye!')
                    quit()
                elif userexit.lower() == 'continue':
                    print("Not loading a file, Plese save to make a new one!")
                    print()
                    newfile = 1
                    return newfile
                else: 
                    print("Attepting to load the file!")
                    print()
                    continue
            else:
                try:
                    with open(file_name_CD, 'r') as file:
                        for line in file:
                            data = line.strip().split(',')
                            row = DC.CD(data[0], data[1], data[2])
                            lst_Inventory.append(row)
                    with open(file_name_track, 'r') as file:
                        for line in file:
                            data = line.strip().split(',')
                            cd = PC.DataProcessor.select_cd(lst_Inventory, int(data[0]))
                            if cd == None:
                                print('Some tracks have no CD Information')
                                print(data)
                            else:
                                track = DC.Track(int(data[1]), data[2], data[3])
                                cd.add_track(track)
                except Exception as e:
                    print('There was a general error!', e, e.__doc__, type(e), sep='\n')
                return lst_Inventory

class ScreenIO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Main Menu\n\n[l] load Inventory from file\n[a] Add CD / Album\n[d] Display Current Inventory')
        print('[c] Choose CD / Album\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, d, c, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'd', 'c', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, d, c, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def print_CD_menu():
        """Displays a sub menu of choices for CD / Album to the user

        Args:
            None.

        Returns:
            None.
        """

        print('CD Sub Menu\n\n[a] Add track\n[d] Display cd / Album details\n[r] Remove track\n[x] exit to Main Menu')

    @staticmethod
    def menu_CD_choice():
        """Gets user input for CD sub menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices a, d, r or x

        """
        choice = ' '
        while choice not in ['a', 'd', 'r', 'x']:
            choice = input('Which operation would you like to perform? [a, d, r or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print(row)
        print('======================================')

    @staticmethod
    def show_tracks(cd):
        """Displays the Tracks on a CD / Album

        Args:
            cd (CD): CD object.

        Returns:
            None.

        """
        print('====== Current CD / Album: ======')
        print(cd)
        print('=================================')
        print(cd.get_tracks())
        print('=================================')

    @staticmethod
    def get_CD_info(cdIdi):
        """function to request CD information from User to add CD to inventory

        Args:
            cdIdi (int): ID of the CD to be used

        Returns:
            cdId (string): Holds the ID of the CD dataset.
            cdTitle (string): Holds the title of the CD.
            cdArtist (string): Holds the artist of the CD.

        """
        cdId = cdIdi
        cdTitle = ScreenIO.get_input(str, 'What is the CD\'s title? ', 'Please enter an string value')
        cdArtist = ScreenIO.get_input(str, 'What is the Artist\'s name? ', 'Please enter an string value')
        return cdId, cdTitle, cdArtist

    @staticmethod
    def get_track_info():
        """function to request Track information from User to add Track to CD / Album


        Returns:
            trkId (string): Holds the ID of the Track dataset.
            trkTitle (string): Holds the title of the Track.
            trkLength (string): Holds the length (time) of the Track.

        """
        trkId = ScreenIO.get_input(int, 'Enter Position on CD / Album: ', 'Please enter an integer value')
        trkTitle = ScreenIO.get_input(str, 'What is the Track\'s title? ', 'Please enter an string value')
        trkLength = ScreenIO.get_input(str, 'What is the Track\'s length? ', 'Please enter an string value')
        return trkId, trkTitle, trkLength

    @staticmethod
    def get_input(value_type, input_message, error_message):
        """ Prompts the user for a value of specified type and returns

        Args:
            value_type (type): Requested data type (int, str, float...)
            input_message (str): Message displayed to the user via input() prompting for data
            error_message (str): Message displayed to the user if an incorrect data type is entered.

        Returns:
            new_value (value_type): Data of the requested type provided by the user
        
        """
        while True:
            try:
                new_value = value_type(input(input_message).strip())
                return new_value
            except ValueError:
                print(error_message)

    @staticmethod
    def get_CDId_info():
        """fuction that gets user input for the CD ID.

        Args:
            None.

        Returns:
            cdId (string)   

        """
        cdId = ScreenIO.get_input(int, 'Enter ID: ', 'Please enter an integer value')
        return cdId
            
                    

        