#------------------------------------------#
# Title: Processing Classes
# Desc: A Module for processing Classes
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# DBiesinger, 2030-Jan-02, Extended functionality to add tracks
# jstevens, 2020-Mar-21, added additional methods
#------------------------------------------#

if __name__ == '__main__':
    raise Exception('This file is not meant to ran by itself')

import DataClasses as DC

class DataProcessor:
    """Processing the data in the application"""

    @staticmethod
    def add_CD(CDInfo, table):
        """function to add CD info in CDinfo to the inventory table.


        Args:
            CDInfo (tuple): Holds information (ID, CD Title, CD Artist) to be added to inventory.
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """

        cdId, title, artist = CDInfo
        try:
            cdId = int(cdId)
        except:
            raise Exception('ID must be an Integer!')
        row = DC.CD(cdId, title, artist)
        table.append(row)

    @staticmethod
    def select_cd(table: list, cd_idx: int) -> DC.CD:
        """selects a CD object out of table that has the ID cd_idx

        Args:
            table (list): Inventory list of CD objects.
            cd_idx (int): id of CD object to return

        Raises:
             Exception: DESCraised in case position is not an integer.

        Returns:
            row (DC.CD): CD object that matches cd_idx, if no match returns None

        """
        try:
            cd_idx = int(cd_idx)
        except:
            raise Exception('ID must be an Integer!')
        for row in table:
            if row.cd_id == cd_idx:
               return row
    
    @staticmethod
    def add_track(track_info: tuple, cd: DC.CD) -> None:
        """adds a Track object with attributes in track_info to cd


        Args:
            track_info (tuple): Tuple containing track info (position, title, Length).
            cd (DC.CD): cd object the track gets added to.

        Raises:
            Exception: DESCraised in case position is not an integer.

        Returns:
            None: DESCRIPTION.

        """
        trkPos, trkTitle, trkLength = track_info
        try:
            trkPos = int(trkPos)
        except:
            raise Exception('Position must be an Integer!')
        track = DC.Track(trkPos, trkTitle, trkLength)
        cd.add_track(track)

    @staticmethod
    def del_track(rem_track: int, cd: DC.CD) -> None:
        """Deletes a Track for the list of cd_tracks


        Args:
            rem_track (int): Position of the track to be deleted.
            cd (DC.CD): cd object the track gets deleted from.

        Raises:
            Exception: DESCraised in case position is not an integer.

        Returns:
            track (string): Track string that matches rem_track, if no match returns None

        """
        tracks = cd.cd_tracks
        try:
            rem_track = int(rem_track)
        except:
            raise Exception('Track must be an Integer!')
        for track in tracks:
            if (track is not None):
                if track.position == rem_track:
                    cd.rmv_track(rem_track)
                    print('Track was removed!')
                    return track

    @staticmethod
    def find_next_ID (table):
        """Function to find the next available ID number

        Takes the table and looks for the next ID number that has not been used by matching the ID value of each CDObject starting at 1 and ascending until no match is found

        Args:
            table (list of CDObjects): 2D data structure (list of CDObjects) that holds the data during runtime

        Returns:
            next_ID (int): Returns the number of the next available ID
        """
        next_ID = 1
        used_id = [cd.cd_id for cd in table]
        while next_ID in used_id:
            next_ID += 1
        print('The next available ID is: ' + str(next_ID))
        return next_ID

    @staticmethod
    def check_ID (idnf, table):
        """Function to check if the user entered ID has been used 

        Takes the user entered ID number and the table and looks in the ID value to see if it has been used before in any of the dict in the table

        Args:
            idnf (int): ID number of the CD to be checked, entered by user
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            usedid (boolean): Returns True if the ID of the CD was matched or False if it was not matched
        """
        if any(row.cd_id == int(idnf) for row in table):
            usedid = True       
        else:
            usedid = False     
        return usedid


