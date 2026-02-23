"""
Act 1 learning content and selection helpers.

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
        ],
    },
    "Pet": {
        "Strength": [
            {
                "text": "Your pet nudges you toward a fun carry drill. Best form is...",
                "options": ["Both hands and steady steps", "One hand swinging", "Throw and catch", "No warmup"],
                "correct_index": 0,
            }
        ],
        "Agility": [
            {
                "text": "Your pet darts left-right. To follow safely, you should...",
                "options": ["Take controlled quick steps", "Sprint blindly", "Close your eyes", "Stomp loudly"],
                "correct_index": 0,
            }
        ],
        "Smarts": [
            {
                "text": "Your pet pauses near fresh prints. This likely means...",
                "options": ["A recent creature passed by", "The ground is fake", "Nothing at all", "It's a trap every time"],
                "correct_index": 0,
            }
        ],
        "Spirit": [
            {
                "text": "Your pet leans in quietly. Best response?",
                "options": ["Mirror calm behavior", "Push it away", "Shout excitedly", "Ignore all signals"],
                "correct_index": 0,
            }
        ],
    },
}


def choose_question(state: dict, source: str, skill: str) -> Question:
    """Pick a question for source+skill, avoiding immediate repeats when possible."""
    pool = QUESTION_BANKS[source][skill]
    key = f"{source}:{skill}"
    last_idx = state["last_question_idx"].get(key)
    candidates = [i for i in range(len(pool)) if i != last_idx] or list(range(len(pool)))
    idx = random.choice(candidates)
    state["last_question_idx"][key] = idx
    return pool[idx]
