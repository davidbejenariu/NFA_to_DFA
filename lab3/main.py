# lab1

with open("input_file.in", "r") as f:
    lines = f.read().split("\n")

for i in range(len(lines)):
    lines[i] = lines[i].replace("\t", "")
    lines[i] = lines[i].replace(",", "")

i = 0
sigma = set()
states = set()
finalStates = set()
transitions = dict()

while i < len(lines):
    if lines[i][0] != '#':
        if lines[i] == "Sigma:":
            i += 1

            while lines[i] != 'End':
                sigma.add(lines[i])
                i += 1
        elif lines[i] == "States:":
            i += 1

            while lines[i] != "End":
                temp = lines[i].split()
                states.add(temp[0])

                if len(temp) > 1:
                    if temp[1] == "S":
                        startState = temp[0]
                    else:
                        finalStates.add(temp[0])

                i += 1
        elif lines[i] == "Transitions:":
            i += 1

            while lines[i] != 'End':
                transition = lines[i].split()
                stateX, wordY, stateZ = transition[0], transition[1], transition[2]
                key = (stateX, wordY)

                if stateX in states and wordY in sigma and stateZ in states:
                    if key not in transitions:
                        transitions[key] = {stateZ}
                    else:
                        transitions[key].add(stateZ)
                else:
                    if stateX not in states:
                        print("Error! State", stateX, "does not exist.")
                    if stateZ not in states:
                        print("Error! State", stateZ, "does not exist.")
                    if wordY not in sigma:
                        print("Error! Word", wordY, "does not exist.")

                i += 1
    i += 1

for state in states:
    for letter in sigma:
        if (state, letter) not in transitions:
            transitions[(state, letter)] = set()

from pprint import pprint

print("The NFA:\n")
print("Sigma =", sigma)
print("States =", end=" ")
pprint(states)
print("The starting state is:", startState)

print("The final state(s) are:", end=" ")

for finalState in finalStates:
    print(finalState, end=" ")

print()
print("The transitions are:")
pprint(transitions)


# lab3

from dataclasses import dataclass


@dataclass()
class FA:
    Sigma: set
    States: set
    StartState: str
    FinalStates: set
    Transitions: dict


nfa = FA(sigma, states, startState, finalStates, transitions)
dfa = FA(sigma, set(), startState, set(), {})

dfa.States.add(startState)

queue = [startState]
newDelta = dict()
left = right = 0

while left <= right:
    currentState = queue[left]
    left += 1

    for letter in dfa.Sigma:
        newState = ''
        newSet = set()

        for i in range(len(currentState)):
            for state in nfa.Transitions[(currentState[i], letter)]:
                if state not in newSet:
                    newState += str(state)
                    newSet.add(state)

        newState = "".join(sorted(newState))

        if currentState != '' and (currentState, letter) not in newDelta:
            newDelta[(currentState, letter)] = newState

        if newState != '' and newState not in queue:
            dfa.States.add(newState)
            queue.append(newState)
            right += 1

dfa.Transitions = newDelta

for state in dfa.States:
    for i in range(len(state)):
        if state[i] in nfa.FinalStates:
            dfa.FinalStates.add(state)

print("\nThe DFA:\n")
print("Sigma =", dfa.Sigma)
print("States =", end=" ")
pprint(dfa.States)
print("The starting state is:", dfa.StartState)

print("The final state(s) are:", end=" ")

for finalState in dfa.FinalStates:
    print(finalState, end=" ")

print()
print("The transitions are:")
pprint(dfa.Transitions)