from urllib.request import urlopen
import json
response = urlopen('https://api.openf1.org/v1/meetings?meeting_key=latest')
meeting=json.loads(response.read().decode('utf-8'))[0]
print(meeting)

# def minsec(secs):
#     first=secs//60
#     last=secs-(first*60)
#     final=str(first) + ":" + str(last)
#     return final

# def race(session):
#     time = 0
#     response = urlopen('https://api.openf1.org/v1/sessions?session_key=' + str(session))
#     sessiondata = json.loads(response.read().decode('utf-8'))[0]
#     base = sessiondata["date_start"]
#     print(sessiondata)
#     response = urlopen('https://api.openf1.org/v1/position?session_key=' + str(session) + '&position=1')
#     poledriver = json.loads(response.read().decode('utf-8'))[0]
#     print(poledriver)
#     # response = urlopen('https://api.openf1.org/v1/location?session_key=' + str(session) + '&driver_number=' + poledriver + '&date=' + base + '00:00')
#     # polelocation = json.loads(response.read().decode('utf-8'))[0]
#     # xoffset=0-polelocation['x']
#     # yoffset=0-polelocation['y']
#     # print(xoffset)
#     # print(yoffset)

# race(9189)

# # from matplotlib import pyplot as plt
# # import fastf1
# # import fastf1.plotting

# # fastf1.plotting.setup_mpl()

# # session = fastf1.get_session(2019, 'Monza', 'Q')

# # session.load()
# # fast_leclerc = session.laps.pick_driver('LEC').pick_fastest()
# # lec_car_data = fast_leclerc.get_car_data()
# # t = lec_car_data['Time']
# # vCar = lec_car_data['Speed']

# # # The rest is just plotting
# # fig, ax = plt.subplots()
# # ax.plot(t, vCar, label='Fast')
# # ax.set_xlabel('Time')
# # ax.set_ylabel('Speed [Km/h]')
# # ax.set_title('Leclerc is')
# # ax.legend()
# # plt.show()