from matplotlib import pyplot as plt
import numpy as np
import streamlit as st
import baroncs as bcs

st.markdown(
    """
The following is a charge state calculator. Choose an element and the charge state distribution will be calculated. 
It is based on the following paper: 

[Charge exchange of very heavy ions in carbon 
foils and in the residual gas of GANIL cyclotrons](https://www.sciencedirect.com/science/article/pii/016890029390622O)

The code is available on [GitHub](https://github.com/jako4295/baroncs).
"""
)

option = st.selectbox("What element would you like to test?", np.arange(6, 93))

charge_obj = bcs.ChargeState()
distx, disty = charge_obj.charge_state_distribution(
    atomic_nr=option,  # atomic number of the projectile
    energy=4.2,  # energy of the projectile in MeV/u
    e0=931.5,  # rest energy in MeV
    dist_onesided_len=5,  # length of the on each side of the mean charge state
    plot=False,  # plot the distribution
)

fig, ax = plt.subplots()
ax.bar(distx, disty * 100)
ax.set_title(f"Charge State Distribution for atom number {option}")
ax.set_ylabel("Percentage")
ax.set_xlabel("Charge State")
ax.text(
    s=f"Mean Charge: {charge_obj.mean_charge_state(option):.2f},\nStandard Deviation: {charge_obj.std_charge_state(option):.2f}",
    x=0.05,
    y=0.95,
    transform=ax.transAxes,
    va="top",
    ha="left",
)
st.pyplot(fig)

# df = charge_obj.dataframe()

# st.dataframe(df)
