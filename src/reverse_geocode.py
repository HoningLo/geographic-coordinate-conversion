#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Convert geographic coordinates (latitude, longitude) to addresses using reverse geocoding.
Support converting TWD97 coordinates to addresses.
"""

from geopy.geocoders import Nominatim
import math


def twd97_to_wgs84(x, y):
    """
    Parameters
    ----------
    x : float
        TWD97 coord system. The default is 174458.0.
    y : float
        TWD97 coord system. The default is 2525824.0.
    Returns
    -------
    list
        [longitude, latitude]
    """
    
    a = 6378137
    b = 6356752.314245
    long_0 = 121 * math.pi / 180.0
    k0 = 0.9999
    dx = 250000
    dy = 0
    
    e = math.pow((1-math.pow(b, 2)/math.pow(a,2)), 0.5)
    
    x -= dx
    y -= dy
    
    M = y / k0
    
    mu = M / ( a*(1-math.pow(e, 2)/4 - 3*math.pow(e,4)/64 - 5 * math.pow(e, 6)/256))
    e1 = (1.0 - pow((1   - pow(e, 2)), 0.5)) / (1.0 +math.pow((1.0 -math.pow(e,2)), 0.5))
    
    j1 = 3*e1/2-27*math.pow(e1,3)/32
    j2 = 21 * math.pow(e1,2)/16 - 55 * math.pow(e1, 4)/32
    j3 = 151 * math.pow(e1, 3)/96
    j4 = 1097 * math.pow(e1, 4)/512
    
    fp = mu + j1 * math.sin(2*mu) + j2 * math.sin(4* mu) + j3 * math.sin(6*mu) + j4 * math.sin(8* mu)
    
    e2 = math.pow((e*a/b),2)
    c1 = math.pow(e2*math.cos(fp),2)
    t1 = math.pow(math.tan(fp),2)
    r1 = a * (1-math.pow(e,2)) / math.pow( (1-math.pow(e,2)* math.pow(math.sin(fp),2)), (3/2))
    n1 = a / math.pow((1-math.pow(e,2)*math.pow(math.sin(fp),2)),0.5)
    d = x / (n1*k0)
    
    q1 = n1* math.tan(fp) / r1
    q2 = math.pow(d,2)/2
    q3 = ( 5 + 3 * t1 + 10 * c1 - 4 * math.pow(c1,2) - 9 * e2 ) * math.pow(d,4)/24
    q4 = (61 + 90 * t1 + 298 * c1 + 45 * math.pow(t1,2) - 3 * math.pow(c1,2) - 252 * e2) * math.pow(d,6)/720
    lat = fp - q1 * (q2 - q3 + q4)
    
    
    q5 = d
    q6 = (1+2*t1+c1) * math.pow(d,3) / 6
    q7 = (5 - 2 * c1 + 28 * t1 - 3 * math.pow(c1,2) + 8 * e2 + 24 * math.pow(t1,2)) * math.pow(d,5) / 120
    lon = long_0 + (q5 - q6 + q7) / math.cos(fp)
    
    lat = (lat*180) / math.pi
    lon = (lon*180) / math.pi
    return  lat, lon


def twd97_to_address(x, y, language='zh-TW'):
    """
    Convert TWD97 coordinates to an address.
    
    Args:
        x (float): TWD97 X coordinate (Easting)
        y (float): TWD97 Y coordinate (Northing)
        language (str): The language code for the results (default is Traditional Chinese)
    
    Returns:
        str: The address corresponding to the coordinates
    """
    # First convert TWD97 to WGS84
    lat, lng = twd97_to_wgs84(x, y)
    
    # Then use the existing function to get the address
    return coordinates_to_address(lat, lng, language)


def coordinates_to_address(latitude, longitude, language='zh-TW'):
    """
    Convert geographic coordinates to an address.
    
    Args:
        latitude (float): The latitude value
        longitude (float): The longitude value
        language (str): The language code for the results (default is Traditional Chinese)
    
    Returns:
        str: The address corresponding to the coordinates
    """
    # Create a geocoder instance with a custom user agent
    geolocator = Nominatim(user_agent="geographic-coordinate-conversion")
    
    # Perform reverse geocoding
    try:
        location = geolocator.reverse((latitude, longitude), exactly_one=True, language=language)
        if location and location.address:
            address = location.raw["address"]
            return ", ".join([address["country"], address["county"], address["town"]])
        else:
            return "無法找到地址"
    except Exception as e:
        return f"發生錯誤: {str(e)}"


def main():
    """
    Main function to process TWD97 coordinates and convert them to addresses.
    Accepts input in the format (x, y)
    """
    print("TWD97座標轉換為地址")
    print("-" * 30)
    
    try:
        # Get TWD97 coordinates from user
        coord_input = input("請輸入 TWD97 座標 (格式為 (x, y), 例如: (303490.09, 2770553.65)): ")
        
        # Parse the input format (x, y)
        coord_input = coord_input.strip()
        if coord_input.startswith("(") and coord_input.endswith(")"):
            coord_input = coord_input[1:-1]  # Remove the parentheses
        
        # Split by comma and convert to floats
        parts = [part.strip() for part in coord_input.split(",")]
        if len(parts) != 2:
            print("錯誤: 輸入格式應為 (x, y)")
            return
        
        try:
            x = float(parts[0])
            y = float(parts[1])
        except ValueError:
            print("錯誤: 請確保座標為有效的數字")
            return
        
        print("\n正在轉換...")
        # First convert to WGS84 for display purposes
        lat, lng = twd97_to_wgs84(x, y)
        address = twd97_to_address(x, y)
        
        print(f"\n轉換結果:")
        print(f"TWD97: ({x}, {y})")
        print(f"對應 WGS84 經緯度: ({lat:.6f}, {lng:.6f})")
        print(f"地址: {address}")
        
    except Exception as e:
        print(f"錯誤: {str(e)}")


if __name__ == "__main__":
    main()
