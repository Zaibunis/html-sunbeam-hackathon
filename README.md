# Build Your Perfect Day (a mini game)

A little Python/Flask game for my class project. You get 10 energy points
and a list of activities, each costing some energy and giving happiness
points. Pick a combo that fits your energy budget, and try to build the
highest-scoring "perfect day" you can. Some activities give bonus points
if you pick them together. At the end, it writes you a mini diary entry
based on what you picked.

## How to run it

1. Install Flask:
   ```
   pip install -r requirements.txt
   ```

2. Run it:
   ```
   python app.py
   ```

3. Open your browser to:
   ```
   http://127.0.0.1:5000
   ```

## How to play
- Check the boxes for the activities you want to do today
- Watch the energy bar — you only have 10 energy points total
- Click "Plan My Day" to see your score, your grade, and your generated diary entry
- Try different combos to find hidden bonus pairs and beat your high score!

## Files
- `app.py` — the whole game (routes, activity data, scoring logic, and the HTML/CSS all in one file)
