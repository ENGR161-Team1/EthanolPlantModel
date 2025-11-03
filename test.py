from systems.processes import Fermentation

test_fermenter = Fermentation(0.85)

print(test_fermenter.name)

print(test_fermenter.ferment({
    "ethanol": 0,
    "water": 100,
    "sugar": 50,
    "fiber": 20
}))