import folium
from folium import plugins


# =========================================================
# AEROGUARD DISASTER MANAGEMENT MAP
# =========================================================

def get_map():

    # -----------------------------------------------------
    # 1. CREATE MAP
    # -----------------------------------------------------

    m = folium.Map(
        location=[18.5204, 73.8567],
        zoom_start=13,
        tiles=None,
        control_scale=True
    )


    # -----------------------------------------------------
    # 2. BASE MAP LAYERS
    # -----------------------------------------------------

    folium.TileLayer(
        "OpenStreetMap",
        name="🗺️ Street Map"
    ).add_to(m)

    folium.TileLayer(
        "CartoDB dark_matter",
        name="🌑 Dark Map"
    ).add_to(m)

    folium.TileLayer(
        "Esri WorldImagery",
        name="🛰️ Satellite"
    ).add_to(m)


    # -----------------------------------------------------
    # 3. CREATE FEATURE GROUPS
    # -----------------------------------------------------

    incidents = folium.FeatureGroup(
        name="🚨 Disaster Incidents"
    )

    drones = folium.FeatureGroup(
        name="🚁 AeroGuard Drones"
    )

    shelters = folium.FeatureGroup(
        name="🟢 Emergency Shelters"
    )

    hospitals = folium.FeatureGroup(
        name="🏥 Hospitals"
    )

    risk_zones = folium.FeatureGroup(
        name="⚠️ Risk Zones"
    )

    routes = folium.FeatureGroup(
        name="🛣️ Evacuation Routes"
    )

    # -----------------------------------------------------
    # 4. DISASTER INCIDENT
    # -----------------------------------------------------

    incident_location = [18.5304, 73.8667]

    folium.Marker(
        incident_location,
        popup=folium.Popup(
            """
            <div style="width:220px">
                <h4>🚨 BUILDING COLLAPSE</h4>
                <b>Severity:</b>
                <span style="color:red"> CRITICAL</span><br>
                <b>People at Risk:</b> 42<br>
                <b>AI Confidence:</b> 94%<br>
                <b>Status:</b> Rescue Required
            </div>
            """,
            max_width=300
        ),
        tooltip="🚨 Critical Disaster"
    ).add_to(incidents)


    # -----------------------------------------------------
    # 5. SECOND INCIDENT - FLOOD
    # -----------------------------------------------------

    flood_location = [18.5150, 73.8500]

    folium.Marker(
        flood_location,
        popup=folium.Popup(
            """
            <div style="width:220px">
                <h4>🌊 FLOOD ALERT</h4>
                <b>Severity:</b> HIGH<br>
                <b>People at Risk:</b> 120<br>
                <b>Water Level:</b> 3.2 m<br>
                <b>Status:</b> Monitoring
            </div>
            """,
            max_width=300
        ),
        tooltip="🌊 Flood Alert"
    ).add_to(incidents)


    # -----------------------------------------------------
    # 6. FIRE INCIDENT
    # -----------------------------------------------------

    fire_location = [18.5400, 73.8400]

    folium.Marker(
        fire_location,
        popup=folium.Popup(
            """
            <div style="width:220px">
                <h4>🔥 FIRE ALERT</h4>
                <b>Severity:</b> MEDIUM<br>
                <b>Status:</b> Monitoring
            </div>
            """,
            max_width=300
        ),
        tooltip="🔥 Fire Alert"
    ).add_to(incidents)


    # -----------------------------------------------------
    # 7. HIGH RISK ZONE
    # -----------------------------------------------------

    folium.Circle(
        location=incident_location,
        radius=900,
        color="red",
        fill=True,
        fill_color="red",
        fill_opacity=0.20,
        weight=2,
        popup="⚠️ HIGH RISK ZONE"
    ).add_to(risk_zones)


    # -----------------------------------------------------
    # 8. MEDIUM RISK ZONE
    # -----------------------------------------------------

    folium.Circle(
        location=flood_location,
        radius=700,
        color="orange",
        fill=True,
        fill_color="orange",
        fill_opacity=0.15,
        weight=2,
        popup="⚠️ FLOOD RISK ZONE"
    ).add_to(risk_zones)


    # -----------------------------------------------------
    # 9. DRONE 01
    # -----------------------------------------------------

    drone_01 = [18.5200, 73.8500]

    folium.Marker(
        drone_01,
        popup=folium.Popup(
            """
            <div style="width:220px">
                <h4>🚁 AEROGUARD DR-01</h4>
                <b>Status:</b>
                <span style="color:green"> ACTIVE</span><br>
                <b>Battery:</b> 78%<br>
                <b>Mission:</b> Search & Rescue<br>
                <b>Altitude:</b> 120 m
            </div>
            """,
            max_width=300
        ),
        tooltip="🚁 DR-01 | Active",
        icon=folium.Icon(
            color="blue",
            icon="plane",
            prefix="fa"
        )
    ).add_to(drones)


    # -----------------------------------------------------
    # 10. DRONE 02
    # -----------------------------------------------------

    drone_02 = [18.5450, 73.8600]

    folium.Marker(
        drone_02,
        popup=folium.Popup(
            """
            <div style="width:220px">
                <h4>🚁 AEROGUARD DR-02</h4>
                <b>Status:</b> STANDBY<br>
                <b>Battery:</b> 92%<br>
                <b>Mission:</b> Ready
            </div>
            """,
            max_width=300
        ),
        tooltip="🚁 DR-02 | Standby",
        icon=folium.Icon(
            color="green",
            icon="plane",
            prefix="fa"
        )
    ).add_to(drones)


    # -----------------------------------------------------
    # 11. EMERGENCY SHELTER 1
    # -----------------------------------------------------

    shelter_01 = [18.5100, 73.8450]

    folium.Marker(
        shelter_01,
        popup=folium.Popup(
            """
            <div style="width:220px">
                <h4>🟢 EMERGENCY SHELTER A</h4>
                <b>Capacity:</b> 500<br>
                <b>Occupied:</b> 284<br>
                <b>Medical Support:</b> Available<br>
                <b>Status:</b> Safe
            </div>
            """,
            max_width=300
        ),
        tooltip="🟢 Emergency Shelter A",
        icon=folium.Icon(
            color="green",
            icon="home"
        )
    ).add_to(shelters)


    # -----------------------------------------------------
    # 12. EMERGENCY SHELTER 2
    # -----------------------------------------------------

    shelter_02 = [18.5450, 73.8750]

    folium.Marker(
        shelter_02,
        popup=folium.Popup(
            """
            <div style="width:220px">
                <h4>🟢 EMERGENCY SHELTER B</h4>
                <b>Capacity:</b> 300<br>
                <b>Occupied:</b> 102<br>
                <b>Status:</b> Safe
            </div>
            """,
            max_width=300
        ),
        tooltip="🟢 Emergency Shelter B",
        icon=folium.Icon(
            color="green",
            icon="home"
        )
    ).add_to(shelters)


    # -----------------------------------------------------
    # 13. HOSPITAL
    # -----------------------------------------------------

    hospital_location = [18.5350, 73.8750]

    folium.Marker(
        hospital_location,
        popup=folium.Popup(
            """
            <div style="width:220px">
                <h4>🏥 EMERGENCY HOSPITAL</h4>
                <b>Distance:</b> 2.4 km<br>
                <b>Emergency Beds:</b> 38<br>
                <b>Ambulance:</b> Available
            </div>
            """,
            max_width=300
        ),
        tooltip="🏥 Emergency Hospital",
        icon=folium.Icon(
            color="red",
            icon="plus-sign"
        )
    ).add_to(hospitals)


    # -----------------------------------------------------
    # 14. SAFE EVACUATION ROUTE
    # -----------------------------------------------------

    evacuation_route = [
        incident_location,
        [18.5260, 73.8580],
        [18.5180, 73.8520],
        shelter_01
    ]

    folium.PolyLine(
        evacuation_route,
        color="green",
        weight=6,
        opacity=0.85,
        tooltip="🟢 Recommended Safe Evacuation Route",
        popup="""
        <b>🟢 SAFE EVACUATION ROUTE</b><br>
        Distance: 3.1 km<br>
        Estimated Time: 8 minutes
        """
    ).add_to(routes)


    # -----------------------------------------------------
    # 15. BLOCKED ROAD
    # -----------------------------------------------------

    blocked_road = [
        [18.5304, 73.8667],
        [18.5350, 73.8700]
    ]

    folium.PolyLine(
        blocked_road,
        color="orange",
        weight=7,
        dash_array="10",
        tooltip="🚧 ROAD BLOCKED"
    ).add_to(routes)


    # -----------------------------------------------------
    # 16. ADD ALL GROUPS TO MAP
    # -----------------------------------------------------

    incidents.add_to(m)
    drones.add_to(m)
    shelters.add_to(m)
    hospitals.add_to(m)
    risk_zones.add_to(m)
    routes.add_to(m)


    # -----------------------------------------------------
    # 17. MAP LAYER CONTROL
    # -----------------------------------------------------

    folium.LayerControl(
        collapsed=False
    ).add_to(m)


    # -----------------------------------------------------
    # 18. FULLSCREEN BUTTON
    # -----------------------------------------------------

    plugins.Fullscreen(
        position="topleft",
        title="Full Screen",
        title_cancel="Exit Full Screen"
    ).add_to(m)


    # -----------------------------------------------------
    # 19. MOUSE POSITION
    # -----------------------------------------------------

    plugins.MousePosition(
        position="bottomleft",
        separator=" | ",
        prefix="Coordinates:"
    ).add_to(m)


    return m