### Major update: parameter free and magnitudes faster than previous versions.
### Paper and pseudocode: https://arxiv.org/abs/1712.09658


### This package: Python implementation of the higher-order network (HON) construction algorithm.
### Paper: "Representing higher-order dependencies in networks"
### Code written by Jian Xu, Apr 2017

### Technical questions? Please contact i[at]jianxu[dot]net
### Demo of HON: please visit http://www.HigherOrderNetwork.com
### Latest code: please visit https://github.com/xyjprc/hon

### See details in README

import BuildRulesFastParameterFree
import BuildRulesFastParameterFreeFreq
import BuildNetwork
import itertools
import math


## Initialize algorithm parameters
MaxOrder = 8
MinSupport = 100

#/home/igor/PycharmProjects/HON/hon-master/data/sfc.csv

## Initialize user parameters
#InputFileName = '/home/igor/PycharmProjects/HON/hon-master/data/traces-simulated-mesh-v100000-t100-mo4.csv'
#OutputRulesFile = '../data/rules-syn.csv'
#OutputNetworkFile = '../data/network-syn.csv'

## Initialize user parameters


#InputFileName = '/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/scenarios/hon_random_sfc_training_data.csv'
InputFileName = '/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/scenarios/hon_sfc_by_len_training_data.csv'
#InputFileName = '/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/scenarios/hon_sfc_var_len_training_data.csv'


#OutputRulesFile = '/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/scenarios/hon_random_sfc_rules.csv'
#OutputNetworkFile = '/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/scenarios/hon_random_sfc_output.csv'

#OutputRulesFile = '/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/scenarios/hon_sfc_var_len_rules.csv'
#OutputNetworkFile = '/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/scenarios/hon_sfc_var_len_output.csv'

OutputRulesFile = '/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/scenarios/hon_sfc_by_len_rules.csv'
OutputNetworkFile = '/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/scenarios/hon_sfc_by_len_output.csv'






########################################################################################################################

LastStepsHoldOutForTesting = 0
MinimumLengthForTraining = 3
InputFileDeliminator = ','
Verbose = True


###########################################
# Functions
###########################################

def ReadSequentialData(InputFileName):
    if Verbose:
        print('Reading raw sequential data')
    RawTrajectories = []
    with open(InputFileName) as f:
        LoopCounter = 0
        for line in f:
            fields = line.strip().split(InputFileDeliminator)

            ## In the context of global shipping, a ship sails among many ports
            ## and generate trajectories.
            ## Every line of record in the input file is in the format of:
            ## [Ship1] [Port1] [Port2] [Port3]...
            ship = fields[0]
            movements = fields[1:]

            LoopCounter += 1
            if LoopCounter % 1000 == 0:
                VPrint(LoopCounter)

            ## Other preprocessing or metadata processing can be added here

            ## Test for movement length
            MinMovementLength = MinimumLengthForTraining + LastStepsHoldOutForTesting
            if len(movements) < MinMovementLength:
                continue

            RawTrajectories.append([ship, movements])


    return RawTrajectories


def truncate(number, digits):
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper




def BuildTrainingAndTesting(RawTrajectories):
    VPrint('Building training and testing')
    Training = []
    Testing = []
    for trajectory in RawTrajectories:
        ship, movement = trajectory
        movement = [key for key,grp in itertools.groupby(movement)] # remove adjacent duplications
        if LastStepsHoldOutForTesting > 0:
            Training.append([ship, movement[:-LastStepsHoldOutForTesting]])
            Testing.append([ship, movement[-LastStepsHoldOutForTesting]])
        else:
            Training.append([ship, movement])
    return Training, Testing

def DumpRules(Rules, OutputRulesFile):
    VPrint('Dumping rules to file')
    with open(OutputRulesFile, 'w') as f:
        for Source in Rules:
            for Target in Rules[Source]:
                f.write(' '.join([','.join([str(x) for x in Source]), ',',Target, ',', str(truncate(Rules[Source][Target],4))]) + '\n')

def DumpNetwork(Network, OutputNetworkFile):
    VPrint('Dumping network to file')
    LineCount = 0
    with open(OutputNetworkFile, 'w') as f:
        for source in Network:
            for target in Network[source]:
                f.write(' '.join([SequenceToNode(source), SequenceToNode(target), str(Network[source][target])]) + '\n')
                LineCount += 1
    VPrint(str(LineCount) + ' lines written.')

def SequenceToNode(seq):
    curr = seq[-1]
    node = curr + '|'
    seq = seq[:-1]
    while len(seq) > 0:
        curr = seq[-1]
        node = node + curr + '.'
        seq = seq[:-1]
    if node[-1] == '.':
        return node[:-1]
    else:
        return node

def VPrint(string):
    if Verbose:
        print(string)


def BuildHON(InputFileName, OutputNetworkFile):
    RawTrajectories = ReadSequentialData(InputFileName)
    TrainingTrajectory, TestingTrajectory = BuildTrainingAndTesting(RawTrajectories)
    VPrint(len(TrainingTrajectory))
    Rules = BuildRulesFastParameterFree.ExtractRules(TrainingTrajectory, MaxOrder, MinSupport)
    # DumpRules(Rules, OutputRulesFile)
    Network = BuildNetwork.BuildNetwork(Rules)
    DumpNetwork(Network, OutputNetworkFile)
    VPrint('Done: '+InputFileName)

def BuildHONfreq(InputFileName, OutputNetworkFile):
    print('FREQ mode!')
    RawTrajectories = ReadSequentialData(InputFileName)
    TrainingTrajectory, TestingTrajectory = BuildTrainingAndTesting(RawTrajectories)
    VPrint(len(TrainingTrajectory))
    Rules = BuildRulesFastParameterFreeFreq.ExtractRules(TrainingTrajectory, MaxOrder, MinSupport)
    # DumpRules(Rules, OutputRulesFile)
    Network = BuildNetwork.BuildNetwork(Rules)
    DumpNetwork(Network, OutputNetworkFile)
    VPrint('Done: '+InputFileName)

###########################################
# Main function
###########################################

if __name__ == "__main__":
    print('FREQ mode!')
    RawTrajectories = ReadSequentialData(InputFileName)
    TrainingTrajectory, TestingTrajectory = BuildTrainingAndTesting(RawTrajectories)
    VPrint(len(TrainingTrajectory))
    Rules = BuildRulesFastParameterFree.ExtractRules(TrainingTrajectory, MaxOrder, MinSupport)
    DumpRules(Rules, OutputRulesFile)
    Network = BuildNetwork.BuildNetwork(Rules)
    #VPrint(Network)
    DumpNetwork(Network, OutputNetworkFile)
