from re import findall
from RAStack.Generator import generate_stack

def combiner(a1: str, a2: str) -> str:
    combined = "{"
    a2 = a2.replace("q", "p")
    split_a1 = findall("{(.*?)}", a1)
    split_a2 = findall("{(.*?)}", a2)
    # Step 1: Combine all states
    combined += split_a1[0] + "," + split_a2[0] + "}"
    # Step 2: Single initial state
    combined += "{" + split_a1[1] + "}"
    # Step 3: Combine all registers
    combined += "{" + split_a1[2] + split_a2[2] + "}"
    # Step 4: Transitions
    combined += "{" + split_a1[3] + split_a2[3] + "}"
    # Step 5: Final States
    combined += "{" + split_a1[4]
    if split_a1[4] != "":
        combined += ","
    combined += split_a2[4] + "}"
    return combined

