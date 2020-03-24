#------------------------------------------#
# Title: CD_Inventory.py
# Desc: The CD Inventory App main Module
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# DBiesinger, 2030-Jan-02, Extended functionality to add tracks
# jstevens, 2020-Mar-21, added sub menu to tracks and additional functionality
#------------------------------------------#

import ProcessingClasses as PC
import IOClasses as IO

CDFileName = 'AlbumInventory.txt'
TrackFileName = 'TrackInventory.txt'
lstFileNames = [CDFileName, TrackFileName]
#lstFileNames = ['AlbumInventory.txt', 'TrackInventory.txt']
lstOfCDObjects = IO.FileIO.load_inventory(lstFileNames)
if lstOfCDObjects == 1:
    print('Did not load a file, please save to start a new one! ')
    lstOfCDObjects = []
else:
    print('The following CDs have been loaded from ' + CDFileName +' and tracks from ' + TrackFileName)
    IO.ScreenIO.show_inventory(lstOfCDObjects) #show loaded inventory at start of script

while True:
    IO.ScreenIO.print_menu()
    strChoice = IO.ScreenIO.menu_choice()

    if strChoice == 'x':
        break
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            lstOfCDObjects = IO.FileIO.load_inventory(lstFileNames)
            IO.ScreenIO.show_inventory(lstOfCDObjects)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.ScreenIO.show_inventory(lstOfCDObjects)
        continue  # start loop back at top.
    elif strChoice == 'a':
        PC.DataProcessor.find_next_ID(lstOfCDObjects)
        cdId = IO.ScreenIO.get_CDId_info()
        usedid = PC.DataProcessor.check_ID(cdId, lstOfCDObjects)
        if usedid == True:
            print('That ID is already being used, Please try again!')
            continue
        tplCdInfo = IO.ScreenIO.get_CD_info(cdId)
        PC.DataProcessor.add_CD(tplCdInfo, lstOfCDObjects)
        IO.ScreenIO.show_inventory(lstOfCDObjects)
        continue  # start loop back at top.
    elif strChoice == 'd':
        IO.ScreenIO.show_inventory(lstOfCDObjects)
        continue  # start loop back at top.
    elif strChoice == 'c':
        IO.ScreenIO.show_inventory(lstOfCDObjects)
        cd_idx = IO.ScreenIO.get_input(int, 'Select the CD / Album index: ', 'Please enter an integer value')
        cdnum = PC.DataProcessor.select_cd(lstOfCDObjects, cd_idx)
        if cdnum == None:
            print('This CD / Album index does not exist')
            continue
        while True:
            IO.ScreenIO.print_CD_menu()
            strChoicecd = IO.ScreenIO.menu_CD_choice()
            if strChoicecd == 'x':
                break
            if strChoicecd == 'a':
                trackInfo = IO.ScreenIO.get_track_info()
                PC.DataProcessor.add_track(trackInfo, cdnum)
            elif strChoicecd == 'd':
                IO.ScreenIO.show_tracks(cdnum)
            elif strChoicecd == 'r':
                IO.ScreenIO.show_tracks(cdnum)
                #rem_trx = input('Select the Track to remove')
                rem_trx = IO.ScreenIO.get_input(int, 'Select the Track to remove: ', 'Please enter an integer value')
                delchk = PC.DataProcessor.del_track(rem_trx, cdnum)
                if delchk == None:
                    print('This track does not exist')
                    continue
            else:
                print('General Error')
    elif strChoice == 's':
        IO.ScreenIO.show_inventory(lstOfCDObjects)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        if strYesNo == 'y':
            IO.FileIO.save_inventory(lstFileNames, lstOfCDObjects)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    else:
        print('General Error')