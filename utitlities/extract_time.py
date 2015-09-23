# import datetime
# a = 'Tue Sep 15 2015 18:12:33 GMT+0000 (UTC)'
# print "original time: {}".format(a)
# time_list = a.split()
# # ctime 'Tue Sep 15 15:16:58 2015'
#
# # convert to ctime
# time_list = time_list[ :-2]
#
# temp = time_list[-1]
# time_list[-1] = time_list[-2]
# time_list[-2] = temp
#
# new_time = " ".join(time_list)
# b = datetime.datetime.strptime(new_time, "%a %b %d %H:%M:%S %Y")
#
# formatted_time = ""
# formatted_time += str(b.year)+str(b.month)+str(b.day)+str(b.hour)
# print formatted_time

import datetime
def get_unix_time(ctime):
    time_list = ctime.split()
    # ctime 'Tue Sep 15 15:16:58 2015'

    # convert to ctime
    time_list = time_list[ :-2]

    temp = time_list[-1]
    time_list[-1] = time_list[-2]
    time_list[-2] = temp

    new_time = " ".join(time_list)
    b = datetime.datetime.strptime(new_time, "%a %b %d %H:%M:%S %Y")
    formatted_time = ""
    formatted_time += str(b.year)+str(b.month)+str(b.day)+str(b.hour)
    return formatted_time
