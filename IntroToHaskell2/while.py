
def my_while(state, cont, act, fin):
    return my_while(act(state), cont, act, fin) if cont(state) else fin(state)

