import datetime                         #for Gantt (time formatting) #duration is in days
import plotly                           #for Gantt (full package)
import plotly as py              #for Gantt
import plotly.figure_factory as ff      #for Gantt
import matplotlib as plt




# convert to date
serial = 43466.0 # 01.01.2019 Excel
seconds = (serial - 25569) * 86400.0 # convert to seconds
date_date = datetime.datetime.utcfromtimestamp(seconds)
date_string = date_date.strftime("%Y-%m-%d %H:%M:%S")

df = [dict(Task="machine_99", Start=0, Finish=1, Resource="job_99")]
df.clear()

start_value = 0 # in min
duration = 120  # in min

for i in range(1, 10):              
    b_dict = dict(Task="M " + str(i), Start=datetime.datetime.utcfromtimestamp((serial - 25569 + \
        (start_value/(60*24.0))) * 86400.0).strftime("%Y-%m-%d %H:%M:%S"), \
            Finish=datetime.datetime.utcfromtimestamp((serial - 25569 + \
                (start_value +duration)/(60*24.0)) * 86400.0).strftime("%Y-%m-%d %H:%M:%S"), Resource="job " + str(i))            
    df.append(b_dict)
    start_value = 10*i


fig = ff.create_gantt(df, index_col='Resource', show_colorbar=True, group_tasks=True)

plt(fig)



