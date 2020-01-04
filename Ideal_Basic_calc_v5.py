from __future__ import division 
from CoolProp.CoolProp import PropsSI
from CoolProp.Plots import StateContainer
import matplotlib.pyplot as plt




# System 1 Inputs

Ref_1   = 'R410a'

T_evp_w = 15       # Compare the evaportor working temp to Refrigerant 2

Q_L_1   = 2.5       # Cooling capacity in kW

T_evp_1 = 0        # Evaporator working temp  
T_con_1 = 57        # Condensor working title



# System 1 Inputs

Ref_2 = 'R290'

Q_L_2   = 2.5       # Cooling capacity in kW

T_evp_2   = 0        # Evaporator working temp  
T_con_2  = 57        # Condensor working title





#Setup

evap_1 = []
COP_1 = []

evap_2 = []
COP_2 = []
COP_r = 0 # For print out generator


# Print out generator

def ideal_printout(Q_L, T_evp, T_con, Ref, COP_r):

    K_evp = T_evp + 273
    K_con = T_con + 273
    
    #Pressures

    P3 = PropsSI('P','T',K_con ,'Q', 0 ,Ref)
    P4 = PropsSI('P','T',K_evp ,'Q', 1 ,Ref)
    p_r = round(P3/P4,2)


    print('*** Ideal Cycle ***', '\n')

    print(Ref,'\n')

    print('Condensor Condtions  |', round(P3/1000000,2),'MPa', T_con,"C")
    print('Evaporator Condtions |', round(P4/1000000,2),'MPa',T_evp,'C','\n')
    print("Pressure Ratio",p_r, '\n')


    # State 1

    h1 = PropsSI('H','T', K_evp,'Q', 1,Ref)
    s1 = PropsSI('S','T', K_evp,'Q', 1,Ref)


    # State 2

    h2 = PropsSI('H','P', P3,'S', s1 ,Ref)




    # State 3


    h3 = PropsSI('H','T', K_con,'Q', 0,Ref)


    # State 4


    h4 = h3


    # Work Calculation


    mF = (Q_L*1000) / (h1 - h4)

    print('Mass Flow = ',round(mF,2),'kg/s','\n')

    Q_H = mF*(h2 - h3)
    Q_H = Q_H/1000

    print('Cooling Input    |', Q_L,'kW')
    print('Heating Output   |',round(Q_H,2),'kW')

    Win = mF*(h2 - h1)
    Win = Win/1000
    print('Work Input       |',round(Win,2),'kW','\n')

    #COP

    
    COP = (h1 - h4) / (h2 - h1)
    COP_r = COP
    
    
    print('COP',round(COP_r,2),'\n')
    print('******', '\n')
    return COP_r



# Ideal cycle iteration generator

def ideal(Q_L, T_evp, T_con, Ref, evap_lst, COP_lst):
    
    
    K_evp = T_evp + 273
    K_con = T_con + 273
    
    #Pressures

    P3 = PropsSI('P','T',K_con ,'Q', 0 ,Ref)
    P4 = PropsSI('P','T',K_evp ,'Q', 1 ,Ref)
    p_r = round(P3/P4,2)

    #print('Condensor Condtions  |', round(P3/1000000,2),'MPa', T_con,"C")
    #print('Evaporator Condtions |', round(P4/1000000,2),'MPa',T_evp,'C','\n')


    # State 1

    h1 = PropsSI('H','T', K_evp,'Q', 1,Ref)
    s1 = PropsSI('S','T', K_evp,'Q', 1,Ref)

    # State 2

    h2 = PropsSI('H','P', P3,'S', s1 ,Ref)

    # State 3


    h3 = PropsSI('H','T', K_con,'Q', 0,Ref)

    # State 4

    h4 = h3

    # Work Calculation
    
    mF = (Q_L*1000) / (h1 - h4)


    Q_H = mF*(h2 - h3)
    Q_H = Q_H/1000


    Win = mF*(h2 - h1)
    Win = Win/1000

    #COP


    COP = (h1 - h4) / (h2 - h1)
    COP = round(COP,2)
    
    #append lists
    evap_lst.append(T_evp)
    COP_lst.append(COP)
    



# Generator

for x in range(0,20):
    
    T_evp_1 = T_evp_1 + 1
    ideal(Q_L_1, T_evp_1, T_con_1, Ref_1, evap_1, COP_1)
    
    T_evp_2 = T_evp_2 + 1
    ideal(Q_L_2, T_evp_2, T_con_2, Ref_2, evap_2, COP_2)
   
 
# Find equiverlant working temp for Ref 2

COP_r = ideal_printout(Q_L_1, T_evp_w, T_con_1, Ref_1, COP_r)
COP_r = round(COP_r,2)



# Draw a line with COP_r identifign the evaporating temp and COP


# Graphical Lines
#       min values
COP_min = [COP_1[0],COP_2[0]]
COP_m = min(COP_min)
evp_min = [evap_1[0],evap_2[0]]
evp_m = min(evp_min)
# draw a line
COP_line_x = [T_evp_w,T_evp_w,evp_m] 
COP_line_y = [COP_m,COP_r, COP_r]
plt.plot(COP_line_x,COP_line_y)



#plt.title(Ref)
plt.plot(evap_1,COP_1, label = Ref_1)
plt.plot(evap_2,COP_2, label = Ref_2)

plt.ylabel('COP')
plt.xlabel('Evap Temp')
plt.legend()
plt.show()