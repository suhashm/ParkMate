import datetime, time
def get_unix_time(ctime):
    time_list = ctime.split()
    # convert to unix ctime 'Tue Sep 15 15:16:58 2015'

    # convert to ctime - this is for hourly analysis and hence ignoring
    time_list = time_list[ :-2]

    temp = time_list[-1]
    time_list[-1] = time_list[-2]
    time_list[-2] = temp

    new_time = " ".join(time_list)
    b = datetime.datetime.strptime(new_time, "%a %b %d %H:%M:%S %Y")
    formatted_time = ""
    formatted_time += str(b.year)+str(b.month).zfill(2)+str(b.day).zfill(2)+'-'+str(b.hour).zfill(2)+str(b.minute).zfill(2)+str(b.second).zfill(2)
    return formatted_time

print get_unix_time("Fri Sep 25 2015 06:13:28 GMT+0000 (UTC)")
