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

The default energy (4.2 MeV/u) and rest energy (931.5 MeV) corresponds to the energies for the LINAC3 at CERN.
"""
)
charge_obj = bcs.ChargeState()
df = charge_obj.dataframe()
elements_options = [str(nr) + " - " + nam for nam, nr in df["Atomic Number"].items()]

col1, col2, col3 = st.columns(3)
with col1:
    energy_input = st.text_input("Energy (MeV/u):", value=4.2)
    try:
        energy_input = float(energy_input)
    except ValueError:
        st.error("Please enter a number")
with col2:
    e0_input = st.text_input("Rest Energy (MeV):", value=931.5)
    try:
        e0_input = float(e0_input)
    except ValueError:
        st.error("Please enter a number")
with col3:
    element_input = st.selectbox(
        "What element would you like to test?",
        elements_options,
        index=int(np.where(df.index == "Lead")[0][0]),
    )
    # convert to atomic number
    element_input = int(element_input.split(" ")[0])

distx, disty = charge_obj.charge_state_distribution(
    atomic_nr=element_input,  # atomic number of the projectile
    energy=energy_input,  # energy of the projectile in MeV/u
    e0=e0_input,  # rest energy in MeV
    dist_onesided_len=5,  # length of the on each side of the mean charge state
    plot=False,  # plot the distribution
)

chosen_element = df["Atomic Number"][df["Atomic Number"] == element_input].index[0]

fig, ax = plt.subplots()
ax.bar(distx, disty * 100)
ax.set_title(f"Charge State Distribution for {chosen_element.lower()}")
ax.set_ylabel("Percentage")
ax.set_xlabel("Charge State")
ax.text(
    s=f"Mean Charge: {charge_obj.mean_charge_state(element_input):.2f},\nStandard Deviation: {charge_obj.std_charge_state(element_input):.2f}",
    x=0.05,
    y=0.95,
    transform=ax.transAxes,
    va="top",
    ha="left",
)
st.pyplot(fig)

st.markdown(
    """
The following is a table showing characteristics for each element. It is calculated using the energy and rest energy input above.
"""
)
df_update = charge_obj.dataframe(energy=energy_input, e0=e0_input)
st.dataframe(df_update)
