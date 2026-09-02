// =========================================================
// GET HTML ELEMENTS
// =========================================================

const plantInput = document.getElementById("plantInput");
const suggestionsBox = document.getElementById("suggestions");
const searchButton = document.getElementById("searchButton");
const searchStatus = document.getElementById("searchStatus");
const plantResults = document.getElementById("plantResults");

const problemInput = document.getElementById("problemInput");
const analyzeButton = document.getElementById("analyzeButton");
const analysisStatus = document.getElementById("analysisStatus");
const problemResult = document.getElementById("problemResult");


// =========================================================
// PLANT NAME SUGGESTIONS
// =========================================================

plantInput.addEventListener("input", async function () {

    const query = plantInput.value.trim();

    suggestionsBox.innerHTML = "";

    if (query.length === 0) {
        return;
    }

    try {

        const response = await fetch(
            `/plant_suggestions?query=${encodeURIComponent(query)}`
        );

        if (!response.ok) {
            throw new Error(
                `Server error: ${response.status}`
            );
        }

        const data = await response.json();

        if (
            data.success &&
            data.suggestions &&
            data.suggestions.length > 0
        ) {

            data.suggestions.forEach(function (plantName) {

                const suggestionItem =
                    document.createElement("div");

                suggestionItem.classList.add(
                    "suggestion-item"
                );

                suggestionItem.textContent =
                    plantName;


                // Select suggestion

                suggestionItem.addEventListener(
                    "click",
                    function () {

                        plantInput.value =
                            plantName;

                        suggestionsBox.innerHTML =
                            "";

                        searchPlant();

                    }
                );


                suggestionsBox.appendChild(
                    suggestionItem
                );

            });

        }

    }

    catch (error) {

        console.error(
            "Suggestion error:",
            error
        );

    }

});


// =========================================================
// SEARCH PLANT FUNCTION
// =========================================================

async function searchPlant() {

    const plantName =
        plantInput.value.trim();


    // Check empty input

    if (plantName.length === 0) {

        searchStatus.textContent =
            "Please enter a plant name.";

        plantResults.innerHTML =
            "";

        return;

    }


    // Show searching message

    searchStatus.textContent =
        "Searching for plant information...";

    plantResults.innerHTML =
        "";

    suggestionsBox.innerHTML =
        "";


    try {

        const response = await fetch(
            `/search_plant?plant=${encodeURIComponent(plantName)}`
        );


        // Check server response

        if (!response.ok) {

            throw new Error(
                `Server error: ${response.status}`
            );

        }


        const data =
            await response.json();


        // Check if search was successful

        if (!data.success) {

            searchStatus.textContent =
                data.message ||
                "Plant not found.";

            return;

        }


        // Check if plants exist

        if (
            !data.plants ||
            data.plants.length === 0
        ) {

            searchStatus.textContent =
                "No plant information found.";

            return;

        }


        // Clear status

        searchStatus.textContent =
            "";


        // Display plant results

        displayPlantResults(
            data.plants
        );

    }

    catch (error) {

        console.error(
            "Plant search error:",
            error
        );

        searchStatus.textContent =
            "An error occurred while searching for the plant.";

    }

}


// =========================================================
// DISPLAY PLANT RESULTS
// =========================================================

function displayPlantResults(plants) {

    plantResults.innerHTML =
        "";


    plants.forEach(function (plant) {

        const card =
            document.createElement("div");


        card.classList.add(
            "plant-card"
        );


        card.innerHTML = `

            <h3>
                🌿 ${plant.typeName || "Unknown Plant"}
            </h3>


            <p>
                <strong>Category:</strong>
                ${formatText(plant.category)}
            </p>


            <p>
                <strong>Light Preference:</strong>
                ${formatText(plant.lightPreference)}
            </p>


            <p>
                <strong>Humidity:</strong>
                ${formatText(plant.humidityPreference)}
            </p>


            <p>
                <strong>Temperature:</strong>
                ${formatTemperature(
                    plant.temperaturePreference
                )}
            </p>


            <p>
                <strong>Watering:</strong>
                ${formatWatering(plant)}
            </p>


            <p>
                <strong>Growth Rate:</strong>
                ${formatText(plant.growthRate)}
            </p>


            <p>
                <strong>Plant Toxicity:</strong>
                ${formatText(plant.plantToxicity)}
            </p>


            <p>
                <strong>Care Tips:</strong>
                ${formatText(plant.careTips)}
            </p>

        `;


        plantResults.appendChild(
            card
        );

    });

}


// =========================================================
// FORMAT TEXT
// =========================================================

function formatText(text) {

    if (
        text === null ||
        text === undefined ||
        text === "" ||
        text === "nan" ||
        text === "NaN" ||
        text === "Not available"
    ) {

        return "Not available";

    }


    return String(text)

        // Separate camelCase words

        .replace(
            /([a-z])([A-Z])/g,
            "$1 $2"
        )

        // Replace underscores

        .replace(
            /_/g,
            " "
        )

        // Capitalize first letter

        .replace(
            /\b\w/g,
            function (letter) {

                return letter.toUpperCase();

            }
        );

}


// =========================================================
// FORMAT TEMPERATURE
// =========================================================

function formatTemperature(temperature) {

    if (
        temperature === null ||
        temperature === undefined ||
        temperature === "" ||
        temperature === "nan" ||
        temperature === "NaN" ||
        temperature === "Not available"
    ) {

        return "Not available";

    }


    // If temperature is already an array

    if (
        Array.isArray(temperature) &&
        temperature.length >= 2
    ) {

        return `${temperature[0]}°C - ${temperature[1]}°C`;

    }


    // If temperature is a string

    if (typeof temperature === "string") {

        // Example:
        // [10, 32]

        const match =
            temperature.match(
                /\[\s*(\d+\.?\d*)\s*,\s*(\d+\.?\d*)\s*\]/
            );


        if (match) {

            return `${match[1]}°C - ${match[2]}°C`;

        }

    }


    return formatText(
        temperature
    );

}


// =========================================================
// CHECK VALID WATERING VALUE
// =========================================================

function isValidWateringValue(value) {

    if (
        value === null ||
        value === undefined ||
        value === "" ||
        value === "nan" ||
        value === "NaN" ||
        value === "Not available"
    ) {

        return false;

    }


    return true;

}


// =========================================================
// FORMAT WATERING INFORMATION
// =========================================================

function formatWatering(plant) {

    const intervals = [];


    // Spring

    if (
        isValidWateringValue(
            plant.springInterval
        )
    ) {

        intervals.push(
            `Spring: every ${plant.springInterval} days`
        );

    }


    // Summer

    if (
        isValidWateringValue(
            plant.summerInterval
        )
    ) {

        intervals.push(
            `Summer: every ${plant.summerInterval} days`
        );

    }


    // Fall

    if (
        isValidWateringValue(
            plant.fallInterval
        )
    ) {

        intervals.push(
            `Fall: every ${plant.fallInterval} days`
        );

    }


    // Winter

    if (
        isValidWateringValue(
            plant.winterInterval
        )
    ) {

        intervals.push(
            `Winter: every ${plant.winterInterval} days`
        );

    }


    if (intervals.length === 0) {

        return "Not available";

    }


    return intervals.join(
        "<br>"
    );

}


// =========================================================
// SEARCH BUTTON EVENT
// =========================================================

searchButton.addEventListener(
    "click",
    searchPlant
);


// =========================================================
// ENTER KEY FOR PLANT SEARCH
// =========================================================

plantInput.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Enter") {

            event.preventDefault();

            searchPlant();

        }

    }
);


// =========================================================
// ANALYZE PLANT PROBLEM
// =========================================================

async function analyzeProblem() {

    const description =
        problemInput.value.trim();


    // Check empty input

    if (description.length === 0) {

        analysisStatus.textContent =
            "Please describe the plant problem.";

        problemResult.innerHTML =
            "";

        return;

    }


    // Show analyzing message

    analysisStatus.textContent =
        "Analyzing plant problem...";

    problemResult.innerHTML =
        "";


    try {

        const response =
            await fetch(
                "/analyze_problem",
                {

                    method:
                        "POST",


                    headers: {

                        "Content-Type":
                            "application/json"

                    },


                    body:
                        JSON.stringify(
                            {

                                description:
                                    description

                            }
                        )

                }
            );


        // Convert response to JSON

        const data =
            await response.json();


        // Check if the server returned an error

        if (!response.ok) {

            analysisStatus.textContent =
                data.message ||
                "An error occurred while analyzing the problem.";

            return;

        }


        // Check success

        if (!data.success) {

            analysisStatus.textContent =
                data.message ||
                "Unable to analyze the problem.";

            return;

        }


        // Clear status

        analysisStatus.textContent =
            "";


        // Display result

        displayProblemResult(
            data
        );

    }

    catch (error) {

        console.error(
            "Problem analysis error:",
            error
        );


        analysisStatus.textContent =
            "An error occurred while analyzing the problem.";

    }

}


// =========================================================
// DISPLAY PROBLEM ANALYSIS RESULT
// =========================================================

function displayProblemResult(data) {

    let warningHTML = "";


    // -----------------------------------------------------
    // LOW CONFIDENCE WARNING
    // -----------------------------------------------------

    if (
        data.warning &&
        data.warning.trim() !== ""
    ) {

        warningHTML = `

            <div class="analysis-warning">

                <strong>⚠️ Important:</strong>

                <p>
                    ${data.warning}
                </p>

            </div>

        `;

    }


    let informationHTML = "";


    // -----------------------------------------------------
    // INSUFFICIENT INFORMATION MESSAGE
    // -----------------------------------------------------

    if (
        data.needs_more_information === true &&
        data.information_message &&
        data.information_message.trim() !== ""
    ) {

        informationHTML = `

            <div class="information-warning">

                <strong>ℹ️ More Information Needed:</strong>

                <p>
                    ${data.information_message}
                </p>

            </div>

        `;

    }


    // -----------------------------------------------------
    // DISPLAY RESULT
    // -----------------------------------------------------

    problemResult.innerHTML = `

        <div class="problem-card">


            <h3>
                🌿 ${data.problem}
            </h3>


            <p>

                <strong>Confidence:</strong>

                ${data.confidence}%

            </p>


            ${warningHTML}


            ${informationHTML}


            <p>

                <strong>Possible Cause:</strong>

                ${data.cause}

            </p>


            <p>

                <strong>Recommendation:</strong>

                ${data.recommendation}

            </p>


        </div>

    `;

}


// =========================================================
// ANALYZE BUTTON EVENT
// =========================================================

analyzeButton.addEventListener(
    "click",
    analyzeProblem
);