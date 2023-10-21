"""Questio A
Your goal for this question is to write a program that accepts two lines (x1,x2) 
and (x3,x4) on the x-axis and returns whether they overlap. 

As an example, (1,5) and (2,6) overlaps but not (1,5) and (6,8).
"""
def sort_vector(vector: tuple) -> tuple:
    """Function which sorts a tuple chaninging its direction to positive"""
    vector = list(vector)
    vector.sort()
    return tuple(vector)

def check_line_overlap(line1: tuple , line2: tuple) -> bool:
    """Method which checkes whether the two lines overlap"""
    sorted_line1 = sort_vector(line1)
    sorted_line2 = sort_vector(line2)

    if  sorted_line1[0] < sorted_line2[0] and sorted_line2[0] < sorted_line1[1]:
        print("The lines overlaps")
    elif sorted_line1[0] < sorted_line2[1] and sorted_line2[1] < sorted_line1[1]:
        print("The lines overlaps")
    else:
        print("None of the lines provided overlaps")
        
if __name__ == "__main__":
    while True:
        try:
            print()
            print("Please provide the coordinates on the x-axis of the for the following two lines")
            print()
            print("Line1 Coordinates:")
            x1 = int(input("Enter x1: "))
            x2 = int(input("Enter x2: "))
            line1 = x1, x2
            print()
            
            print("Line 2 Coordinates: ")
            x3 = int(input("Enter x3: "))
            x4 = int(input("Enter x4: "))
            line2 = x3, x4
    
            check_line_overlap(line1, line2)
           
        except ValueError:  # Handle non-integer inputs.
            print("Invalid input. Please enter a numerical value.")
            
