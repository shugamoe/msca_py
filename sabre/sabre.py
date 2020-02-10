import re
import requests
import base64
import pickle
import calendar, datetime

def get_new_token():
    """
    """
    client_id=b"V1:99276b8l9reqsssl:DEVCENTER:EXT"
    client_secret=b"eEJF29wm"

    client_id64=base64.b64encode(client_id)
    client_secret64=base64.b64encode(client_secret)

    credentials_part = client_id64.decode("utf-8") + ":" + client_secret64.decode("utf-8")
    credentials = base64.b64encode(credentials_part.encode("utf-8"))

    url = "https://api.test.sabre.com/v2/auth/token"
    headers = {"Authorization": "Basic " + credentials.decode("utf-8")}
    params = {"grant_type": "client_credentials"}

    r = requests.post(url, headers=headers, data=params)
    assert r.status_code is 200, "Oops..."
    token = r.json()

    token["expire_time"] = calendar.timegm(datetime.datetime.now().utctimetuple()) + token["expires_in"]
    
    with open("sabre_token.pkl", "wb") as pkl_file:
        pickle.dump(token, pkl_file)

    return token

# instaflights_search
if __name__ == "__main__":
    cur_time = calendar.timegm(datetime.datetime.now().utctimetuple())
    with open("sabre_token.pkl", "rb") as pkl_file:
        token = pickle.load(pkl_file)

    if cur_time > token["expire_time"]:
        token = get_new_token()


    # tkey = "T1RLAQLJBDu33WLgtIfwnE0r5GdTTRlLnxDRNNHOVqTVPoQ1XYnZlsVhAADAiqwaYarwke9NscIiI3np8nZHJZ6oujczDmwTr82lQzG96IHDTyo5iPcdYLqm2G3NwV+3FnpPVe/+rqm9kafmHepDjhuL14tw1jPAcUVuyHvB63k9EboYCFkRLrWg7wrW3+APLFDKvPGpfdHmgSzsMoOTjwo1dz+lFbt+AEeM8Z9sjMuHzwOlDKFPdyLTuZxIh0X87791+WdlkxGhzplGZaw8bSu+LwMptl18KWCLN3IVc5oAOI39oeb+fpX6JkMm"
    # flight_header = {"Authorization": "Bearer {}".format(tkey)}
    flight_header = {"Authorization": "Bearer {access_token}".format(**token)}
    flight_params = {"origin":"JFK", 
            "destination":"LAX",
            "departuredate":"2018-01-07",
            "returndate": "2018-01-08",
            "onlineitinerariesonly": "N",
            "limit": 1,
            "offset": 1,
            "eticketsonly": "N",
            "sortby": "totalfare",
            "order": "asc",
            "sortby2": "departuretime",
            "order2": "asc",
            "pointofsalecountry": "US"}
    flights = requests.get("https://api.test.sabre.com/v1/shop/flights",
            headers=flight_header, params=flight_params)
    info_dict = flights.json()

    # You will need to return the price, the legs, the departure time, the arrival time, the
    # duration of the flight.
    price = info_dict["PricedItineraries"][0]["AirItineraryPricingInfo"]\
            ["PTC_FareBreakdowns"]["PTC_FareBreakdown"]["PassengerFare"]\
            ["TotalFare"]

    print("The total price is: ${}".format(price["Amount"]))
    print("There are two legs to the trip, an initial leg, and the return leg")
    initial_leg = info_dict["PricedItineraries"][0]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][0]["FlightSegment"][0]
    return_leg = info_dict["PricedItineraries"][0]["AirItinerary"]["OriginDestinationOptions"]["OriginDestinationOption"][1]["FlightSegment"][0]

    print("\nThe intial leg departs from {} ({} | GMT {}) and arrives at {} ({} | GMT {}) for a total travel time of: {:.2f} hours".format(
        initial_leg["DepartureAirport"]["LocationCode"], re.sub("T", " T ", initial_leg["DepartureDateTime"]),
        initial_leg["DepartureTimeZone"]["GMTOffset"],
        initial_leg["ArrivalAirport"]["LocationCode"], re.sub("T", " T ", initial_leg["ArrivalDateTime"]),
        initial_leg["ArrivalTimeZone"]["GMTOffset"],
        initial_leg["ElapsedTime"] / 60))

    print("\nThe intial leg departs from {} ({} | GMT {}) and arrives at {} ({} | GMT {}) for a total travel time of: {:.2f} hours".format(
        return_leg["DepartureAirport"]["LocationCode"], re.sub("T", " T ", return_leg["DepartureDateTime"]), 
        return_leg["DepartureTimeZone"]["GMTOffset"],
        return_leg["ArrivalAirport"]["LocationCode"], re.sub("T", " T ", return_leg["ArrivalDateTime"]), 
        return_leg["ArrivalTimeZone"]["GMTOffset"],
        return_leg["ElapsedTime"] / 60))

