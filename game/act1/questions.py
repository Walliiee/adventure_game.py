"""Act 1 learning content and selection helpers.

Questions are organized by study source (solo/teacher/mentor/parent/pet)
and skill, with lightweight non-repeating selection per source+skill.
"""
from __future__ import annotations

import random

from game.act1.constants import SKILLS

Question = dict[str, object]

SOURCE_SKILLS: dict[str, tuple[str, ...]] = {
    "Solo": SKILLS,
    "Teacher": ("Smarts", "Spirit"),
    "Mentor": ("Strength", "Agility"),
    "Parent": ("Spirit", "Smarts"),
    "Pet": SKILLS,
}

QUESTION_BANKS: dict[str, dict[str, list[Question]]] = {
    "Solo": {
        "Strength": [
            {
                "text": "What's the safest way to carry a heavy orb?",
                "options": ["In one hand", "Close to your body with both hands", "On your head", "Tossing it"],
                "correct_index": 1,
            },
            {
                "text": "After hard training, what helps your muscles recover best?",
                "options": ["Skip water", "Gentle rest and water", "Train twice as hard", "Lift heavy bags immediately"],
                "correct_index": 1,
            },
            {
                "text": "Before a long hike, what should you do first?",
                "options": ["Stretch and check your gear", "Run without warming up", "Carry everything in one hand", "Ignore the weather"],
                "correct_index": 0,
            },
            {
                "text": "When lifting a heavy pack onto your shoulders, what protects your back?",
                "options": ["Bending at the waist", "Using your legs and keeping back straight", "Twisting while lifting", "Holding breath"],
                "correct_index": 1,
            },
            {
                "text": "What's the best way to build carrying endurance?",
                "options": ["Short daily practice with gradually increasing weight", "One massive carry per month", "Never practice carrying", "Only lift when absolutely necessary"],
                "correct_index": 0,
            },
            {
                "text": "If your hands get tired from holding orbs, you should...",
                "options": ["Switch to one hand", "Rest briefly and adjust grip", "Grip tighter", "Drop them"],
                "correct_index": 1,
            },
            {
                "text": "Which food gives lasting energy for long tracking days?",
                "options": ["Candy and sweets", "Nuts, dried fruit, and whole grains", "Only meat", "Water alone"],
                "correct_index": 1,
            },
            {
                "text": "Why is core strength important for a Keeper?",
                "options": ["It helps balance on uneven terrain", "It looks good", "It is not important", "Only for showing off"],
                "correct_index": 0,
            },
        ],
        "Agility": [
            {
                "text": "What's the best way to step so you don't startle a creature?",
                "options": ["Stomp loudly", "Move slowly and quietly", "Run toward it", "Jump"],
                "correct_index": 1,
            },
            {
                "text": "When crossing wet stones, what's safest?",
                "options": ["Rush", "Take short balanced steps", "Close your eyes", "Carry extra weight"],
                "correct_index": 1,
            },
            {
                "text": "To improve reflexes, what's a good habit?",
                "options": ["Practice controlled footwork", "Stand still all day", "Never bend knees", "Always sprint"],
                "correct_index": 0,
            },
            {
                "text": "When backpedaling from a creature, what prevents falls?",
                "options": ["Looking at the sky", "Short steps, staying low, checking behind you", "Long leaps", "Closing eyes"],
                "correct_index": 1,
            },
            {
                "text": "How do you safely change direction on loose gravel?",
                "options": ["Plant and pivot sharply", "Shuffle-step with bent knees", "Sprint straight through", "Freeze in place"],
                "correct_index": 1,
            },
            {
                "text": "What's the key to moving silently through dry leaves?",
                "options": ["Stepping on the edges, rolling from heel to toe", "Stomping to scare creatures away", "Running fast", "Jumping over patches"],
                "correct_index": 0,
            },
            {
                "text": "Why should you keep your knees slightly bent when observing creatures?",
                "options": ["To look shorter", "To react quickly without losing balance", "It is uncomfortable", "No reason"],
                "correct_index": 1,
            },
            {
                "text": "What helps you recover balance if you start to slip?",
                "options": ["Tensing up and waving arms", "Bending knees and widening stance", "Closing eyes", "Jumping"],
                "correct_index": 1,
            },
        ],
        "Smarts": [
            {
                "text": "What do Moss Bunnies eat?",
                "options": ["Berries", "Insects", "Grass and leaves", "Seeds"],
                "correct_index": 2,
            },
            {
                "text": "Why do Keepers record creature habits?",
                "options": ["To boast", "To predict safe encounter times", "To ignore patterns", "To avoid learning"],
                "correct_index": 1,
            },
            {
                "text": "Which orb type is usually better for larger creatures?",
                "options": ["Mini orb", "Mega orb", "Any pebble", "No orb ever"],
                "correct_index": 1,
            },
            {
                "text": "What do fresh, sharp claw marks on a tree suggest?",
                "options": ["An old, abandoned territory", "A creature has recently passed", "The tree is sick", "Nothing important"],
                "correct_index": 1,
            },
            {
                "text": "Why should you note the wind direction before approaching a creature?",
                "options": ["To decide if you need a coat", "To avoid being smelled before being seen", "It does not matter", "To predict rain"],
                "correct_index": 1,
            },
            {
                "text": "What does scattered, overturned pebbles near a riverbank likely indicate?",
                "options": ["Nothing", "A Pebble Otter has been playing there", "Earthquake", "Wind"],
                "correct_index": 1,
            },
            {
                "text": "Which sense do many forest creatures rely on most?",
                "options": ["Sight in bright light", "Hearing and smell", "Taste", "None"],
                "correct_index": 1,
            },
            {
                "text": "What does it mean when birds suddenly go silent?",
                "options": ["They are sleeping", "Something has disturbed them—possibly a larger creature", "It is time to leave", "Nothing special"],
                "correct_index": 1,
            },
        ],
        "Spirit": [
            {
                "text": "What should you do if a creature looks scared?",
                "options": ["Chase it", "Stay calm and still, speak softly", "Throw food at it", "Leave immediately"],
                "correct_index": 1,
            },
            {
                "text": "When you're frustrated in training, what's healthiest?",
                "options": ["Yell at companions", "Take a breath and reset", "Quit forever", "Blame others"],
                "correct_index": 1,
            },
            {
                "text": "How do you build trust with animals over time?",
                "options": ["Be consistent and gentle", "Force quick results", "Ignore boundaries", "Make loud surprises"],
                "correct_index": 0,
            },
            {
                "text": "If a creature lowers its head and avoids eye contact, it is likely feeling...",
                "options": ["Aggressive", "Scared or submissive", "Playful", "Hungry"],
                "correct_index": 1,
            },
            {
                "text": "What's the best response when a creature surprises you?",
                "options": ["Freeze and assess before acting", "Shout and run", "Throw your orb immediately", "Pretend to be bigger"],
                "correct_index": 0,
            },
            {
                "text": "Why is patience more important than speed in creature bonding?",
                "options": ["It lets the creature set the pace of trust", "It is slower", "It does not matter", "Creatures dislike fast people"],
                "correct_index": 0,
            },
            {
                "text": "How can you tell if a creature is starting to relax around you?",
                "options": ["It runs away", "It stops tensing, breathes slower, and may approach", "It attacks", "It ignores you completely"],
                "correct_index": 1,
            },
            {
                "text": "What's a sign that you are pushing a creature too hard?",
                "options": ["It eats eagerly", "It shows stress signs like pacing or avoidance", "It sleeps", "It follows you"],
                "correct_index": 1,
            },
        ],
    },
    "Teacher": {
        "Smarts": [
            {
                "text": "Teacher asks: Which clue best shows a creature nest nearby?",
                "options": ["Repeated tracks and soft bedding", "Random rocks", "No signs at all", "A loud whistle"],
                "correct_index": 0,
            },
            {
                "text": "Teacher asks: Why classify habitats by region?",
                "options": ["For decoration only", "To match creatures with likely environments", "To make maps harder", "No reason"],
                "correct_index": 1,
            },
            {
                "text": "Teacher asks: What does a sudden drop in temperature near ruins suggest?",
                "options": ["A storm is coming", "A Ruin Wraith may be nearby", "The sun went down", "Nothing"],
                "correct_index": 1,
            },
            {
                "text": "Teacher asks: How do you tell fresh tracks from old ones?",
                "options": ["Fresh tracks have sharp edges and may show moisture", "Old tracks are bigger", "You cannot tell", "All tracks look the same"],
                "correct_index": 0,
            },
            {
                "text": "Teacher asks: Why do some creatures prefer the highlands?",
                "options": ["They enjoy thin air and open skies", "They like storms", "No reason", "They are lost"],
                "correct_index": 0,
            },
        ],
        "Spirit": [
            {
                "text": "Teacher asks: What's the first step in calming yourself before contact?",
                "options": ["Hold your breath", "Slow, steady breathing", "Run circles", "Shout"],
                "correct_index": 1,
            },
            {
                "text": "Teacher asks: Respect in the wild means...",
                "options": ["Taking control", "Listening to animal signals", "Ignoring fear signs", "Only thinking of winning"],
                "correct_index": 1,
            },
            {
                "text": "Teacher asks: If a creature flattens its ears, what should you do?",
                "options": ["Approach quickly", "Back away and give space", "Make loud noises", "Stare at it"],
                "correct_index": 1,
            },
            {
                "text": "Teacher asks: What's the best way to teach a young creature to trust orbs?",
                "options": ["Force it inside immediately", "Let it investigate empty orbs at its own pace", "Hide orbs", "Use treats only"],
                "correct_index": 1,
            },
            {
                "text": "Teacher asks: Why should you never corner a creature?",
                "options": ["It might fight or panic", "It is easier to catch", "It becomes friendly", "It falls asleep"],
                "correct_index": 0,
            },
        ],
    },
    "Mentor": {
        "Strength": [
            {
                "text": "Mentor says: During lifting drills, keep your...",
                "options": ["Back rounded", "Core tight and back neutral", "Head down", "Feet together"],
                "correct_index": 1,
            },
            {
                "text": "Mentor says: Endurance improves best with...",
                "options": ["Consistent practice", "One giant workout", "No sleep", "Skipping meals"],
                "correct_index": 0,
            },
            {
                "text": "Mentor says: When your pack feels heavy mid-hike, you should...",
                "options": ["Drop everything", "Adjust straps, tighten core, and take short breaks", "Run faster to finish", "Carry it on one shoulder"],
                "correct_index": 1,
            },
            {
                "text": "Mentor says: Grip strength matters most for...",
                "options": ["Writing notes", "Holding orbs steady during capture", "Sleeping", "Eating"],
                "correct_index": 1,
            },
            {
                "text": "Mentor says: The best recovery after a hard day is...",
                "options": ["Staying up late", "Good sleep, light stretching, and hydration", "Another workout", "Skipping meals"],
                "correct_index": 1,
            },
        ],
        "Agility": [
            {
                "text": "Mentor says: For quick direction changes, focus on...",
                "options": ["Heavy heel strikes", "Low center of gravity", "Locked knees", "Big jumps every step"],
                "correct_index": 1,
            },
            {
                "text": "Mentor says: Balance starts with...",
                "options": ["Ignoring posture", "Stable foot placement", "Fast spinning", "Uneven breathing"],
                "correct_index": 1,
            },
            {
                "text": "Mentor says: When dodging a charging creature, never...",
                "options": ["Plant your feet and pivot", "Freeze directly in its path", "Dive sideways", "Run perpendicular"],
                "correct_index": 1,
            },
            {
                "text": "Mentor says: To stop quickly on a slope, you should...",
                "options": ["Dig in with heels, lean back, keep low", "Sprint faster downhill", "Jump", "Close eyes"],
                "correct_index": 0,
            },
            {
                "text": "Mentor says: Agility is NOT about...",
                "options": ["Being the fastest", "Controlled, purposeful movement", "Reacting safely", "Reading terrain"],
                "correct_index": 0,
            },
        ],
    },
    "Parent": {
        "Spirit": [
            {
                "text": "Parent asks: If a creature backs away, you should...",
                "options": ["Give it space", "Corner it", "Grab quickly", "Call it weak"],
                "correct_index": 0,
            },
            {
                "text": "Parent asks: Kindness in training looks like...",
                "options": ["Patience and clear routines", "Punishment", "Rushing growth", "Ignoring mood"],
                "correct_index": 0,
            },
            {
                "text": "Parent asks: What do you do if your companion seems sad?",
                "options": ["Ignore it", "Spend quiet time together and check for needs", "Force it to work", "Replace it"],
                "correct_index": 1,
            },
            {
                "text": "Parent asks: Why should you apologize to a creature if you startle it?",
                "options": ["It understands your tone and calms faster", "It does not matter", "It makes you look silly", "Creatures do not remember"],
                "correct_index": 0,
            },
            {
                "text": "Parent asks: The best way to end a training session is...",
                "options": ["Stop abruptly", "On a positive note with praise and rest", "Push until exhaustion", "Ignore the creature"],
                "correct_index": 1,
            },
        ],
        "Smarts": [
            {
                "text": "Parent asks: Why clean gear after field practice?",
                "options": ["For style", "To keep tools safe and reliable", "No need", "Only before festivals"],
                "correct_index": 1,
            },
            {
                "text": "Parent asks: Planning routes helps because...",
                "options": ["You waste more time", "You avoid hazards and arrive prepared", "Maps are boring", "Creatures dislike planning"],
                "correct_index": 1,
            },
            {
                "text": "Parent asks: Why should you note the weather before heading out?",
                "options": ["It is fun", "Storms can strand you or spook creatures", "It does not matter", "Only to dress right"],
                "correct_index": 1,
            },
            {
                "text": "Parent asks: What's the first thing to do if you get lost?",
                "options": ["Panic and run", "Stop, think, and retrace your steps calmly", "Keep walking blindly", "Shout for help only"],
                "correct_index": 1,
            },
            {
                "text": "Parent asks: Why pack extra water even for short trips?",
                "options": ["It is heavy", "Delays and unexpected events happen", "It looks professional", "Creatures need it"],
                "correct_index": 1,
            },
        ],
    },
    "Pet": {
        "Strength": [
            {
                "text": "Your pet nudges you toward a fun carry drill. Best form is...",
                "options": ["Both hands and steady steps", "One hand swinging", "Throw and catch", "No warmup"],
                "correct_index": 0,
            },
            {
                "text": "Your pet brings you a heavy stick. Playing tug-of-war helps...",
                "options": ["Build grip and arm strength", "Waste time", "Tire the pet", "Nothing"],
                "correct_index": 0,
            },
            {
                "text": "Your pet wants to wrestle gently. This play builds...",
                "options": ["Core stability and controlled power", "Aggression", "Fear", "Nothing useful"],
                "correct_index": 0,
            },
            {
                "text": "Your pet drops a stone and looks at you. Best response?",
                "options": ["Pick it up with good form as a game", "Ignore it", "Kick it away", "Throw it hard"],
                "correct_index": 0,
            },
        ],
        "Agility": [
            {
                "text": "Your pet darts left-right. To follow safely, you should...",
                "options": ["Take controlled quick steps", "Sprint blindly", "Close your eyes", "Stomp loudly"],
                "correct_index": 0,
            },
            {
                "text": "Your pet leaps over a log. You should...",
                "options": ["Use a small hop with bent knees", "Ignore the obstacle", "Run into it", "Leap without looking"],
                "correct_index": 0,
            },
            {
                "text": "Your pet zigzags through trees. This teaches you...",
                "options": ["Quick direction changes while watching ahead", "Nothing", "To ignore the pet", "To run straight"],
                "correct_index": 0,
            },
            {
                "text": "Your pet stops suddenly on a slope. You learn to...",
                "options": ["Plant feet and absorb momentum with bent knees", "Keep running", "Fall over", "Jump"],
                "correct_index": 0,
            },
        ],
        "Smarts": [
            {
                "text": "Your pet pauses near fresh prints. This likely means...",
                "options": ["A recent creature passed by", "The ground is fake", "Nothing at all", "It's a trap every time"],
                "correct_index": 0,
            },
            {
                "text": "Your pet sniffs the air and whines. What should you do?",
                "options": ["Check wind direction and surroundings carefully", "Ignore it", "Shout", "Run away"],
                "correct_index": 0,
            },
            {
                "text": "Your pet stares at a bush. It probably...",
                "options": ["Saw or smelled something worth investigating", "Is bored", "Wants to sleep there", "Is broken"],
                "correct_index": 0,
            },
            {
                "text": "Your pet ignores a trail you found. Maybe...",
                "options": ["The scent is old and not worth following", "Your pet is wrong", "The trail is important", "You should force it"],
                "correct_index": 0,
            },
        ],
        "Spirit": [
            {
                "text": "Your pet leans in quietly. Best response?",
                "options": ["Mirror calm behavior", "Push it away", "Shout excitedly", "Ignore all signals"],
                "correct_index": 0,
            },
            {
                "text": "Your pet tucks its tail and hides. It needs...",
                "options": ["Reassurance and space, not forcing interaction", "Discipline", "Loud encouragement", "Isolation"],
                "correct_index": 0,
            },
            {
                "text": "Your pet wags after a failed capture. It teaches you...",
                "options": ["To stay positive and try again patiently", "To quit", "That failure is bad", "Nothing"],
                "correct_index": 0,
            },
            {
                "text": "Your pet approaches a new creature calmly. It shows you...",
                "options": ["That slow, respectful introductions work best", "To rush in", "That creatures are scary", "To run"],
                "correct_index": 0,
            },
        ],
    },
}


def choose_question(state, source, skill):
    """Pick a question for source+skill, avoiding immediate repeats when possible."""
    pool = QUESTION_BANKS[source][skill]
    key = f"{source}:{skill}"
    last_idx = state["last_question_idx"].get(key)
    candidates = [i for i in range(len(pool)) if i != last_idx] or list(range(len(pool)))
    idx = random.choice(candidates)
    state["last_question_idx"][key] = idx
    return pool[idx]
