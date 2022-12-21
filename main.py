import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.stats import skewnorm
import csv

# definition of the scenario name (needed for the generation of the file names)
# values for the scenario must be changed manually
scenario = "B"

# number of families to simulate
numberOfSimulatedFamilies = 1000

# gender distribution in percent
sexRatioMale = 50
sexRatioFemale = 50

# infant mortality rate in percent
earlyDeathRatio = 40  # 20 # 40 # 50
earlyLifeRatio = 60  # 80 # 60 # 50

a = 6  # skewness of the distribution of children
loc = 3  # 2 # 3 # 4 # expected value of the number of children
scale = 6  # standard deviation of the number of children

# maximum number of generations to be simulated
# serves to limit the runtime
maxGeneration = 11  # 8 # 11 # 15

# definition of the existing structure of the families
# for each location a number of simulated individuals is entered
# list is filled with zeros, because comparison values are needed for the simulation
# simulation can generate more different values and then needs values for a larger-smaller comparison
aimList = [10, 6, 6, 6, 4, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0]  # zeros, because comparison values must be there

# number of branches required results from the number of locations
aimListWithout0 = []
for element in aimList:
    if element != 0:
        aimListWithout0.append(element)
neededBranches = len(aimListWithout0)

# definition of the proportion of persons with/without children
noChildlessRatio = 80
childlessRatio = 20


def nChilds(my, sd):
    """
    This function generates a random number of children.
    :param my: expected value (integer)
    :param sd: standard deviation (integer)
    :return: number of children (integer)
    """
    return (np.random.normal(loc=my, scale=sd, size=None))


def skewChilds(a, loc, scale):
    """
    This function generates a skewed random number of children.
    :param a: skewness of the distribution of children (integer)
    :param loc: expected value of the number of children (integer)
    :param scale: standard deviation of the number of children (integer)
    :return: number of children (integer)
    """
    return (skewnorm.rvs(a=a, loc=loc, scale=scale, size=1))


def ratioRandom(firstRatio, secondRatio):
    """
    This function randomly decides between two states (childless/non-childless, male/female, etc.).
    For this purpose, the probabilities for the states are given, which must add up to 100 percent.
    :param firstRatio: probability of the first possibility in percent (integer)
    :param secondRatio: probability of the second possibility in percent (integer)
    :return: 0 for the first state, 1 for the second state (integer)
    """
    if firstRatio + secondRatio != 100:
        print("Error: Ratio is not 100 percent")
    values = [[0, 1], [firstRatio, secondRatio]]
    randomValue = sum(([position] * value for position, value in zip(*values)), [])
    return (random.choice(randomValue))


# branches sometimes die out when there are no male offspring left
# for verification serves list with number of generations after branches died out
extinctGenerationList = []

# list of lists about the number of (male) persons per simulated generation
# for each simulated family there is a list
numberPerGenerationListList = []
maleAduldNumberPerGenerationListList = []

# father and child assignment dictionary
fathersDict = {}  # key: id child, value: id father

gen1List = []  # List of the number of relevant generations (after how many generations there are enough branches)
gen2List = []  # generation with enough people per branch

# iterate each family
for famNum in range(0, numberOfSimulatedFamilies):
    print("-------------------- family", famNum)

    # properties of the initial person are set
    personList = [{"id": 1,  # father ID
                   "idFather": 0,  # no father
                   "generation": 0,  # generation 0
                   "sex": 0,  # male
                   "earlyDeath": 0,  # not died as a child
                   "childless": 0,  # had children
                   "aduldMaleChildrenList": []}]  # List of male children (list to be filled)

    # father receives ID 1, other persons receive IDs starting from value 2
    id = 2
    # start with generation 1 for the successor generation
    generation = 1

    # initialization of a value for the relevant generation
    # number of generations after which the target state is reached
    relevantGeneration = ""

    gen1 = ""  # number of relevant generations
    gen2 = ""  # generation with enough people per branch

    # people generation
    # iteration of the generation until the desired state (aimList) is reached or exceeded.
    # persons are generated up to the specified maximum generation
    for generation in range(1, maxGeneration + 1):
        # identify possible fathers
        # search in last generation
        for person in personList:
            if person["generation"] == generation - 1:  # last generation
                if person["sex"] == 0:  # fathers can only be male
                    if person["earlyDeath"] == 0:  # fathers can not have died early
                        # add property whether someone was childless
                        # only not with initial person, because that had in any case children
                        if person["id"] != 1:
                            person.update({"childless": ratioRandom(noChildlessRatio, childlessRatio)})
                            # property is only created here for runtime reasons
                            # alternatively, this can also be generated at each person
                        # check if he remained childless
                        if person["childless"] == 0:  # had children (0), had no children (1)
                            # save ID
                            idFather = person["id"]
                            # create children (number random)
                            for child in range(int(round(skewChilds(a, loc, scale)[0], 0))):
                                # creation of a dictionary per child
                                childDict = {}
                                # assign properties
                                childDict.update({"id": id})
                                childDict.update({"idFather": idFather})
                                childDict.update({"generation": generation})
                                childDict.update({"sex": ratioRandom(sexRatioMale, sexRatioFemale)})
                                childDict.update({"earlyDeath": ratioRandom(earlyLifeRatio, earlyDeathRatio)})
                                childDict.update({"aduldMaleChildrenList": []})
                                personList.append(childDict)  # add person
                                fathersDict.update({id: idFather})  # add father and child dictionary
                                id = id + 1  # count up ID, as this is not to be assigned twice

                                # add the list of male children of the father with the ID of the child
                                # only if male and not died early
                                if childDict["sex"] == 0 and childDict["earlyDeath"] == 0:
                                    personList[childDict["idFather"]]["aduldMaleChildrenList"].append(id)
    print("Status: Persons were generated")

    # check from which generated generation of the result is suitable

    # IDs of all males (list per generation)
    branchListOverall = []

    # iterate generations
    for generation in range(1, maxGeneration + 1):
        # from generation 4 it is checked how many branches there are
        # a branch here can be a male person with descendants
        # there must be at least x (neededBranches) many branches representing each location
        # then it is checked in which generation there are so many people in each branch that they exceed the aimList

        # execute only if relevantGeneration has no suitable value yet
        # relevantGeneration describes the generation in which enough branches have been simulated
        if relevantGeneration == "":
            personCounter = 0  # number of men in a generation
            branchList = []  # IDs of men of one generation

            # adult men of a generation count
            for p in personList:
                # exclude early deceased, female or persons of other generation
                if p["earlyDeath"] != 0 or p["sex"] != 0 or p["generation"] != generation:
                    continue
                personCounter = personCounter + 1  # count up
                branchList.append(p["id"])  # save ID

            branchListOverall.append(branchList)  # per generation a list with the IDs

            print("Status: Number of adult males (in generation):", len(branchList), "(" + str(generation) + ")")

            # checking whether there are enough branches in one generation
            if len(branchList) >= neededBranches:
                # checking whether there were four branches four generations before
                # this must be done to prevent branches die out
                # increment IDs of the branchesList
                fathersBefore = []
                for idCheck in branchList:
                    for prevoiusGen in range(1, 5):  # four generations
                        for p in personList:
                            if p["id"] == idCheck:
                                idCheck = p["idFather"]
                                break
                    # save list of progenitors four generations before
                    fathersBefore.append(idCheck)
                # delete duplicates
                # now if several people have the same ancestor within four generations, they are recognized as one branch
                fathersBefore = set(fathersBefore)
                # check if there are still more than ten branches present
                if len(fathersBefore) >= neededBranches:
                    relevantGeneration = generation
                    print("Status: Relevant generation (enough branches available):", relevantGeneration)
                    # now subtract four generation from this
                    relevantGeneration = relevantGeneration - 4

        # checking which generation outperforms the aimList
        # only if relevantGeneration is not "", otherwise there is no start generation yet
        if relevantGeneration != "" and gen1 == "":
            # generate list for each generation with number of adult males
            branchListList = []
            # generations iterate
            for gen in range(relevantGeneration, maxGeneration + 1):
                # list for each branch
                branchInnerlist = []
                # check if the list is already four elements long
                try:
                    branchListListPosition = relevantGeneration
                except:
                    branchListListPosition = -1  # last element, if the list is not four elements large
                # iterate branches (list of IDs)
                for branch in branchListOverall[
                    branchListListPosition]:  # must use the branchList four generations before, not the last one
                    innerCounter = 0
                    # people iterate
                    for p in personList:
                        # use only the people with appropriate generation
                        if p["generation"] == gen:
                            # only males who did not die at an early age
                            if p["sex"] == 0 and p["earlyDeath"] == 0:
                                # person is descendant of branch (id)
                                # counting people
                                fatherId = fathersDict[p["id"]]
                                # until progenitor found, then stop
                                while fatherId != 1:
                                    # if branch is greater than fatherId, a match can never be obtained
                                    if fatherId < branch:
                                        break
                                    if fatherId == branch:
                                        innerCounter = innerCounter + 1
                                        break  # do not search further
                                    fatherId = fathersDict[fatherId]  # next father
                    branchInnerlist.append(innerCounter)
                branchInnerlist.sort(reverse=True)
                branchListList.append(branchInnerlist)

                # at which position of branchListList the conditions apply
                # can also be different positions
                # since the last generation is interested check which generation fits completely into the target form
                # create two lists, sort and check each element against each other
                # works only if values per generation are always larger and not smaller (!)
                # otherwise it is to be checked whether from the row a value was before already in such a way (additional loop)

                newListbig = branchListList
                newList = branchInnerlist
                newList.sort(reverse=True)  # sort descending

                # if the check fails, failed is set to 1 and the next generation is checked
                failed = 0
                for position, element in enumerate(newList):

                    # if the list is too short, then there must be a termination message
                    if len(aimList) == position:
                        print("Error: List (aimList) too short, append more zeros")
                        break

                    if aimList[position] > newList[position]:
                        # check if there was already a suitable value in the branch before (and the number of persons in the branch has thus been reduced)
                        failedBefore = 0
                        for newPosition in range(0, len(newListbig)):

                            if aimList[position] >= newListbig[newPosition][position]:
                                failedBefore = 1

                        if failedBefore == 1:
                            failed = 1
                            break

                print("Status: List element not yet larger than aimList in generation", gen)

                if gen1 == "":  # only save the data at the first hit, algorithm goes through next generations also for the graphs below
                    # this is the sought condition
                    # output only if first element of newList is not 0
                    if newList[0] != 0:
                        print("Status: Generation list", gen, ":", newList[0:neededBranches])
                        print("Status: Target list:", aimList[0:neededBranches])
                        if failed == 0:
                            gen1 = relevantGeneration
                            gen1List.append(gen1)
                            gen2 = gen
                            gen2List.append(gen2)
                            print("Status: Relevant Generation (enough branches):", relevantGeneration)
                            print("Status: Generation with enough people per branch:", gen)
                            break

    # family analysis
    generationList = []
    numberPerGenerationList = []
    maleAduldNumberPerGenerationList = []
    extinctGeneration = ""  # generation in which the family dies out
    for generation in range(0, maxGeneration + 1):
        numberPerGeneration = 0
        maleAduldNumberPerGeneration = 0
        for person in personList:
            if person["generation"] == generation:
                numberPerGeneration = numberPerGeneration + 1
                # male adult only
                if person["sex"] == 0 and person["earlyDeath"] == 0:
                    maleAduldNumberPerGeneration = maleAduldNumberPerGeneration + 1
        generationList.append(generation)
        numberPerGenerationList.append(numberPerGeneration)
        maleAduldNumberPerGenerationList.append(maleAduldNumberPerGeneration)
        if numberPerGeneration == 0 and extinctGeneration == "":
            extinctGeneration = generation

    # only include the dying generations if the family is really extinct
    if extinctGeneration != "":
        extinctGenerationList.append(extinctGeneration)
    numberPerGenerationListList.append(numberPerGenerationList)
    maleAduldNumberPerGenerationListList.append(maleAduldNumberPerGenerationList)

# histogram

# determination of the previous generations
gen3List = []
for position, element in enumerate(gen1List):
    # comparison how big the distance is
    difference = gen2List[position] - element
    if difference <= 4:
        gen3List.append(element)
    else:
        gen3List.append(gen2List[position] - 4)

print("gen3List")
plt.hist(gen3List, bins=(max(gen3List) - min(gen3List) + 1))
plt.xlabel("Generations")
plt.ylabel("Percentage share")
plt.show()

print("gen1List (enough branches)")
plt.hist(gen1List, bins=(max(gen1List) - min(gen1List) + 1))
plt.xlabel("Generationen")
plt.ylabel("Percentage share")
plt.show()

print("gen2List (enough branches with enough people)")
plt.hist(gen2List, bins=(max(gen2List) - min(gen2List) + 1))
plt.xlabel("Generationen")
plt.ylabel("Percentage share")
plt.show()

extinctGenerationList = sorted(extinctGenerationList)
plt.plot(extinctGenerationList)
plt.show()
print(max(extinctGenerationList))

print("Number of persons per generation")

# flip list
newNumberPerGenerationList = []
for num in range(neededBranches):
    newNumberPerGenerationList.append(0)
for list in numberPerGenerationListList:
    for position, i in enumerate(list):
        newNumberPerGenerationList[position] = newNumberPerGenerationList[position] + i

# calculate average
for position, i in enumerate(newNumberPerGenerationList):
    newNumberPerGenerationList[position] = i / numberOfSimulatedFamilies

plt.plot(newNumberPerGenerationList)
plt.show()

print("Number of adult males per generation")

# flip list
maleAduldnewNumberPerGenerationList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for list in maleAduldNumberPerGenerationListList:
    for position, i in enumerate(list):
        maleAduldnewNumberPerGenerationList[position] = maleAduldnewNumberPerGenerationList[position] + i

# calculate average
for position, i in enumerate(maleAduldnewNumberPerGenerationList):
    maleAduldnewNumberPerGenerationList[position] = i / numberOfSimulatedFamilies

plt.plot(maleAduldnewNumberPerGenerationList)
plt.show()

# outputs the contents of the gen1list, gen2list, gen3list, and extinctGenerationList lists

filename = "gen1list-" + scenario + ".csv"
with open(filename, 'w', newline='') as csvWriter:
    writer = csv.writer(csvWriter)
    for element in gen1List:
        writer.writerow([element])

with open("gen2list-" + scenario + ".csv", 'w', newline='') as csvWriter:
    writer = csv.writer(csvWriter)
    for element in gen2List:
        writer.writerow([element])

with open("gen3list-" + scenario + ".csv", 'w', newline='') as csvWriter:
    writer = csv.writer(csvWriter)
    for element in gen3List:
        writer.writerow([element])

with open("extinctGenerationList-" + scenario + ".csv", 'w', newline='') as csvWriter:
    writer = csv.writer(csvWriter)
    for element in extinctGenerationList:
        writer.writerow([element])

# testing the distributions

# normal distribution
list = []
for i in range(0, 1000):
    list.append(nChilds(5, 2))

list = sorted(list)
plt.plot(list)
plt.show()

# skewed distribution
data = skewnorm.rvs(a=6, loc=2, scale=6, size=1000)
plt.hist(data)
plt.show()
