from ExcitonFitting import Exciton, ExcitonGroup, Config, Lineshape
VoigtLineshape = Lineshape.VoigtLineshape
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from PetrizzeTheme import petrizze_template

petrizze_template()

def create_true_excitons(i=0):
    true_excitons = Config.TRUE_EXCITON_GROUP.copy()
    true_excitons["T"].energy = Config.ENERGY_RANGE_B[i]

    return true_excitons


def go():
    n_frames = len(Config.ENERGY_RANGE_B)

    x = Config.X_RANGE

    fig, ax = plt.subplots()

    def update(frame):
        true_excitons = create_true_excitons(frame)

        y = true_excitons.spectra(x)

        ax.clear()
        ax.plot(x, y, label='True Excitons')

        for exciton in true_excitons.exciton_list:
            y_e = exciton.spectra(x)
            ax.plot(x, y_e, '--', label=exciton.label)

        ax.legend()
        ax.set_ylabel('Intensity (a.u.)')
        ax.set_xlabel('Energy (eV)')
    
    ani = FuncAnimation(fig, update, frames=n_frames, interval=50)
    ani.save("Out\\Plots\\Animation.gif", writer="pillow")

go()
