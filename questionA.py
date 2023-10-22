"""Questio A
Your goal for this question is to write a program that accepts two lines (x1,x2) 
and (x3,x4) on the x-axis and returns whether they overlap. 

As an example, (1,5) and (2,6) overlaps but not (1,5) and (6,8).
"""
def sort_vector(vector: tuple) -> tuple:
    """Function which sorts a vector coordinates changing its direction to positive"""
    vector = list(vector)
    vector.sort()
    return tuple(vector)

def check_if_dot(line: tuple) -> bool:
    """Function which checks whether the line is a dot"""
    line_is_dot = False
    if line[0] == line[1]:
        line_is_dot = True
    return line_is_dot
 
def check_line_overlap(line1: tuple , line2: tuple):
    """Function which checks whether the two lines overlaps"""
    sorted_line1 = sort_vector(line1)
    sorted_line2 = sort_vector(line2)

    if  sorted_line1[0] < sorted_line2[0] and sorted_line2[0] < sorted_line1[1]:
        print()
        print("######## The lines overlaps :( please try again ########")
    elif sorted_line1[0] < sorted_line2[1] and sorted_line2[1] < sorted_line1[1]:
        print()
        print("######## The lines overlaps :( please try again. ########")
    else:
        print()
        print("######## Well done!!! None of the lines provided overlaps ########")

        
if __name__ == "__main__":
    while True:
        try:
            print()
            print("Please provide the coordinates on the x-axis for the following two lines ->")
            print()
            print("-------Line1 Coordinates:--------")
            x1 = int(input("Enter x1: "))
            x2 = int(input("Enter x2: "))
            
            print(f"The coordinates entered for your line1 are: ({x1},{x2})") 
            line1 = x1, x2
            print()
            
            if check_if_dot(line1) == True:
                print("----------------------------------------")
                print(f"Line1 with coordinates ({line1[0]},{line1[1]}) is a dot.") 
                print(f"Please insert a line")
                print("----------------------------------------")
                continue
   
            print("------Line 2 Coordinates:--------")
            x3 = int(input("Enter x3: "))
            x4 = int(input("Enter x4: "))
            print(f"The coordinates entered for your line2 are: ({x3},{x4})")
            line2 = x3, x4
            
            if check_if_dot(line2) == True:
                print("----------------------------------------")
                print(f"Line2 with coordinates ({line2[0]},{line2[1]}) is a dot.") 
                print(f"Please insert a line")
                print("----------------------------------------")
                continue
            
            check_line_overlap(line1, line2)
           
        except ValueError:  # Handle non-integer inputs.
            print()
            print("You have just entered an invalid input.")
            print("Please enter a numerical value.")
            
