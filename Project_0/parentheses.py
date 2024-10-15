from networkx import reverse_view

def complete_parentheses(exp):
    exp.reverse()
    i = 0
    # Continue until list has only one element
    while len(exp) > 1:     
        current = exp[i]
        if current == ')':
            # if next element is number or an expression place a left parentheses
            if isinstance(exp[i+1],(int,float)) or len(exp[i+1]) > 1 :  
                fill(exp,i)
        i = i+1
        # if we reached the end of the list, reset index
        if i == len(exp):  
            i = 0   

    # Split the string in list elements
    result = exp[0].split()
    # Normalize list
    result.reverse()
    return result

def fill(exp, index):
        # Place a parenthesis in the fourth place after the index/ e.g )5-6-> )5-6(  (the list is reversed)
        exp.insert(index+4 ,'(')
        combined = ' '.join(str(exp[i]) for i in range(index,index+5))
        # The expression is now combined in one string/  e.g. ')5-6('
        del exp[index:index+5]                      
        # Delete the spare elements and place the expression in list as a whole string
        exp.insert(index,combined)
    

# Main Method
if __name__ == '__main__':
    print("The initial expression is:")
    exp = [1,'+',2,')','*',3,'-',4,')','*',5,'-',6,')',')',')']
    print(exp)
    filled_exp = complete_parentheses(exp)
    print("The final expression is:")
    print(filled_exp)

 