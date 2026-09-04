import streamlit as st
import folium
from streamlit_folium import st_folium

from location_search import search_location
from route import get_routes
from weather import get_weather
from model import predict_risk


# ==============================
# PAGE SETTINGS
# ==============================

st.set_page_config(
    page_title="NER-SMART",
    page_icon="🗺️",
    layout="wide"
)


# ==============================
# HEADER
# ==============================

st.title("🗺️ NER-SMART")

st.subheader(
    "AI-Powered Disaster-Aware Navigation"
)

st.write(
    "Safe and intelligent navigation across "
    "the North Eastern Region of India."
)

st.divider()


# ==============================
# FROM LOCATION
# ==============================

st.markdown("### 📍 From")

from_text = st.text_input(
    "Search starting location",
    placeholder="Example: Guwahati",
    key="from_text"
)

from_results = []

if from_text:
    from_results = search_location(from_text)


from_location = None
from_selected = ""


if from_results:

    from_options = [
        result["display_name"]
        for result in from_results
    ]

    from_selected = st.selectbox(
        "Select starting location",
        from_options,
        key="from_select"
    )

    from_index = from_options.index(
        from_selected
    )

    from_location = from_results[from_index]

elif from_text:

    st.warning(
        "No NER location found."
    )


# ==============================
# TO LOCATION
# ==============================

st.markdown("### 🏁 To")

to_text = st.text_input(
    "Search destination",
    placeholder="Example: Shillong",
    key="to_text"
)

to_results = []

if to_text:
    to_results = search_location(to_text)


to_location = None
to_selected = ""


if to_results:

    to_options = [
        result["display_name"]
        for result in to_results
    ]

    to_selected = st.selectbox(
        "Select destination",
        to_options,
        key="to_select"
    )

    to_index = to_options.index(
        to_selected
    )

    to_location = to_results[to_index]

elif to_text:

    st.warning(
        "No NER destination found."
    )


# ==============================
# DISASTER CONTROLS
# ==============================

st.markdown(
    "## 🚨 Disaster & Road Conditions"
)

col1, col2, col3 = st.columns(3)


with col1:

    flood_risk = st.slider(
        "🌊 Flood Risk",
        1,
        5,
        1
    )


with col2:

    landslide_risk = st.slider(
        "⛰️ Landslide Risk",
        1,
        5,
        1
    )


with col3:

    road_condition = st.slider(
        "🛣️ Road Condition",
        1,
        5,
        5
    )


st.divider()


# ==============================
# FIND SAFE ROUTES
# ==============================

if st.button(
    "🔍 Find Safe Routes",
    use_container_width=True
):

    if from_location and to_location:

        from_lat = float(
            from_location["lat"]
        )

        from_lon = float(
            from_location["lon"]
        )

        to_lat = float(
            to_location["lat"]
        )

        to_lon = float(
            to_location["lon"]
        )


        # ==============================
        # WEATHER
        # ==============================

        weather = get_weather(
            from_lat,
            from_lon
        )

        st.markdown(
            "## 🌦️ Live Weather"
        )

        rainfall = 0


        if weather:

            current = weather.get(
                "current",
                {}
            )

            temperature = current.get(
                "temperature_2m",
                "N/A"
            )

            rainfall = current.get(
                "rain",
                0
            )


            col1, col2 = st.columns(2)


            with col1:

                st.metric(
                    "🌡️ Temperature",
                    f"{temperature} °C"
                )


            with col2:

                st.metric(
                    "🌧️ Rain",
                    f"{rainfall} mm"
                )


        else:

            st.warning(
                "Weather data unavailable."
            )


        # ==============================
        # GET ROAD ROUTES
        # ==============================

        with st.spinner(
            "Finding safe road routes..."
        ):

            routes = get_routes(
                from_lat,
                from_lon,
                to_lat,
                to_lon
            )


        if routes:

            st.success(
                f"✅ {len(routes)} route(s) found!"
            )


            # ==============================
            # AI RISK PREDICTION
            # ==============================

            accessibility = 80

            route_risks = []


            for i in range(len(routes)):

                route_flood = min(
                    5,
                    flood_risk + i
                )

                route_landslide = min(
                    5,
                    landslide_risk + i
                )

                route_condition = max(
                    1,
                    road_condition - i
                )


                route_risk = predict_risk(
                    rainfall,
                    route_flood,
                    route_landslide,
                    route_condition,
                    accessibility
                )


                route_risks.append(
                    route_risk
                )


            # ==============================
            # AI ROUTE RISK
            # ==============================

            st.markdown(
                "## 🤖 AI Route Risk"
            )


            for i, risk in enumerate(
                route_risks
            ):

                if risk == "Low":

                    st.success(
                        f"🟢 Route {i + 1}: "
                        f"Safest Route — Low Risk"
                    )

                elif risk == "Medium":

                    st.warning(
                        f"🟡 Route {i + 1}: "
                        f"Moderate Risk"
                    )

                else:

                    st.error(
                        f"🔴 Route {i + 1}: "
                        f"High Risk — Avoid"
                    )


            # ==============================
            # EMERGENCY ALERT
            # ==============================

            risk = route_risks[0]


            if risk == "High":

                st.error(
                    "🚨 EMERGENCY ALERT: "
                    "High-risk conditions detected. "
                    "Please avoid this route."
                )

            elif risk == "Medium":

                st.warning(
                    "⚠️ CAUTION: "
                    "Moderate-risk conditions detected. "
                    "Travel carefully."
                )

            else:

                st.success(
                    "✅ SAFE TRAVEL: "
                    "Current conditions are suitable "
                    "for this route."
                )


            # ==============================
            # WHY THIS ROUTE?
            # ==============================

            st.markdown(
                "### 💡 Why this route?"
            )

            st.write(
                f"🌧️ Rainfall: {rainfall} mm"
            )

            st.write(
                f"🌊 Flood Risk: "
                f"{flood_risk}/5"
            )

            st.write(
                f"⛰️ Landslide Risk: "
                f"{landslide_risk}/5"
            )

            st.write(
                f"🛣️ Road Condition: "
                f"{road_condition}/5"
            )

            st.write(
                "🤖 AI combines weather, "
                "disaster and road conditions "
                "to estimate route safety."
            )


            # ==============================
            # DYNAMIC REROUTING
            # ==============================

            st.markdown(
                "## 🔄 Dynamic Rerouting"
            )


            danger_detected = st.checkbox(
                "🚨 Simulate New Disaster Ahead"
            )


            if danger_detected:

                st.error(
                    "🚨 New hazard detected "
                    "on current route!"
                )

                st.warning(
                    "🔄 AI is recalculating "
                    "the safest route..."
                )


                if risk == "High":

                    st.error(
                        "⛔ Current route is unsafe. "
                        "Please avoid this route."
                    )

                else:

                    st.success(
                        "🟢 Route risk updated. "
                        "Continue with caution."
                    )


            # ==============================
            # MAP
            # ==============================

            st.markdown(
                "## 🗺️ Route Map"
            )


            m = folium.Map(
                location=[
                    (from_lat + to_lat) / 2,
                    (from_lon + to_lon) / 2
                ],
                zoom_start=9
            )


            # START MARKER

            folium.Marker(
                [
                    from_lat,
                    from_lon
                ],
                tooltip="📍 Start",
                popup=from_selected,
                icon=folium.Icon(
                    color="blue",
                    icon="play"
                )
            ).add_to(m)


            # DESTINATION MARKER

            folium.Marker(
                [
                    to_lat,
                    to_lon
                ],
                tooltip="🏁 Destination",
                popup=to_selected,
                icon=folium.Icon(
                    color="red",
                    icon="flag"
                )
            ).add_to(m)


            # ==============================
            # ROUTE COLORS
            # ==============================

            risk_colors = {
                "Low": "green",
                "Medium": "orange",
                "High": "red"
            }


            for i, route in enumerate(
                routes
            ):

                coordinates = [
                    [
                        point[1],
                        point[0]
                    ]
                    for point in route[
                        "geometry"
                    ]
                ]


                route_risk = route_risks[i]


                route_color = risk_colors.get(
                    route_risk,
                    "gray"
                )


                route_tooltip = (
                    f"🛣️ Route {i + 1} - "
                    f"{route_risk} Risk"
                )


                folium.PolyLine(
                    coordinates,
                    color=route_color,
                    weight=6,
                    opacity=0.8,
                    tooltip=route_tooltip
                ).add_to(m)


            st_folium(
                m,
                width=1100,
                height=600,
                returned_objects=[]
            )


            # ==============================
            # ROUTE DETAILS
            # ==============================

            st.markdown(
                "## 🚗 Route Details"
            )


            for i, route in enumerate(
                routes
            ):

                risk = route_risks[i]


                if risk == "Low":

                    route_name = (
                        "🟢 Safest Route"
                    )

                elif risk == "Medium":

                    route_name = (
                        "🟡 Moderate Risk Route"
                    )

                else:

                    route_name = (
                        "🔴 High Risk Route / Avoid"
                    )


                st.markdown(
                    f"### Route {i + 1} — "
                    f"{route_name}"
                )


                col1, col2, col3 = (
                    st.columns(3)
                )


                with col1:

                    st.metric(
                        "Distance",
                        f"{route['distance']:.1f} km"
                    )


                with col2:

                    st.metric(
                        "Estimated Time",
                        f"{route['duration']:.1f} hours"
                    )


                with col3:

                    st.metric(
                        "AI Risk",
                        risk
                    )


        else:

            st.error(
                "❌ No road route found."
            )


    else:

        st.warning(
            "Please select both From and To locations."
        )


# ==============================
# LEGEND
# ==============================

st.divider()

st.info(
    "🟢 Safest Route  | "
    "🟡 Moderate Risk  | "
    "🔴 High Risk / Avoid"
)

st.caption(
    "NER-SMART — SIH 2026 Prototype"
)