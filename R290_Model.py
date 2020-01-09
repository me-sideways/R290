import CoolProp
from CoolProp.CoolProp import PropsSI
from CoolProp.HumidAirProp import HAPropsSI
import matplotlib.pyplot as plt


''' R290 Chiller Model v1.3

Jason Beattie | jason.beattie@protonmail.com 8/01/2020

Use this is calculate the highest temp that the cooling coil can be to get the room to a confortable Temp/RH

R32 GWP : 675
R290 GWP: 3


v1.3

Include COP calculation for R290 and R32, water flow calculation

Using ideal cycles for a direct comparision, super heat and subcooling will need to be varied
'''


''' Dew Point for comfort calculation

'''
#Inputs for dewpoint calculation


Tair_comfort  = 25
RH_comfort    = 0.65 # > 70RH is uncomfortable

#Dew Point Graph Setup

T_air = 15 # Start Temp
T_range = 20 # dT of range

# Setup

DP_lst = []
Tair_lst = []




def dewpoint(T_air, RH):

    '''

    Dew Point Calculator
    Simple Inputs
    
    Pv = RH * Pg(@ Tair_1)
    T_dp = T(sat) @ Pv


    '''
    T_air = T_air + 273
    Psat = PropsSI('P','T', T_air,'Q',1 ,'water')
    #print('Psat',Psat/1000, 'KPa')

    Pv = RH * Psat
    #print('Psat',Pv/1000, 'KPa')

    T_dp = PropsSI('T','P', Pv,'Q',1 ,'water')
    T_dp = round(T_dp - 273,2)
    #print('Dew Point |',T_dp,'C')

    return T_dp
    
def dewpoint_list(T_air, RH):
    ''' 
    Appends Lists to Chart DP againt air temp
    '''

    Psat = PropsSI('P','T', T_air,'Q',1 ,'water')
    #print('Psat',Psat/1000, 'KPa')

    Pv = RH * Psat
    #print('Psat',Pv/1000, 'KPa')

    T_dp = PropsSI('T','P', Pv,'Q',1 ,'water')
    #print('Dew Point |', T_dp - 273)
    Tair_lst.append(T_air - 273)
    DP_lst.append(T_dp - 273)
       
def plot_dewpoint():
    ''' Dew Point Plotter

    '''
    for temp in range(T_air,T_range + T_air +1):
            
        dewpoint_list(temp + 273,RH_1)
        

    plt.plot(Tair_lst,DP_lst)

    plt.ylabel('Dew Point')
    plt.xlabel('Air Temp')
    plt.legend()
    plt.show()


# Print Dewpoint Calculation

Tdp_comfort = dewpoint(Tair_comfort,RH_comfort)  # 
print('*** Dew Point Calculation ***','\n')
print('Comfort Air')
print(Tair_comfort,'C',RH_comfort*100,'%RH','\n')
print('Dew Point |',Tdp_comfort,'C','\n')

# *** End Dew Point Calculation ***


# Water-Air Heat Exchanger Design | Ignore for now




''' Cooling and Dehumidification 
 
Calculate the water taken out of the air, with the inital condtion in a stead state cycle

This is more for sanity check 

Notes
DEW POINT TEMP CAN BE THE AVERGE in the water loop
 
*** As long as the center of the core is dehumifing
 
T_water_hi = T_dp + dT_water / 2
T_water_lo = T_dp - dT_water / 2
T_water_average = T_dp
 


   
'''


# Air

T_air_in = 27       # Temp of hot room air
air_RH_in = 0.75 # relative humidity of hot room air

V_fan = 6 # m3 / min

# Setup

T_air_in = T_air_in + 273
T_air_out = Tdp_comfort + 273



def cool_dehum(T_air_in,air_RH_in,V_fan):

    ''' Notes
    
    Not knowing Qout

    Dry air mass balance:   m_air_in = m_air_out = m_air
    Air Mass Calculation:   m_air = V/v_spec = V_fan / v_in
    Water Mass Balance:     ( m_air_in * w_in ) = ( m_air_out * w_out ) + m_condensate   = >            m_condensate = m_air * (w_in - w_out)
    Energy Balance:         Q =  [ m_air * ( h_air_in - h_air_out ) ] - m_condensate * h_condensate

    '''


    h_air_in = HAPropsSI('H','T',T_air_in,'P',101325,'R',air_RH_in)
    #print('h_air_in', h_air_in)

    h_air_out = HAPropsSI('H','T',T_air_out,'P',101325,'R',1)
    #print('h_air_out',h_air_out)

    w_in = HAPropsSI('W','T',T_air_in,'P',101325,'R',air_RH_in)
    #print('w_in',w_in)

    w_out = HAPropsSI('W','T',T_air_out,'P',101325,'R',1)
    #print('w_out',w_out)

    v_in = HAPropsSI('V','T',T_air_in,'P',101325,'R',air_RH_in)
    #print('v_in',v_in)

    m_air = V_fan / v_in
    #print('m_air',m_air)

    m_condensate = m_air * (w_in - w_out)
    #print('m_condensate', m_condensate)

    h_condensate = PropsSI('H','T',T_air_out,'Q', 0,'water')
    #print('h_condensate', h_condensate)

    Q_out = ( m_air * ( h_air_in - h_air_out ) ) - m_condensate * h_condensate
    Q_out = round(((Q_out/1000)/60),2)
    print(Q_out,'kW')

    print(round(m_condensate,3),'L/min')





# cool_dehum(T_air_in,air_RH_in,V_fan)

''' COP comparision with R32 and R290 

R290 is slightly more effiecnt thant R32, but will have more losses from pumping the cooling water and HX losses. 

To mitigate this there has be a rise in the evaportator temp to compansate for these losses and compete for engery useage against R32.

The R290 systen CAN NOT use more power for a given Cooling Capacity than R32


Technical Notes:

Same condensor working temp

'''


# System Comparision


T_con = 45                  # Condensor working temp
Q_L   = 2.5                 # Cooling capacity in kW
water_dT = 4                # Cooling water dT

#Comparision

Ref_1   = 'R32'              # Control Sytem (Base Line)
Ref_2    = 'R290'            # System to be compared (KEEP R290 or higher performing gas here bugs if switched)

T_evp_1 = 15                 # Working Temp of Evaporator for system 1 to compare



# Water Loop Setup



T_water_lo = Tdp_comfort - (water_dT / 2)

T_evp_2 = T_water_lo
T_evp_1 = T_evp_1

T_con = T_con


# End Cooling and Humidifing section




def ideal_printout(Q_L, T_evp, T_con, Ref):

    K_evp = T_evp + 273
    K_con = T_con + 273
    
    #Pressures

    P3 = PropsSI('P','T',K_con ,'Q', 0 ,Ref)
    P4 = PropsSI('P','T',K_evp ,'Q', 1 ,Ref)
    p_r = round(P3/P4,2)

    print('***',Ref,'Ideal Cycle ***', '\n')
    #print(Ref,'\n')
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
    
    print('COP',round(COP_r,2),'\n','\n')
    print('*** End Ideal Cycle Calculation for',Ref,'***', '\n')
    return COP_r



ideal_printout(Q_L, T_evp_1, T_con, Ref_1)
ideal_printout(Q_L, T_evp_2, T_con, Ref_2)


## Add water loop flow rate calculation
''' Water Loop Calculation

Find the mass flow needed to maintain a specific dT


Use dT & water temps from cool_dehum section

Ignore pumping losses for now


Q = m_water * (h_water_hi - h_water_low)
'''

# Inputs

Q_water = Q_L #+ Q_pumping
#water_dT = water_dT
#T_water_lo = Tdp_comfort - (water_dT / 2)
T_water_hi = Tdp_comfort + (water_dT / 2)

def water_flow(Q_water, T_water_high, T_water_low):

    print('*** Start Water Loop Flow Calculation ***','\n')
    h_water_hi = PropsSI('H','T',T_water_hi + 273,'Q', 0,'water') # Aprox a saturated liquid 
    h_water_lo = PropsSI('H','T',T_water_lo + 273,'Q', 0,'water') # Aprox a saturated liquid 
    #print(h_water_hi/1000)
    #print(h_water_lo/1000)
    m_water = (Q_water*1000) / (h_water_hi - h_water_lo)

    print('Water High |',T_water_hi,'C')
    print('Water Low  |',T_water_lo,'C')
    print('Water Flow |',round(m_water*60,2), 'L/min','\n')
    print('*** End Water Loop Flow Calculation ***')
    return m_water

water_flow(Q_water, T_water_hi, T_water_lo)

## Add model room to dehumify and cool
# Double check COP numbers



