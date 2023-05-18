from collections import Counter

def valid_string(input_str: str) -> str:
    flag = list()
    for _, val in Counter(input_str).items():
        flag.append(val)
    
    if len(set(flag)) == 1:
        return "YES"
    
    return "NO"


if __name__ == "__main__":
    print(valid_string('abcc'))