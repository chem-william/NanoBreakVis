from pathlib import Path
from datetime import date
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import mpld3
from pydantic import ValidationError
import streamlit.components.v1 as components

from experiment import Experiment, Solvent

sns.set_style(style="white")
sns.set(
    style="ticks",
    rc={
        "font.family": "Liberation Sans",
        "font.size": 40,
        "axes.linewidth": 2,
        "lines.linewidth": 3,
    },
    font_scale=1.5,
    palette=sns.color_palette("Set2"),
)


@st.cache_data
def load_data(file_name: str):
    return np.genfromtxt(file_name, delimiter=",", dtype=None)


@st.cache_data
def create_1d_histograms(data, log_range: (float, float), bins: int):
    histogram, binedges = np.histogram(data, range=log_range, bins=bins)
    binedges = (binedges[1:] + binedges[:-1]) / 2

    return histogram, binedges


@st.cache_data
def create_2d_histograms(data, log_range: (float, float), bins: int):
    hists_2d = []
    for trace in data:
        H, *_ = np.histogram2d(
            trace, np.arange(len(trace)), bins=bins, range=[[-10, 0.0], [0, len(trace)]]
        )
        hists_2d.append(H)

    hists_2d = np.array(hists_2d)
    return hists_2d


def main() -> None:
    st.title("NanoBreakVis - Visualizing break-junction experiments")

    with st.expander("How to Use This"):
        st.write(Path("README.md").read_text())

    st.subheader("Upload your CSV from Fidelity")
    uploaded_files = st.file_uploader(
        "Drag and Drop or Click to Upload", type=".csv", accept_multiple_files=True
    )
    data_sets = []
    if not uploaded_files:
        st.info(
            "Using example data. Upload one or more files above to use your own data!"
        )
        tunneling = load_data("example_tunneling_data.csv")
        data_sets.append(tunneling)
        molecular = load_data("example_molecular_data.csv")
        data_sets.append(molecular)
    else:
        st.success("Uploaded your file(s)!")
        progress_text = "Loading files(s).."
        progress_bar = st.progress(0, text=progress_text)
        # uploaded_files = [uploaded_files]  # XXX: hack until decision on multiple files
        for idx, uploaded_file in enumerate(uploaded_files):
            loaded_dataset = load_data(uploaded_file)
            data_sets.append(loaded_dataset)
            progress_bar.progress(idx / len(uploaded_files) * 100, text=progress_text)

    # with st.expander("Raw Dataframe"):
    #     st.write(df)

    # create json of data
    exp_data = {
        "date": date.today(),
        "name_experimentalist": "John Smith",
        "name_principal_investigator": "Jane Doe",
        "method": "Some method",
        "analyte": {"smiles": "C1=CC=CC=C1", "concentration": 0.1},
        "temperature": 298.15,
        "pressure": 1.0,
        "solvent": {"smiles": "CCO", "supplier": "Sigma-Aldrich"},
        "bias_voltage": 1.0,
        "acquisition_rate": 100.0,
        "pulling_rate": 1.0,
        "electrode": {
            "material": "gold",
            "purity": 99.99,
            "manufacturer": "Some company",
            "diameter": 1.0,
        },
        "procedure": "Some procedure",
    }
    try:
        experiment = Experiment(**exp_data)
    except ValidationError as e:
        st.json(e.json())
    st.json(experiment.json())

    logarize = not st.checkbox(r"Don't take log$_{10}$ of data")
    bins = st.slider(
        "📊 Amount of bins:",
        4,
        512,
        128,
        help="Selects the amount of bins that are used to create the 1D-histogram of the uploaded data",
    )
    log_range = st.slider(
        "📏 Select range:",
        -15.0,
        10.0,
        (-10.0, 0.0),
        help="Selects the range of the conductance that is used to display the 1D-histogram of the uploaded data",
    )
    fig, ax_1dhist = plt.subplots()
    g1, g2 = st.columns((1, 1))
    for dataset in data_sets:
        if logarize:
            dataset = np.log10(dataset)
        histogram, binedges = create_1d_histograms(
            dataset, log_range=log_range, bins=bins
        )

        ax_1dhist.plot(binedges, histogram)

    ax_1dhist.set_ylabel("Counts")
    ax_1dhist.set_xlim(log_range)
    ax_1dhist.set_ylim(0)
    ax_1dhist.set_xlabel(r"Conductance")
    ax_1dhist.spines["top"].set_visible(False)
    ax_1dhist.spines["right"].set_visible(False)
    st.subheader("1D-histogram")
    fig_html = mpld3.fig_to_html(fig)
    components.html(fig_html, height=800)


if __name__ == "__main__":
    st.set_page_config(
        "Break-junction visualizer by William Bro-Jørgensen",
        "📊",
        initial_sidebar_state="expanded",
        layout="wide",
    )
    main()
