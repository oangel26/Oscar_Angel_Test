import math
import requests
import collections
import time


class GeoDistributedLRUCache:
    def __init__(self, nodes_ip: list, capacity: int, expiration_time: int):
        """
        Initializes the GeoDistributedLRUCache object with necessary configurations.

        Parameters:
        - nodes_ip: A list containing the IPs of the available nodes.
        - capacity: The maximum number of items each cache can hold.
        - expiration_time: The time after which a cache entry will be expired.
        """
        self.node_cache = {}  # Dictionary to store cache data for each node.
        self.node_cache_expiration_time = {}  # Dictionary to store expiration time of cache for each node.
        self.node_location = {}  # Dictionary to store location information of each node.
        self.expiration_time = expiration_time  # Global expiration time for each cache item.
        self.capacity = capacity  # Global capacity for each node's cache.
        
        # Initializing cache, expiration times, and locations for each node.
        for server in nodes_ip:
            location = self.get_location(server)
            self.node_location[server] = location
            self.node_cache_expiration_time[server] = {}
            self.node_cache[server] = collections.OrderedDict()

        # Static location data, for demonstration purposes.
        self.node_location =  {'172.217.22.14': {'latitude': 32.0803, 'longitude': 34.7805}, 
                               '208.67.222.222' : {'latitude': 37.774778, 'longitude': -122.397966 }}

        
    def get_ip(self):
        """
        Fetches the user's IP address.

        Returns:
        - A string containing the IP address of the requester.
        """
        response = requests.get('https://api64.ipify.org?format=json').json()
        return response["ip"]

    
    def get_location(self, ip_address : str) -> dict:
        """
        Fetches location information for a given IP address.

        Parameters:
        - ip_address: The IP for which to fetch the location.

        Returns:
        - A dictionary containing latitude and longitude of the IP.
        """
        response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
        return {"latitude": response.get("latitude"), "longitude": response.get("longitude")}
    

    def haversine_distance(self, lat1: float , lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculates the Haversine distance between two geographical points on the earth.

        Parameters:
        - lat1, lon1: The latitude and longitude of the first point.
        - lat2, lon2: The latitude and longitude of the second point.

        Returns:
        - A float representing the distance between the two points in kilometers.
        """
        earth_radius = 6371.0  # Earth’s radius in kilometers.

        # Converting latitudes and longitudes from degrees to radians.
        lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Applying the Haversine formula.
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad
        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return earth_radius * c  # Distance in kilometers.
        
    
    def get_nearest_server(self) -> str:
        """
        Identifies the nearest server based on the haversine distance from the user's location.

        Returns:
        - A string representing the IP address of the nearest server.
        """
        user_location  = self.get_location(self.get_ip()) 
        user_location = {'latitude': 51.5161, 'longitude': 0.0584}  # Static user location for demonstration.
        nearest_server, min_distance = None, float('inf')
        
        for ip, server_location in self.node_location.items():
            distance = self.haversine_distance(user_location["latitude"], user_location["longitude"],
                                               server_location["latitude"], server_location["longitude"])
            if distance < min_distance:
                min_distance, nearest_server = distance, ip
                
        return nearest_server

    
    def set(self, key, value):
        """
        Adds or updates a cache entry in the nearest server.

        Parameters:
        - key: The key to be set or updated in the cache.
        - value: The value to be associated with the key in the cache.
        """
        server = self.get_nearest_server()
        
        # Remove the LRU item if the cache has reached its capacity.
        if len(self.node_cache[server]) >= self.capacity:
            oldest_key, _ = self.node_cache[server].popitem(last=False)
            del self.node_cache_expiration_time[server][oldest_key]
            
        # Add or update the cache entry.
        self.node_cache[server][key] = value
        self.node_cache_expiration_time[server][key] = time.time() + self.expiration_time

    
    def get(self, key):
        """
        Retrieves a value from the cache of the nearest server based on the key.

        Parameters:
        - key: The key to look up in the cache.

        Returns:
        - The cached value associated with the key, or None if the key is not found.
        """
        server = self.get_nearest_server()
        value = self.node_cache[server].get(key)
        
        if value:  # Refresh the expiration time if the key is found.
            self.node_cache_expiration_time[server][key] = time.time() + self.expiration_time
            
        return value
    
    
    def delete_expired_cache(self):
        """
        Removes expired cache entries from all servers.
        """
        current_time = time.time()
        
        for server, expiration_times in self.node_cache_expiration_time.items():
            expired_keys = [key for key, exp_time in expiration_times.items() if exp_time < current_time]
            
            for key in expired_keys:
                del self.node_cache[server][key]
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