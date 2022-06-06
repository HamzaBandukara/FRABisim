def generate_flower(size: int) -> str:
    labels = [x for x in range(1, size + 1)]
    second_labels = [labels[x] for x in range(1, size)]
    second_labels.append(labels[0])
    s = "{q1,p1}{q1}{"
    tmp = "(q1"
    for i in range(1, size + 1):
        tmp += "," + str(i)
    tmp += ")(p1"
    for i in range(1, size + 1):
        tmp += "," + str(i)
    s += tmp + ")}{"
    for tag in range(size):
        for i in range(size):
            s += f"(q1,{tag},{labels[i]},K,q1)(p1,{tag},{labels[i]},K,p1)"
        s += f"(q1,{tag},{labels[tag]},G,q1)(p1,{tag},{second_labels[tag]},G,p1)"
    s += "}{}"
    return s

if __name__ == '__main__':
    print(generate_flower(2))
