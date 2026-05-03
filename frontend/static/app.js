const { useEffect, useState } = React;

const API_BASE_URL = window.API_BASE_URL || "http://127.0.0.1:5002";

function App() {
    const [backendData, setBackendData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState("");

    async function loadGreeting() {
        setIsLoading(true);
        setError("");

        try {
            const response = await fetch(`${API_BASE_URL}/api/hello`);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "The Flask backend returned an error.");
            }

            setBackendData(data);
        } catch (loadError) {
            setError(loadError.message || "Could not reach the Flask backend.");
        } finally {
            setIsLoading(false);
        }
    }

    useEffect(() => {
        loadGreeting();
    }, []);

    return React.createElement(
        "main",
        { className: "app-shell" },
        React.createElement(
            "section",
            { className: "hero" },
            React.createElement(
                "div",
                { className: "status-pill" },
                React.createElement("span", { className: "status-dot" }),
                "React frontend + Flask API"
            ),
            React.createElement("h1", null, "Split and ready."),
            React.createElement(
                "p",
                { className: "intro" },
                "This React frontend is now separate from Flask. It calls the backend API and renders the response here."
            ),
            React.createElement(
                "div",
                { className: "response-panel" },
                isLoading &&
                    React.createElement("p", { className: "muted" }, "Loading from Flask..."),
                error &&
                    React.createElement("p", { className: "error" }, error),
                backendData &&
                    React.createElement(
                        React.Fragment,
                        null,
                        React.createElement("span", { className: "label" }, "Backend response"),
                        React.createElement("h2", null, backendData.message),
                        React.createElement("p", null, backendData.detail),
                        React.createElement(
                            "time",
                            null,
                            `Fetched at ${backendData.timestamp}`
                        )
                    )
            ),
            React.createElement(
                "button",
                { onClick: loadGreeting, disabled: isLoading },
                isLoading ? "Refreshing" : "Refresh from backend"
            )
        )
    );
}

ReactDOM.createRoot(document.getElementById("root")).render(
    React.createElement(App)
);
