import streamlit as st
import random
import matplotlib.pyplot as plt
import time

st.title("Dinamična simulacija ocjena topica")

# Parametri
num_topics = st.sidebar.slider("Broj topica", 5, 30, 10)
num_iterations = st.sidebar.slider("Broj iteracija simulacije", 10, 500, 100)
delay = st.sidebar.slider("Delay između iteracija (ms)", 50, 1000, 200)

# Definiraj topice i njihove 'težine' za vjerojatnost thumbs up
# Težina između 0.2 i 0.8 (veća = više thumbs up)
topic_weights = {f"Topic_{i+1}": random.uniform(0.2, 0.8) for i in range(num_topics)}

# Inicijalna stanja
topics = {
    topic: {
        "score": 1.0,
        "thumbs_up": 0,
        "thumbs_down": 0,
        "weight": weight
    }
    for topic, weight in topic_weights.items()
}

start_sim = st.button("Pokreni simulaciju")

placeholder_table = st.empty()
placeholder_chart = st.empty()

def simulate_once(topics, user_id):
    for topic, data in topics.items():
        # Vjerojatnost thumbs up ovisno o weight topica
        if random.random() < data["weight"]:
            rating, category = 2.0, "thumbs_up"
        else:
            rating, category = 0.0, "thumbs_down"

        old_score = data["score"]
        data["score"] = ((old_score * user_id) + rating) / (user_id + 1)
        data[category] += 1

if start_sim:
    for i in range(num_iterations):
        simulate_once(topics, i)

        # Sortiraj po score
        sorted_topics = dict(sorted(topics.items(), key=lambda x: x[1]["score"], reverse=True))
        total_score = sum(t["score"] for t in sorted_topics.values())

        # Prikaz tablice
        table_data = []
        for topic, data in sorted_topics.items():
            probability = data["score"] / total_score if total_score > 0 else 0
            table_data.append({
                "Topic": topic,
                "Score": round(data["score"], 2),
                "Thumbs Up": data["thumbs_up"],
                "Thumbs Down": data["thumbs_down"],
                "Display Probability": f"{probability:.2%}"
            })

        placeholder_table.table(table_data)

        # Prikaz grafa (generator zamijenjen listom)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar([row['Topic'] for row in table_data], [d["score"] for d in sorted_topics.values()], color='skyblue')
        ax.set_xlabel("Topic")
        ax.set_ylabel("Score")
        ax.set_ylim(0, 2.2)
        ax.set_title("Promjena ocjena topica kroz simulaciju")
        plt.xticks(rotation=45)
        placeholder_chart.pyplot(fig)

        time.sleep(delay / 1000)
else:
    st.info("Pritisni 'Pokreni simulaciju' da vidiš dinamičke promjene ocjena.")

