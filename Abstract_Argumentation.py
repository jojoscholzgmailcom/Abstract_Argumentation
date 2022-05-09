import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from ipywidgets import *
from IPython.display import display
import re
arguments = {"A", "B", "C", "D"}#{"A", "B", "C", "D", "E"}
attacks = {("A", "B"), ("B", "A"), ("C", "D"), ("D", "C"), ("C", "B")}#{("A", "D"), ("B", "D"), ("C", "D"), ("E", "A"), ("E", "B"), ("E", "C")}

def is_conflict_free(current_set, attacks):
    for attack in attacks:
        if attack[0] in current_set and attack[1] in current_set:
            return False
    return True

def does_set_attack(argument, current_set, attacks):
    for attack in attacks:
        if attack[1] == argument and attack[0] in current_set:
            return True
    return False

def is_acceptable(argument, current_set, attacks):
    for attack in attacks:
        if attack[1] == argument and not does_set_attack(attack[0], current_set, attacks):
            return False
    return True

def is_admissible(current_set, attacks):
    if not is_conflict_free(current_set, attacks):
        return False
    for argument in current_set:
        if not is_acceptable(argument, current_set, attacks):
            return False
    return True

def will_set_be_admissible(argument, current_set, attacks):
    attacked_arguments = set()
    for attack in attacks:
        if (attack[0] == argument and attack[1] in current_set) or (attack[1] == argument and attack[0] in current_set) or (attack[1] == argument and not does_set_attack(attack[0], current_set, attacks)):
            return False, None
        if attack[0]==0:
            attacked_arguments.add(attack[1])
    return True, attacked_arguments

def is_preferred_extension(current_set, arguments, attacks):
    if not is_admissible(current_set, attacks):
        return False
    for argument in arguments:
        if not argument in current_set and is_acceptable(argument, current_set, attacks):
            return False
    return True

def is_set_subset(cSet, sets):
    for current_set in sets:
        if cSet.issubset(current_set) and not cSet == current_set:
            return True
    return False

def generate_all_admissible_sets(arguments, attacks, current_set, depth):
    if depth >= len(arguments):
        return set(frozenset(set()))
    admissible_set = set()
    admissible_set.add(frozenset(set()))
    for argument in arguments:
        if argument in current_set:
            continue
        new_set = current_set.copy()
        new_set.add(argument)
        if is_admissible(new_set, attacks):
            admissible_set.add(frozenset(new_set))
        admissible_set2 = generate_all_admissible_sets(arguments, attacks, new_set, depth + 1)
        admissible_set.update(admissible_set2)
    return admissible_set

# This method was not used and therfore is not tested
def generate_all_admissible_sets_faster(arguments, attacks, current_set, depth):
    if depth >= len(arguments)+len(current_set):
        return set(frozenset(set()))
    admissible_set = set()
    admissible_set.add(frozenset(current_set))
    for argument in arguments:
        if argument in current_set:
            continue
        new_arguments = arguments.copy()
        bool_value, attacked_arguments = will_set_be_admissible(argument, current_set, attacks)
        new_set = current_set.copy()
        if bool_value:
            new_set.add(argument)
            admissible_set.add(frozenset(new_set))
            new_arguments.remove(argument)
            for r_argument in attacked_arguments:
                new_arguments.remove(r_argument)
        admissible_set2 = generate_all_admissible_sets_faster(new_arguments, attacks, new_set, depth + 1)
        admissible_set.update(admissible_set2)
    return admissible_set

def generate_all_complete_extensions(arguments, attacks):
    admissible_extensions = generate_all_admissible_sets(arguments, attacks, set(), 0)
    complete_extensions = set()
    for admissible_extension in admissible_extensions:
        complete_extensions.add(admissible_extension)
        for argument in arguments:
            if not argument in admissible_extension and is_acceptable(argument, admissible_extension, attacks):
                complete_extensions.remove(admissible_extension)
    return complete_extensions

def generate_all_complete_extensions_faster(arguments, attacks, admissible_extensions):
    complete_extensions = set()
    for admissible_extension in admissible_extensions:
        complete_extensions.add(admissible_extension)
        for argument in arguments:
            if not argument in admissible_extension and is_acceptable(argument, admissible_extension, attacks):
                complete_extensions.remove(admissible_extension)
                break
    return complete_extensions

def generate_preferred_extensions(arguments, attacks):
    preferred_extensions = set()
    admissible_extensions = generate_all_admissible_sets(arguments, attacks, set(), 0)
    for admissible_extension in admissible_extensions:
        if not is_set_subset(admissible_extension, admissible_extensions):
            preferred_extensions.add(admissible_extension)
    return preferred_extensions

def generate_preferred_extensions_faster(complete_extensions):
    preferred_extensions = set()
    for admissible_extension in complete_extensions:
        if not is_set_subset(admissible_extension, complete_extensions):
            preferred_extensions.add(admissible_extension)
    return preferred_extensions

def generate_stable_extensions(arguments, attacks):
    preferred_extensions = generate_preferred_extensions(arguments, attacks)
    stable_extensions = set()
    for preferred_extension in preferred_extensions:
        attacked = True
        for argument in arguments:
            if argument in preferred_extension:
                continue
            if not does_set_attack(argument, preferred_extension, attacks):
                attacked = False
                break
        if attacked:
            stable_extensions.add(preferred_extension)
    return stable_extensions

def generate_stable_extensions_faster(arguments, attacks, preferred_extensions):
    stable_extensions = set()
    for preferred_extension in preferred_extensions:
        attacked = True
        for argument in arguments:
            if argument in preferred_extension:
                continue
            if not does_set_attack(argument, preferred_extension, attacks):
                attacked = False
                break
        if attacked:
            stable_extensions.add(preferred_extension)
    return stable_extensions

def generate_grounded_extension(arguments, attacks):
    grounded_extension = set()
    hasChanged = True
    while hasChanged:
        hasChanged = False
        for argument in arguments:
            if argument in grounded_extension:
                continue
            if(is_acceptable(argument, grounded_extension, attacks)):
                grounded_extension.add(argument)
                hasChanged = True
    return grounded_extension

# This one should not be used, as it has not be tested yet
def generate_preferred_extensions_shortcut(arguments, attacks):
    preferred_extensions = set()
    admissible_extensions = generate_all_admissible_sets(arguments, attacks, generate_grounded_extension(arguments, attacks), 0)
    for admissible_extension in admissible_extensions:
        if not is_set_subset(admissible_extension, admissible_extensions):
            preferred_extensions.add(admissible_extension)
    return preferred_extensions

def getGraphFromStrings(str_arguments, str_attacks):
    arguments = re.split("\s*,\s*", str_arguments)
    attacks = set()
    split_attacks = re.split("\s*\)\s*,\s*\(\s*", str_attacks)
    for attack in split_attacks:
        attack = re.sub("[\(\)]", "", attack)
        attackparts = re.split("\s*,\s*", attack)
        attacks.add((attackparts[0], attackparts[1]))
    output(arguments, attacks)

def get_string_set(current_set):
    string_set = "{"
    count = len(current_set)
    for argument in current_set:
        count -= 1
        string_set += argument
        if count > 0:
            string_set += ", "
    string_set += "}"
    return string_set

def string_set_with_subsets(current_set, allows_empty_set):
    count = len(current_set)
    if len(current_set)>1:
        string_set = "are: {"
    elif len(current_set)==1:
        string_set = "is: "
    elif allows_empty_set:
        string_set = "is: {"
    else:
        string_set = "does not exist."
    for cSet in current_set:
        count -= 1
        string_set += get_string_set(cSet)
        if count > 0:
            string_set += ", "
    if len(current_set)>1 or (len(current_set) == 0 and allows_empty_set):
        string_set += "}"
    return string_set

def output(arguments, attacks):
    G = nx.DiGraph(directed=True)
    G.add_nodes_from(arguments)
    G.add_edges_from(attacks)
    options = {
        'node_color': 'white',
        'node_size': 250,
        'width': 2,
        'arrowstyle': '-|>',
        'arrowsize': 12,
        'pos': nx.planar_layout(G)
    }
    fig, ax = plt.subplots(figsize=(10,10))
    nx.draw_networkx(G, arrows=True, **options)
    print("This is the attack graph:")
    plt.show()
    admissible_extensions = generate_all_admissible_sets(arguments, attacks, set(), 0)
    complete_extensions = generate_all_complete_extensions_faster(arguments, attacks, admissible_extensions)
    preferred_extensions = generate_preferred_extensions_faster(complete_extensions)
    stable_extensions = generate_stable_extensions_faster(arguments, attacks, preferred_extensions)
    print("The admissible extensions of this graph", string_set_with_subsets(admissible_extensions, True), "\n")
    print("The complete extensions of this graph", string_set_with_subsets(complete_extensions, True), "\n")
    print("The preferred extensions of this graph", string_set_with_subsets(preferred_extensions, True), "\n")
    print("The stable extensions of this graph", string_set_with_subsets(stable_extensions, False), "\n")
    print("The grounded extension of this graph is:", get_string_set(generate_grounded_extension(arguments, attacks)))

def readCommaStyleGraph(str_graph):
    attacks = set()
    arguments = set()
    str_attacks = re.split("\s*,\s*", str_graph)
    for str_attack in str_attacks:
        str_participants = re.split("\s+", str_attack)
        arguments.add(str_participants[0])
        for i in range(1,len(str_participants)):
            arguments.add(str_participants[i])
            attacks.add((str_participants[i], str_participants[0]))
    output(arguments, attacks)

def generateStatistics(filename, minArguments, maxArguments, minEdgeProb, maxEdgeProb, stepSize, repetitions):
    file = open(filename+".csv", "w")
    file.write("Index,Arguments,Edge Probability,Admissible sets,Complete sets,Prefered sets,Stable sets\n")
    for numArguments in range(minArguments, maxArguments):
        for numEdgeProb in np.arange(minEdgeProb, maxEdgeProb, stepSize):
            file.write(generate_specific_statistics(numArguments, numEdgeProb, repetitions))
    file.close()

def generateLengthStatistics(filename, minArguments, maxArguments, minEdgeProb, maxEdgeProb, stepSize, repetitions):
    file = open(filename+".csv", "w")
    file.write("Index,Arguments,Edge Probability,Type,Set length\n")
    for numArguments in range(minArguments, maxArguments):
        for numEdgeProb in np.arange(minEdgeProb, maxEdgeProb, stepSize):
            file.write(generate_specific_length_statistics(numArguments, numEdgeProb, repetitions))
    file.close()

def generateCombinedStatistics():
    count_extensions = "Index,Arguments,Edge Probability,Edges,Admissible sets,Complete sets,Prefered sets,Stable sets\n"
    length_extension = "Index,Arguments,Edge Probability,Edges,Type,Set length\n"
    for numArguments in range(1, 8):
        for numEdgeProb in np.arange(0.1, 0.9, 0.1):
            for index in range(200):
                graph = nx.fast_gnp_random_graph(numArguments, numEdgeProb, directed=True)
                arguments = set()
                attacks = set()
                nodes = nx.nodes(graph)
                edges = nx.edges(graph)
                for node in nodes:
                    print(node)
                    arguments.add(node)
                for edge in edges:
                    attacks.add(edge)
                admissible_extensions = generate_all_admissible_sets(arguments, attacks, set(), 0)
                complete_extensions = generate_all_complete_extensions_faster(arguments, attacks, admissible_extensions)
                preferred_extensions = generate_preferred_extensions_faster(complete_extensions)
                stable_extensions = generate_stable_extensions_faster(arguments, attacks, preferred_extensions)
                count_extensions += str(index)+","+str(numArguments)+","+str(numEdgeProb)+","+str(nx.number_of_edges(graph))+","+str(len(admissible_extensions))+","+str(len(complete_extensions))+","+str(len(preferred_extensions))+","+str(len(stable_extensions))+"\n"
                for admissible_extension in admissible_extensions:
                    length_extension += str(index)+","+str(numArguments)+","+str(numEdgeProb)+","+str(nx.number_of_edges(graph))+","+"admissible"+","+str(len(admissible_extension))+"\n"
                for complete_extension in complete_extensions:
                    length_extension += str(index)+","+str(numArguments)+","+str(numEdgeProb)+","+str(nx.number_of_edges(graph))+","+"complete"+","+str(len(complete_extension))+"\n"
                for preferred_extension in preferred_extensions:
                    length_extension += str(index)+","+str(numArguments)+","+str(numEdgeProb)+","+str(nx.number_of_edges(graph))+","+"preferred"+","+str(len(preferred_extension))+"\n"
                for stable_extension in stable_extensions:
                    length_extension += str(index)+","+str(numArguments)+","+str(numEdgeProb)+","+str(nx.number_of_edges(graph))+","+"stable"+","+str(len(stable_extension))+"\n"
    file = open("count_statistics.csv", "w")
    file.write(count_extensions)
    file.close()
    file = open("length_statistics.csv", "w")
    file.write(length_extension)
    file.close()


def generate_specific_statistics(numArguments, numEdgeProb, repetitions):
    str_instances = ""
    for index in range(repetitions):
        graph = nx.fast_gnp_random_graph(numArguments, numEdgeProb, directed=True)
        arguments = set()
        attacks = set()
        nodes = nx.nodes(graph)
        edges = nx.edges(graph)
        for node in nodes:
            print(node)
            arguments.add(node)
        for edge in edges:
            attacks.add(edge)
        admissible_extensions = generate_all_admissible_sets(arguments, attacks, set(), 0)
        complete_extensions = generate_all_complete_extensions_faster(arguments, attacks, admissible_extensions)
        preferred_extensions = generate_preferred_extensions_faster(complete_extensions)
        stable_extensions = generate_stable_extensions_faster(arguments, attacks, preferred_extensions)
        str_instances += str(index)+","+str(numArguments)+","+str(numEdgeProb)+","+str(nx.number_of_edges(graph))+","+str(len(admissible_extensions))+","+str(len(complete_extensions))+","+str(len(preferred_extensions))+","+str(len(stable_extensions))+"\n"
    return str_instances

def generate_specific_length_statistics(numArguments, numEdgeProb, repetitions):
    str_instances = ""
    for index in range(repetitions):
        graph = nx.fast_gnp_random_graph(numArguments, numEdgeProb, directed=True)
        arguments = set()
        attacks = set()
        nodes = nx.nodes(graph)
        edges = nx.edges(graph)
        for node in nodes:
            print(node)
            arguments.add(node)
        for edge in edges:
            attacks.add(edge)
        admissible_extensions = generate_all_admissible_sets(arguments, attacks, set(), 0)
        for admissible_extension in admissible_extensions:
            str_instances += str(index)+","+str(numArguments)+","+str(numEdgeProb)+","+"admissible"+","+str(len(admissible_extension))+"\n"
        complete_extensions = generate_all_complete_extensions_faster(arguments, attacks, admissible_extensions)
        for complete_extension in complete_extensions:
            str_instances += str(index)+","+str(numArguments)+","+str(numEdgeProb)+","+"complete"+","+str(len(complete_extension))+"\n"
        preferred_extensions = generate_preferred_extensions_faster(complete_extensions)
        for preferred_extension in preferred_extensions:
            str_instances += str(index)+","+str(numArguments)+","+str(numEdgeProb)+","+"preferred"+","+str(len(preferred_extension))+"\n"
        stable_extensions = generate_stable_extensions_faster(arguments, attacks, preferred_extensions)
        for stable_extension in stable_extensions:
            str_instances += str(index)+","+str(numArguments)+","+str(numEdgeProb)+","+"stable"+","+str(len(stable_extension))+"\n"
    return str_instances

        