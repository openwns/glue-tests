#! /usr/bin/env python

# this is needed, so that the script can be called from everywhere
import os
import sys
base, tail = os.path.split(sys.argv[0])
os.chdir(base)

# Append the python sub-dir of WNS--main--x.y ...
sys.path.append(os.path.join('..', '..', '..', 'sandbox', 'default', 'lib', 'python2.4', 'site-packages'))

# ... because the module WNS unit test framework is located there.
import pywns.WNSUnit

testSuite = pywns.WNSUnit.TestSuite()

# create a system test
testSuite.addTest(pywns.WNSUnit.ProbesTestSuite(sandboxPath = os.path.join('..', '..', '..', 'sandbox'),
                                                
                                                configFile = 'config.py',
                                                runSimulations = True,
                                                shortDescription = 'One-on-one communication with: Copper, Glue, IP, Constanze',
                                                disabled = False,
                                                disabledReason = ""))

testSuite.addTest(pywns.WNSUnit.ProbesTestSuite(sandboxPath = os.path.join('..', '..', '..', 'sandbox'),
                                                
                                                configFile = 'config80211.py',
                                                runSimulations = True,
                                                shortDescription = 'One-on-one communication with: Copper, 802.11, IP, Constanze',
                                                disabled = False,
                                                disabledReason = ""))

testSuite.addTest(pywns.WNSUnit.ProbesTestSuite(sandboxPath = os.path.join('..', '..', '..', 'sandbox'),
                                                workingDir = "PyConfig/funTutorial",
                                                configFile = 'config1.py',
                                                runSimulations = True,
                                                shortDescription = 'Tutorial1',
                                                requireReferenceOutput = False,
                                                disabled = False,
                                                disabledReason = ""))

testSuite.addTest(pywns.WNSUnit.ProbesTestSuite(sandboxPath = os.path.join('..', '..', '..', 'sandbox'),
                                                workingDir = "PyConfig/funTutorial",
                                                configFile = 'config2.py',
                                                runSimulations = True,
                                                shortDescription = 'Tutorial2',
                                                requireReferenceOutput = False,
                                                disabled = False,
                                                disabledReason = ""))

testSuite.addTest(pywns.WNSUnit.ProbesTestSuite(sandboxPath = os.path.join('..', '..', '..', 'sandbox'),
                                                workingDir = "PyConfig/funTutorial",
                                                configFile = 'config3.py',
                                                runSimulations = True,
                                                shortDescription = 'Tutorial3',
                                                requireReferenceOutput = False,
                                                disabled = False,
                                                disabledReason = ""))

testSuite.addTest(pywns.WNSUnit.ProbesTestSuite(sandboxPath = os.path.join('..', '..', '..', 'sandbox'),
                                                workingDir = "PyConfig/funTutorial",
                                                configFile = 'config4.py',
                                                runSimulations = True,
                                                shortDescription = 'Tutorial4',
                                                requireReferenceOutput = False,
                                                disabled = False,
                                                disabledReason = ""))

testSuite.addTest(pywns.WNSUnit.ProbesTestSuite(sandboxPath = os.path.join('..', '..', '..', 'sandbox'),
                                                workingDir = "PyConfig/funTutorial",
                                                configFile = 'config5.py',
                                                runSimulations = True,
                                                shortDescription = 'Tutorial5',
                                                requireReferenceOutput = False,
                                                disabled = False,
                                                disabledReason = ""))

testSuite.addTest(pywns.WNSUnit.ProbesTestSuite(sandboxPath = os.path.join('..', '..', '..', 'sandbox'),
                                                workingDir = "PyConfig/funTutorial",
                                                configFile = 'config6.py',
                                                runSimulations = True,
                                                shortDescription = 'Tutorial6',
                                                requireReferenceOutput = False,
                                                disabled = False,
                                                disabledReason = ""))

testSuite.addTest(pywns.WNSUnit.ProbesTestSuite(sandboxPath = os.path.join('..', '..', '..', 'sandbox'),
                                                workingDir = "PyConfig/funTutorial",
                                                configFile = 'config7.py',
                                                runSimulations = True,
                                                shortDescription = 'Tutorial7',
                                                requireReferenceOutput = False,
                                                disabled = False,
                                                disabledReason = ""))

testSuite.addTest(pywns.WNSUnit.ProbesTestSuite(sandboxPath = os.path.join('..', '..', '..', 'sandbox'),
                                                workingDir = "PyConfig/funTutorial",
                                                configFile = 'config8.py',
                                                runSimulations = True,
                                                shortDescription = 'Tutorial8',
                                                requireReferenceOutput = False,
                                                disabled = False,
                                                disabledReason = ""))

testSuite.addTest(pywns.WNSUnit.ProbesTestSuite(sandboxPath = os.path.join('..', '..', '..', 'sandbox'),
                                                workingDir = "PyConfig/funTutorial",
                                                configFile = 'config9.py',
                                                runSimulations = True,
                                                shortDescription = 'Tutorial9',
                                                requireReferenceOutput = False,
                                                disabled = False,
                                                disabledReason = ""))


if __name__ == '__main__':
    # This is only evaluated if the script is called by hand

    # if you need to change the verbosity do it here
    verbosity = 2

    pywns.WNSUnit.verbosity = verbosity

    # Create test runner
    testRunner = pywns.WNSUnit.TextTestRunner(verbosity=verbosity)

    # Finally, run the tests.
    testRunner.run(testSuite)
