import math
import requests
import collections
import time


class GeoDistributedLRUCache:
    def __init__(self, nodes_ip: list, capacity: int, expiration_time: int):
        """Constructor of the GeoDistributedLRUCache Object"""
        self.node_cache = {}
        self.node_cache_expiration_time = {}
        self.node_location = {}
        self.expiration_time = expiration_time
        self.capacity = capacity
        for server in nodes_ip:
            #location = self.get_location(server)
            # self.node_location[server] = location # {'172.217.22.14': {'latitude': 32.0803, 'longitude': 34.7805}, '208.67.222.222' : {'latitude': 37.774778, 'longitude': -122.397966 }}
            self.node_cache_expiration_time[server] = {}
            self.node_cache[server] = collections.OrderedDict()
        self.node_location =  {'172.217.22.14': {'latitude': 32.0803, 'longitude': 34.7805}, '208.67.222.222' : {'latitude': 37.774778, 'longitude': -122.397966 }} # Dummy static innput for code to make it work
     
        
    def get_ip(self):
        """Method which obtains users ip information"""
        response = requests.get('https://api64.ipify.org?format=json').json()
        return response["ip"]


    def get_location(self, ip_address : str) -> dict:
        """Gets the location in latitude and longitud for an ip passed as parameter"""
        response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
        location_data = {
            "latitude": response.get("latitude"),
            "longitude": response.get("longitude")
        }
        return location_data


    def haversine_distance(self, lat1: float , lon1: float, lat2: float, lon2: float) -> float:
        # Radius of the Earth in kilometers (mean value)
        earth_radius = 6371.0

        # Convert latitude and longitude from degrees to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        # Haversine formula
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad
        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Calculate the distance
        distance = earth_radius * c
        
        return distance
        
    
    def get_nearest_server(self) -> str:
        """Returns the nearest server from the users location"""
        # my_devise_location = self.get_location(self.get_ip()) # {'latitude': 51.5161, 'longitude': 0.0584}
        my_devise_location = {'latitude': 51.5161, 'longitude': 0.0584} # Dummy parameters, the API needs to be payed to consistently work
        min_distance = 40075/2 # circunference of the earth at the ecuator divided by 2 (longest distance from any point)
        for ip, server_location in self.node_location.items():
            distance = self.haversine_distance(my_devise_location["latitude"], my_devise_location["longitude"], server_location["latitude"], server_location["longitude"])
            if distance < min_distance:
                min_distance = distance
                nearest_server = ip
        return nearest_server
            

    def set(self, key, value):
        """Set the cache for the nearest node. In case the capacity of the cache is full, it deletes the LRU cache first"""
        server = self.get_nearest_server() # gets nearest earth distance server
        if len(self.node_cache[server]) >= self.capacity: # checks if memory of chache is at its maximum
            item = self.node_cache[server].popitem(False) # pops the Least Used Cache stored in memory
            self.node_cache_expiration_time[server].pop(item[0]) # deletes time registration of the deleted cache
        self.node_cache[server][key] = value # sets the nearest server with given cache
        self.node_cache_expiration_time[server][key] = time.time() + self.expiration_time #  current time of seting + expiration time
       

    def get(self, key):
        """Gets the value stored in cache for a given key. It searches for nearest server"""
        server = self.get_nearest_server() # gets nearest earth distance server
        cache_value = self.node_cache[server].get(key) # gets cache stored from server
        if cache_value != None: # if cache exists
            self.node_cache_expiration_time[server][key] = time.time() + self.expiration_time # node_cache_expiration time is updated
        return cache_value
    
    
    def delete_expired_cache(self):
        """It deletes the expired cache for all nodes."""
        now = time.time()
        keys_to_delete = []
        for server, cache_expiration_times in self.node_cache_expiration_time.items():
            keys_to_delete = []
            for key, cache_time in cache_expiration_times.items():
                if cache_time < now:
                    keys_to_delete.append(self.node_cache[server].popitem(key)[0])
       
            for key in keys_to_delete:
                del self.node_cache_expiration_time[server][key]
                    

if __name__ == "__main__":
    # Usage
    # {'latitude': 32.0803, 'longitude': 34.7805}, {'latitude': 37.774778, 'longitude': -122.397966 } # add more servers as needed
    server_nodes = ['172.217.22.14', '208.67.222.222']
    cache = GeoDistributedLRUCache(server_nodes, 4, 3)
    cache.set('key0', 'value0')
    print(cache.get('key0'))
    print(cache.node_cache)
    cache.set('key1', 'value1')
    print(cache.get('key1'))
    cache.set('key2', 'value2')
    cache.set('key3', 'value3')
    cache.set('key4', 'value4')
    cache.set('key5', 'value5')
    cache.set('key6', 'value2')
    print(cache.node_cache)
    print(cache.node_cache_expiration_time)
    time.sleep(6)
    print(cache.node_cache_expiration_time)
    cache.delete_expired_cache()
    print(cache.node_cache)
    print(cache.node_cache_expiration_time)
    
    
    
