import requests as req
import json


API_KEY='''978d8d40e1cf0a3f95cd1e227858daaf'''



# phnom_penh = req.get(f'http://api.openweathermap.org/data/2.5/weather?q=phnom penh&appid={API_KEY}').json()

# print(phnom_penh)

# siem_reap = req.get(f'http://api.openweathermap.org/data/2.5/weather?q=siem reap&appid={API_KEY}').json()

# print(siem_reap)

conversion_factor={
    'pm2_5':1,
    'pm10':1,
    'o3':1.96,
    'no2':1.88,
    'so2':2.62,
    'co':1.15*1000,
    'nh3':0.7,
    'aqi':1
}

breakpoint={
    'pm2_5':{

        'good': [0, 12],
        'moderate': [12.1, 35.4],
        'unhealthy for sensitive groups': [35.5, 55.4],
        'unhealthy': [55.5, 150.4],
        'very unhealthy': [150.5, 250.4],
        'hazardous': [250.5, 500.4],

    },
    'pm10':{

        'good': [0, 54],
        'moderate': [55, 154],
        'unhealthy for sensitive groups': [155, 254],
        'unhealthy': [255, 354],
        'very unhealthy': [355, 424],
        'hazardous': [425, 604],

    },
    'o3':{

        'good': [0, 54],
        'moderate': [55, 70],
        'unhealthy for sensitive groups': [71, 85],
        'unhealthy': [86, 105],
        'very unhealthy': [106, 200],
        'hazardous': [201, 604],

    },
    'no2':{

        'good': [0, 53],
        'moderate': [54, 100],
        'unhealthy for sensitive groups': [101, 360],
        'unhealthy': [361, 649],
        'very unhealthy': [650, 1249],
        'hazardous': [1250, 2049],

    },
    'so2':{

        'good': [0, 35],
        'moderate': [36, 75],
        'unhealthy for sensitive groups': [76, 185],
        'unhealthy': [186, 304],
        'very unhealthy': [305, 604],
        'hazardous': [605, 1004],

    },
    'co':{

        'good': [0, 4.4],
        'moderate': [4.5, 9.4],
        'unhealthy for sensitive groups': [9.5, 12.4],
        'unhealthy': [12.5, 15.4],
        'very unhealthy': [15.5, 30.4],
        'hazardous': [30.5, 50.4],

    },
    
    'nh3': {

        'good': [0, 200],
        'satisfactory': [201, 400],
        'moderately polluted': [401, 800],
        'poor': [801, 1200],
        'very poor': [1201, 1800],
        'severe': [1801, float('inf')],

    },

    'aqi':{

        'good': [0, 50],
        'moderate': [51, 100],
        'unhealthy for sensitive groups': [101, 150],
        'unhealthy': [151, 200],
        'very unhealthy': [201, 300],
        'hazardous': [301, 500],
        'conversion_factor':1
    }
}

def fetch_air_quality(lat, lon):
    url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}'
    response = req.get(url)
    return json.dumps(response.json(), indent=4)


def index_calulator(components):
    # pollutants order [cp,no2,o3,so2,pm2_5,pm10,nh3]
    indices=[]

    # print(components.items())
    for pollutant,level in components.items():
        # print(f'{pollutant},{level}')
        

        for key, value in breakpoint[pollutant].items():
            index='good'
            r_cf=1/conversion_factor[pollutant]
            
            if value[0]<=(level*r_cf)<=value[1]:
                # print(f'Normalized value : {pollutant},{level*r_cf}')
                index=key
                # print(index)
                C_p= level *r_cf
                I_hi=breakpoint['aqi'][index][1]
                I_lo=breakpoint['aqi'][index][0]
                BP_hi=breakpoint[pollutant][index][1]
                BP_lo=breakpoint[pollutant][index][0]

                aqi_sub=((I_hi-I_lo)/(BP_hi-BP_lo))*(C_p-BP_lo)+I_lo
                indices.append(aqi_sub)

                # print(aqi_sub)
                # print('\n')
                continue



    return indices


def aqi_calculation(lat,long,city_name):
    clean_data = fetch_air_quality(lat, long)
    data=json.loads(clean_data)
    components=data['list'][0]['components']

    components.pop('no')

    # print(components.items())
    indices=index_calulator(components)
    print(f"Calculated aqi in {city_name}: ",max(indices))
    # pollutants=[pm2_5,pm10,o3,no2,so2,co]
    aqi=None

    return clean_data

phnom_penh_aq = aqi_calculation(11.5625, 104.916, city_name="Phnom Penh")
print("Phnom Penh Air Quality:")
print((phnom_penh_aq))

siem_reap_aq = aqi_calculation(13.5, 104, city_name="Siem Reap")
print("Siem Reap Air Quality:")
print(siem_reap_aq)

