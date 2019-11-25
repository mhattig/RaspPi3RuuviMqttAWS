'''
Manage the size of the RuuviSensors.json file. If the used file
system gets to greater than 50%, then RuuviSensors.json is reduced
so that only 25% is used. The older data in RuuviSensors.json 
is removed.
'''
import os
import config  # all config parameters are in this file.

logging = config.logging

'''
When the high water percentage of disk usage is exceeded, then return the number of 
bytes to get the disk usage down to the low water percentage.
'''
def byte_count_to_reduce(low_water_percent=40, high_water_percent=50):

    disk = os.statvfs('/')
    total_blocks = disk.f_blocks # Total number of blocks in the filesystem.
    free_blocks = disk.f_bavail # Free blocks available to non-super user.
    block_size = disk.f_frsize  # Fundamental file system block size.
    reduce_byte_count = 0

    percent = int(((total_blocks - free_blocks)/total_blocks) * 100)

    if logging:
        print('current disk usage = {}%'.format(percent))

    if percent > high_water_percent:
        delta_percent = percent - low_water_percent
        reduce_block_count = int((delta_percent * total_blocks)/100)
        reduce_byte_count = reduce_block_count * block_size
        if logging:
            print('Reducing file size.')
            print('Byte reduction = {} bytes. Disk reduction {}%.'.\
                format(reduce_block_count, delta_percent))

    return reduce_byte_count

'''
Reduce the file size by bytecount.
'''
def reduce_file(in_filename, bytecount):
    if bytecount:
        temp_filename = 'temp.txt'
        with open(in_filename, 'rb') as inFile:
            inFile.seek(bytecount)
            with open(temp_filename, 'wb') as outFile:
                for chunk in iter(lambda: inFile.read(20000), b''):
                    outFile.write(chunk)
        os.remove(in_filename)
        os.rename(temp_filename, in_filename)

'''
Manage a file's size relateive to the entire disk space avaialable.
Remove older data in the file when file is too large.
'''
def manage_file_size(filename):
    byte_count = byte_count_to_reduce()
    if byte_count:
        reduce_file(filename, bytecount)

'''
Test byte_count_to_reduce() on PC before loading on RP3. 
Go find current disk size and disk utilization, then plug into variables.
'''
def test_rbc(low, high):
    gig_count = int(byte_count_to_reduce(low_water_percent=low, high_water_percent=high)/1000000000)

    my_disk_utilization = 25    # my disk is 69% full
    my_disk_space = 32         # my disk size is 250GB

    if high < my_disk_utilization:
        actual_gig = int(my_disk_space * ((my_disk_utilization - low)/100))
    else :
        actual_gig = 0

    # Print calculated and actual values then compare
    print('{} {} = {},{}'.format(low, high, gig_count, actual_gig))

'''
Use main to for test.
'''
def main():

    if False :
        print('Test byte_count_to_reduce()')
        test_rbc(10, 20) 
        test_rbc(10, 30) 
        test_rbc(10, 40) 
        test_rbc(10, 50) 
        test_rbc(10, 60) 
        test_rbc(10, 70) 

        test_rbc(50, 55) 
        test_rbc(50, 60) 
        test_rbc(50, 65) 
        test_rbc(50, 70) 

    if False:
        # test.txt created by gen_text.py.
        # test.txt has timestamps on every line
        # manually examine final file to verify oldest data removed
        print('Test file reduction with a large test file named test.txt')
        os.system('ls -l test.txt')
        for i in range(5):
            reduce_file('test.txt', 2000)
            os.system('ls -l test.txt')

if __name__ == "__main__":
    main()
