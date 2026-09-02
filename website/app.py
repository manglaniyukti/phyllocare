from flask import Flask, render_template, request, jsonify

import pandas as pd
import joblib
import os
import re
import math
import traceback


# ============================================================
# CREATE FLASK APPLICATION
# ============================================================

app = Flask(__name__)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


PROJECT_DIR = os.path.dirname(
    BASE_DIR
)


DATA_PATH = os.path.join(
    PROJECT_DIR,
    "data",
    "final_plant_dataset.csv"
)


MODEL_PATH = os.path.join(
    PROJECT_DIR,
    "model",
    "plant_problem_model.pkl"
)


# ============================================================
# USE THE VECTORIZER CREATED WITH THE NEW MODEL
# ============================================================

VECTORIZER_PATH = os.path.join(
    PROJECT_DIR,
    "model",
    "plant_problem_vectorizer.pkl"
)


# ============================================================
# LOAD DATASET
# ============================================================

plants_df = pd.read_csv(
    DATA_PATH
)


# ============================================================
# LOAD PLANT PROBLEM MODEL
# ============================================================

problem_model = joblib.load(
    MODEL_PATH
)


# ============================================================
# LOAD PLANT PROBLEM VECTORIZER
# ============================================================

problem_vectorizer = joblib.load(
    VECTORIZER_PATH
)


# ============================================================
# STARTUP INFORMATION
# ============================================================

print("\n========================================")

print("PhyloCare Application Started")

print("========================================\n")


print("Plant dataset loaded successfully!")

print("Plant problem model loaded successfully!")

print("Plant problem vectorizer loaded successfully!\n")


print("Dataset columns:")

print(
    plants_df.columns.tolist()
)


print("\nModel type:")

print(
    type(problem_model)
)


# ============================================================
# CHECK MODEL AND VECTORIZER COMPATIBILITY
# ============================================================

try:

    vectorizer_features = len(
        problem_vectorizer.get_feature_names_out()
    )


    model_features = problem_model.n_features_in_


    print("\nModel features:")

    print(
        model_features
    )


    print("\nVectorizer features:")

    print(
        vectorizer_features
    )


    if model_features == vectorizer_features:

        print(
            "\nSUCCESS: Model and vectorizer are compatible!"
        )


    else:

        print(
            "\nWARNING: Model and vectorizer feature counts do not match!"
        )


except Exception as error:

    print(
        "\nCould not check model/vectorizer compatibility:"
    )

    print(
        error
    )


print("\n========================================\n")


# ============================================================
# HELPER FUNCTION
# MAKE VALUES SAFE FOR JSON
# ============================================================

def safe_value(
    value,
    default="Not available"
):

    if value is None:

        return default


    try:

        if pd.isna(value):

            return default


    except (
        TypeError,
        ValueError
    ):

        pass


    if isinstance(
        value,
        float
    ):

        if math.isnan(value):

            return default


        if value.is_integer():

            return int(
                value
            )


    return value


# ============================================================
# TEXT CLEANING FUNCTION
# ============================================================

def clean_text(text):

    text = str(
        text
    ).lower()


    text = re.sub(

        r"[^a-zA-Z\s]",

        "",

        text

    )


    text = re.sub(

        r"\s+",

        " ",

        text

    ).strip()


    return text


# ============================================================
# COMMON PLANT NAME ALIASES
# ============================================================

plant_aliases = {

    # --------------------------------------------------------
    # INDIAN COMMON PLANTS
    # --------------------------------------------------------

    "tulsi": "holy basil",

    "holy basil": "holy basil",

    "neem": "neem tree",

    "curry leaf": "curry leaf",

    "curry leaves": "curry leaf",


    # --------------------------------------------------------
    # COMMON FLOWERS
    # --------------------------------------------------------

    "rose": "roses",

    "roses": "roses",

    "hibiscus": "tropical hibiscus",

    "jasmine": "jasmine",

    "marigold": "marigolds",

    "marigolds": "marigolds",

    "sunflower": "sunflower",

    "bougainvillea": "bougainvillea",

    "lotus": "lotus",


    # --------------------------------------------------------
    # HOUSEPLANTS
    # --------------------------------------------------------

    "money plant": "pothos",

    "pothos": "pothos",

    "snake plant": "snake plants",

    "snake plants": "snake plants",

    "spider plant": "spider plants",

    "spider plants": "spider plants",

    "peace lily": "peace lily",

    "rubber plant": "rubber plant",

    "jade plant": "jade plant",

    "lucky bamboo": "lucky bamboo",

    "areca palm": "areca palm",

    "aloe vera": "aloe vera",


    # --------------------------------------------------------
    # HERBS
    # --------------------------------------------------------

    "mint": "mint",

    "lemongrass": "lemongrass",

    "basil": "basil",

    "coriander": "vietnamese coriander",

    "parsley": "parsley",

    "rosemary": "rosemary",

    "thyme": "thyme",

    "oregano": "oregano",

    "ashwagandha": "ashwagandha",


    # --------------------------------------------------------
    # FRUITS
    # --------------------------------------------------------

    "mango": "mango",

    "banana": "banana",

    "lemon": "lemon tree",

    "guava": "guava",

    "papaya": "papaya",

    "pomegranate": "pomegranate",


    # --------------------------------------------------------
    # VEGETABLES
    # --------------------------------------------------------

    "tomato": "tomatoes",

    "tomatoes": "tomatoes",

    "potato": "potatoes",

    "potatoes": "potatoes",

    "spinach": "spinach",


    # --------------------------------------------------------
    # OTHER COMMON PLANTS
    # --------------------------------------------------------

    "monstera": "monstera",

    "philodendron": "philodendron",

    "fern": "ferns",

    "ferns": "ferns",

    "orchid": "orchids",

    "orchids": "orchids",

    "cactus": "cactus",

    "succulent": "succulents"

}


# ============================================================
# PROBLEM DISPLAY NAMES
# ============================================================

problem_display_names = {

    "underwatering":
    "Underwatering",


    "overwatering":
    "Overwatering",


    "low_light":
    "Insufficient Light",


    "nutrient_deficiency":
    "Nutrient Deficiency",


    "pest_problem":
    "Pest Problem",


    "fungal_disease":
    "Possible Fungal Disease",


    "temperature_stress":
    "Temperature Stress",


    "healthy":
    "No Major Problem Detected",


    "root_rot":
    "Root Rot",


    "sunburn":
    "Sunburn",


    "low_humidity":
    "Low Humidity",


    "transplant_stress":
    "Transplant Stress",


    "poor_drainage":
    "Poor Drainage",


    "physical_damage":
    "Physical Damage",


    "dormancy":
    "Natural Dormancy"

}


# ============================================================
# PROBLEM CAUSES AND RECOMMENDATIONS
# ============================================================

problem_recommendations = {

    "underwatering": {

        "cause":
        "The plant may not be receiving enough water, or the soil may be drying too quickly.",

        "recommendation":
        "Check the soil moisture regularly and water the plant when the soil becomes appropriately dry."

    },


    "overwatering": {

        "cause":
        "The plant may be receiving water too frequently, causing the soil to remain excessively wet.",

        "recommendation":
        "Allow the soil to dry before watering again. Check that the pot has proper drainage and avoid watering on a fixed schedule without checking the soil."

    },


    "low_light": {

        "cause":
        "The plant may not be receiving enough suitable light.",

        "recommendation":
        "Move the plant to a brighter location with lighting appropriate for its species."

    },


    "nutrient_deficiency": {

        "cause":
        "The plant may not be receiving sufficient nutrients from the soil.",

        "recommendation":
        "Check the soil condition and consider using an appropriate balanced fertilizer."

    },


    "pest_problem": {

        "cause":
        "The plant may be affected by insects or other common pests.",

        "recommendation":
        "Inspect the leaves and stems carefully. Remove visible pests and use an appropriate plant-safe treatment if necessary."

    },


    "fungal_disease": {

        "cause":
        "The plant may have a fungal or moisture-related disease problem.",

        "recommendation":
        "Improve air circulation, avoid keeping foliage excessively wet, and monitor whether the problem spreads."

    },


    "temperature_stress": {

        "cause":
        "The plant may be exposed to temperatures that are too hot or too cold.",

        "recommendation":
        "Move the plant away from extreme heat or cold and maintain a suitable temperature for the plant."

    },


    "healthy": {

        "cause":
        "No major plant problem was detected from the description.",

        "recommendation":
        "Continue the current care routine and monitor the plant regularly."

    },


    "root_rot": {

        "cause":
        "The roots may have been damaged by excess moisture and poor conditions around the root system.",

        "recommendation":
        "Check the roots and improve drainage. Avoid keeping the soil constantly wet."

    },


    "sunburn": {

        "cause":
        "The plant may have been exposed to excessively strong direct sunlight.",

        "recommendation":
        "Move the plant to a location with more suitable light and gradually adjust sunlight exposure."

    },


    "low_humidity": {

        "cause":
        "The surrounding air may be too dry for the plant.",

        "recommendation":
        "Increase humidity around the plant using suitable methods and keep it away from very dry air sources."

    },


    "transplant_stress": {

        "cause":
        "The plant may be adjusting to disturbance of its roots or a recent change of pot or soil.",

        "recommendation":
        "Give the plant time to adjust and maintain stable watering and environmental conditions."

    },


    "poor_drainage": {

        "cause":
        "Water may not be draining properly from the pot or soil.",

        "recommendation":
        "Use a pot with drainage holes and ensure the potting mix allows excess water to drain properly."

    },


    "physical_damage": {

        "cause":
        "The plant may be damaged through physical contact, handling, falling, or another accident.",

        "recommendation":
        "Remove severely damaged plant parts if necessary and avoid further disturbance while the plant recovers."

    },


    "dormancy": {

        "cause":
        "The plant may be in a natural period of reduced growth, often caused by seasonal changes.",

        "recommendation":
        "Reduce unnecessary care changes and continue basic maintenance."

    }

}


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# FLEXIBLE PLANT SEARCH FUNCTION
# ============================================================

def search_plants(
    user_input
):

    user_input = str(
        user_input
    ).lower().strip()


    search_term = plant_aliases.get(
        user_input,
        user_input
    )


    plant_names = (

        plants_df["typeName"]

        .fillna("")

        .astype(str)

        .str.lower()

        .str.strip()

    )


    # --------------------------------------------------------
    # EXACT MATCH
    # --------------------------------------------------------

    exact_matches = plants_df[
        plant_names == search_term
    ]


    if not exact_matches.empty:

        return exact_matches


    # --------------------------------------------------------
    # STARTS WITH
    # --------------------------------------------------------

    starts_with_matches = plants_df[

        plant_names.str.startswith(

            search_term,

            na=False

        )

    ]


    # --------------------------------------------------------
    # CONTAINS
    # --------------------------------------------------------

    contains_matches = plants_df[

        plant_names.str.contains(

            search_term,

            na=False,

            regex=False

        )

    ]


    # --------------------------------------------------------
    # COMMON EXAMPLES
    # --------------------------------------------------------

    if "commonExamples" in plants_df.columns:

        common_examples = (

            plants_df["commonExamples"]

            .fillna("")

            .astype(str)

            .str.lower()

        )


        example_matches = plants_df[

            common_examples.str.contains(

                search_term,

                na=False,

                regex=False

            )

        ]


    else:

        example_matches = plants_df.iloc[0:0]


    # --------------------------------------------------------
    # COMBINE RESULTS
    # --------------------------------------------------------

    results = pd.concat(

        [

            starts_with_matches,

            contains_matches,

            example_matches

        ],

        ignore_index=True

    )


    # --------------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------------

    results = results.drop_duplicates(

        subset=["typeName"]

    )


    return results


# ============================================================
# PLANT SEARCH API
# ============================================================

@app.route(
    "/search_plant",
    methods=["GET"]
)
def search_plant():

    try:

        plant_name = request.args.get(

            "plant",

            ""

        ).strip()


        # ----------------------------------------------------
        # CHECK EMPTY INPUT
        # ----------------------------------------------------

        if not plant_name:

            return jsonify({

                "success": False,

                "message":
                "Please enter a plant name."

            })


        # ----------------------------------------------------
        # SEARCH PLANT
        # ----------------------------------------------------

        results = search_plants(
            plant_name
        )


        # ----------------------------------------------------
        # CHECK RESULTS
        # ----------------------------------------------------

        if results.empty:

            return jsonify({

                "success": False,

                "message":
                f"No plants were found for '{plant_name}'."

            })


        # ----------------------------------------------------
        # LIMIT RESULTS
        # ----------------------------------------------------

        results = results.head(
            10
        )


        plant_results = []


        # ----------------------------------------------------
        # CREATE RESPONSE
        # ----------------------------------------------------

        for _, plant in results.iterrows():

            plant_results.append({

                "typeName":
                safe_value(
                    plant.get("typeName")
                ),


                "origin":
                safe_value(
                    plant.get("origin")
                ),


                "category":
                safe_value(
                    plant.get("category")
                ),


                "lightPreference":
                safe_value(
                    plant.get("lightPreference")
                ),


                "humidityPreference":
                safe_value(
                    plant.get("humidityPreference")
                ),


                "temperaturePreference":
                safe_value(
                    plant.get("temperaturePreference")
                ),


                "springInterval":
                safe_value(
                    plant.get("springInterval"),
                    None
                ),


                "summerInterval":
                safe_value(
                    plant.get("summerInterval"),
                    None
                ),


                "fallInterval":
                safe_value(
                    plant.get("fallInterval"),
                    None
                ),


                "winterInterval":
                safe_value(
                    plant.get("winterInterval"),
                    None
                ),


                "growthRate":
                safe_value(
                    plant.get("growthRate")
                ),


                "plantToxicity":
                safe_value(
                    plant.get("plantToxicity")
                ),


                "careTips":
                safe_value(
                    plant.get("careTips")
                )

            })


        # ----------------------------------------------------
        # RETURN RESPONSE
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "count":
            len(
                plant_results
            ),

            "plants":
            plant_results

        })


    except Exception as error:

        print(
            "\nPLANT SEARCH ERROR:"
        )

        print(
            error
        )


        traceback.print_exc()


        return jsonify({

            "success": False,

            "message":
            "An error occurred while retrieving plant information."

        }), 500


# ============================================================
# PLANT PROBLEM ANALYSIS API
# ============================================================

@app.route(
    "/analyze_problem",
    methods=["POST"]
)
def analyze_problem():

    try:

        # ----------------------------------------------------
        # GET JSON DATA
        # ----------------------------------------------------

        data = request.get_json(
            silent=True
        )


        if data is None:

            return jsonify({

                "success": False,

                "message":
                "Invalid request data."

            }), 400


        # ----------------------------------------------------
        # GET DESCRIPTION
        # ----------------------------------------------------

        description = str(

            data.get(

                "description",

                ""

            )

        ).strip()


        # ----------------------------------------------------
        # CHECK EMPTY DESCRIPTION
        # ----------------------------------------------------

        if not description:

            return jsonify({

                "success": False,

                "message":
                "Please describe your plant problem."

            }), 400


        # ----------------------------------------------------
        # CLEAN TEXT
        # ----------------------------------------------------

        cleaned_description = clean_text(
            description
        )


        # ----------------------------------------------------
        # CHECK CLEANED TEXT
        # ----------------------------------------------------

        if not cleaned_description:

            return jsonify({

                "success": False,

                "message":
                "Please enter a valid plant problem description."

            }), 400


        # ====================================================
        # INPUT VALIDATION
        # THIS HAPPENS BEFORE THE ML MODEL
        # ====================================================

        words = cleaned_description.split()


        # ----------------------------------------------------
        # CHECK VERY SHORT INPUT
        # ----------------------------------------------------

        if len(words) < 3:

            return jsonify({

                "success": False,

                "message":
                (
                    "Please provide more information about the plant problem. "
                    "Describe symptoms such as leaf color, soil condition, "
                    "watering, light, temperature, or visible damage."
                )

            }), 400


        # ----------------------------------------------------
        # COMMON INVALID OR RANDOM INPUTS
        # ----------------------------------------------------

        invalid_inputs = {

            "hello",
            "hi",
            "hey",
            "hii",
            "hiii",
            "test",
            "testing",
            "nothing",
            "problem",
            "plant problem",
            "help",
            "please help",
            "asdf",
            "asdfgh",
            "asdfghjkl",
            "qwerty",
            "random",
            "invalid",
            "information",
            "insufficient information",
            "no idea",
            "dont know",
            "do not know"

        }


        if cleaned_description in invalid_inputs:

            return jsonify({

                "success": False,

                "message":
                (
                    "Please provide a valid description of the plant problem. "
                    "For example, describe changes in the leaves, soil, "
                    "watering conditions, light, or other visible symptoms."
                )

            }), 400


        # ====================================================
        # PLANT AND SYMPTOM KEYWORDS
        # ====================================================

        plant_keywords = {

            "plant",
            "plants",
            "leaf",
            "leaves",
            "root",
            "roots",
            "stem",
            "stems",
            "flower",
            "flowers",
            "soil",
            "pot",
            "tree",
            "trees",
            "garden",
            "seed",
            "seeds",
            "growth",
            "growing",
            "water",
            "watering"

        }


        symptom_keywords = {

            # COLOR PROBLEMS

            "yellow",
            "yellowing",
            "brown",
            "browning",
            "black",
            "white",
            "spots",
            "spot",
            "discoloration",


            # WATER PROBLEMS

            "dry",
            "wet",
            "moist",
            "water",
            "watering",
            "overwatered",
            "underwatered",
            "drought",
            "soggy",


            # LEAF PROBLEMS

            "drooping",
            "droop",
            "wilting",
            "wilt",
            "curling",
            "curled",
            "falling",
            "fall",
            "dying",
            "dead",


            # PESTS

            "pest",
            "pests",
            "insect",
            "insects",
            "bugs",
            "bug",
            "aphids",
            "mites",
            "mealybugs",


            # DISEASE

            "fungus",
            "fungal",
            "disease",
            "mold",
            "mould",
            "rot",
            "rotting",


            # LIGHT

            "light",
            "sunlight",
            "sun",
            "shade",
            "dark",


            # TEMPERATURE

            "hot",
            "cold",
            "heat",
            "temperature",
            "frost",


            # HUMIDITY

            "humidity",
            "humid",
            "dry air",


            # NUTRIENTS

            "nutrient",
            "nutrients",
            "fertilizer",
            "fertiliser",
            "deficiency",


            # OTHER PROBLEMS

            "damage",
            "damaged",
            "broken",
            "burn",
            "burned",
            "burnt",
            "stress",
            "transplant",
            "drainage",
            "drain"

        }


        # ====================================================
        # CHECK FOR MEANINGFUL PLANT CONTEXT
        # ====================================================

        has_plant_context = False


        for keyword in plant_keywords:

            if keyword in cleaned_description:

                has_plant_context = True

                break


        # ====================================================
        # CHECK FOR SYMPTOMS
        # ====================================================

        has_symptom = False


        for keyword in symptom_keywords:

            if keyword in cleaned_description:

                has_symptom = True

                break


        # ----------------------------------------------------
        # NO PLANT CONTEXT AND NO SYMPTOM
        # ----------------------------------------------------

        if not has_plant_context and not has_symptom:

            return jsonify({

                "success": False,

                "message":
                (
                    "Please provide a valid plant problem description. "
                    "Describe what is happening to your plant, such as "
                    "yellow leaves, dry soil, spots, wilting, pests, "
                    "or other visible symptoms."
                )

            }), 400


        # ----------------------------------------------------
        # TOO LITTLE USEFUL INFORMATION
        # ----------------------------------------------------

        if len(words) < 5:

            return jsonify({

                "success": False,

                "message":
                (
                    "There is not enough information to analyze the plant problem reliably. "
                    "Please provide more details about the symptoms, such as "
                    "leaf color, soil condition, watering, light, or visible damage."
                )

            }), 400


        # ----------------------------------------------------
        # HAS PLANT WORD BUT NO ACTUAL SYMPTOM
        # ----------------------------------------------------

        if has_plant_context and not has_symptom:

            return jsonify({

                "success": False,

                "message":
                (
                    "Please provide more details about what is wrong with the plant. "
                    "Describe specific symptoms such as yellow or brown leaves, "
                    "dry or wet soil, wilting, spots, pests, or poor growth."
                )

            }), 400


        # ====================================================
        # DISPLAY ANALYSIS INFORMATION IN TERMINAL
        # ====================================================

        print(
            "\n========================================"
        )


        print(
            "PLANT PROBLEM ANALYSIS"
        )


        print(
            "========================================"
        )


        print(
            "\nOriginal description:"
        )


        print(
            description
        )


        print(
            "\nCleaned description:"
        )


        print(
            cleaned_description
        )


        # ====================================================
        # TRANSFORM TEXT
        # ONLY VALID INPUT REACHES THIS POINT
        # ====================================================

        vector = problem_vectorizer.transform(

            [
                cleaned_description
            ]

        )


        print(
            "\nText transformed successfully."
        )


        print(
            "Vector features:"
        )


        print(
            vector.shape[1]
        )


        # ====================================================
        # PREDICT PLANT PROBLEM
        # ====================================================

        prediction = problem_model.predict(
            vector
        )[0]


        print(
            "\nPrediction:"
        )


        print(
            prediction
        )


        # ====================================================
        # CALCULATE CONFIDENCE
        # ====================================================

        confidence = 0.0


        if hasattr(
            problem_model,
            "predict_proba"
        ):

            probabilities = problem_model.predict_proba(
                vector
            )[0]


            confidence = float(

                max(
                    probabilities
                ) * 100

            )


        print(
            "\nConfidence:"
        )


        print(
            confidence
        )


        # ====================================================
        # CONVERT PREDICTION TO STRING
        # ====================================================

        prediction = str(
            prediction
        ).strip()


        # ====================================================
        # GET DISPLAY NAME
        # ====================================================

        display_name = problem_display_names.get(

            prediction,

            prediction.replace(
                "_",
                " "
            ).title()

        )


        # ====================================================
        # GET RECOMMENDATION INFORMATION
        # ====================================================

        information = problem_recommendations.get(

            prediction,

            {

                "cause":
                "The exact cause could not be determined from the available information.",


                "recommendation":
                (
                    "Monitor the plant carefully and check its watering, "
                    "light, soil, and environmental conditions."
                )

            }

        )


        # ====================================================
        # LOW CONFIDENCE WARNING
        # ====================================================

        warning = ""


        if confidence < 30:

            warning = (

                "⚠️ This prediction has low confidence. "
                "Please do not rely completely on this result. "
                "Try providing more details about the symptoms for a more reliable analysis."

            )


        # ====================================================
        # RETURN VALID PREDICTION
        # ====================================================

        return jsonify({

            "success": True,


            "problem":
            display_name,


            "confidence":
            round(
                confidence,
                2
            ),


            "cause":
            information.get(

                "cause",

                "Cause information is not available."

            ),


            "recommendation":
            information.get(

                "recommendation",

                "Recommendation information is not available."

            ),


            "warning":
            warning,


            "needs_more_information":
            False,


            "information_message":
            ""

        })


    except Exception as error:

        print(
            "\n========================================"
        )


        print(
            "PROBLEM ANALYSIS ERROR"
        )


        print(
            "========================================"
        )


        traceback.print_exc()


        return jsonify({

            "success":
            False,


            "message":
            f"Server error: {str(error)}"

        }), 500

# ============================================================
# PLANT NAME SUGGESTIONS API
# ============================================================

@app.route(
    "/plant_suggestions",
    methods=["GET"]
)
def plant_suggestions():

    query = request.args.get(

        "query",

        ""

    ).lower().strip()


    # --------------------------------------------------------
    # EMPTY QUERY
    # --------------------------------------------------------

    if not query:

        return jsonify({

            "success": True,

            "suggestions": []

        })


    # --------------------------------------------------------
    # GET PLANT NAMES
    # --------------------------------------------------------

    plant_names = (

        plants_df["typeName"]

        .fillna("")

        .astype(str)

        .str.strip()

    )


    plant_names_lower = (

        plant_names

        .str.lower()

    )


    # --------------------------------------------------------
    # STARTS WITH QUERY
    # --------------------------------------------------------

    starts_with_matches = plants_df[

        plant_names_lower.str.startswith(

            query,

            na=False

        )

    ]


    # --------------------------------------------------------
    # CONTAINS QUERY
    # --------------------------------------------------------

    contains_matches = plants_df[

        plant_names_lower.str.contains(

            query,

            na=False,

            regex=False

        )

    ]


    # --------------------------------------------------------
    # PRIORITY SUGGESTIONS
    # --------------------------------------------------------

    priority_suggestions = (

        starts_with_matches["typeName"]

        .dropna()

        .drop_duplicates()

        .tolist()

    )


    # --------------------------------------------------------
    # OTHER SUGGESTIONS
    # --------------------------------------------------------

    other_suggestions = (

        contains_matches["typeName"]

        .dropna()

        .drop_duplicates()

        .tolist()

    )


    # --------------------------------------------------------
    # ALIAS SUGGESTIONS
    # --------------------------------------------------------

    alias_start_matches = []


    alias_contains_matches = []


    for alias in plant_aliases:

        if alias.lower().startswith(
            query
        ):

            suggestion = alias.title()


            if suggestion not in alias_start_matches:

                alias_start_matches.append(
                    suggestion
                )


        elif query in alias.lower():

            suggestion = alias.title()


            if suggestion not in alias_contains_matches:

                alias_contains_matches.append(
                    suggestion
                )


    # --------------------------------------------------------
    # COMBINE SUGGESTIONS
    # --------------------------------------------------------

    all_possible_suggestions = (

        alias_start_matches

        +

        priority_suggestions

        +

        alias_contains_matches

        +

        other_suggestions

    )


    # --------------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------------

    all_suggestions = []


    for suggestion in all_possible_suggestions:

        if suggestion not in all_suggestions:

            all_suggestions.append(
                suggestion
            )


    # --------------------------------------------------------
    # LIMIT RESULTS
    # --------------------------------------------------------

    all_suggestions = all_suggestions[:15]


    # --------------------------------------------------------
    # RETURN RESPONSE
    # --------------------------------------------------------

    return jsonify({

        "success":
        True,


        "suggestions":
        all_suggestions

    })


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )