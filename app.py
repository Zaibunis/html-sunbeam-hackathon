# Perfect Day - a little game I made for my python class
# you pick activities to fill up your day (without running out of energy)
# and try to score as high as possible. also writes you a mini diary entry
# based on what you picked lol

from flask import Flask, render_template_string, request

app = Flask(__name__)

ENERGY_BUDGET = 10

# each activity: id, emoji, name, energy cost, happiness points, diary line
ACTIVITIES = [
    {"id": "sleep_in",     "emoji": "😴", "name": "Sleep In",         "cost": 2, "points": 10,
     "line": "You slept in and woke up feeling wonderfully rested."},
    {"id": "coffee",       "emoji": "☕", "name": "Morning Coffee",   "cost": 1, "points": 8,
     "line": "You started the morning with a really good cup of coffee."},
    {"id": "jog",          "emoji": "🏃", "name": "Sunrise Jog",      "cost": 3, "points": 15,
     "line": "You went for a jog as the sun came up and it woke you right up."},
    {"id": "breakfast",    "emoji": "🥞", "name": "Big Breakfast",    "cost": 2, "points": 12,
     "line": "You made yourself a big, delicious breakfast."},
    {"id": "hobby",        "emoji": "🎨", "name": "Work on a Hobby",  "cost": 3, "points": 18,
     "line": "You spent time on your favorite hobby and totally lost track of time."},
    {"id": "call_friend",  "emoji": "📞", "name": "Call a Friend",    "cost": 1, "points": 10,
     "line": "You called an old friend and caught up for a while."},
    {"id": "walk",         "emoji": "🌳", "name": "Walk in the Park", "cost": 2, "points": 13,
     "line": "You took a slow walk outside and enjoyed the fresh air."},
    {"id": "cook",         "emoji": "🍝", "name": "Cook a Nice Meal", "cost": 3, "points": 16,
     "line": "You cooked yourself a proper, delicious meal."},
    {"id": "movie",        "emoji": "🎬", "name": "Watch a Movie",    "cost": 2, "points": 11,
     "line": "You watched a movie you'd been wanting to see for ages."},
    {"id": "book",         "emoji": "📖", "name": "Read a Book",      "cost": 2, "points": 12,
     "line": "You curled up and read a good chunk of a book."},
    {"id": "stars",        "emoji": "🌌", "name": "Stargazing",       "cost": 2, "points": 14,
     "line": "You lay outside and watched the stars for a while."},
    {"id": "dance",        "emoji": "💃", "name": "Dance Party",      "cost": 3, "points": 17,
     "line": "You put on music and had a little dance party, just for you."},
]

# bonus points if you pick BOTH activities in a pair
COMBOS = [
    ({"coffee", "jog"},         5, "☕ + 🏃 Perfect Morning Combo!"),
    ({"cook", "movie"},         5, "🍝 + 🎬 Cozy Night In!"),
    ({"call_friend", "dance"},  5, "📞 + 💃 Social Butterfly!"),
    ({"book", "stars"},         5, "📖 + 🌌 Peaceful Soul!"),
]


def get_activity(activity_id):
    for a in ACTIVITIES:
        if a["id"] == activity_id:
            return a
    return None


def grade_for_score(score):
    if score >= 65:
        return "A Truly Perfect Day!", "🌟"
    elif score >= 50:
        return "A Really Great Day", "😊"
    elif score >= 35:
        return "A Pretty Good Day", "🙂"
    else:
        return "An Okay Day (try a different combo!)", "😌"


# ---------- shared styling ----------

STYLE = """
<style>
  body {
    font-family: 'Kalam', cursive;
    background-color: #fffdf5;
    background-image: repeating-linear-gradient(#fffdf5, #fffdf5 27px, #dbe9f4 28px);
    margin: 0;
    padding: 0;
    color: #333;
  }
  .wrap {
    max-width: 650px;
    margin: 0 auto;
    padding: 30px 20px 60px 20px;
  }
  h1 {
    text-align: center;
    color: #ff914d;
    font-size: 2.3rem;
    margin-bottom: 5px;
  }
  .subtitle {
    text-align: center;
    color: #555;
    margin-bottom: 25px;
  }
  .box {
    background: #ffffff;
    border: 2px solid #333;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 6px 6px 0px rgba(0,0,0,0.15);
    margin-bottom: 20px;
  }
  .energy-bar-outer {
    background: #eee;
    border: 2px solid #333;
    border-radius: 8px;
    height: 24px;
    overflow: hidden;
    margin-bottom: 6px;
  }
  .energy-bar-inner {
    background: #a2d5f2;
    height: 100%;
    width: 0%;
    transition: width 0.2s ease;
  }
  #energy-label {
    text-align: center;
    font-size: 0.9rem;
    margin-bottom: 20px;
    color: #555;
  }
  .activity {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 6px;
    border-bottom: 1px solid #eee;
  }
  .activity label {
    flex-grow: 1;
    cursor: pointer;
  }
  .cost-tag {
    background: #ffe9c7;
    border: 1px solid #e0b976;
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 0.8rem;
  }
  button {
    background-color: #a2d5f2;
    border: 2px solid #333;
    border-radius: 6px;
    padding: 10px 20px;
    font-family: 'Kalam', cursive;
    font-size: 1.05rem;
    cursor: pointer;
    display: block;
    margin: 20px auto 0 auto;
  }
  button:hover { background-color: #7fc1e8; }
  .error {
    background: #ffe0e0;
    border: 2px solid #d9534f;
    color: #a83232;
    border-radius: 8px;
    padding: 10px 14px;
    text-align: center;
    margin-bottom: 20px;
  }
  .score {
    text-align: center;
    font-size: 2rem;
    color: #ff914d;
    margin: 10px 0 0 0;
  }
  .grade {
    text-align: center;
    font-size: 1.3rem;
    margin-bottom: 20px;
  }
  .bonus-list {
    text-align: center;
    color: #4a8f4a;
    margin-bottom: 15px;
  }
  .diary-text {
    font-size: 1.1rem;
    line-height: 1.6;
    background: #fffbe6;
    border: 1px solid #eee0a8;
    border-radius: 8px;
    padding: 16px;
  }
  a.again {
    display: block;
    text-align: center;
    margin-top: 20px;
    color: #555;
  }
</style>
"""

# ---------- page 1: pick your activities ----------

FORM_PAGE = STYLE + """
<link href="https://fonts.googleapis.com/css2?family=Kalam:wght@400;700&display=swap" rel="stylesheet">
<div class="wrap">
  <h1>🌞 Build Your Perfect Day</h1>
  <p class="subtitle">You've got {{ budget }} energy points. Pick activities to fill your day without running out!</p>

  {% if error %}
    <div class="error">{{ error }}</div>
  {% endif %}

  <form action="/play" method="POST">
    <div class="box">
      <div class="energy-bar-outer">
        <div class="energy-bar-inner" id="energy-bar"></div>
      </div>
      <div id="energy-label">0 / {{ budget }} energy used</div>

      {% for a in activities %}
        <div class="activity">
          <input type="checkbox" name="activities" value="{{ a.id }}"
                 id="{{ a.id }}" data-cost="{{ a.cost }}"
                 onchange="updateEnergy()"
                 {% if a.id in selected %}checked{% endif %}>
          <label for="{{ a.id }}">{{ a.emoji }} {{ a.name }}</label>
          <span class="cost-tag">{{ a.cost }} energy</span>
        </div>
      {% endfor %}
    </div>

    <button type="submit">Plan My Day →</button>
  </form>
</div>

<script>
function updateEnergy() {
  var boxes = document.querySelectorAll('input[type=checkbox]:checked');
  var total = 0;
  boxes.forEach(function(b) { total += parseInt(b.getAttribute('data-cost')); });

  var budget = {{ budget }};
  var pct = Math.min((total / budget) * 100, 100);
  var bar = document.getElementById('energy-bar');
  bar.style.width = pct + '%';
  bar.style.background = total > budget ? '#f2a2a2' : '#a2d5f2';

  document.getElementById('energy-label').textContent = total + ' / ' + budget + ' energy used';
}
window.onload = updateEnergy;
</script>
"""

# ---------- page 2: result ----------

RESULT_PAGE = STYLE + """
<link href="https://fonts.googleapis.com/css2?family=Kalam:wght@400;700&display=swap" rel="stylesheet">
<div class="wrap">
  <h1>{{ grade_emoji }} {{ grade_title }}</h1>
  <p class="score">{{ score }} points</p>
  <p class="grade">out of a possible ~75</p>

  {% if bonuses %}
    <div class="bonus-list">
      {% for b in bonuses %}<div>✨ {{ b }}</div>{% endfor %}
    </div>
  {% endif %}

  <div class="box">
    <h2>📔 Your Day, In Your Own Words</h2>
    <p class="diary-text">{{ diary_text }}</p>
  </div>

  <a href="/" class="again">↺ play again / plan a different day</a>
</div>
"""


@app.route("/")
def home():
    return render_template_string(FORM_PAGE, activities=ACTIVITIES, budget=ENERGY_BUDGET,
                                   error=None, selected=[])


@app.route("/play", methods=["POST"])
def play():
    chosen_ids = request.form.getlist("activities")
    chosen = [get_activity(a_id) for a_id in chosen_ids if get_activity(a_id)]

    total_cost = sum(a["cost"] for a in chosen)

    # no activities picked
    if len(chosen) == 0:
        return render_template_string(
            FORM_PAGE, activities=ACTIVITIES, budget=ENERGY_BUDGET,
            error="You didn't plan anything at all! Pick a few activities first.",
            selected=[]
        )

    # too many activities, over budget
    if total_cost > ENERGY_BUDGET:
        return render_template_string(
            FORM_PAGE, activities=ACTIVITIES, budget=ENERGY_BUDGET,
            error="Whoa, that's too much for one day (" + str(total_cost) +
                  " energy used, only " + str(ENERGY_BUDGET) + " available). Remove something!",
            selected=chosen_ids
        )

    # calculate score
    base_score = sum(a["points"] for a in chosen)
    chosen_id_set = set(chosen_ids)

    bonus_points = 0
    bonus_messages = []
    for pair, bonus, message in COMBOS:
        if pair.issubset(chosen_id_set):
            bonus_points += bonus
            bonus_messages.append(message)

    total_score = base_score + bonus_points

    # build the diary paragraph out of the chosen activities
    lines = [a["line"] for a in chosen]
    diary_text = "Today was a good one. " + " ".join(lines)

    grade_title, grade_emoji = grade_for_score(total_score)
    if total_score >= 65:
        diary_text += " Honestly? Pretty much the perfect day."
    elif total_score < 35:
        diary_text += " It was fine, but I think tomorrow could be better."

    return render_template_string(
        RESULT_PAGE,
        score=total_score,
        grade_title=grade_title,
        grade_emoji=grade_emoji,
        bonuses=bonus_messages,
        diary_text=diary_text
    )


if __name__ == "__main__":
    app.run(debug=True)
