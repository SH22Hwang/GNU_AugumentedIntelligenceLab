from mpIdea import *

hands, mp_hands, mp_drawings = prepareMediaPipeTools()
solution(hands, mp_hands, mp_drawings, *Calibrator.calibrate())

hands.close()

