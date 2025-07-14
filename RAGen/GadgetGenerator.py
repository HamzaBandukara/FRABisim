import itertools


class Counter:
    def __init__(self):
        self.counter = 1

    def val(self):
        return self.counter

    def inc(self):
        self.counter += 1

    def gen_state(self):
        state = f"q{self.val()}"
        self.inc()
        return state


def generate(size: int, steps: int=2, rev=False):
    states = "q0"
    initial = "q0"
    registers = "(q0)"
    transitions =""
    finals = ""
    state_counter = Counter()
    current_reg = 1
    size += 1
    current_state = "q0"
    filled_r = []
    final_reg_order = []
    while current_reg < size:
        step = size - current_reg if (size - current_reg) < steps else steps
        next_regs = [x for x in range(current_reg, current_reg + step)]
        if rev:
            final_reg_order.extend(next_regs[::-1])
        else:
            final_reg_order.extend(next_regs)
        all_paths = list(itertools.permutations(next_regs))
        map_path = {} if len(next_regs) > 1 else set()
        for path in all_paths:
            current_path = map_path
            path = list(path)
            for i in range(step - 1):
                if path[i] not in current_path:
                    current_path[path[i]] = {}
                    if i == step -2:
                        current_path[path[i]] = set()
                current_path = current_path[path[i]]
            current_path.add(path[-1])
        latest = []
        nstates, nregs, ntrans = add_rec(current_state, filled_r, map_path, state_counter, latest)
        current_state = latest[0]
        states += nstates
        registers += nregs
        transitions += ntrans
        current_reg = current_reg + step
        filled_r.extend(next_regs)
        if current_reg >= size - 1: break
        # if flw_state is None:
        #     nstates, nregs, ntrans = add_flw(current_state, size, state_counter)
        #     states += nstates
        #     registers += nregs
        #     transitions += ntrans
        #     flw_state = nstates.split(",")[1]
        # else:
        #     transitions += ",({},t0,1,L,{})".format(current_state, flw_state)
    # if flw_state is None:
    nstates, nregs, ntrans = add_flw(current_state, size, state_counter)
    states += nstates
    registers += nregs
    transitions += ntrans
    # else:
    #     transitions += ",({},t0,1,L,{})".format(current_state, flw_state)
    final_counter = 0
    r_tmp = ",({}" + (",{}" * len(filled_r)).format(*filled_r) + ")"
    for final_counter in range(len(final_reg_order)):
        reg = final_reg_order[final_counter]
        next_state = state_counter.gen_state()
        states += f",{next_state}"
        registers += r_tmp.format(next_state)
        transitions += ",({},read,{},K,{})".format(current_state,reg,next_state)
        current_state = next_state
    transitions = transitions[1:]
    automaton = "{" + "{}|{}|{}|{}|{}".format(states, initial, registers, transitions, finals).replace("|", "}{") + "}"
    return automaton


def add_flw(start_state, size, counter):
    states, regs, trans = "", "", ""
    prev = []
    current = 0
    prev_state = start_state
    while current < size:
        current += 1
        prev.append(current)
        next_state = counter.gen_state()
        trans += ",({},pop,{},L,{})".format(prev_state, current, next_state)
        regs += f",({next_state}" + (",{}" * current).format(*prev) + ")"
        states += f",{next_state}"
        prev_state = next_state
        if current == size - 1:
            break
        for x in prev:
            trans += ",({},t0,{},K,{})".format(next_state,x,next_state)
    for tag in ("t{}".format(i) for i in range(1, size)):
        for i in prev:
            trans += ",({},{},{},L,{})".format(prev_state, tag, i, prev_state)
            trans += ",({},{},{},K,{})".format(prev_state, tag, i, prev_state)
    return states, regs, trans

def add_rec(state, old, the_map, counter, latest):
    states, regs, trans = "", "", ""
    for key in the_map:
        if isinstance(the_map, set):
            if len(latest) == 0:
                latest.append(counter.gen_state())
                the_state = latest[0]
                filled = [x for x in old]
                filled.append(key)
                states += f",{the_state}"
                regs += f",({the_state}" + (",{}" * len(filled)).format(*filled) + ")"
            else:
                the_state = latest[0]
            trans += ",({},write,{},L,{})".format(state, key, the_state)
            continue
        the_state = counter.gen_state()
        filled = [x for x in old]
        filled.append(key)
        trans += ",({},write,{},L,{})".format(state, key, the_state)
        states += f",{the_state}"
        regs += f",({the_state}" + (",{}" * len(filled)).format(*filled) + ")"
        n_s, n_r, n_t = add_rec(the_state, filled, the_map[key], counter, latest)
        states += n_s
        regs += n_r
        trans += n_t
    return states, regs, trans


if __name__ == '__main__':
    print(generate(4,4))