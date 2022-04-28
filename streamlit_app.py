import streamlit as st
import pandas as pd

# Import for navbar
from streamlit_option_menu import option_menu

# Import for dyanmic tagging
from streamlit_tags import st_tags, st_tags_sidebar

# Imports for aggrid
from st_aggrid import AgGrid
from st_aggrid import AgGrid
import pandas as pd
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode
from st_aggrid import GridUpdateMode, DataReturnMode

# Import for API calls
import requests

from dashboard_utils.gui import keyboard_to_url
from dashboard_utils.gui import load_keyboard_class

#######################################################

# The code below is for the layout of the page
if "widen" not in st.session_state:
    layout = "centered"
else:
    layout = "wide" if st.session_state.widen else "centered"

st.set_page_config(layout=layout, page_title="Zero-Shot Text Classifier", page_icon="🤗")

# Set up session state so app interactions don't reset the app

if not "valid_inputs_received" in st.session_state:
    st.session_state["valid_inputs_received"] = False

# st.image(
#     "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/balloon_1f388.png",
#     width=130,
# )

st.image(
    # "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/balloon_1f388.png",
    "logo.png",
    width=160,
)

st.sidebar.image(
    "30days_logo.jpeg",
)

st.title("Zero-Shot Text Classifier")

st.write(
    "This app allows users to classify data on the fly in an unsupervised way, via Zero-Shot Learning and the DistilBART model."
)

with st.sidebar:
    selected = option_menu(
        "",
        ["Demo", "Unlocked Mode"],
        icons=["bi-joystick", "bi-key-fill"],
        menu_icon="",
        default_index=0,
    )

keyboard_to_url(
    key="g",
    url="https://github.com/CharlyWargnier/zero-shot-classifier/blob/main/streamlit_app.py",
)
keyboard_to_url(
    key_code=190,
    url="https://github.dev/CharlyWargnier/zero-shot-classifier/blob/main/streamlit_app.py",
)

load_keyboard_class()
# st.sidebar.write("Shortcuts:")
st.sidebar.header("Shortcuts")
st.sidebar.write(
    '<span class="kbdx">G</span>  &nbsp; GitHub',
    unsafe_allow_html=True,
)

st.sidebar.write(
    '<span class="kbdx">&thinsp;.&thinsp;</span>  &nbsp; GitHub Dev (VS Code)',
    unsafe_allow_html=True,
)

st.sidebar.markdown("---")

# Sidebar
st.sidebar.header("About")
st.sidebar.markdown(
    "[Streamlit](https://streamlit.io) is a Python library that allows the creation of interactive, data-driven web applications in Python."
)

st.sidebar.header("Resources")
st.sidebar.markdown(
    """
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Cheat sheet](https://docs.streamlit.io/library/cheatsheet)
- [Book](https://www.amazon.com/dp/180056550X) (Getting Started with Streamlit for Data Science)
- [Blog](https://blog.streamlit.io/how-to-master-streamlit-for-data-science/) (How to master Streamlit for data science)
"""
)

st.sidebar.header("Deploy")
st.sidebar.markdown(
    "You can quickly deploy Streamlit apps using [Streamlit Cloud](https://streamlit.io/cloud) in just a few clicks."
)

# st.sidebar.write("Debug info:  \n")
# st.sidebar.write("- Streamlit version", f"`{st.__version__}`")

st.checkbox(
    "Widen layout",
    key="widen",
    help="Tick this box to change the layout to 'wide' mode",
)

with st.expander("Roadmap - ToDo", expanded=False):

    st.write(
        """

-   Add "ValueError" warning message when API key is not valid?
-   Check API cap limit for both pages
-   Remove To-dos
-   Remove hashed comments
-   Add markdown link in top paragraph
-   Remove space in top header
-   Add notes about datachaz

 	    """
    )
    st.markdown("")

with st.expander("Roadmap - Discard?", expanded=False):

    st.write(
        """

-   Add help tooltip for Enter API key
-   Change message in show_spinner show_spinner
-   Add a message when the model is being trained (it will take a minute)
-   Reduce font size in navbar

 	    """
    )
    st.markdown("")

with st.expander("Roadmap - Done", expanded=False):
    st.write(
        """

-   Add Markdown line in the sidebar
-   Change logo
-   Add content from 30days of streamlit from corp repo
-   Add link to 30days
-   [P1] Add session state to the unlocked mode
-   Add a variable for cap limit
-   [P2] Add link to blog post
-   Retry API key once Hugging Face has fixed the issue.
-   Add session state to allow for interactivity with the table
-   Add warning message when no labels are inputed
-   Change keyphrases as they are not great
-   P1 - Mode code in "demo" to "full mode"
-   Remove hashed comment
-   Change lenthg limit on full mode to 50
-   P1 - Make sure it's deploying fine!
-   Change icons in sidebar menu
-   Move keyboards shortcuts class to a separate file
-   Change MAX_LINES in API key section (atm fixed at 10)
-   P1 - Fix "ValueError: If using all scalar values, you must pass an index"
-   Change github.dev links to the correct repo
-   SessionState tab 1 demo
-   SessionState tab 2 own API key
	    """
    )

    st.markdown("")


def main():
    st.caption("")


if selected == "Demo":

    API_KEY = st.secrets["API_KEY"]

    API_URL = (
        "https://api-inference.huggingface.co/models/valhalla/distilbart-mnli-12-3"
    )

    headers = {"Authorization": f"Bearer {API_KEY}"}

    with st.form(key="my_form"):

        multiselectComponent = st_tags(
            label="",
            text="Add labels - 3 max",
            value=["Transactional", "Informational"],
            suggestions=[
                "Navigational",
                "Transactional",
                "Informational",
                "Positive",
                "Negative",
                "Neutral",
            ],
            maxtags=3,
        )

        new_line = "\n"
        nums = [
            "I want to buy something but I don't know what",
            "I want to order clothes from this shop",
            "How to ask a question about a product",
            "Request a refund through the Google Play store",
            "I have a question for you",
        ]

        sample = f"{new_line.join(map(str, nums))}"

        linesDeduped2 = []

        MAX_LINES = 5
        text = st.text_area(
            "Enter keyphrase to classify",
            sample,
            height=200,
            key="2",
            help="At least two keyphrases for the classifier to work, one per line, "
            + str(MAX_LINES)
            + " keyphrases max as part of the demo",
        )
        lines = text.split("\n")  # A list of lines
        linesList = []
        for x in lines:
            linesList.append(x)
        linesList = list(dict.fromkeys(linesList))  # Remove dupes
        linesList = list(filter(None, linesList))  # Remove empty

        if len(linesList) > MAX_LINES:

            st.info(
                f"❄️  Only the first "
                + str(MAX_LINES)
                + " keyprases will be reviewed. Unlock that limit by switching to 'Unlocked Mode'"
            )

        linesList = linesList[:MAX_LINES]

        submit_button = st.form_submit_button(label="Submit")

    if not submit_button and not st.session_state.valid_inputs_received:
        st.stop()

    elif submit_button and not text:
        st.warning("❄️ There is no keyphrases to classify")
        st.session_state.valid_inputs_received = False
        st.stop()

    elif submit_button and not multiselectComponent:
        st.warning("❄️ You have not added any labels, please add some! ")
        st.session_state.valid_inputs_received = False
        st.stop()

    elif submit_button and len(multiselectComponent) == 1:
        st.warning("❄️ Please make sure to add at least two labels for classification")
        st.session_state.valid_inputs_received = False
        st.stop()

    elif submit_button or st.session_state.valid_inputs_received:

        if submit_button:
            st.session_state.valid_inputs_received = True

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            # Unhash to check status codes from the API response
            # st.write(response.status_code)
            return response.json()

        listtest = ["I want a refund", "I have a question"]
        listToAppend = []

        for row in linesList:
            output2 = query(
                {
                    "inputs": row,
                    "parameters": {"candidate_labels": multiselectComponent},
                    "options": {"wait_for_model": True},
                }
            )

            listToAppend.append(output2)

            df = pd.DataFrame.from_dict(output2)

        st.success("✅ Done!")

        df = pd.DataFrame.from_dict(listToAppend)

        st.markdown("## Check classifier results")

        cs, c1 = st.columns([2, 2])

        with cs:

            @st.cache
            def convert_df(df):
                # IMPORTANT: Cache the conversion to prevent computation on every rerun
                return df.to_csv().encode("utf-8")

            csv = convert_df(df)  #

            st.caption("")

            st.download_button(
                label="Download results as CSV",
                data=csv,
                file_name="results.csv",
                mime="text/csv",
            )

        gb = GridOptionsBuilder.from_dataframe(df)
        # enables pivoting on all columns, however i'd need to change ag grid to allow export of pivoted/grouped data, however it select/filters groups
        gb.configure_default_column(
            enablePivot=True, enableValue=True, enableRowGroup=True
        )
        gb.configure_selection(selection_mode="multiple", use_checkbox=True)
        gb.configure_side_bar()  # side_bar is clearly a typo :) should by sidebar
        gridOptions = gb.build()

        response = AgGrid(
            df,
            gridOptions=gridOptions,
            enable_enterprise_modules=True,
            update_mode=GridUpdateMode.MODEL_CHANGED,
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
            height=400,
            fit_columns_on_grid_load=False,
            configure_side_bar=True,
        )

elif selected == "Unlocked Mode":

    with st.form(key="my_form"):
        API_KEY2 = st.text_input("Enter API key")
        # API_KEY = st.secrets["API_KEY"]

        API_URL = (
            "https://api-inference.huggingface.co/models/valhalla/distilbart-mnli-12-3"
        )

        headers = {"Authorization": f"Bearer {API_KEY2}"}

        multiselectComponent = st_tags(
            label="",
            text="Add labels - 3 max",
            value=["Transactional", "Informational"],
            suggestions=[
                "Navigational",
                "Transactional",
                "Informational",
                "Positive",
                "Negative",
                "Neutral",
            ],
            maxtags=3,
        )

        new_line = "\n"
        nums = [
            "I want to buy something but I don't know what",
            "I want to order clothes from this shop",
            "How to ask a question about a product",
            "Request a refund through the Google Play store",
            "I have a question for you",
        ]

        sample = f"{new_line.join(map(str, nums))}"

        linesDeduped2 = []

        MAX_LINES_FULL = 50
        text = st.text_area(
            "Enter keyphrase to classify",
            sample,
            height=200,
            key="2",
            help="At least two keyphrases for the classifier to work, one per line, "
            + str(MAX_LINES_FULL)
            + " keyphrases max in 'unlocked mode'. You can tweak 'MAX_LINES_FULL' in the code to change this",
        )

        lines = text.split("\n")  # A list of lines
        linesList = []
        for x in lines:
            linesList.append(x)
        linesList = list(dict.fromkeys(linesList))  # Remove dupes
        linesList = list(filter(None, linesList))  # Remove empty

        if len(linesList) > MAX_LINES_FULL:
            st.info(
                f"❄️ Only the first "
                + str(MAX_LINES_FULL)
                + " keyprases are reviewed. Tweak 'MAX_LINES_FULL' in the code to change this"
            )

            linesList = linesList[:MAX_LINES_FULL]

        submit_button = st.form_submit_button(label="Submit")

    if not submit_button and not st.session_state.valid_inputs_received:
        st.stop()

    elif submit_button and not text:
        st.warning("❄️ There is no keyphrases to classify")
        st.session_state.valid_inputs_received = False
        st.stop()

    elif submit_button and not multiselectComponent:
        st.warning("❄️ You have not added any labels, please add some! ")
        st.session_state.valid_inputs_received = False
        st.stop()

    elif submit_button and len(multiselectComponent) == 1:
        st.warning("❄️ Please make sure to add at least two labels for classification")
        st.session_state.valid_inputs_received = False
        st.stop()

    elif submit_button or st.session_state.valid_inputs_received:

        if submit_button:

            st.session_state.valid_inputs_received = True

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            # Unhash to check status codes from the API response
            # st.write(response.status_code)
            return response.json()

        listtest = ["I want a refund", "I have a question"]
        listToAppend = []

        for row in linesList:
            output2 = query(
                {
                    "inputs": row,
                    "parameters": {"candidate_labels": multiselectComponent},
                    "options": {"wait_for_model": True},
                }
            )

            listToAppend.append(output2)

            df = pd.DataFrame.from_dict(output2)

        st.success("✅ Done!")

        df = pd.DataFrame.from_dict(listToAppend)

        st.markdown("## Check classifier results")

        cs, c1 = st.columns([2, 2])

        with cs:

            @st.cache
            def convert_df(df):
                # IMPORTANT: Cache the conversion to prevent computation on every rerun
                return df.to_csv().encode("utf-8")

            csv = convert_df(df)  #

            st.caption("")

            st.download_button(
                label="Download results as CSV",
                data=csv,
                file_name="results.csv",
                mime="text/csv",
            )

        gb = GridOptionsBuilder.from_dataframe(df)
        # enables pivoting on all columns, however i'd need to change ag grid to allow export of pivoted/grouped data, however it select/filters groups
        gb.configure_default_column(
            enablePivot=True, enableValue=True, enableRowGroup=True
        )
        gb.configure_selection(selection_mode="multiple", use_checkbox=True)
        gb.configure_side_bar()  # side_bar is clearly a typo :) should by sidebar
        gridOptions = gb.build()

        response = AgGrid(
            df,
            gridOptions=gridOptions,
            enable_enterprise_modules=True,
            update_mode=GridUpdateMode.MODEL_CHANGED,
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
            height=400,
            fit_columns_on_grid_load=False,
            configure_side_bar=True,
        )

if __name__ == "__main__":
    main()
