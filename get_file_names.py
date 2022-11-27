import os 
import shutil
target_dir = 'C:/Users/Mohammed Hager/Documents/Python_Analytics/top_100/'
source = 'C:/Users/Mohammed Hager/Documents/Python_Analytics/real/'
# file_names = os.listdir(target_dir)
# arr = []
# for file_name in file_names:
#     arr.append(int(file_name.split(".")[0]))
# print((sorted(arr)))

number_list = [91, 117, 184, 195, 200, 203, 207, 208, 209, 210, 223, 240, 289, 307, 311, 313, 322, 324, 329, 330, 334, 352, 358, 367, 382, 385, 394, 398, 402, 411, 416, 417, 427, 430, 433, 451, 
461, 462, 469, 474, 488, 508, 512, 528, 529, 533, 535, 539, 542, 544, 546, 549, 555, 557, 559, 563, 571, 573, 576, 579, 583, 590, 592, 594, 595, 600, 604, 609, 613, 617, 618, 626, 
627, 634, 636, 637, 644, 645, 647, 648, 650, 652, 653, 658, 659, 660, 663, 666, 668, 669, 670, 674, 675, 677, 682, 692, 693, 695, 696, 697]

file_names = os.listdir(target_dir)
for file_name in file_names:
    one = target_dir+file_name
    name = int(file_name.split(".")[0])
    two = source + str(number_list.index(name))+".txt"
    shutil.copyfile(one, two )
