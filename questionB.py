def compare_versions(version1: str, version2: str) -> str:
    """Compares two version strings and indicattes whether one is greater than, equal, or less than"""
    list_v1 = version1.split('.')
    list_v2 = version2.split('.')
    result = ""
    
    if (len(list_v1) < len(list_v2)):
        for i in range(len(list_v2) - len(list_v1)):
            list_v1.append('0')
            
    elif (len(list_v1) > len(list_v2)):
        for i in range(len(list_v1) - len(list_v2)):
            list_v2.append('0')

    for i in range(len(list_v1)):        
        if list_v1[i] > list_v2[i]:
            result = (f"{version1} is greater than {version2}")
            break
        elif  list_v1[i] < list_v2[i]:
            result = (f"{version1} is less than {version2}")
            break
        else:
            result = (f"{version1} is equal to {version2}")
    return result


if __name__ == "__main__":
    print(compare_versions("1.1.1", "1.1.2"))
    print(compare_versions("1000.0.0", "1.0.0.0.0.0"))
    print(compare_versions("10.0", "1.0.0.0.0.0"))
    print(compare_versions("1.0.0.0.0.0","10.0"))
    print(compare_versions("1.0","10.0"))
    print(compare_versions("1.0.0.a.0.0","10.b"))
    print(compare_versions("10.b.a","10.b"))
    print(compare_versions("10.b.a","10.b.b"))
