from systems.processes import Fermentation, Filtration

# Test Fermentation and Filtration classes
test_fermenter = Fermentation(0.85)
print(test_fermenter.name)
print(test_fermenter.ferment({
    "ethanol": 0,
    "water": 100,
    "sugar": 50,
    "fiber": 20
}))

test_filter = Filtration(0.90)
print(test_filter.name)
print(test_filter.filter({
    "ethanol": 25.5,
    "water": 100,
    "sugar": 7.5,
    "fiber": 20
}))