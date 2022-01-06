import re
from fractions import Fraction




def main():
    with open('measurements.txt') as f: #import most of measurement data stored in text file for convenience
        measurements = f.readlines()

    newMeasurements = []
    for measurment in measurements: 
        numberstr = ""
        done = True in [char.isdigit() for char in measurment] #split the number of the measurement from the unit of the measurement
        seenNum = False
        while done:
            if measurment[0].isdigit():
                seenNum = True
            if seenNum:
                numberstr += measurment[0]
                measurment = measurment[1:]
            else:
                measurment = measurment[1:]
            done = True in [char.isdigit() for char in measurment]
        measurementstr = measurment.strip().lower()
        measurementNum = numify(numberstr)
        converted = convertToOz(measurementstr, measurementNum)
        print(converted)
        curMeasurement = (numberstr, measurementstr)
        newMeasurements += curMeasurement

    # print(newMeasurements)


def numify(measurementnum): 
    if measurementnum == "70ml/2": #annoying edge case
        num = 2
    elif '/' in measurementnum:
        num = float(sum(Fraction(s) for s in measurementnum.split())) #deal with different ways strings represent numbers 
    elif '.' in measurementnum:
        num = float(measurementnum)
    elif '-' in measurementnum:
        a,b = measurementnum.split("-")
        num = float((int(a)+int(b))/2)
    elif 'or' in measurementnum:
        a,b = measurementnum.split("or")
        num = float((int(a)+int(b))/2)
    elif measurementnum == '':
        num = ''
    else:
        num = float(measurementnum)
    return num

def convertToOz(measurementstr, num):
    if measurementstr == 'oz' or measurementstr =='fl oz': #convert standard other measurements to fluid ounces
        convertedNum = num
    elif measurementstr =='tsp':
        convertedNum = num/6
    elif measurementstr =='tblsp':
        convertedNum = num/2
    elif measurementstr =='cup' or measurementstr =='cups':
        convertedNum = num*8
    elif measurementstr =='shots' or measurementstr =='shot' or measurementstr =='jigger' or measurementstr =='jiggers':
        convertedNum = num*1.5
    elif measurementstr =='pint' or measurementstr =='pints':
        convertedNum = num*16
    elif measurementstr =='qt':
        convertedNum = num*32
    elif measurementstr =='cl':
        convertedNum = num/2.957
    elif measurementstr =='ml':
        convertedNum = num/29.574
    elif measurementstr =='dl':
        convertedNum = num*3.381
    elif measurementstr =='gr':
        convertedNum = num/29.574
    elif measurementstr =='L':
        convertedNum = num*33.814
    elif measurementstr =='gal':
        convertedNum = num*128
    elif measurementstr =='lb':
        convertedNum = num*15.34
    elif measurementstr =='can':
        convertedNum = num*12
    else:
        return "null"
    return convertedNum


    
    #types:
    # 
    # proportions, dash, wedge, fill with, part, splash, fresh, parts, twist of, dashes, top up, drops, cubes, " ", fifth, small bottle, Juice of, slice, Squeeze, crushed, bottle, Float, Pinch, sprigs, stick, piece, Top, dashes, glass, chunks, cube, Top up with, Garnish, long strip, orange, mini, to taste, fill with, around rim aboout 1 pinch, pinches, (if needed), Turkish apple, Garnish with, inch, chunk, whole, handful, (Claret), Over, scoops, inch strips, Rimmed, Full Glass, Mikey bottle, large bottle, crushed, splashes, cans, Large Sprig, Measures, pods, About 8 Drops, full glass

    



main()