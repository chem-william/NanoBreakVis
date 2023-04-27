from pathlib import Path
from datetime import date
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import mpld3
from pydantic import ValidationError
import streamlit_pydantic
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
    col1, col2 = st.columns((3, 1))
    col1.title("NanoBreakVis - Visualizing break-junction experiments")

    with col1.expander("How to Use This"):
        col1.write(Path("README.md").read_text())

    col1.subheader("Upload your CSV from a break-junction experiment")
    uploaded_files = col1.file_uploader(
        "Drag and Drop or Click to Upload", type=".csv", accept_multiple_files=True
    )
    data_sets = []
    if not uploaded_files:
        col1.info(
            "Using example data. Upload one or more files above to use your own data!"
        )
        tunneling = load_data("example_tunneling_data.csv")
        data_sets.append(tunneling)
        molecular = load_data("example_molecular_data.csv")
        data_sets.append(molecular)
    else:
        col1.success("Uploaded your file(s)!")
        progress_text = "Loading files(s).."
        progress_bar = col1.progress(0, text=progress_text)
        # uploaded_files = [uploaded_files]  # XXX: hack until decision on multiple files
        for idx, uploaded_file in enumerate(uploaded_files):
            loaded_dataset = load_data(uploaded_file)
            data_sets.append(loaded_dataset)
            progress_bar.progress(idx / len(uploaded_files) * 100, text=progress_text)

    logarize = not col1.checkbox(r"Don't take log$_{10}$ of data")
    bins = col1.slider(
        "📊 Amount of bins:",
        4,
        512,
        128,
        help="Selects the amount of bins that are used to create the 1D-histogram of the uploaded data",
    )
    log_range = col1.slider(
        "📏 Select range:",
        -15.0,
        10.0,
        (-10.0, -0.5),
        help="Selects the range of the conductance that is used to display the 1D-histogram of the uploaded data",
    )
    fig, ax_1dhist = plt.subplots()
    for dataset in data_sets:
        if logarize:
            dataset = np.log10(dataset, where=dataset > 0)
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
    col1.subheader("1D-histogram")
    container1 = col1.container()
    with container1:
        fig_html = mpld3.fig_to_html(fig)
        components.html(fig_html, height=800)

    # col2.subheader("Information about dataset")
    # from_model_tab, from_instance_tab = st.tabs(
    #     ["Form inputs from model", "Form inputs from instance"]
    # )
    #
    container2 = col2.container()
    with container2:
        with st.form(key="pydantic_form"):
            data = streamlit_pydantic.pydantic_input(
                key="my_input_model", model=Experiment
            )
            with st.expander("Current Input State", expanded=False):
                st.json(data)
            submit_button = st.form_submit_button(
                label="Submit", help="Submit the inputted information"
            )


if __name__ == "__main__":
    st.set_page_config(
        "Break-junction visualizer by William Bro-Jørgensen",
        "📊",
        initial_sidebar_state="expanded",
        layout="wide",
    )
    main()
