# Safegame

The goal of the project is to show how [Model Checking](https://en.wikipedia.org/wiki/Model_checking) verification method can be applied to multiplayer game development. The main idea is to generate a verification model based on the game model template, game parameters and a property which must be checked. Finally, [NuSMV](http://nusmv.fbk.eu) model checker can be applied to verify whether the generated model satifies the property. This approach is implemented for [Penguin Clash](https://github.com/RZRussel/statemachinegenerator/wiki/What-is-Penguin-Clash-game-about%3F) game as an example.

## Getting started

Follow guide below to run the project and perform verification. It is recommended to use Mac OS or Linux operating systems.

### Installing Python packages

The project is written in Python 3. Additionally PyYAML library is used to support game specifications in [YAML](https://en.wikipedia.org/wiki/YAML) language.

<b>For Linux:</b>
```
sudo apt-get install python3
sudo apt-get install python3-yaml
```

<b>For Mac OS:</b>
```
sudo brew install python3
sudo python3 -m easy_install pyyaml
```

### Installing NuSMV

NuSMV model checker is necessary to automatically verify that a game model satisfies a property. The tool can be downloaded from the [official website](http://nusmv.fbk.eu/NuSMV/download/getting_bin-v2.html). To simplify work with the model checker append string 
```export PATH="<path to model checker directory>/NuSMV-2.6.0-Darwin/bin:$PATH"``` to shell configuration file. On Linux it is located at path ```~/.bashrc``` and on Mac OS - ```~/.bash_profile```.

### Checking installation

Switch to the project directory and run:
```
python3 smv.py -s resources/specification.yaml -t resources/template.smv -c resources/movement_behavior.smv
NuSMV -v 5 movement_behavior_model.smv
```

If the model checker starts verification process and doesn't terminate with an error than installation completed successfully. 
Press CTRL+C to terminate the NuSMV execution.

To get more information about tool usage run:
```
python3 smv.py -v
```

<b>[Read Wiki page to learn more about Safegame](https://github.com/RZRussel/statemachinegenerator/wiki)</b>

<b>[Read user manual to learn more about NuSMV](http://nusmv.fbk.eu/NuSMV/userman/index-v2.html)</b>
