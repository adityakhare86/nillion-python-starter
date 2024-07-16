from functools import reduce  # Import reduce from functools
from nada_dsl import *


def return_val_if_any_false(list_of_bool, val):
    """
    Returns val if any boolean inside list_of_bool is false.

    Parameters:
    - list_of_bool (list of bool): List of boolean values to be checked.
    - val: Value to be returned if any boolean in the list is false.

    Returns:
    - val: If any boolean in the list is false.
    - 0: If none of the booleans in the list are false.
    """

    # Initialize a constant zero value
    zero_value = UnsignedInteger(0)

    # Define a function to return the desired value
    def select_value(bool_value):
        return bool_value * val + (1 - bool_value) * zero_value

    # Use reduce to apply the select_value function across all booleans
    final_value = reduce(select_value, list_of_bool, zero_value)

    return final_value


def initialize_collaborators(nr_collaborators):
    """
    Initialize collaborators with unique identifiers.

    Parameters:
    - nr_collaborators (int): Number of collaborators.

    Returns:
    - collaborators (list): List of Party objects representing collaborators.
    """
    collaborators = []
    for i in range(nr_collaborators):
        collaborators.append(Party(name="Collaborator" + str(i)))

    return collaborators


def initialize_work_and_capacity(nr_collaborators, collaborators):
    """
    Initialize work and capacity vectors for collaborators.

    Parameters:
    - nr_collaborators (int): Number of collaborators.
    - collaborators (list): List of Party objects representing collaborators.

    Returns:
    - work_to_be_done (list): List representing work to be allocated.
    - capacity (list): List representing capacity (ability to do work) for each collaborator.
    """
    work_to_be_done = []
    capacity = []
    for i in range(nr_collaborators):
        # Generate random work to be done (for demonstration purposes)
        work_to_be_done.append(SecretUnsignedInteger(Input(name="work_" + str(i), party=collaborators[i])))
        # Generate random capacity (for demonstration purposes)
        capacity.append(SecretUnsignedInteger(Input(name="capacity_" + str(i), party=collaborators[i])))

    return work_to_be_done, capacity


def allocate_work(nr_collaborators, work_to_be_done, capacity, outparty):
    """
    Allocate work to collaborators based on their capacity to maximize work done.

    Parameters:
    - nr_collaborators (int): Number of collaborators.
    - work_to_be_done (list): List representing work to be allocated.
    - capacity (list): List representing capacity (ability to do work) for each collaborator.
    - outparty (Party): Party object representing the output party.

    Returns:
    - allocated_work (list): List of Output objects representing allocated work for each collaborator.
    """
    allocated_work = []
    total_capacity = reduce(lambda x, y: x + y, capacity)

    for c in range(nr_collaborators):
        # Allocate work proportional to capacity using secure division
        allocated_work_c = work_to_be_done[c] * (capacity[c] / total_capacity)
        allocated_work.append(Output(allocated_work_c, "allocated_work_collaborator" + str(c), outparty))

    return allocated_work


def nada_main():

    # 0. Compiled-time constants
    nr_collaborators = 3

    # 1. Parties initialization
    collaborators = initialize_collaborators(nr_collaborators)
    outparty = Party(name="OutParty")

    # 2. Inputs initialization
    work_to_be_done, capacity = initialize_work_and_capacity(nr_collaborators, collaborators)

    # 3. Computation
    # Allocate work based on capacity
    allocated_work = allocate_work(nr_collaborators, work_to_be_done, capacity, outparty)

    # 4. Output
    results = allocated_work
    return results


# Run the main function
if __name__ == "__main__":
    results = nada_main()
    print(results)
