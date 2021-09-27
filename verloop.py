from flask import Flask, jsonify, request
from urllib.parse import urlencode
import requests
from dict2xml import dict2xml

# import lxml.etree as et

# import xml.etree.ElementTree as ele



app = Flask(__name__)


@app.route("/getAddressDetails", methods=['GET','POST'])    
 # methods for API tasks     


def lat_lng():
    if (request.method == 'POST'):
        sample_json = request.get_json()
        json_dict = dict(sample_json)
        address = json_dict['address']
        output_format = json_dict['data_type']

        api_key = ""            # please add API key here
        endpoint = f"https://maps.googleapis.com/maps/api/geocode/{output_format}"
        params = {
            "address": address, 
            "key": api_key
        }
        url_params = urlencode(params)
        url = f"{endpoint}?{url_params}"
        r = requests.get(url)
        if r.status_code not in range(200, 299):
            return {}
        latlng = {}
        try:
            latlng = r.json()['results'][0]['geometry']['location']
        except:
            pass

        latitude = latlng.get("lat")
        longitude = latlng.get("lng")
        
        add_dict = {
            "coordinates": {
                            "lat": latitude,
                            "lng": longitude
        }, 
        "address": address
        }


        if output_format == "json":
            return jsonify(add_dict)
        else:
             return dict2xml(add_dict, "root")
            # def data2xml(d, name='data'):
            #     r = et.Element(name)
            #     return et.tostring(buildxml(r, d))

            # def buildxml(r, d):
            #     if isinstance(d, dict):
            #         for k, v in d.items():
            #             s = et.SubElement(r, k)
            #             buildxml(s, v)

            #     elif isinstance(d, str):
            #         r.text = d
            #     else:
            #         r.text = str(d)
            #     return r

            # return data2xml(add_dict)

            # def GenerateXML(fileName):
            #     root = ele.Element("Root")

            #     m1 = ele.Element("Coordinates")
            #     root.append(m1)

            #     b1 = ele.SubElement(m1, "lat")
            #     b1.text = latitude
            #     b2 = ele.SubElement(m1, "lng")
            #     b2.text = longitude

            #     m2 = ele.Element("Address")
            #     m2.text = address

            #     tree = ele.ElementTree(root)

            #     return tree



if __name__ == '__main__':
    app.run(debug = True, port = 8000)  
    # testing the Flask app

    

