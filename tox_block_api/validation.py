from typing import Tuple, List

def validate_multiple_inputs(input: List[str]) -> Tuple[List[str], str]:
    
    errors = None
    
    try:
        # check if JSON contains the key "input_texts"
        input = input.get("input_data", None)
        if input is None:
            raise KeyError("The key 'input_data' was not found in the received JSON.") 
        # check if input is list
        if isinstance(input,list):
            # check if list is empty
            if len(input) == 0:
                raise ValueError("Passed an empty list.")
            # check if all list items are non-empty strings
            for i, item in enumerate(input):
                if not isinstance(item,str):
                    raise TypeError(f"The list item at position {i} is not a string.")
                if item == "":
                    raise ValueError(f"The list item at position {i} is an empty string.")
        else:
            raise TypeError("The passed object is not a list of strings.")  
    except (ValueError, TypeError, KeyError) as exc:
        errors = str(exc)   
        
    return input, errors



def validate_single_input(input: str) -> Tuple[str, str]:
    
    errors = None
    
    try:
        # check if JSON contains the key "input_texts"
        input = input.get("input_data", None)
        if input is None:
            raise KeyError("The key 'input_data' was not found in the received JSON.") 
        # check if input is non-empty string
        if isinstance(input,str):
            if input == "":
                raise ValueError("Passed an empty string.")
        else:
            raise TypeError("The passed object is not a string.")
        
    except (ValueError, TypeError, KeyError) as exc:
        errors = str(exc)
        
    return input, errors