import streamlit as st
import pandas as pd

# Import for navbar
from streamlit_option_menu import option_menu

# Import for dyanmic tagging
from streamlit_tags import st_tags, st_tags_sidebar

# Import for keyboard shortcuts
# import streamlit.components.v1 as components

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

st.image(
    "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/325/balloon_1f388.png",
    width=150,
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

#######################################

keyboard_to_url(
    key="g",
    url="https://github.com/CharlyWargnier/zero-shot-classifier/blob/main/streamlit_app.py",
)
keyboard_to_url(
    key_code=190,
    url="https://github.dev/CharlyWargnier/zero-shot-classifier/blob/main/streamlit_app.py",
)

load_keyboard_class()
st.sidebar.write("Shortcuts:")
st.sidebar.write(
    '<span class="kbdx">G</span>  &nbsp; GitHub',
    unsafe_allow_html=True,
)

st.sidebar.write(
    '<span class="kbdx">&thinsp;.&thinsp;</span>  &nbsp; GitHub Dev (VS Code)',
    unsafe_allow_html=True,
)

st.sidebar.write("Debug info:  \n")
st.sidebar.write("- Streamlit version", f"`{st.__version__}`")

#######################################################

st.checkbox(
    "Widen layout",
    key="widen",
    help="Tick this box to change the layout to 'wide' mode",
)


with st.expander("Roadmap - ToDo", expanded=False):

    st.write(
        """

-   P1 - Mode code in "demo" to "full mode"
-   Remove hashed comment
-   Change keyphrases as they are not great
-   Remove space in top header
-   Add warning message when API key is not valid?
-   Add notes about datachaz
-   Add link to blog post
-   Add link to 30days

 	    """
    )
    st.markdown("")

with st.expander("Roadmap - Optional", expanded=False):

    st.write(
        """

-   Add link to streamlit.io
-   Change message in show_spinner show_spinner
-   Add a message when the model is being trained (it will take a minute)
-   Reduce font size in navbar

 	    """
    )
    st.markdown("")

with st.expander("Roadmap - Done", expanded=False):
    st.write(
        """
-   Add warning message when no labels are inputed
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
    st.write("")
    # pages = {
    #    "👾 Zero-Shot Demo": demo,
    #    "🔑 Unlock with your API key": No_demo_API_key,
    # }


# region Demo with Streamlit API key

if selected == "Demo":
    # def demo():

    API_KEY = st.secrets["API_KEY"]

    API_URL = (
        "https://api-inference.huggingface.co/models/valhalla/distilbart-mnli-12-3"
    )

    headers = {"Authorization": f"Bearer {API_KEY}"}

    # @st.experimental_memo(ttl=600)
    # @st.cache(show_spinner=True, allow_output_mutation=True)
    # def query(payload):
    #     response = requests.post(API_URL, headers=headers, json=payload)
    #     return response.json()

    # endregion Streamlit_API_KEY

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
            "I have a question for you or to you",
        ]

        sample = f"{new_line.join(map(str, nums))}"

        # st.caption("Enter keyword or keyphrase - One per line - 5 lines max")
        linesDeduped2 = []
        MAX_LINES = 10
        text = st.text_area(
            "Enter keyphrase to classify",
            sample,
            height=200,
            key="2",
            help="At least two keyphrases for the classifier to work, One per line, 10 keyphrases max as part of the demo",
        )
        lines = text.split("\n")  # A list of lines
        linesList = []
        for x in lines:
            linesList.append(x)
        linesList = list(dict.fromkeys(linesList))  # Remove dupes
        linesList = list(filter(None, linesList))  # Remove empty

        if len(linesList) > MAX_LINES:
            st.info(
                f"🚨 Only the first 10 keyprases will be reviewed. Unlock that limit by adding your HuggingFace your API key - See left side-bar"
            )

            linesList = linesList[:MAX_LINES]

        submit_button = st.form_submit_button(label="Submit")

    if not submit_button:
        st.stop()

    elif submit_button and not multiselectComponent:
        st.warning("You have not added any labels, please add some! ")
        st.stop()

    elif submit_button and len(multiselectComponent) == 1:
        st.warning("Please make sure to add at least two labels for classification")
        st.stop()

    else:

        # @st.experimental_memo(ttl=600)
        # @st.experimental_singleton
        # @st.experimental_memo
        # @st.cache(show_spinner=True, allow_output_mutation=True)
        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            # Unhash to check status codes from the API response
            # st.write(response.status_code)
            return response.json()

        listtest = ["I want a refund", "I have a question"]

        listToAppend = []

        # You can find the list of parameters for HuggingFace API inference here -> https://huggingface.co/docs/api-inference/detailed_parameters

        # import time

        # with st.spinner("Fetching results. It may take a while!"):
        #     time.sleep(5)
        #     st.success("✅ Done!")

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

        ##############################

        # # new df from the column of lists
        # split_df = pd.DataFrame(df["labels"].tolist())
        # # display the resulting df
        # split_df
        #
        # st.table(split_df)
        #
        # ##############################
        #
        # # new df from the column of lists
        # split_df = pd.DataFrame(df["labels"].tolist(), columns=["v1", "v2", "v3"])
        # # concat df and split_df
        # dfNew = pd.concat([df, split_df], axis=1)
        # # display df
        # dfNew

        # df = df.reset_index().rename(
        #     columns={"sequence": "keyphrase", "scores": "label scores"}
        # )
        
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

# endregion Demo with Streamlit API key

# region Custom API key

elif selected == "Full unlocked version":
    # def No_demo_API_key():

    with st.form(key="my_form"):

        ####### WORKING #####################################

        # API_KEY = st.secrets["API_KEY"]

        API_KEY = st.text_input("Enter API key")

        API_URL = (
            "https://api-inference.huggingface.co/models/valhalla/distilbart-mnli-12-3"
        )

        headers = {"Authorization": f"Bearer {API_KEY}"}

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()

        ####### WORKING #####################################

        linesDeduped2 = []
        MAX_LINES = 100
        text = st.text_area(
            "Enter keyword or keyphrase - One per line - 200 max", height=200, key="2"
        )
        lines = text.split("\n")  # A list of lines
        linesList = []
        for x in lines:
            linesList.append(x)
        linesList = list(dict.fromkeys(linesList))  # Remove dupes
        linesList = list(filter(None, linesList))  # Remove empty

        if len(linesList) > MAX_LINES:
            st.info(
                f"🚨 Only the first 100 lines will be reviewed. We're planning to increase the allowance soon. Stay tuned!"
            )
            linesList = linesList[:MAX_LINES]

        multiselectComponent = st_tags(
            label="Type more labels here",
            text="Type more labels here",
            value=["Transational", "Navigational", "Informational"],
            suggestions=[
                "five",
                "six",
            ],
            maxtags=4,
        )

        submit_button = st.form_submit_button(label="Submit")

    if not submit_button:
        st.stop()

    else:

        try:

            def query(payload):
                response = requests.post(API_URL, headers=headers, json=payload)
                return response.json()

            listtest = ["I want a refund", "I have a question"]

            listToAppend = []

            for row in linesList:
                output2 = query(
                    {
                        # "inputs": "Hi, I recently bought a device from your company but it is not working as advertised and I would like to get reimbursed!",
                        "inputs": row,
                        # "parameters": {"candidate_labels": ["refund", "legal", "faq"]},
                        # "parameters": {"candidate_labels": multiselect},
                        "parameters": {"candidate_labels": multiselectComponent},
                    }
                )
                # st.write(output2)

                listToAppend.append(output2)

                df = pd.DataFrame.from_dict(output2)

            df = pd.DataFrame.from_dict(listToAppend)

            st.markdown("## ** Check results **")

            cs, c1 = st.columns([2, 2])

            with cs:
                CSVButton2 = download_button(df, "Data.csv", "🎁 Download (.csv)")

            df

        except ValueError:
            "ValueError"


# endregion Custom API key

if __name__ == "__main__":
    main()
